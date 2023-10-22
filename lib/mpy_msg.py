"""
Author:     Bastian Neuwirth
Date:       29.10.2021
Version:    0.1
Descr.:     This module delivers functions to debug, warn and log any operations
            executed within the morPy framework.
"""

def log(mpy_trace, prj_dict, log_message, level):

    """ This function writes an event to a specified file and/or prints it out
        according to it's severity (level).
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        log_message - The message to be logged
        level - Severity: debug/info/warning/error/critical/denied
    :return
        -

    TODO
    Reserve a process to work on a log queue for all other threads
        > Implement the feature for a minimum of 3 logical cores
        > Have a thread queue implemented per enabled threads per core (see mpy_param.py 'mt_max_threads_cnt_abs')
    Implement a mechanism to keep logfile size in check
    """

    import mpy_fct
    import gc

#   FIXME Wait for an interrupt to end
    while prj_dict['mpy_interrupt'] == True:
        pass

#   Event handling (counting and formatting)
    log_event_dict = log_event_handler(prj_dict, log_message, level)
    level_dict = log_event_dict['level_dict']

#   The log level will be evaluated as long as logging or prints to console are enabled. The
#   mpy_trace may be manipulated.
    if prj_dict['mpy_msg_print'] == True or prj_dict['mpy_log_enable'] == True:
        mpy_trace_eval = log_eval(mpy_trace, prj_dict, log_event_dict['level'], level_dict)

#   Retrieve a log specific datetimestamp
    time_lst = mpy_fct.datetime_now(mpy_trace_eval)
    datetimestamp = time_lst['datetimestamp']
    datetime_value = time_lst['datetime_value']

#   TODO log_enable evaluation
#   Def new function log_eval(~)
#   Always log the levels, that would raise an interrupt as long as prj_dict['mpy_log_enable'] is true.
#       prj_dict['mpy_log_lvl_nolog'] == False and
#       mpy_trace_eval['log_enable'] == True and
#       prj_dict['mpy_log_enable'] == True
#   Update log_dict with the return value
#   Use the return before log_txt and log_db call

#   Prepare a passthrough dictionary for logging operations
    log_dict = { \
                'level' : log_event_dict['level'], \
                'datetimestamp' : datetimestamp, \
                'datetime_value' : datetime_value, \
                'module' : mpy_trace_eval['module'], \
                'operation' : mpy_trace_eval['operation'], \
                'tracing' : mpy_trace_eval['tracing'], \
                'process_id' : mpy_trace_eval['process_id'], \
                'thread_id' : mpy_trace_eval['thread_id'], \
                'task_id' : mpy_trace_eval['task_id'], \
                'log_message' : log_message, \
                'log_msg_complete' : 'VOID', \
                'log_enable' : mpy_trace_eval['log_enable'] , \
                'interrupt_enable' : mpy_trace_eval['interrupt_enable']
                }

#   Build the complete log message
    msg = log_msg_builder(prj_dict, log_dict)

#   Prepare a passthrough dictionary for logging operations
    log_dict['log_msg_complete'] = msg

    if prj_dict['mpy_log_enable'] == True and \
        log_dict['log_enable'] == True and \
        prj_dict['mpy_log_txt_enable'] == True:

    #   Write to text file - Fallback if SQLite functionality is broken
        log_txt(log_dict, prj_dict, log_dict)

    if prj_dict['mpy_log_enable'] == True and \
        log_dict['log_enable'] == True and \
        prj_dict['mpy_log_db_enable'] == True:

    #   Write to logging database
        log_db(log_dict, prj_dict, log_dict)

#   Print messages according to mpy_param.py
    if prj_dict['mpy_msg_print'] == True:

    #   Print the events according to their log level
        mpy_msg_print(mpy_trace, prj_dict, log_dict)

#   Garbage collection
    del log_dict
    del mpy_trace
    gc.collect()

def log_eval(mpy_trace, prj_dict, level, level_dict):

    """ This function evaluates the log level and makes manipulation of mpy_trace
        possible for passdown only. That means, for the purpose of logging, certain
        parameters (keys) may be altered in check with mpy_param.py or other parts
        of the code to hide, extend, enable or what else is needed for a log.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        level - uppercase formatted level
        level_dict - Dictionary defining all possible log levels of the morPy framework
    :return
        mpy_trace_eval - Evaluated and/or manipulated mpy_trace
    """

    import copy

