"""
Author:     Bastian Neuwirth
Date:       28.06.2021
Version:    0.1
Descr.:     This module delivers functions to work with a SQLite database. The
            main database as defined in prj_dict will be referenced.

ToDo
-----------------
SQLite Tutorial

    SQLite Select
    SQLite Order By
    SQLite Select Distinct
    SQLite Where
    SQLite Limit
    SQLite BETWEEN
    SQLite IN
    SQLite Like
    SQLite IS NULL
    SQLite GLOB
    SQLite Join
    SQLite Inner Join
    SQLite Left Join
    SQLite Cross Join
    SQLite Self-Join
    SQLite Full Outer Join
    SQLite Group By
    SQLite Having
    SQLite Union
    SQLite Except
    SQLite Intersect
    SQLite Subquery
    SQLite EXISTS
    SQLite Case
    SQLite Insert
    SQLite Update
    SQLite Delete
    SQLite Replace
    SQLite Transaction

SQLite Data Definition

    SQLite Data Types
    SQLite Date & Time
ok  SQLite Create Table
    SQLite Primary Key
    SQLite Foreign Key
    SQLite NOT NULL Constraint
    SQLite UNIQUE Constraint
    SQLite CHECK constraints
    SQLite AUTOINCREMENT
    SQLite Alter Table
    SQLite Rename Column
    SQLite Drop Table
    SQLite Create View
    SQLite Drop View
    SQLite Index
    SQLite Expression-based Index
    SQLite Trigger
    SQLite VACUUM
    SQLite Transaction
    SQLite Full-text Search

SQLite Tools

    SQLite Commands
    SQLite Show Tables
    SQLite Describe Table
    SQLite Dump
    SQLite Import CSV
    SQLite Export CSV

SQLite Functions

    SQLite AVG
    SQLite COUNT
    SQLite MAX
    SQLite MIN
    SQLite SUM
"""

def sqlite3_db_connect(mpy_trace, prj_dict, db_path):

    """ This function connects to a SQLite database. The database will be
        created if it does not exist already.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
        db_path - Path to the db to be adressed or altered
    :return
        conn - Connection object or None
    """

    import mpy_fct, mpy_msg
    import sys, sqlite3

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_sqlite3'
    operation = 'sqlite3_db_connect(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Create a log
#   Connecting to SQLite database.
    log_message = prj_dict['sqlite3_db_connect_conn'] + '\n' \
                  + prj_dict['sqlite3_db_connect_Path'] + ': ' + str(db_path)
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    conn = None
    try:
        conn = sqlite3.connect(db_path)

    #   Create a log
    #   SQLite database connected.
        log_message = prj_dict['sqlite3_db_connect_ready'] + '\n' \
                      + 'conn: ' + str(conn)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        return conn

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

def sqlite3_db_disconnect(mpy_trace, prj_dict, db_path):

    """ This function disconnects a SQLite database.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
        db_path - Path to the db to be adressed or altered
    :return
        -
    """

    import mpy_fct, mpy_msg
    import sys, sqlite3

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_sqlite3'
    operation = 'sqlite3_db_disconnect(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    try:

    #   Create a log
    #   Disconnecting from SQLite database.
        log_message = prj_dict['sqlite3_db_disconnect_discon'] + '\n' \
                      + prj_dict['sqlite3_db_disconnect_path'] + ': ' + str(db_path)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        conn = sqlite3.connect(db_path)

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:
        try:
            if conn:
                conn.close()

            #   Create a log
            #   SQLite database disconnected.
                log_message = prj_dict['sqlite3_db_disconnect_ready'] + '\n' \
                              + 'conn: ' + str(conn)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Error detection
        except Exception as e:
            log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                          + prj_dict['err_excp'] + ': {}'. format(e)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

