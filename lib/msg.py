r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers functions to debug, warn and log any operations
            executed within the morPy framework. At the same time it processes
            all kinds of messaging, whether it be via console or ui.
"""

import lib.fct as morpy_fct
from lib.common import textfile_write
from lib.decorators import core_wrap
from lib.mp import is_udict

import sys
import time
from sqlite3 import Connection as sqlite3_Connection


def log(trace: dict, app_dict: dict, level: str, message: callable, verbose: bool) -> None:
    r"""
    This function writes an event to a specified file and/or prints it out
    according to it's severity (level).

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param level: Severity: debug/info/warning/error/critical/denied
    :param message: A callable (e.g., lambda or function) that returns the log message.
    :param verbose: If True, message is only logged in verbose mode.

    :example:
        log(trace, app_dict, level, message)

    TODO Implement a mechanism to keep logfile size in check
        > Preferably auto delete logs based on "no errors occurred" per process, task, thread and __main__
    """

    trace_eval: dict | None = None

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
            if udict_true:
                with app_dict["morpy"].lock:
                    interrupt = app_dict["morpy"]["interrupt"]
            else:
                interrupt = app_dict["morpy"]["interrupt"]


        # Event handling (counting and formatting)
        log_event_dict = log_event_handler(level)

        # The log level will be evaluated as long as logging or prints to console are enabled. The
        # trace may be manipulated.
        if app_dict["morpy"]["conf"]["msg_print"] or app_dict["morpy"]["conf"]["log_enable"]:
            trace_eval = log_eval(trace, app_dict, log_event_dict["level"])

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
            'module' : trace_eval["module"],
            'operation' : trace_eval["operation"],
            'tracing' : trace_eval["tracing"],
            'process_id' : trace_eval["process_id"],
            'thread_id' : trace_eval["thread_id"],
            'task_id' : trace_eval["task_id"],
            'message' : message,
            'log_msg_complete' : None,
            'log_enable' : trace_eval["log_enable"] ,
            'pnt_enable' : trace_eval["pnt_enable"] ,
            'interrupt_enable' : trace_eval["interrupt_enable"]
        }

        # Build the complete log message
        msg = log_msg_builder(app_dict, log_dict)
        log_dict["log_msg_complete"] = msg

        # Buffer logging parameters
        logging = app_dict["morpy"]["conf"]["log_enable"] and log_dict["log_enable"]
        write_log_txt = logging and app_dict["morpy"]["conf"]["log_txt_enable"]
        write_log_db = logging and app_dict["morpy"]["conf"]["log_db_enable"]
        print_log = app_dict["morpy"]["conf"]["msg_print"]

        if trace["process_id"] == app_dict["morpy"]["proc_master"]:
            # Go on with logging directly if calling process is orchestrator.
            log_task(trace, app_dict, log_dict, write_log_txt, write_log_db, print_log)
        else:
            # Enqueue the orchestrator task
            task = [log_task, trace, app_dict, log_dict, write_log_txt, write_log_db, print_log]
            log_enqueue(app_dict, task=task)
            # Generate print required for GUIs in the regarding child process.
            # FIXME child processes need their own io stream
            # if print_log:
            #     msg_print(trace, app_dict, log_dict)

    except Exception as e:
        from lib.exceptions import MorPyException
        # Severe morPy logging error.
        err_msg = f'{app_dict["loc"]["morpy"]["log_crit_fail"]}\n{e}'
        raise MorPyException(trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error", message=err_msg)

    finally:
        # Clean up
        del log_dict
        del trace


def log_enqueue(app_dict: dict, priority: int=-100, task: list=None) -> None:
    r"""
    Adds a logging task to the morPy process queue.

    :param app_dict: morPy global dictionary containing app configurations
    :param priority: Integer representing task priority (lower is higher priority)
    :param task: Tuple of a callable, *args and **kwargs (func, *args, **kwargs)

    :example:
        task = [log_task, trace, app_dict]
        log_enqueue(trace, app_dict, task=task)
    """

    # Substitute UltraDict references to mitigate RecursionError
    def substitute(obj):
        from UltraDict import UltraDict
        if isinstance(obj, UltraDict):
            name_val = obj.name
            return (f"__morPy_shared_ref__::{name_val}",
                    obj.shared_lock,
                    obj.auto_unlink,
                    obj.recurse)
        elif isinstance(obj, list):
            return [substitute(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(substitute(item) for item in obj)
        elif isinstance(obj, dict):
            return {substitute(key): substitute(value) for key, value in obj.items()}
        else:
            return obj

    if task:
        # Substitute UltraDict references in task to avoid recursion issues.
        task_sanitized = substitute(task)

        with app_dict["morpy"].lock:
            next_task_id = app_dict["morpy"]["tasks_created"] + 1

            with app_dict["morpy"]["heap_shelf"].lock:
                task_sys_id = id(task)

                # Push task to heap shelf
                task_qed = (priority, next_task_id, task_sys_id, task_sanitized, False)

                app_dict["morpy"]["heap_shelf"][next_task_id] = task_qed

        app_dict["morpy"]["tasks_created"] += 1


def log_task(trace: dict, app_dict: dict, log_dict: dict, write_log_txt: bool, write_log_db: bool,
             print_log: bool) -> None:
    r"""
    Task that finally writes the logs. May be handed to orchestrator via priority queue.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations
    :param write_log_txt: If True, log is written to textfile.
    :param write_log_db: If True, log is written to database.
    :param print_log: If True, logs are printed to console.

    :example:
        log_task(trace, app_dict, log_dict, write_log_txt, write_log_db, print_log)
    """

    if write_log_txt:
        # Write to text file - Fallback if SQLite functionality is broken
        log_txt_write(log_dict, app_dict, log_dict)

    if write_log_db:
        # Write to logging database
        log_db_write(log_dict, app_dict, log_dict)

    if print_log:
        # Print the events according to their log level
        msg_print(trace, app_dict, log_dict)


def log_eval(trace: dict, app_dict: dict, level: str) -> dict:
    r"""
    This function evaluates the log level and makes manipulation of trace
    possible for pass-down only. That means, for the purpose of logging, certain
    parameters (keys) may be altered in check with mpy_param.py or other parts
    of the code to hide, extend, enable or what else is needed for a log.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param level: uppercase formatted level

    :return trace_eval: Evaluated and/or manipulated trace
    """

    import copy

    # Deepcopy trace to manipulate it "pass-down only"
    trace_eval = copy.deepcopy(trace)

    # Set defaults
    log_enable = True
    pnt_enable = True
    trace_eval["pnt_enable"] = True

    # Check, if logging is enabled globally.
    if app_dict["morpy"]["conf"]["log_enable"]:
        # Evaluate the log level, if it is excluded from logging.
        if level in app_dict["morpy"]["conf"]["log_lvl_nolog"]:
            trace_eval["log_enable"] = False
            log_enable = False
    else:
        log_enable = False

    # Check, if printing is enabled globally.
    if app_dict["morpy"]["conf"]["msg_print"]:
        # Evaluate the log level, if it is excluded from printing.
        if level in app_dict["morpy"]["conf"]["log_lvl_noprint"]:
            trace_eval["pnt_enable"] = False
            pnt_enable = False
    else:
        pnt_enable = False

    # Evaluate the log level, if it will raise an interrupt.
    if level in app_dict["morpy"]["conf"]["log_lvl_interrupts"]:
        trace_eval["interrupt_enable"] = True

    # Count occurrences per log level. Count only if relevant regarding app parameters.
    # (see mpy_param.py to alter behaviour)
    if log_enable or pnt_enable:
        app_dict["morpy"]["events_total"] += 1
        app_dict["morpy"][f'events_{level.upper()}'] += 1

    return trace_eval


def log_event_handler(level: str) -> dict:
    r"""
    This function handles the log levels by formatting and counting events.

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
    except KeyError: level = 'undefined'

    return {
            'level' : level,
            'level_dict' : level_dict
            }