#   Deepcopy mpy_trace to manipulate it passdown only
    mpy_trace_eval = copy.deepcopy(mpy_trace)

#   Evaluate the log level, if it is excluded from logging.
    for lvl_nolog in prj_dict['mpy_log_lvl_nolog']:

        if level == lvl_nolog:
            mpy_trace_eval['log_enable'] = False
            break

#   Evaluate the log level, if it will raise an interrupt.
    for lvl_intpt in prj_dict['mpy_log_lvl_interrupts']:

        if level == lvl_intpt:
            mpy_trace_eval['interrupt_enable'] = True
            break

    return mpy_trace_eval

def log_event_handler(prj_dict, log_message, level):

    """ This function handles the log levels by formatting and counting events.
    :param
        prj_dict - morPy global dictionary
        log_message - The message to be logged
        level - Defines the log level as handed by the calling function
    :return - dictionary
        level - uppercase formatted level
        level_dict - Dictionary defining all possible log levels of the morPy framework
    """

#   standardizing the log level to uppercase
    level = str(level.upper())

#   Log level definition
    level_dict = { \
                'INIT' : 'INIT', \
                'DEBUG' : 'DEBUG', \
                'INFO' : 'INFO', \
                'WARNING' : 'WARNING', \
                'DENIED' : 'DENIED', \
                'ERROR' : 'ERROR', \
                'CRITICAL' : 'CRITICAL', \
                'EXIT' : 'EXIT', \
                'UNDEFINED' : 'UNDEFINED' \
                }

#   Set logging level UNDEFINED if not part of level definition
    try:
        level = level_dict[level]
    except:
        level = 'UNDEFINED'

#   Count occurences per log level; count only if logging is enabled or if
#   prints are generated (see mpy_param.py paramters mpy_msg_print and mpy_log_enable)
    if prj_dict['mpy_msg_print'] == True or prj_dict['mpy_log_enable'] == True:

        prj_dict['events_total'] = int(prj_dict['events_total']) + 1
        prj_dict['events_' + level] = int(prj_dict['events_' + level]) + 1

    return {
            'level' : level, \
            'level_dict' : level_dict
            }

def log_interrupt(mpy_trace, prj_dict):

    """ This function handles the interrupt routine of morPy.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
    :return
        -

    TODO
    Change the way an interrupt is displayed. Working threads should somehow
    not overwrite the interrupt message or copy it or something.
        > use condition objects i.e. notify()
        > see https://docs.python.org/2/library/threading.html#condition-objects
    """

    import mpy_fct

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_msg'
    # operation = 'log_interrupt(~)'
    mpy_trace = mpy_fct.tracing(mpy_trace['module'], mpy_trace['operation'], mpy_trace)
    mpy_trace['log_enable'] = False

#   Set the global interrupt flag
    prj_dict['mpy_interrupt'] = True

#   >>> INTERRUPT <<< Press Enter to continue...
    msg_text = prj_dict['mpy_msg_print_intrpt']
    log_wait_for_input(mpy_trace, prj_dict, msg_text)

#   Reset the global interrupt flag
    prj_dict['mpy_interrupt'] = False

def log_msg_builder(prj_dict, log_dict):

    """ This function formats a complete log message ready to print.
    :param
        prj_dict - morPy global dictionary
        log_dict - Passthrough dictionary for logging operations
    :return
        msg - hand back the standardized and complete log message
    """

#   Apply standard formats
    log_message = log_dict['log_message']

#   Format the message
    msg_indented = ''

#   Indentation
    for line in log_message.splitlines():
        line_Indented = '\t' + str(line)

        if msg_indented == '':
            msg_indented = line_Indented
        else:
            msg_indented = msg_indented + '\n' + line_Indented

#   Build the log message
    msg = (log_dict['level'] + ' - ' + log_dict['datetimestamp'] + '\n\t' \
          + prj_dict['log_msg_builder_trace'] + ': ' + log_dict['tracing'] + '\n\n\t' \
          + prj_dict['log_msg_builder_process_id'] + ': ' + str(log_dict['process_id']) + '\n\t' \
          + prj_dict['log_msg_builder_thread_id'] + ': ' + str(log_dict['thread_id']) + '\n\n' \
          + str(msg_indented + '\n'))

    return msg