def sqlite3_db_statement(mpy_trace, prj_dict, db_path, db_smnt):

    """ This function handles any sqlite3 statement as given to it.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
        db_path - Path to the db to be adressed or altered
        db_smnt - The statement to be executed
    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_fct, mpy_msg
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_sqlite3'
    operation = 'sqlite3_db_statement(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing Parameters
    db_smnt = str(db_smnt)
    check = False

#   Create a log
#   Executing a SQLite3 statement.
    log_message = prj_dict['sqlite3_db_statement_exec'] + '\n' \
                  + prj_dict['sqlite3_db_statement_db'] + ': ' + str(db_path) + '\n' \
                  + prj_dict['sqlite3_db_statement_smnt'] + ': ' + db_smnt
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Execution
    try:

    #   Connect the database
        conn = sqlite3_db_connect(mpy_trace, prj_dict, db_path)

    #   Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

        c = conn.cursor()

    #   Insert a new row and write to cell(s)
        c.execute(db_smnt)

    #   Commit changes to the database and close the cursor
        conn.commit()
        c.close()

    #   Disconnect from the database
        sqlite3_db_disconnect(mpy_trace, prj_dict, db_path)

    #   Create a log
    #   Statement executed.
        log_message = prj_dict['sqlite3_db_statement_ready'] + '\n' \
                      + prj_dict['sqlite3_db_statement_db'] + ': ' + str(db_path)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                      + prj_dict['sqlite3_db_statement_smnt'] + ': {}'. format(db_smnt)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

#   Return a dictionary
    return{
        'check' : check
        }

def sqlite3_tbl_check(mpy_trace, prj_dict, db_path, table_name):

    """ This function checks on the existence of a table inside a given SQLite
        database.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
        db_path - Path to the db to be adressed or altered
        table_name - Name of the database table to be checked on
    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_fct, mpy_msg
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_sqlite3'
    operation = 'sqlite3_tbl_check(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    table_name = str(table_name)
    check = False

#   Create a log
#   Checking the existence of a SQLite database table.
    log_message = prj_dict['sqlite3_tbl_check_start'] + '\n' \
                  + prj_dict['sqlite3_tbl_check_db'] + ': ' + str(db_path) + '\n' \
                  + prj_dict['sqlite3_tbl_check_tbl'] + ': ' + table_name
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Define the execution statement
    exec_statement = \
        'SELECT count(name) FROM sqlite_master WHERE ' \
         + 'type=\"table\" AND name=\"{}\"'. \
         format(table_name)

#   Execution
    try:
    #   Connect the database
        conn = sqlite3_db_connect(mpy_trace, prj_dict, db_path)

    #   Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

        c = conn.cursor()

    #   Check for the existence of a table
        c.execute(exec_statement)

    #   Check the count of found tables
        if c.fetchone()[0] == 1:
            check = True
        #   Table exists.
            msg = prj_dict['sqlite3_tbl_check_tbl_ex']

        else:
        #   Table does not exist.
            msg = prj_dict['sqlite3_tbl_check_tbl_nex']

    #   Create a log
        log_message = msg + '\n' \
                      + prj_dict['sqlite3_tbl_check_db'] + ': ' + str(db_path) + '\n' \
                      + prj_dict['sqlite3_tbl_check_tbl'] + ': ' + table_name + '\n' \
                      + 'check: ' + str(check)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Close the cursor
        c.close()

    #   Disconnect from the database
        sqlite3_db_disconnect(mpy_trace, prj_dict, db_path)

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                      + prj_dict['sqlite3_tbl_check_smnt'] + ': {}'. format(exec_statement)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

#   Return a dictionary
    return{
        'check' : check
        }