def log_interrupt(trace: dict, app_dict: dict) -> None:
    r"""
    This function handles the interrupt routine of morPy.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    """

    trace: dict = morpy_fct.tracing(trace["module"], trace["operation"], trace)
    trace["log_enable"] = False

    udict_true = is_udict(app_dict["morpy"])

    # Set the global interrupt flag
    if udict_true:
        with app_dict["morpy"].lock:
            app_dict["morpy"]["interrupt"] = True
    else:
        app_dict["morpy"]["interrupt"] = True

    # INTERRUPT <<< Type [y]es to quit or anything else to try continuing.
    input_str_long: str = app_dict["loc"]["morpy"]["log_interrupt_yes"]
    input_str_short_1: str = input_str_long[0]
    input_str_short_2: str = input_str_long[1:]
    interrupt_prompt = (
        f'{app_dict["loc"]["morpy"]["log_interrupt_1"]} '
        f'[{input_str_short_1}]{input_str_short_2} '
        f'{app_dict["loc"]["morpy"]["log_interrupt_2"]}'
    )

    # Flush any buffered output so that no stray log messages are printed
    sys.stdout.flush()
    sys.stderr.flush()

    # Instead of using sys.stdout (which may be redirected), use sys.__stdout__
    # to ensure that the prompt is printed cleanly.
    sys.__stdout__.write(f"{interrupt_prompt}\n")
    sys.__stdout__.flush()
    usr_input = sys.__stdin__.readline().strip()

    print('\n')

    if usr_input.strip().lower() in {input_str_short_1.lower(), input_str_long.lower()}:
        # Reset the global interrupt flag
        if udict_true:
            with app_dict["morpy"].lock:
                app_dict["morpy"]["exit"] = True
        else:
            app_dict["morpy"]["exit"] = False

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

    message = log_dict["message"]
    msg_indented = ''

    # Message indentation
    for line in message.splitlines():
        line_indented = f'\t{line}'

        # Check, if msg_indented is an empty string
        if msg_indented:
            msg_indented = f'{msg_indented}\n{line_indented}'
        else:
            msg_indented = line_indented

    # Build the log message
    if app_dict["morpy"]["conf"]["msg_verbose"]:
        msg = (f'{log_dict["level"].upper()} - {log_dict["datetimestamp"]}\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_trace"]}: {log_dict["tracing"]}\n\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_process_id"]}: {log_dict["process_id"]}\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_thread_id"]}: {log_dict["thread_id"]}\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_task_id"]}: {log_dict["task_id"]}\n\n'
              f'{msg_indented}\n')
    else:
        msg = f'{log_dict["level"].upper()} - {log_dict["datetimestamp"]}\n{msg_indented}\n'

    return msg


