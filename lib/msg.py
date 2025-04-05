r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers functions to debug, warn and log any operations
            executed within the morPy framework. At the same time it processes
            all kinds of messaging, whether it be via console or ui.

TODO make logging a class
    > Needed to efficiently share the lock on the db
"""

import lib.fct as morpy_fct
from lib.common import textfile_write
from lib.decorators import metrics

import sys
import time
from heapq import heappush, heappop

from lib.mp import is_udict


@metrics
def log(morpy_trace: dict, app_dict: dict, level: str, message: callable, verbose: bool) -> None:
    r"""
    This function writes an event to a specified file and/or prints it out
    according to it's severity (level).

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param level: Severity: debug/info/warning/error/critical/denied
    :param message: A callable (e.g., lambda or function) that returns the log message.
    :param verbose: If True, message is only logged in verbose mode.

    :return
        -

    :example:
        log(morpy_trace, app_dict, level, message)

    TODO Implement a mechanism to keep logfile size in check
        > Preferably auto delete logs based on "no errors occurred" per process, task, thread and __main__
    """

    morpy_trace_eval: dict = None

    try:
        # Wait for an interrupt to end
        udict_true = is_udict(app_dict["morpy"])
        if udict_true:
            with app_dict["morpy"].lock:
                interrupt = app_dict["morpy"]["interrupt"]
        else:
            interrupt = app_dict["morpy"]["interrupt"]

        while interrupt:
            time.sleep(0.05)


        # Event handling (counting and formatting)
        log_event_dict = log_event_handler(app_dict, message, level)
        level_dict = log_event_dict["level_dict"]

        # The log level will be evaluated as long as logging or prints to console are enabled. The
        # morpy_trace may be manipulated.
        if app_dict["conf"]["msg_print"] or app_dict["conf"]["log_enable"]:
            morpy_trace_eval = log_eval(morpy_trace, app_dict, log_event_dict["level"], level_dict)

        # Retrieve a log specific datetimestamp
        time_lst = morpy_fct.datetime_now()
        datetimestamp = time_lst["datetimestamp"]
        datetime_value = time_lst["datetime_value"]

        # Prepare a passthrough dictionary for logging operations
        log_dict = {
            'level' : log_event_dict["level"],
            'verbose' : verbose,
            'datetimestamp' : datetimestamp,
            'datetime_value' : datetime_value,
            'module' : morpy_trace_eval["module"],
            'operation' : morpy_trace_eval["operation"],
            'tracing' : morpy_trace_eval["tracing"],
            'process_id' : morpy_trace_eval["process_id"],
            'thread_id' : morpy_trace_eval["thread_id"],
            'task_id' : morpy_trace_eval["task_id"],
            'message' : message,
            'log_msg_complete' : None,
            'log_enable' : morpy_trace_eval["log_enable"] ,
            'pnt_enable' : morpy_trace_eval["pnt_enable"] ,
            'interrupt_enable' : morpy_trace_eval["interrupt_enable"]
        }

        # Build the complete log message
        msg = log_msg_builder(app_dict, log_dict)
        log_dict["log_msg_complete"] = msg

        # Buffer logging parameters
        logging = app_dict["conf"]["log_enable"] and log_dict["log_enable"]
        write_log_txt = logging and app_dict["conf"]["log_txt_enable"]
        write_log_db = logging and app_dict["conf"]["log_db_enable"]
        print_log = app_dict["conf"]["msg_print"]

        if morpy_trace["process_id"] == app_dict["morpy"]["proc_master"]:
            # Go on with logging directly if calling process is orchestrator.
            log_task(morpy_trace, app_dict, log_dict, write_log_txt, write_log_db, print_log)
        else:
            # Enqueue the orchestrator task
            task = [log_task, morpy_trace, app_dict, log_dict, write_log_txt, write_log_db, print_log]
            log_enqueue(app_dict, task=task)
            # Generate print required for GUIs in the regarding child process.
            if print_log:
                msg_print(morpy_trace, app_dict, log_dict)

        # Clean up
        del log_dict
        del morpy_trace

    except Exception as e:
        # Severe morPy logging error.
        raise RuntimeError(f'{app_dict["loc"]["morpy"]["log_crit_fail"]}:\n{e}')

def log_enqueue(app_dict: dict, priority: int=-100, task: list=None) -> None:
    r"""
    Adds a logging task to the morPy process queue.

    :param app_dict: morPy global dictionary containing app configurations
    :param priority: Integer representing task priority (lower is higher priority)
    :param task: Tuple of a callable, *args and **kwargs (func, *args, **kwargs)

    :return: -

    :example:
        task = [log_task, morpy_trace, app_dict]
        log_enqueue(morpy_trace, app_dict, task=task)
    """

    if task:
        with app_dict["morpy"].lock:
            morpy_dict = app_dict["morpy"]
            task_lookup = morpy_dict["task_lookup"]
            heap = morpy_dict["heap"]

            with app_dict["morpy"]["orchestrator"].lock:
                counter = app_dict["morpy"]["orchestrator"]["task_counter"] + 1
                app_dict["morpy"]["orchestrator"]["task_counter"] = counter

            # Substitute UltraDict references in task to avoid recursion issues.
            app_dict_substitute = (f'__morPy_shared_ref__::{app_dict.name}', app_dict.shared_lock, app_dict.auto_unlink,
                                   app_dict.recurse)
            task[2] = app_dict_substitute

            task_sys_id = id(task)

            # Push task to queue
            task_qed = (priority, counter, task_sys_id, task, False)

            heappush(heap, task_qed)
            app_dict["morpy"]["heap"] = heap # reassign to trigger synchronization

            task_lookup.add(task_sys_id)
            app_dict["morpy"]["task_lookup"] = task_lookup # reassign to trigger synchronization

            morpy_dict.apply_update()

def log_task(morpy_trace: dict, app_dict: dict, log_dict: dict, write_log_txt: bool, write_log_db: bool,
             print_log: bool) -> None:
    r"""
    Task that finally writes the logs. May be handed to orchestrator via priority queue.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations
    :param write_log_txt: If True, log is written to textfile.
    :param write_log_db: If True, log is written to database.
    :param print_log: If True, logs are printed to console.

    :return:
        -

    :example:
        log_task(morpy_trace, app_dict, log_dict, write_log_txt, write_log_db, print_log)
    """

    if write_log_txt:
        # Write to text file - Fallback if SQLite functionality is broken
        log_txt(log_dict, app_dict, log_dict)

    if write_log_db:
        # Write to logging database
        log_db(log_dict, app_dict, log_dict)

    if print_log:
        # Print the events according to their log level
        msg_print(morpy_trace, app_dict, log_dict)

def log_eval(morpy_trace: dict, app_dict: dict, level: str, level_dict: dict) -> dict:
    r"""
    This function evaluates the log level and makes manipulation of morpy_trace
    possible for passdown only. That means, for the purpose of logging, certain
    parameters (keys) may be altered in check with mpy_param.py or other parts
    of the code to hide, extend, enable or what else is needed for a log.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param level: uppercase formatted level
    :param level_dict: Dictionary defining all possible log levels of the morPy framework

    :return morpy_trace_eval: Evaluated and/or manipulated morpy_trace
    """

    import copy

    # Deepcopy morpy_trace to manipulate it "passdown only"
    morpy_trace_eval = copy.deepcopy(morpy_trace)

    # Set defaults
    log_enable = True
    pnt_enable = True
    morpy_trace_eval["pnt_enable"] = True

    # Check, if logging is enabled globally.
    if app_dict["conf"]["log_enable"]:

        # Evaluate the log level, if it is excluded from logging.
        for lvl_nolog in app_dict["conf"]["log_lvl_nolog"]:

            if level == lvl_nolog:
                morpy_trace_eval["log_enable"] = False
                log_enable = False
                break

    else: log_enable = False

    # Check, if printing is enabled globally.
    if app_dict["conf"]["msg_print"]:

        # Evaluate the log level, if it is excluded from printing.
        for lvl_noprint in app_dict["conf"]["log_lvl_noprint"]:

            if level == lvl_noprint:
                morpy_trace_eval["pnt_enable"] = False
                pnt_enable = False
                break

    else: pnt_enable = False

    # Evaluate the log level, if it will raise an interrupt.
    for lvl_intpt in app_dict["conf"]["log_lvl_interrupts"]:

        if level == lvl_intpt:
            morpy_trace_eval["interrupt_enable"] = True
            break

    # Count occurrences per log level. Count only if relevant regarding app parameters.
    # (see mpy_param.py to alter behaviour)
    if log_enable or pnt_enable:

        app_dict["run"]["events_total"] += 1
        app_dict["run"][f'events_{level.upper()}'] += 1

    return morpy_trace_eval

def log_event_handler(app_dict: dict, message: str, level: str) -> dict:
    r"""
    This function handles the log levels by formatting and counting events.

    :param app_dict: morPy global dictionary
    :param message: The message to be logged
    :param level: Defines the log level as handed by the calling function

    :return: dict
        level - uppercase formatted level
        level_dict - Dictionary defining all possible log levels of the morPy framework
    """

    # standardizing the log level to uppercase
    level = f'{level.lower()}'

    # Log level definition. Dictionary serves the purpose of avoiding a loop over a list.
    level_dict = {
        'init' : 'init',
        'debug' : 'debug',
        'info' : 'info',
        'warning' : 'warning',
        'denied' : 'denied',
        'error' : 'error',
        'critical' : 'critical',
        'exit' : 'exit',
        'undefined' : 'undefined'
    }

    # Set logging level UNDEFINED if not part of level definition
    try: level = level_dict[level]
    except: level = 'undefined'

    return {
            'level' : level,
            'level_dict' : level_dict
            }

def log_interrupt(morpy_trace: dict, app_dict: dict) -> None:
    r"""
    This function handles the interrupt routine of morPy.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary

    :return: -

    FIXME function is unstable.
        > Input after prompt does not work
        > Overwritten for the time being
    """

    import lib.fct as morpy_fct

    morpy_trace: dict = morpy_fct.tracing(morpy_trace["module"], morpy_trace["operation"], morpy_trace)
    morpy_trace["log_enable"] = False

    udict_true = is_udict(app_dict["morpy"])

    # Set the global interrupt flag
    if udict_true:
        with app_dict["morpy"].lock:
            app_dict["morpy"]["interrupt"] = True
    else:
        app_dict["morpy"]["interrupt"] = True

    # INTERRUPT <<< Type [y]es to quit or anything else to continue.
    input_str_long: str = app_dict["loc"]["morpy"]["msg_print_intrpt_yes"]
    input_str_short_1: str = input_str_long[0]
    input_str_short_2: str = input_str_long[1:]
    interrupt_prompt = (
        f'{app_dict["loc"]["morpy"]["msg_print_intrpt_1"]} '
        f'[{input_str_short_1}]{input_str_short_2} '
        f'{app_dict["loc"]["morpy"]["msg_print_intrpt_2"]}'
    )

    # Flush any buffered output so that no stray log messages are printed
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(0.1)

    # Instead of using sys.stdout (which may be redirected), use sys.__stdout__
    # to ensure that the prompt is printed cleanly.
    sys.__stdout__.write(f"{interrupt_prompt}\n")
    sys.__stdout__.flush()
    # usr_input = sys.__stdin__.readline().strip()
    # FIXME
    usr_input = "y"

    if usr_input.strip().lower() in {input_str_short_1.lower(), input_str_long.lower()}:
        # Reset the global interrupt flag
        if udict_true:
            with app_dict["morpy"].lock:
                app_dict["morpy"]["exit"] = True
        else:
            app_dict["morpy"]["exit"] = True
    else:
        # Reset the global interrupt flag
        if udict_true:
            with app_dict["morpy"].lock:
                app_dict["morpy"]["interrupt"] = False
        else:
            app_dict["morpy"]["interrupt"] = False

def log_msg_builder(app_dict: dict, log_dict: dict) -> str:
    r"""
    This function formats a complete log message ready to print.

    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations

    :return msg: hand back the standardized and complete log message
    """

    # Apply standard formats
    message = log_dict["message"]

    # Format the message
    msg_indented = ''

    # Indentation
    for line in message.splitlines():
        line_indented = f'\t{line}'

        # Check, if msg_indented is an empty string
        if msg_indented:
            msg_indented = f'{msg_indented}\n{line_indented}'
        else:
            msg_indented = line_indented

    # Build the log message
    if app_dict["conf"]["msg_verbose"]:
        msg = (f'{log_dict["level"].upper()} - {log_dict["datetimestamp"]}\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_trace"]}: {log_dict["tracing"]}\n\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_process_id"]}: {log_dict["process_id"]}\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_thread_id"]}: {log_dict["thread_id"]}\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_task_id"]}: {log_dict["task_id"]}\n\n'
              f'{msg_indented}\n')
    else:
        msg = f'{log_dict["level"].upper()} - {log_dict["datetimestamp"]}\n{msg_indented}\n'

    return msg

def msg_print(morpy_trace: dict, app_dict: dict, log_dict: dict) -> None:
    r"""
    This function prints logs on screen according to their log level. For
    further debugging an interrupt can be enabled for the according log
    levels.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations

    :return:
        -
    """

    # print messages according to their log level
    pnt = True

    for lvl_pnt in app_dict["conf"]["log_lvl_noprint"]:

        if log_dict["level"] == lvl_pnt:
            pnt = False
            break

    if pnt:
        print(log_dict["log_msg_complete"])
        # Enforce immediate output
        sys.stdout.flush()

    # Raise an interrupt if certain log levels are met
    if log_dict["interrupt_enable"]:
        log_interrupt(morpy_trace, app_dict)

def log_txt(morpy_trace: dict, app_dict: dict, log_dict: dict) -> None:
    r"""
    This function writes the logs into the defined textfile.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations

    :return:
        -
    """

    import lib.fct as morpy_fct

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'msg'
    operation: str = 'log_db(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
    morpy_trace["log_enable"] = False

    # Write to text file - Fallback if SQLite functionality is broken
    filepath = app_dict["conf"]["log_txt_path"]
    textfile_write(morpy_trace, app_dict, filepath, log_dict["log_msg_complete"])

def log_db(morpy_trace: dict, app_dict: dict, log_dict: dict) -> None:
    r"""
    This function writes the logs into the defined logging database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations

    :return:
        -
    """

    import lib.fct as morpy_fct

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'msg'
    operation: str = 'log_db(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
    morpy_trace["log_enable"] = False

    # Define the table to be adressed.
    db_path = app_dict["conf"]["log_db_path"]
    table_name = f'log_{app_dict["run"]["init_loggingstamp"]}'

    check: bool = log_db_table_check(morpy_trace, app_dict, db_path, table_name)

    # Define the columns for logging and their data types.
    columns = ["level","process_id","thread_id","task_id","datetimestamp","module","operation","tracing","message"]
    col_types = ["CHAR(20)","BIGINT","BIGINT","BIGINT","DATETIME","TEXT","TEXT","TEXT","TEXT"]

    # Check, if the actual logging table already exists.
    if not check:

        # Create table for logging during runtime.
        log_db_table_create(morpy_trace, app_dict, db_path, table_name)

        # Add columns to the new log table.
        log_db_table_add_column(morpy_trace, app_dict, db_path, table_name, columns, col_types)

    # Insert the actual log into the logging database table.
    log_db_row_insert(morpy_trace, app_dict, db_path, table_name, columns, log_dict)

def log_db_connect(morpy_trace: dict, app_dict: dict, db_path: str) -> object | None:
    r"""
    This function connects to a SQLite database. The database will be
    created if it does not exist already.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered

    :return:
        conn - Connection object or None
    """

    import lib.fct as morpy_fct
    import sys, sqlite3

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'msg'
    operation: str = 'log_db_connect(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
    morpy_trace["log_enable"] = False

    try:
        conn = sqlite3.connect(db_path)

        return conn

    except Exception as e:
        from lib.exceptions import MorPyException
        msg = (
            f'{type(e).__name__}: {e}\n'
            f'{app_dict["loc"]["morpy"]["log_db_connect_excpt"]}\n'
            f'db_path: {db_path}'
        )
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error", message=msg)

def log_db_disconnect(morpy_trace: dict, app_dict: dict, db_path: str) -> None:
    r"""
    This function disconnects a SQLite database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered

    :return:
        -
    """

    import lib.fct as morpy_fct
    import sys, sqlite3

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'msg'
    operation: str = 'log_db_disconnect(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
    morpy_trace["log_enable"] = False

    conn = None
    try:
        conn = sqlite3.connect(db_path)

    except Exception as e:
        from lib.exceptions import MorPyException
        msg = (
            f'{type(e).__name__}: {e}\n'
            f'{app_dict["loc"]["morpy"]["log_db_disconnect_excpt"]}\n'
            f'db_path: {db_path}'
        )
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error", message=msg)

    finally:
        if conn:
            conn.close()

def log_db_table_create(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str) -> None:
    r"""
    This function creates a table inside a SQLite database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered
    :param table_name: Name of the database table to be created

    :return:
        -
    """

    import lib.fct as morpy_fct
    import sys

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'msg'
    operation: str = 'log_db_table_create(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
    morpy_trace["log_enable"] = False

    # Apply standard formats
    table_name = f'{table_name}'

    # Define the execution statement
    exec_statement = \
        f'CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY)'

    # Execution
    try:
        # Connect the database
        conn = log_db_connect(morpy_trace, app_dict, db_path)

        # Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

        # Create the actual table
        conn.execute(exec_statement)

        # Commit changes to the database
        conn.commit()

        # Disconnect from the database
        log_db_disconnect(morpy_trace, app_dict, db_path)

    except Exception as e:
        from lib.exceptions import MorPyException
        msg = (
            f'{type(e).__name__}: {e}\n'
            f'{app_dict["loc"]["morpy"]["log_db_table_create_excpt"]}\n'
            f'{app_dict["loc"]["morpy"]["log_db_table_create_stmt"]}: {exec_statement}'
        )
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error", message=msg)

def log_db_table_check(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str) -> bool | None:
    r"""
    This function checks on the existence of a table inside a given SQLite
    database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered
    :param table_name: Name of the database table to be created

    :return check: If TRUE, the table was found
    """

    import lib.fct as morpy_fct
    import sys

    module: str = 'msg'
    operation: str = 'log_db_table_check(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    morpy_trace["log_enable"] = False
    table_name = f'{table_name}'
    check: bool = False

    # Define the execution statement
    exec_statement = (f'SELECT count(name) FROM sqlite_master WHERE type=\'table\' AND name=\'{table_name}\'')

    try:
        # Connect the database
        conn = log_db_connect(morpy_trace, app_dict, db_path)

        # Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

        c = conn.cursor()

        # Check for the existence of a table
        c.execute(exec_statement)

        # Check the count of found tables
        if c.fetchone()[0] == 1:
            check: bool = True

        # Close the cursor
        c.close()

        # Disconnect from the database
        log_db_disconnect(morpy_trace, app_dict, db_path)

        return check

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

def log_db_table_add_column(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str, columns: list,
                            col_types: list) -> bool | None:
    r"""
    This function inserts a column into a table inside a given SQLite
    database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be adressed or altered
    :param table_name: Name of the database table to be created
    :param columns: List of the columns to be added
    :param col_types: List of datatypes for the columns as specified for SQLite

    :return check: If TRUE, the function was successful
    """

    import lib.fct as morpy_fct
    import sys

    module: str = 'msg'
    operation: str = 'log_db_table_add_column(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    morpy_trace["log_enable"] = False
    table_name = f'{table_name}'

    try:
        # Check the existence of the table
        check: bool = log_db_table_check(morpy_trace, app_dict, db_path, table_name)

        if check:

            # Connect the database
            conn = log_db_connect(morpy_trace, app_dict, db_path)

            # Activate WAL mode to acces the database
            conn.execute('pragma journal_mode=wal;')

            i = 0

            for col in columns:
                # Define the execution statement
                exec_statement = f'ALTER TABLE {table_name} ADD COLUMN {columns[i]} {col_types[i]}'

                # Execution
                try:
                    # Insert a new row and write to cell(s)
                    conn.execute(exec_statement)

                    # Commit changes to the database and close the cursor
                    conn.commit()

                # Error detection
                except Exception as e:
                    # The log table could not be edited.
                    raise RuntimeError(
                        f'{app_dict["loc"]["morpy"]["log_db_table_add_column_excpt"]}\n'
                        f'{app_dict["loc"]["morpy"]["log_db_table_add_column_stmt"]}: {exec_statement}'
                    )

                i += 1

            # Disconnect from the database
            log_db_disconnect(morpy_trace, app_dict, db_path)

        else:
            # The log table could not be found. Logging not possible.
            message = app_dict["log_db_table_add_column_failed"]
            log(morpy_trace, app_dict, message, 'critical')

        return check

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

def log_db_row_insert(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str, columns: list,
                      log_dict: dict) -> dict[str, int | bool | None] | None:
    r"""
    This function inserts a row into a table inside a given SQLite
    database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be adressed or altered
    :param table_name: Name of the database table to be created
    :param columns: List of the columns to be added
    :param log_dict: Passthrough dictionary for logging operations

    :return: dict
        check - If TRUE, the function was successful
        row_id - ID of the row inserted
    """

    import lib.fct as morpy_fct
    import sys

    module: str = 'msg'
    operation: str = 'log_db_row_insert(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    morpy_trace["log_enable"] = False
    table_name = f'{table_name}'
    row_id = 0

    try:
        # Define the execution statement
        exec_statement = f'INSERT INTO {table_name} (\'level\',\'process_id\',\'thread_id\',\'task_id\',\'datetimestamp\',\'module\',\'operation\',\'tracing\',\'message\') VALUES (?,?,?,?,?,?,?,?,?)'

        # Check the existence of the table
        check: bool = log_db_table_check(morpy_trace, app_dict, db_path, table_name)

        if check:

            # Connect the database
            conn = log_db_connect(morpy_trace, app_dict, db_path)

            # Activate WAL mode to acces the database
            conn.execute('pragma journal_mode=wal;')

            # Execution
            try:
                c = conn.cursor()

                # Insert a new row and write to cell(s)
                c.execute(exec_statement, (
                          log_dict["level"].upper(),
                          log_dict["process_id"],
                          log_dict["thread_id"],
                          log_dict["task_id"],
                          log_dict["datetime_value"],
                          log_dict["module"],
                          log_dict["operation"],
                          log_dict["tracing"],
                          log_dict["message"]),
                          )

                # Check for the last ID
                row_id = int(c.lastrowid)

                # Commit changes to the database and close the cursor
                conn.commit()
                c.close()

            # Error detection
            except Exception as e:
                # The log entry could not be created.
                raise RuntimeError(
                    f'{app_dict["loc"]["morpy"]["log_db_row_insert_excpt"]}\n'
                    f'{app_dict["loc"]["morpy"]["log_db_row_insert_stmt"]}: {exec_statement}'
                )

            # Disconnect from the database
            log_db_disconnect(morpy_trace, app_dict, db_path)

        else:
            # The log table could not be found. Logging not possible.
            message = app_dict["log_db_row_insert_failed"]
            log(morpy_trace, app_dict, message, 'critical')

        return{
            'check' : check ,
            'row_id' : row_id
            }

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")