def mpy_msg_print(mpy_trace, prj_dict, log_dict):

    """ This function prints logs on screen according to their log level. For
        further debugging an interrupt can be enabled for the according log
        levels.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        log_dict - Passthrough dictionary for logging operations
    :return
        -

    TODO
    Also Enable an Interrupt with TKinter (not just console)
    """

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_msg'
    # operation = 'mpy_msg_print(~)'
    # mpy_trace = mpy_fct.tracing(mpy_trace['module'], mpy_trace['operation'], mpy_trace)
    # mpy_trace['log_enable'] = False

#   print messages according to their log level
    pnt = True

    for lvl_pnt in prj_dict['mpy_log_lvl_noprint']:

        if log_dict['level'] == lvl_pnt:
            pnt = False
            break

    if pnt == True:
        print(log_dict['log_msg_complete'])

#   Raise an interrupt if certain log levels are met
    if log_dict['interrupt_enable'] == True:
        log_interrupt(mpy_trace, prj_dict)

def log_txt(mpy_trace, prj_dict, log_dict):

    """ This function writes the logs into the defined textfile.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        log_dict - Passthrough dictionary for logging operations
    :return
        -
    """

    import mpy_fct

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_msg'
    operation = 'log_db(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)
    mpy_trace['log_enable'] = False

#   Write to text file - Fallback if SQLite functionality is broken
    filepath = prj_dict.get('log_txt_path')
    mpy_fct.txt_wr(mpy_trace, prj_dict, filepath, log_dict['log_msg_complete'])

def log_db(mpy_trace, prj_dict, log_dict):

    """ This function writes the logs into the defined logging database.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        log_dict - Passthrough dictionary for logging operations
    :return
        -
    """

    import mpy_fct

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_msg'
    operation = 'log_db(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)
    mpy_trace['log_enable'] = False

#   Define the table to be adressed
    db_path = prj_dict['log_db_path']
    table_name = 'log_' + str(prj_dict['init_loggingstamp'])

    check = log_db_table_check(mpy_trace, prj_dict, db_path, table_name)

#   Define the columns for logging and their data types
    columns = ['level','process_id','thread_id','task_id','datetimestamp','module','operation','tracing','message']
    col_types = ['CHAR(20)','BIGINT','BIGINT','BIGINT','DATETIME','TEXT','TEXT','TEXT','TEXT']

#   Create table for logging during runtime
    if check == False:

        log_db_table_create(mpy_trace, prj_dict, db_path, table_name)

    #   Add columns to the new log table
        log_db_table_add_column(mpy_trace, prj_dict, db_path, table_name, columns, col_types)

#   Insert the actual log into the logging database table
    log_db_row_insert(mpy_trace, prj_dict, db_path, table_name, columns, log_dict)

def log_db_connect(mpy_trace, prj_dict, db_path):

    """ This function connects to a SQLite database. The database will be
        created if it does not exist already.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        db_path - Path to the db to be adressed or altered
    :return
        conn - Connection object or None
    """

    import mpy_fct
    import sys, sqlite3

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_msg'
    operation = 'log_db_connect(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)
    mpy_trace['log_enable'] = False


    conn = None
    try:
        conn = sqlite3.connect(db_path)

        return conn

#   Error detection
    except Exception as e:
    #   The database could not be found and/or connected.
        log_message = prj_dict['log_db_connect_excpt'] + '\n' \
                      + 'db_path: ' + str(db_path) + '\n'  \
                      + prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'critical')

def log_db_disconnect(mpy_trace, prj_dict, db_path):

    """ This function disconnects a SQLite database.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        db_path - Path to the db to be adressed or altered
    :return
        -
    """

    import mpy_fct
    import sys, sqlite3

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_msg'
    operation = 'log_db_disconnect(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)
    mpy_trace['log_enable'] = False

    conn = None
    try:
        conn = sqlite3.connect(db_path)

#   Error detection
    except Exception as e:
    #   The database could not be found and/or disconnected.
        log_message = prj_dict['log_db_disconnect_excpt'] + '\n' \
                      + 'db_path: ' + str(db_path) + '\n'  \
                      + prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'critical')

    finally:
        if conn:
            conn.close()