def msg_print(trace: dict, app_dict: dict, log_dict: dict) -> None:
    r"""
    This function prints logs on screen according to their log level. For
    further debugging an interrupt can be enabled for the according log
    levels.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations
    """

    # print messages according to their log level
    pnt = True

    for lvl_pnt in app_dict["morpy"]["conf"]["log_lvl_noprint"]:

        if log_dict["level"] == lvl_pnt:
            pnt = False
            break

    if pnt:
        print(log_dict["log_msg_complete"])
        # Enforce immediate output
        sys.stdout.flush()

    # Raise an interrupt if certain log levels are met
    if log_dict["interrupt_enable"]:
        log_interrupt(trace, app_dict)


@core_wrap
def log_txt_write(trace: dict, app_dict: dict, log_dict: dict) -> None:
    r"""
    This function writes the logs into the defined textfile.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations
    """

    trace["log_enable"] = False

    # Write to text file - Fallback if SQLite functionality is broken
    filepath = app_dict["morpy"]["conf"]["log_txt_path"]
    textfile_write(trace, app_dict, filepath, log_dict["log_msg_complete"])


@core_wrap
def log_db_init(trace: dict, app_dict: dict) -> None:
    r"""
    This function writes the logs into the defined logging database.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    """

    trace["log_enable"] = False

    # Define the table to be addressed.
    db_path = app_dict["morpy"]["conf"]["log_db_path"]
    table_name = f'log_{app_dict["morpy"]["init_loggingstamp"]}'

    # Define the columns for logging and their data types.
    columns = ["level","process_id","thread_id","task_id","datetimestamp","module","operation","tracing","message"]
    col_types = ["CHAR(20)","BIGINT","BIGINT","BIGINT","DATETIME","TEXT","TEXT","TEXT","TEXT"]

    # Create table for logging during runtime.
    log_db_table_create(trace, app_dict, db_path, table_name)

    # Add columns to the new log table.
    log_db_table_add_column(trace, app_dict, db_path, table_name, columns, col_types)