def sqlite3_tbl_create(mpy_trace, prj_dict, db_path, table_name):

    """ This function creates a table inside a SQLite database.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
        db_path - Path to the db to be adressed or altered
        table_name - Name of the database table to be created
    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_fct, mpy_msg
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_sqlite3'
    operation = 'sqlite3_tbl_create(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    table_name = str(table_name)
    check = False

#   Create a log
#   Creating a SQLite database table.
    log_message = prj_dict['sqlite3_tbl_create_start'] + '\n' \
                  + prj_dict['sqlite3_tbl_create_db'] + ': ' + str(db_path) + '\n' \
                  + prj_dict['sqlite3_tbl_create_tbl'] + ': ' + table_name
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Define the execution statement
    exec_statement = \
        'CREATE TABLE IF NOT EXISTS {} '. \
        format(table_name) \
        + '(ID INTEGER PRIMARY KEY)'

#   Execution
    try:
    #   Connect the database
        conn = sqlite3_db_connect(mpy_trace, prj_dict, db_path)

    #   Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

    #   Create the actual table
        conn.execute(exec_statement)

    #   Commit changes to the database
        conn.commit()

    #   Create a log
    #   SQLite table created.
        log_message = prj_dict['sqlite3_tbl_create_ready'] + '\n' \
                      + prj_dict['sqlite3_tbl_create_db'] + ': ' + str(db_path) + '\n' \
                      + prj_dict['sqlite3_tbl_create_tbl'] + ': ' + table_name
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

    #   Disconnect from the database
        sqlite3_db_disconnect(mpy_trace, prj_dict, db_path)

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                      + prj_dict['sqlite3_tbl_create_smnt'] + ': {}'. format(exec_statement)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

#   Return a dictionary
    return{
        'check' : check
        }

def sqlite3_tbl_column_add(mpy_trace, prj_dict, db_path, table_name, columns, col_types):

    """ This function inserts a column into a table inside a given SQLite
        database.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
        db_path - Path to the db to be adressed or altered
        table_name - Name of the database table to be created
        columns - List of the columns to be added
        col_types - List of datatypes for the columns as specified for SQLite
    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_fct, mpy_msg
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_sqlite3'
    operation = 'sqlite3_tbl_column_add(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    table_name = str(table_name)
    columns_str = str(columns)
    col_types_str = str(col_types).upper()
    check = False
    plausible = False

    try:

    #   Create a log
        log_message = prj_dict['sqlite3_tbl_column_add_start'] + '\n' \
                      + prj_dict['sqlite3_tbl_column_add_db'] + ': ' + str(db_path) + '\n' \
                      + prj_dict['sqlite3_tbl_column_add_tbl'] + ': ' + table_name
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Compare items in columns and col_types
        i = 0
        for col in columns:
            i = i + 1

    #   List data types as a string
        j = 0
        for clt in col_types:
            j = j + 1

    #   Check input plausibility
        if i == j:
            plausible = True

        #   Check the existence of the table
            check = sqlite3_tbl_check(mpy_trace, prj_dict, db_path, table_name)

        if check == True and plausible == True:

        #   Connect the database
            conn = sqlite3_db_connect(mpy_trace, prj_dict, db_path)

        #   Activate WAL mode to acces the database
            conn.execute('pragma journal_mode=wal;')

            k = 0

            try:

                for col in columns:

                #   Define the execution statement
                    exec_statement = \
                        'ALTER TABLE {} ADD COLUMN {} {}'. \
                        format(table_name,columns[k],col_types[k])

                #   Insert a new row and write to cell(s)
                    conn.execute(exec_statement)

                #   Commit changes to the database and close the cursor
                    conn.commit()

                #   Iterate
                    k = k + 1

            #   Create a log
            #   Columns added to SQLite table.
                log_message = prj_dict['sqlite3_tbl_column_add_start'] + '\n' \
                              + prj_dict['sqlite3_tbl_column_add_db'] + ': ' + str(db_path) + '\n' \
                              + prj_dict['sqlite3_tbl_column_add_tbl'] + ': ' + table_name + '\n' \
                              + prj_dict['sqlite3_tbl_column_add_col'] + ': ' + columns_str + '\n' \
                              + prj_dict['sqlite3_tbl_column_add_datatype'] + ': ' + col_types_str
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

            #   Disconnect from the database
                sqlite3_db_disconnect(mpy_trace, prj_dict, db_path)

            #   Return a dictionary
                return{
                    'check' : check
                    }

        #   Error detection
            except Exception as e:
                log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                              + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                              + prj_dict['sqlite3_tbl_column_add_smnt'] + ': {}'. format(exec_statement)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    #   Log and print a denial
        if check == False:
        #   Create a log
        #   The table does not exist. Columns could not be inserted.
            log_message = prj_dict['sqlite3_tbl_column_add_tbl_nex'] + '\n' \
                          + prj_dict['sqlite3_tbl_column_add_db'] + ': ' + str(db_path) + '\n' \
                          + prj_dict['sqlite3_tbl_column_add_tbl'] + ': ' + table_name + '\n' \
                          + 'check: ' + str(check)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

    #   Log and print a denial
        if plausible == False:
        #   Create a log
        #   The number of columns does not match the number of datatypes handed over to the function.
            log_message = prj_dict['sqlite3_tbl_column_add_mismatch'] + '\n' \
                          + prj_dict['sqlite3_tbl_column_add_col'] + ': ' + columns_str + '\n' \
                          + prj_dict['sqlite3_tbl_column_add_numcol'] + ': ' + str(i) + '\n' \
                          + prj_dict['sqlite3_tbl_column_add_datatype'] + ': ' + col_types_str + '\n' \
                          + prj_dict['sqlite3_tbl_column_add_numdatatype'] + ': ' + str(j)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