def log_db_table_create(mpy_trace, prj_dict, db_path, table_name):

    """ This function creates a table inside a SQLite database.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        db_path - Path to the db to be adressed or altered
        table_name - Name of the database table to be created
    :return
        -
    """

    import mpy_fct
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_msg'
    operation = 'log_db_table_create(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)
    mpy_trace['log_enable'] = False

#   Apply standard formats
    table_name = str(table_name)

#   Define the execution statement
    exec_statement = \
        'CREATE TABLE IF NOT EXISTS {} '. \
        format(table_name) \
        + '(ID INTEGER PRIMARY KEY)'

#   Execution
    try:
    #   Connect the database
        conn = log_db_connect(mpy_trace, prj_dict, db_path)

    #   Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

    #   Create the actual table
        conn.execute(exec_statement)

    #   Commit changes to the database
        conn.commit()

    #   Disconnect from the database
        log_db_disconnect(mpy_trace, prj_dict, db_path)

#   Error detection
    except Exception as e:
    #   The log table for runtime could not be created.
        log_message = prj_dict['log_db_table_create_excpt'] + '\n' \
                      + prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n'  \
                      + prj_dict['log_db_table_create_stmt'] + ': {}'. format(exec_statement)
        log(mpy_trace, prj_dict, log_message, 'critical')

def log_db_table_check(mpy_trace, prj_dict, db_path, table_name):

    """ This function checks on the existence of a table inside a given SQLite
        database.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        db_path - Path to the db to be adressed or altered
        table_name - Name of the database table to be checked on
    :return (dictionary)
        check - If TRUE, the table was found
    """

    import mpy_fct
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_msg'
    operation = 'log_db_table_check(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)
    mpy_trace['log_enable'] = False

#   Apply standard formats
    table_name = str(table_name)
    check = False

#   Define the execution statement
    exec_statement = \
        'SELECT count(name) FROM sqlite_master WHERE ' \
         + 'type=\'table\' AND name=\'{}\''. \
         format(table_name)

#   Execution
    try:
    #   Connect the database
        conn = log_db_connect(mpy_trace, prj_dict, db_path)

    #   Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

        c = conn.cursor()

    #   Check for the existence of a table
        c.execute(exec_statement)

    #   Check the count of found tables
        if c.fetchone()[0] == 1:
            check = True

    #   Close the cursor
        c.close()

    #   Disconnect from the database
        log_db_disconnect(mpy_trace, prj_dict, db_path)

        return check

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n'  \
                      + prj_dict['log_db_table_create_stmt'] + ': {}'. format(exec_statement)
        log(mpy_trace, prj_dict, log_message, 'critical')

def log_db_table_add_column(mpy_trace, prj_dict, db_path, table_name, columns, col_types):

    """ This function inserts a column into a table inside a given SQLite
        database.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        db_path - Path to the db to be adressed or altered
        table_name - Name of the database table to be created
        columns - List of the columns to be added
        col_types - List of datatypes for the columns as specified for SQLite
    :return
        check - If TRUE, the function was successful
    """

    import mpy_fct
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_msg'
    operation = 'log_db_table_add_column(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)
    mpy_trace['log_enable'] = False

#   Apply standard formats
    table_name = str(table_name)

#   Execution
    try:
    #   Check the existence of the table
        check = log_db_table_check(mpy_trace, prj_dict, db_path, table_name)

        if check == True:

        #   Connect the database
            conn = log_db_connect(mpy_trace, prj_dict, db_path)

        #   Activate WAL mode to acces the database
            conn.execute('pragma journal_mode=wal;')

            i = 0

            for col in columns:
            #   Define the execution statement
                exec_statement = \
                    'ALTER TABLE {} ADD COLUMN {} {}'. \
                    format(table_name,columns[i],col_types[i])

            #   Execution
                try:
                #   Insert a new row and write to cell(s)
                    conn.execute(exec_statement)

                #   Commit changes to the database and close the cursor
                    conn.commit()

            #   Error detection
                except Exception as e:
                #   The log table could not be edited.
                    log_message = prj_dict['log_db_table_add_column_excpt'] + '\n' \
                                  + prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                                  + prj_dict['err_excp'] + ': {}'. format(e) \
                                  + prj_dict['log_db_table_add_column_stmt'] + ': {}'. format(exec_statement)
                    log(mpy_trace, prj_dict, log_message, 'critical')

                i = i + 1

        #   Disconnect from the database
            log_db_disconnect(mpy_trace, prj_dict, db_path)

        else:
        #   The log table could not be found. Logging not possible.
            log_message = prj_dict['log_db_table_add_column_failed']
            log(mpy_trace, prj_dict, log_message, 'critical')

        return check

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n'  \
                      + prj_dict['log_db_table_create_stmt'] + ': {}'. format(exec_statement)
        log(mpy_trace, prj_dict, log_message, 'critical')