@core_wrap
def log_db_write(trace: dict, app_dict: dict, log_dict: dict) -> None:
    r"""
    This function writes the logs into the defined logging database.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations
    """

    trace["log_enable"] = False

    # Define the table to be addressed.
    db_path = app_dict["morpy"]["conf"]["log_db_path"]
    table_name = f'log_{app_dict["morpy"]["init_loggingstamp"]}'

    # Insert the actual log into the logging database table.
    log_db_row_insert(trace, app_dict, db_path, table_name, log_dict)


# Suppress linting for mandatory arguments.
# noinspection PyUnusedLocal
@core_wrap
def log_db_connect(trace: dict, app_dict: dict, db_path: str) -> sqlite3_Connection:
    r"""
    This function connects to a SQLite database. The database will be
    created if it does not exist already.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered

    :return conn: SQLite3 connection object
    """

    import sqlite3

    trace["log_enable"] = False
    return sqlite3.connect(db_path)


@core_wrap
def log_db_table_create(trace: dict, app_dict: dict, db_path: str, table_name: str) -> None:
    r"""
    This function creates a table inside a SQLite database.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered
    :param table_name: Name of the database table to be created
    """

    trace["log_enable"] = False

    table_name = f'{table_name}'
    # Define the execution statement
    exec_statement = f'CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY)'
    # Connect the database
    conn = log_db_connect(trace, app_dict, db_path)
    # Activate WAL mode to access the database
    conn.execute('pragma journal_mode=wal;')
    # Create the actual table
    conn.execute(exec_statement)
    # Commit changes to the database
    conn.commit()


@core_wrap
def log_db_table_add_column(trace: dict, app_dict: dict, db_path: str, table_name: str, columns: list,
                            col_types: list) -> None:
    r"""
    This function inserts a column into a table inside a given SQLite
    database.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered
    :param table_name: Name of the database table to be created
    :param columns: List of the columns to be added
    :param col_types: List of datatypes for the columns as specified for SQLite
    """

    trace["log_enable"] = False

    table_name = f'{table_name}'
    # Connect the database
    conn = log_db_connect(trace, app_dict, db_path)
    # Activate WAL mode to access the database
    conn.execute('pragma journal_mode=wal;')

    for i, _ in enumerate(columns):
        # Define the execution statement
        exec_statement = f'ALTER TABLE {table_name} ADD COLUMN {columns[i]} {col_types[i]}'
        # Insert a new row and write to cell(s)
        conn.execute(exec_statement)
        # Commit changes to the database and close the cursor
        conn.commit()


@core_wrap
def log_db_row_insert(trace: dict, app_dict: dict, db_path: str, table_name: str, log_dict: dict) -> dict[str, int | bool | None] | None:
    r"""
    This function inserts a row into a table inside a given SQLite
    database.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered
    :param table_name: Name of the database table to be created
    :param log_dict: Passthrough dictionary for logging operations

    :return: dict
        check - If TRUE, the function was successful
        row_id - ID of the row inserted
    """

    trace["log_enable"] = False
    table_name = f'{table_name}'

    # Define the execution statement
    exec_statement = f'INSERT INTO {table_name} (\'level\',\'process_id\',\'thread_id\',\'task_id\',\'datetimestamp\',\'module\',\'operation\',\'tracing\',\'message\') VALUES (?,?,?,?,?,?,?,?,?)'

    # Connect the database
    conn = log_db_connect(trace, app_dict, db_path)

    # Activate WAL mode to access the database
    conn.execute('pragma journal_mode=wal;')

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

    return{
        'row_id' : row_id
        }