#   Return a dictionary
    return{
        'check' : check
        }

def sqlite3_row_insert(mpy_trace, prj_dict, db_path, table_name, columns, cell_data):

    """ This function inserts a row into a table inside a given SQLite
        database.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
        db_path - Path to the db to be adressed or altered
        table_name - Name of the database table to be created
        columns - List with the names of the columns to be written into. You
                  may reference a number of columns within that list. Number
                  of columns has to match number of data written to cells.
        cell_data - Yields the data to be written into the cells. You may
                    reference a number of cells within that list. Number
                    of values has to match number of columns adressed.
    :return - dictionary
        check - The function ended with no errors
        row_id - ID of the row inserted
    """

    import mpy_fct, mpy_msg
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_sqlite3'
    operation = 'sqlite3_row_insert(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    table_name = str(table_name)
    check = False
    plausible = False

    try:

    #   Build strings from columns and data for SQLite
        col_formatted = ''
        i = 0
        dat_formatted = ''
        j = 0

        for col in columns:
            if i == 0:
                col_formatted = '\"' + str(col) + '\"'
            else:
                col_formatted = col_formatted + ',\"' + str(col) + '\"'
            i = i + 1

        for cld in cell_data:
            if j == 0:
                dat_formatted = '\"' + str(cld) + '\"'
            else:
                dat_formatted = dat_formatted + ',\"' + str(cld) + '\"'
            j = j + 1

    #   Define the execution statement
        exec_statement = \
            'INSERT INTO {} ({}) VALUES ({})'. \
            format(table_name,col_formatted,dat_formatted)

    #   Create a log
    #   Inserting a row into a SQLite database table.
        log_message = prj_dict['sqlite3_row_insert_start'] + '\n' \
                      + prj_dict['sqlite3_row_insert_db'] + ': ' + str(db_path) + '\n' \
                      + prj_dict['sqlite3_row_insert_tbl'] + ': ' + table_name
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Plausibility check for columns and according data
        if i == j:
            plausible = True

        #   Create a log
            log_message = prj_dict['sqlite3_row_insert_match'] + '\n' \
                          + 'plausible: ' + str(plausible)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Check the existence of the table
            check = sqlite3_tbl_check(mpy_trace, prj_dict, db_path, table_name)

        if check == True and plausible == True:

        #   Execution
            try:
            #   Connect the database
                conn = sqlite3_db_connect(mpy_trace, prj_dict, db_path)

            #   Activate WAL mode to acces the database
                conn.execute('pragma journal_mode=wal;')

                c = conn.cursor()

            #   Insert a new row and write to cell(s)
                c.execute(exec_statement)

            #   Check for the last ID
                row_id = int(c.lastrowid)

            #   Commit changes to the database and close the cursor
                conn.commit()
                c.close()

            #   Disconnect from the database
                sqlite3_db_disconnect(mpy_trace, prj_dict, db_path)

            #   Create a log
            #   Row inserted into SQLite table.
                log_message = prj_dict['sqlite3_row_insert_ready'] + '\n' \
                              + prj_dict['sqlite3_row_insert_db'] + ': ' + str(db_path) + '\n' \
                              + prj_dict['sqlite3_row_insert_tbl'] + ': ' + table_name + '\n' \
                              + prj_dict['sqlite3_row_insert_col'] + ': ' + col_formatted + '\n' \
                              + prj_dict['sqlite3_row_insert_data'] + ': ' + dat_formatted
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

                return{
                    'check' : check , \
                    'row_id' : row_id
                    }

        #   Error detection
            except Exception as e:
                log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                              + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                              + prj_dict['sqlite3_row_insert_smnt'] + ': {}'. format(exec_statement)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    #   Log and print a denial
        if check == False:
        #   Create a log
        #   The table does not exist.
            log_message = prj_dict['sqlite3_row_insert_tblnex'] + '\n' \
                          + prj_dict['sqlite3_row_insert_db'] + ': ' + str(db_path) + '\n' \
                          + prj_dict['sqlite3_row_insert_tbl'] + ': ' + table_name + '\n' \
                          + 'check: ' + str(check)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

    #   Log and print a denial
        if plausible == False:
        #   Create a log
        #   The number of columns does not match the number of values handed to the function.
            log_message = prj_dict['sqlite3_row_insert_mismatch'] + '\n' \
                          + prj_dict['sqlite3_row_insert_col'] + ': ' + col_formatted + '\n' \
                          + prj_dict['sqlite3_row_insert_numcol'] + ': ' + str(i) + '\n' \
                          + prj_dict['sqlite3_row_insert_val'] + ': ' + dat_formatted + '\n' \
                          + prj_dict['sqlite3_row_insert_numval'] + ': ' + str(j)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'check' : check
        }

