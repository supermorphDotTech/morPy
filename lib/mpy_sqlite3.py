"""
Author:     Bastian Neuwirth
Date:       28.06.2021
Version:    0.1
Descr.:     This module delivers functions to work with a SQLite database. The
            main database as defined in prj_dict will be referenced.

#TODO
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
    log_message = (f'{prj_dict["sqlite3_db_connect_conn"]}\n'
                  f'{prj_dict["sqlite3_db_connect_Path"]}: {db_path}')
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    conn = None
    try:
        conn = sqlite3.connect(db_path)

    #   Create a log
    #   SQLite database connected.
        log_message = (f'{prj_dict["sqlite3_db_connect_ready"]}\n'
                      f'conn: {conn}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        return conn

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}')
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
        log_message = (f'{prj_dict["sqlite3_db_disconnect_discon"]}\n'
                      f'{prj_dict["sqlite3_db_disconnect_path"]}: {db_path}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        conn = sqlite3.connect(db_path)

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:
        try:
            if conn:
                conn.close()

            #   Create a log
            #   SQLite database disconnected.
                log_message = (f'{prj_dict["sqlite3_db_disconnect_ready"]}\n'
                              f'conn: {conn}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Error detection
        except Exception as e:
            log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                          f'{prj_dict["err_excp"]}: {e}')
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
    db_smnt = f'{db_smnt}'
    check = False

#   Create a log
#   Executing a SQLite3 statement.
    log_message = (f'{prj_dict["sqlite3_db_statement_exec"]}\n'
                  f'{prj_dict["sqlite3_db_statement_db"]}: {db_path}\n'
                  f'{prj_dict["sqlite3_db_statement_smnt"]}: {db_smnt}')
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
        log_message = (f'{prj_dict["sqlite3_db_statement_ready"]}\n'
                      f'{prj_dict["sqlite3_db_statement_db"]}: {db_path}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

        check = True

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}\n'
                      f'{prj_dict["sqlite3_db_statement_smnt"]}: {db_smnt}')
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
    table_name = f'{table_name}'
    check = False

#   Create a log
#   Checking the existence of a SQLite database table.
    log_message = (f'{prj_dict["sqlite3_tbl_check_start"]}\n'
                  f'{prj_dict["sqlite3_tbl_check_db"]}: {db_path}\n'
                  f'{prj_dict["sqlite3_tbl_check_tbl"]}: {table_name}')
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Define the execution statement
    exec_statement = f'SELECT count(name) FROM sqlite_master WHERE type=\"table\" AND name=\"{table_name}\"'

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
            msg = prj_dict["sqlite3_tbl_check_tbl_ex"]

        else:
        #   Table does not exist.
            msg = prj_dict["sqlite3_tbl_check_tbl_nex"]

    #   Create a log
        log_message = (f'{msg}\n'
                      f'{prj_dict["sqlite3_tbl_check_db"]}: {db_path}\n'
                      f'{prj_dict["sqlite3_tbl_check_tbl"]}: {table_name}\n'
                      f'check: {check}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Close the cursor
        c.close()

    #   Disconnect from the database
        sqlite3_db_disconnect(mpy_trace, prj_dict, db_path)

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}\n'
                      f'{prj_dict["sqlite3_tbl_check_smnt"]}: {exec_statement}')
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
    table_name = f'{table_name}'
    check = False

#   Create a log
#   Creating a SQLite database table.
    log_message = (f'{prj_dict["sqlite3_tbl_create_start"]}\n'
                  f'{prj_dict["sqlite3_tbl_create_db"]}: {db_path}\n'
                  f'{prj_dict["sqlite3_tbl_create_tbl"]}: {table_name}')
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Define the execution statement
    exec_statement = f'CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY)'

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
        log_message = (f'{prj_dict["sqlite3_tbl_create_ready"]}\n'
                      f'{prj_dict["sqlite3_tbl_create_db"]}: {db_path}\n'
                      f'{prj_dict["sqlite3_tbl_create_tbl"]}: {table_name}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

    #   Disconnect from the database
        sqlite3_db_disconnect(mpy_trace, prj_dict, db_path)

        check = True

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}\n'
                      f'{prj_dict["sqlite3_tbl_create_smnt"]}: {exec_statement}')
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
    table_name = f'{table_name}'
    columns_str = f'{columns}'
    col_types_str = f'{col_types}'.upper()
    check = False
    plausible = False

    try:

    #   Create a log
        log_message = (f'{prj_dict["sqlite3_tbl_column_add_start"]}\n'
                      f'{prj_dict["sqlite3_tbl_column_add_db"]}: {db_path}\n'
                      f'{prj_dict["sqlite3_tbl_column_add_tbl"]}: {table_name}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Compare items in columns and col_types
        i = 0
        for col in columns:
            i += 1

    #   List data types as a string
        j = 0
        for clt in col_types:
            j += 1

    #   Check input plausibility
        if i == j:
            plausible = True

        #   Check the existence of the table
            check = sqlite3_tbl_check(mpy_trace, prj_dict, db_path, table_name)

    #   Proceed only if table exists and column count is plausible.
        if check:

        #   Connect the database
            conn = sqlite3_db_connect(mpy_trace, prj_dict, db_path)

        #   Activate WAL mode to acces the database
            conn.execute('pragma journal_mode=wal;')

            k = 0
            try:

                for col in columns:

                #   Define the execution statement
                    exec_statement = f'ALTER TABLE {table_name} ADD COLUMN {columns[k]} {col_types[k]}'

                #   Insert a new row and write to cell(s)
                    conn.execute(exec_statement)

                #   Commit changes to the database and close the cursor
                    conn.commit()

                #   Iterate
                    k += 1

            #   Create a log
            #   Columns added to SQLite table.
                log_message = (f'{prj_dict["sqlite3_tbl_column_add_start"]}\n'
                              f'{prj_dict["sqlite3_tbl_column_add_db"]}: {db_path}\n'
                              f'{prj_dict["sqlite3_tbl_column_add_tbl"]}: {table_name}\n'
                              f'{prj_dict["sqlite3_tbl_column_add_col"]}: {columns_str}\n'
                              f'{prj_dict["sqlite3_tbl_column_add_datatype"]}: {col_types_str}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

            #   Disconnect from the database
                sqlite3_db_disconnect(mpy_trace, prj_dict, db_path)

            #   Return a dictionary
                return{
                    'check' : check
                    }

        #   Error detection
            except Exception as e:
                log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                              f'{prj_dict["err_excp"]}: {e}\n'
                              f'{prj_dict["sqlite3_tbl_column_add_smnt"]}: {exec_statement}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    #   Log and print a denial
        if not check:
        #   Create a log
        #   The table does not exist. Columns could not be inserted.
            log_message = (f'{prj_dict["sqlite3_tbl_column_add_tbl_nex"]}\n'
                          f'{prj_dict["sqlite3_tbl_column_add_db"]}: {db_path}\n'
                          f'{prj_dict["sqlite3_tbl_column_add_tbl"]}: {table_name}\n'
                          f'check: {check}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

    #   Log and print a denial
        if not plausible:
        #   Create a log
        #   The number of columns does not match the number of datatypes handed over to the function.
            log_message = (f'{prj_dict["sqlite3_tbl_column_add_mismatch"]}\n'
                          f'{prj_dict["sqlite3_tbl_column_add_col"]}: {columns_str}\n'
                          f'{prj_dict["sqlite3_tbl_column_add_numcol"]}: {i}\n'
                          f'{prj_dict["sqlite3_tbl_column_add_datatype"]}: {col_types_str}\n'
                          f'{prj_dict["sqlite3_tbl_column_add_numdatatype"]}: {j}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}')
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
    table_name = f'{table_name}'
    check = False
    plausible = False

    try:

    #   Build strings from columns and data for SQLite
        col_formatted = ''
        i = 0
        dat_formatted = ''
        j = 0

        for col in columns:
            if i:
                col_formatted = f'{col_formatted},\"{col}\"'
            else:
                col_formatted = f'\"{col}\"'
            i += 1

        for cld in cell_data:
            if j:
                dat_formatted = f'{dat_formatted},\"{cld}\"'
            else:
                dat_formatted = f'\"{cld}\"'
            j += 1

    #   Define the execution statement
        exec_statement = f'INSERT INTO {table_name} ({col_formatted}) VALUES ({dat_formatted})'

    #   Create a log
    #   Inserting a row into a SQLite database table.
        log_message = (f'{prj_dict["sqlite3_row_insert_start"]}\n'
                      f'{prj_dict["sqlite3_row_insert_db"]}: {db_path}\n'
                      f'{prj_dict["sqlite3_row_insert_tbl"]}: {table_name}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Plausibility check for columns and according data.
        if i == j:
            plausible = True

        #   Create a log
            log_message = (f'{prj_dict["sqlite3_row_insert_match"]}\n'
                          f'plausible: {plausible}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Check the existence of the table
            check = sqlite3_tbl_check(mpy_trace, prj_dict, db_path, table_name)

    #   Proceed only if table exists and column count is plausible.
        if check:

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
                log_message = (f'{prj_dict["sqlite3_row_insert_ready"]}\n'
                              f'{prj_dict["sqlite3_row_insert_db"]}: {db_path}\n'
                              f'{prj_dict["sqlite3_row_insert_tbl"]}: {table_name}\n'
                              f'{prj_dict["sqlite3_row_insert_col"]}: {col_formatted}\n'
                              f'{prj_dict["sqlite3_row_insert_data"]}: {dat_formatted}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

                return{
                    'check' : check , \
                    'row_id' : row_id
                    }

        #   Error detection
            except Exception as e:
                log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                              f'{prj_dict["err_excp"]}: {e}\n'
                              f'{prj_dict["sqlite3_row_insert_smnt"]}: {exec_statement}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    #   Log and print a denial
        if not check:
        #   Create a log
        #   The table does not exist.
            log_message = (f'{prj_dict["sqlite3_row_insert_tblnex"]}\n'
                          f'{prj_dict["sqlite3_row_insert_db"]}: {db_path}\n'
                          f'{prj_dict["sqlite3_row_insert_tbl"]}: {table_name}\n'
                          f'check: {check}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

    #   Log and print a denial
        if not plausible:
        #   Create a log
        #   The number of columns does not match the number of values handed to the function.
            log_message = (f'{prj_dict["sqlite3_row_insert_mismatch"]}\n'
                          f'{prj_dict["sqlite3_row_insert_col"]}: {col_formatted}\n'
                          f'{prj_dict["sqlite3_row_insert_numcol"]}: {i}\n'
                          f'{prj_dict["sqlite3_row_insert_val"]}: {dat_formatted}\n'
                          f'{prj_dict["sqlite3_row_insert_numval"]}: {j}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}')
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
    table_name = f'{table_name}'
    check = False
    plausible = False
    dat_sets = ''

    try:

    #   Compare the amount of Columns and Cells
        col_formatted = ''
        i = 0
        dat_formatted = ''
        j = 0

        for col in columns:
            if i:
                col_formatted = f'{col_formatted},\"{col}\"'
            else:
                col_formatted = f'\"{col}\"'
            i += 1

        for cld in cell_data:
            if j:
                dat_formatted = f'{dat_formatted},\"{cld}\"'
            else:
                dat_formatted = f'\"{cld}\"'
            j += 1

    #   Plausibility check for columns and according data
        if i == j:
            plausible = True

        #   Create a log
        #   Updating a row of a SQLite database table.
            log_message = (f'{prj_dict["sqlite3_row_update_start"]}\n'
                          f'{prj_dict["sqlite3_row_update_db"]}: {db_path}\n'
                          f'{prj_dict["sqlite3_row_update_tbl"]}: {table_name}\n'
                          f'{prj_dict["sqlite3_row_update_col"]}: {col_formatted}\n'
                          f'{prj_dict["sqlite3_row_update_data"]}: {dat_formatted}\n'
                          f'{prj_dict["sqlite3_row_update_id"]}: {row_id}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Check the existence of the table
            check = sqlite3_tbl_check(mpy_trace, prj_dict, db_path, table_name)

    #   Proceed only if table exists and column count is plausible.
        if check:

        #   Execution
            try:
            #   Build the datasets fo be updated
                k = 0

                for dat in columns:
                    if k:
                        dat_sets = f'{dat_sets}, \"{columns[k]})\" = \"{cell_data[k]}\"'
                    else:
                        dat_sets = f'\"{columns[k]}\" = \"{cell_data[k]}\"'
                    k += 1

            #   Define the execution statement
                exec_statement = f'UPDATE {table_name} SET {dat_sets} WHERE ID = {row_id}'

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
                log_message = (f'{prj_dict["sqlite3_row_update_ready"]}\n'
                              f'{prj_dict["sqlite3_row_update_db"]}: {db_path}\n'
                              f'{prj_dict["sqlite3_row_update_tbl"]}: {table_name}\n'
                              f'{prj_dict["sqlite3_row_update_col"]}: {col_formatted}\n'
                              f'{prj_dict["sqlite3_row_update_data"]}: {dat_formatted}\n'
                              f'{prj_dict["sqlite3_row_update_id"]}: {row_id}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

                return{
                    'check' : check , \
                    'row_id' : row_id
                    }

        #   Error detection
            except Exception as e:
                log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                              f'{prj_dict["err_excp"]}: {e}\n'
                              f'{prj_dict["sqlite3_row_update_smnt"]}: {exec_statement}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    #   Log and print a denial
        if not check:
        #   Create a log
        #   The table does not exist.
            log_message = (f'{prj_dict["sqlite3_row_update_tbl_nex"]}\n'
                          f'{prj_dict["sqlite3_row_update_db"]}: {db_path}\n'
                          f'{prj_dict["sqlite3_row_update_tbl"]}: {table_name}\n'
                          f'check: {check}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

    #   Log and print a denial
        if not plausible:
        #   Create a log
        #   The number of columns does not match the number of values handed to the function.
            log_message = (f'{prj_dict["sqlite3_row_update_mismatch"]}\n'
                          f'{prj_dict["sqlite3_row_update_col"]}: {col_formatted}\n'
                          f'{prj_dict["sqlite3_row_update_numcol"]}: {i}\n'
                          f'{prj_dict["sqlite3_row_update_val"]}: {dat_formatted}\n'
                          f'{prj_dict["sqlite3_row_update_numval"]}: {j}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}')
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
    table_name = f'{table_name}'
    where = f'{where}'
    check = False
    plausible = False
    dat_sets = ''

    try:

    #   Compare the amount of Columns and Cells
        col_formatted = ''
        i = 0
        dat_formatted = ''
        j = 0

        for col in columns:
            if i:
                col_formatted = f'{col_formatted},\"{col}\"'
            else:
                col_formatted = f'\"{col}\"'
            i += 1

        for cld in cell_data:
            if j:
                dat_formatted = f'{dat_formatted},\"{cld}\"'
            else:
                dat_formatted = f'\"{cld}\"'
            j += 1

    #   Plausibility check for columns and according data
        if i == j:
            plausible = True

        #   Create a log
        #   Updating a row of a SQLite database table.
            log_message = (f'{prj_dict["sqlite3_row_update_where_start"]}\n'
                          f'{prj_dict["sqlite3_row_update_where_db"]}: {db_path}\n'
                          f'{prj_dict["sqlite3_row_update_where_tbl"]}: {table_name}\n'
                          f'{prj_dict["sqlite3_row_update_where_col"]}: {col_formatted}\n'
                          f'{prj_dict["sqlite3_row_update_where_data"]}: {dat_formatted}\n'
                          f'where: {where}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Check the existence of the table
            check = sqlite3_tbl_check(mpy_trace, prj_dict, db_path, table_name)

        if check and plausible:

        #   Execution
            try:
            #   Build the datasets fo be updated
                k = 0

                for dat in columns:
                    if k:
                        dat_sets = f'{dat_sets},\"{columns[k]}\" = \"{cell_data[k]}\"'
                    else:
                        dat_sets = f'\"{columns[k]}\" = \"{cell_data[k]}\"'
                    k += 1

            #   Define the execution statement
                exec_statement = f'UPDATE {table_name} SET {dat_sets} WHERE {where}'

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
                log_message = (f'{prj_dict["sqlite3_row_update_where_ready"]}\n'
                              f'{prj_dict["sqlite3_row_update_where_db"]}: {db_path}\n'
                              f'{prj_dict["sqlite3_row_update_where_tbl"]}: {table_name}\n'
                              f'{prj_dict["sqlite3_row_update_where_col"]}: {col_formatted}\n'
                              f'{prj_dict["sqlite3_row_update_where_data"]}: {dat_formatted}\n'
                              f'where: {where}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'info')

                return{
                    'check' : check , \
                    'where' : where
                    }

        #   Error detection
            except Exception as e:
                log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                              f'{prj_dict["err_excp"]}: {e}\n'
                              f'{prj_dict["sqlite3_row_update_where_smnt"]}: {exec_statement}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    #   Log and print a denial
        if not check:
        #   Create a log
        #   The table does not exist.
            log_message = (f'{prj_dict["sqlite3_row_update_where_tbl_nex"]}\n'
                          f'{prj_dict["sqlite3_row_update_where_db"]}: {db_path}\n'
                          f'{prj_dict["sqlite3_row_update_where_tbl"]}: {table_name}\n'
                          f'check: {check}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

    #   Log and print a denial
        if not plausible:
        #   Create a log
        #   The number of columns does not match the number of values handed to the function.
            log_message = (f'{prj_dict["sqlite3_row_update_where_mismatch"]}\n'
                          f'{prj_dict["sqlite3_row_update_where_col"]}: {col_formatted}\n'
                          f'{prj_dict["sqlite3_row_update_where_numcol"]}: {i}\n'
                          f'{prj_dict["sqlite3_row_update_where_val"]}: {dat_formatted}\n'
                          f'{prj_dict["sqlite3_row_update_where_numval"]}: {j}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'denied')

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'check' : check , \
        'where' : where
        }