def log_db_row_insert(mpy_trace, prj_dict, db_path, table_name, columns, log_dict):

    """ This function inserts a row into a table inside a given SQLite
        database.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        db_path - Path to the db to be adressed or altered
        table_name - Name of the database table to be created
        columns - List with the names of the columns to be written into. You
                  may reference a number of columns within that list. Number
                  of columns has to match number of data written to cells.
        log_dict - Passthrough dictionary for logging operations
    :return (dictionary)
        check - If TRUE, the function was successful
        row_id - ID of the row inserted
    """

    import mpy_fct
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_msg'
    operation = 'log_db_row_insert(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)
    mpy_trace['log_enable'] = False

#   Preparation
    table_name = str(table_name)
    row_id = 0

#   Execution
    try:

    #   Define the execution statement
        exec_statement = \
            '''INSERT INTO {} ('level','process_id','thread_id','task_id','datetimestamp','module','operation','tracing','message') VALUES (?,?,?,?,?,?,?,?,?)'''. \
            format(table_name)

    #   Check the existence of the table
        check = log_db_table_check(mpy_trace, prj_dict, db_path, table_name)

        if check == True:

        #   Connect the database
            conn = log_db_connect(mpy_trace, prj_dict, db_path)

        #   Activate WAL mode to acces the database
            conn.execute('pragma journal_mode=wal;')

        #   Execution
            try:
                c = conn.cursor()

            #   Insert a new row and write to cell(s)
                c.execute(exec_statement, (\
                          log_dict['level'], \
                          log_dict['process_id'], \
                          log_dict['thread_id'], \
                          log_dict['task_id'], \
                          log_dict['datetime_value'], \
                          log_dict['module'], \
                          log_dict['operation'], \
                          log_dict['tracing'], \
                          log_dict['log_message']) \
                          )

            #   Check for the last ID
                row_id = int(c.lastrowid)

            #   Commit changes to the database and close the cursor
                conn.commit()
                c.close()

        #   Error detection
            except Exception as e:
            #   The log entry could not be created.
                log_message = prj_dict['log_db_row_insert_excpt'] + '\n' \
                              + prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                              + prj_dict['err_excp'] + ': {}'. format(e) + '\n'  \
                              + prj_dict['log_db_row_insert_stmt'] + ': {}'. format(exec_statement)
                log(mpy_trace, prj_dict, log_message, 'critical')

        #   Disconnect from the database
            log_db_disconnect(mpy_trace, prj_dict, db_path)

        else:
        #   The log table could not be found. Logging not possible.
            log_message = prj_dict['log_db_row_insert_failed']
            log(mpy_trace, prj_dict, log_message, 'critical')

        return{
            'check' : check , \
            'row_id' : row_id
            }

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n'  \
                      + prj_dict['log_db_table_create_stmt'] + ': {}'. format(exec_statement)
        log(mpy_trace, prj_dict, log_message, 'critical')

def log_regex_replace(mpy_trace, prj_dict, search_obj, search_for, replace_by):

    """ This function substitutes characters or strings in an input object.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        search_for - The character or string to be replaced
        replace_by - The character or string to substitute

    :return
        result - The substituted chracter or string
    """

    import mpy_fct
    import sys, re

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_msg'
    operation = 'log_regex_replace(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    search_obj = str(search_obj)
    search_for = str(search_for)
    replace_by = str(replace_by)

    try:
        result = re.sub(search_for, replace_by, search_obj)

        return result

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'critical')

def log_wait_for_input(mpy_trace, prj_dict, msg_text):

    """ This function makes the program wait until a user input was made.
        The user input can be returned to the calling module.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        msg_text - The text to be displayed before user input
    :return
        usr_input - Returns the input of the user
    """

    import mpy_fct
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_msg'
    operation = 'log_wait_for_input(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    try:

        usr_input = input(str(msg_text) + '\n')

        return usr_input

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'critical')