def sqlite3_row_update(mpy_trace, prj_dict, db_path, table_name, columns, cell_data, row_id):

    """ This function updates a row of a table inside a given SQLite
        database. Only addressed columns will be updated.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
        db_path - Path to the db to be adressed or altered
        table_name - Name of the database table to be created
        columns - List of the columns to be added
        cell_data - Yields the data to be written into the cells. You may
                    reference a number of cells within that list. Number
                    of values has to match number of columns adressed.
        row_id - Addresses the ID (first column) of a row
    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_fct, mpy_msg
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_sqlite3'
    operation = 'sqlite3_row_update(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    table_name = str(table_name)
    check = False
    plausible = False

    try:

    #   Compare the amount of Columns and Cells
        col_formatted = ''
        i = 0
        dat_formatted = ''
        j = 0

        for col in columns:
            if i == 0:
                col_formatted = '\"' + str(col) + '\"'
            else:
                col_formatted = col_formatted + ',\"' + str(col) + '\"'
            i = i + 1

        for cld in cell_data:
            if j == 0:
                dat_formatted = '\"' + str(cld) + '\"'
            else:
                dat_formatted = dat_formatted + ',\"' + str(cld) + '\"'
            j = j + 1

    #   Plausibility check for columns and according data
        if i == j:
            plausible = True

        #   Create a log
        #   Updating a row of a SQLite database table.
            log_message = prj_dict['sqlite3_row_update_start'] + '\n' \
                          + prj_dict['sqlite3_row_update_db'] + ': ' + str(db_path) + '\n' \
                          + prj_dict['sqlite3_row_update_tbl'] + ': ' + str(table_name) + '\n' \
                          + prj_dict['sqlite3_row_update_col'] + ': ' + col_formatted + '\n' \
                          + prj_dict['sqlite3_row_update_data'] + ': ' + dat_formatted + '\n' \
                          + prj_dict['sqlite3_row_update_id'] + ': ' + str(row_id)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Check the existence of the table
            check = sqlite3_tbl_check(mpy_trace, prj_dict, db_path, table_name)

        if check == True and plausible == True:

        #   Execution
            try:
            #   Build the datasets fo be updated
                k = 0

                for dat in columns:
                    if k == 0:
                        dat_sets = '\"' + str(columns[k]) \
                            + '\" = \"' + str(cell_data[k]) + '\"'
                    else:
                        dat_sets = dat_sets + ', ' + '\"' + str(columns[k]) \
                            + '\" = \"' + str(cell_data[k]) + '\"'
                    k = k + 1

            #   Define the execution statement
                exec_statement = \
                    'UPDATE {} SET {} WHERE ID = {}'. \
                    format(table_name,dat_sets,row_id)

            #   Connect the database
                conn = sqlite3_db_connect(mpy_trace, prj_dict, db_path)

            #   Activate WAL mode to acces the database
                conn.execute('pragma journal_mode=wal;')

                c = conn.cursor()

            #   Insert a new row and write to cell(s)
                c.execute(exec_statement)

            #   Commit changes to the database and close the cursor
                conn.commit()
                c.close()

            #   Disconnect from the database
                sqlite3_db_disconnect(mpy_trace, prj_dict, db_path)

            #   Create a log
            #   Updated a row of a SQLite table.
                log_message = prj_dict['sqlite3_row_update_ready'] + '\n' \
                              + prj_dict['sqlite3_row_update_db'] + ': ' + str(db_path) + '\n' \
                              + prj_dict['sqlite3_row_update_tbl'] + ': ' + str(table_name) + '\n' \
                              + prj_dict['sqlite3_row_update_col'] + ': ' + col_formatted + '\n' \
                              + prj_dict['sqlite3_row_update_data'] + ': ' + dat_formatted + '\n' \
                              + prj_dict['sqlite3_row_update_id'] + ': ' + str(row_id)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

                return{
                    'check' : check , \
                    'row_id' : row_id
                    }

        #   Error detection
            except Exception as e:
                log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                              + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                              + prj_dict['sqlite3_row_update_smnt'] + ': {}'. format(exec_statement)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    #   Log and print a denial
        if check == False:
        #   Create a log
        #   The table does not exist.
            log_message = prj_dict['sqlite3_row_update_tbl_nex'] + '\n' \
                          + prj_dict['sqlite3_row_update_db'] + ': ' + str(db_path) + '\n' \
                          + prj_dict['sqlite3_row_update_tbl'] + ': ' + str(table_name) + '\n' \
                          + 'check: ' + str(check)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

    #   Log and print a denial
        if plausible == False:
        #   Create a log
        #   The number of columns does not match the number of values handed to the function.
            log_message = prj_dict['sqlite3_row_update_mismatch'] + '\n' \
                          + prj_dict['sqlite3_row_update_col'] + ': ' + col_formatted + '\n' \
                          + prj_dict['sqlite3_row_update_numcol'] + ': ' + str(i) + '\n' \
                          + prj_dict['sqlite3_row_update_val'] + ': ' + dat_formatted + '\n' \
                          + prj_dict['sqlite3_row_update_numval'] + ': ' + str(j)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'check' : check
        }

def sqlite3_row_update_where(mpy_trace, prj_dict, db_path, table_name, columns, cell_data, where):

    """ This function updates a row of a table inside a given SQLite
        database. Only addressed columns will be updated.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
        db_path - Path to the db to be adressed or altered
        table_name - Name of the database table to be created
        columns - List of the columns to be added
        cell_data - Yields the data to be written into the cells. You may
                    reference a number of cells within that list. Number
                    of values has to match number of columns adressed.
        where - SQL-Statement to specify the update of the table
    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_fct, mpy_msg
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_sqlite3'
    operation = 'sqlite3_row_update_where(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    table_name = str(table_name)
    where = str(where)
    check = False
    plausible = False

    try:

    #   Compare the amount of Columns and Cells
        col_formatted = ''
        i = 0
        dat_formatted = ''
        j = 0

        for col in columns:
            if i == 0:
                col_formatted = '\"' + str(col) + '\"'
            else:
                col_formatted = col_formatted + ',\"' + str(col) + '\"'
            i = i + 1

        for cld in cell_data:
            if j == 0:
                dat_formatted = '\"' + str(cld) + '\"'
            else:
                dat_formatted = dat_formatted + ',\"' + str(cld) + '\"'
            j = j + 1

    #   Plausibility check for columns and according data
        if i == j:
            plausible = True

        #   Create a log
        #   Updating a row of a SQLite database table.
            log_message = prj_dict['sqlite3_row_update_where_start'] + '\n' \
                          + prj_dict['sqlite3_row_update_where_db'] + ': ' + str(db_path) + '\n' \
                          + prj_dict['sqlite3_row_update_where_tbl'] + ': ' + str(table_name) + '\n' \
                          + prj_dict['sqlite3_row_update_where_col'] + ': ' + col_formatted + '\n' \
                          + prj_dict['sqlite3_row_update_where_data'] + ': ' + dat_formatted + '\n' \
                          + 'where: ' + str(where)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Check the existence of the table
            check = sqlite3_tbl_check(mpy_trace, prj_dict, db_path, table_name)

        if check == True and plausible == True:

        #   Execution
            try:
            #   Build the datasets fo be updated
                k = 0

                for dat in columns:
                    if k == 0:
                        dat_sets = '\"' + str(columns[k]) \
                            + '\" = \"' + str(cell_data[k]) + '\"'
                    else:
                        dat_sets = dat_sets + ', ' + '\"' + str(columns[k]) \
                            + '\" = \"' + str(cell_data[k]) + '\"'
                    k = k + 1

            #   Define the execution statement
                exec_statement = \
                    'UPDATE {} SET {} WHERE {}'. \
                    format(table_name,dat_sets,where)

            #   Connect the database
                conn = sqlite3_db_connect(mpy_trace, prj_dict, db_path)

            #   Activate WAL mode to acces the database
                conn.execute('pragma journal_mode=wal;')

                c = conn.cursor()

            #   Insert a new row and write to cell(s)
                c.execute(exec_statement)

            #   Commit changes to the database and close the cursor
                conn.commit()
                c.close()

            #   Disconnect from the database
                sqlite3_db_disconnect(mpy_trace, prj_dict, db_path)

            #   Create a log
            #   Updated a row of a SQLite table.
                log_message = prj_dict['sqlite3_row_update_where_ready'] + '\n' \
                              + prj_dict['sqlite3_row_update_where_db'] + ': ' + str(db_path) + '\n' \
                              + prj_dict['sqlite3_row_update_where_tbl'] + ': ' + str(table_name) + '\n' \
                              + prj_dict['sqlite3_row_update_where_col'] + ': ' + col_formatted + '\n' \
                              + prj_dict['sqlite3_row_update_where_data'] + ': ' + dat_formatted + '\n' \
                              + 'where: ' + str(where)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

                return{
                    'check' : check , \
                    'where' : where
                    }

        #   Error detection
            except Exception as e:
                log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                              + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                              + prj_dict['sqlite3_row_update_where_smnt'] + ': {}'. format(exec_statement)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    #   Log and print a denial
        if check == False:
        #   Create a log
        #   The table does not exist.
            log_message = prj_dict['sqlite3_row_update_where_tbl_nex'] + '\n' \
                          + prj_dict['sqlite3_row_update_where_db'] + ': ' + str(db_path) + '\n' \
                          + prj_dict['sqlite3_row_update_where_tbl'] + ': ' + str(table_name) + '\n' \
                          + 'check: ' + str(check)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

    #   Log and print a denial
        if plausible == False:
        #   Create a log
        #   The number of columns does not match the number of values handed to the function.
            log_message = prj_dict['sqlite3_row_update_where_mismatch'] + '\n' \
                          + prj_dict['sqlite3_row_update_where_col'] + ': ' + col_formatted + '\n' \
                          + prj_dict['sqlite3_row_update_where_numcol'] + ': ' + str(i) + '\n' \
                          + prj_dict['sqlite3_row_update_where_val'] + ': ' + dat_formatted + '\n' \
                          + prj_dict['sqlite3_row_update_where_numval'] + ': ' + str(j)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'check' : check , \
        'where' : where
        }