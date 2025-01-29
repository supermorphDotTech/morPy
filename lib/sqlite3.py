r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers functions to work with a SQLite database. The
            main database as defined in app_dict will be referenced.

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

# TODO make this a class
# Update how this works (use sets and dicts)

import lib.fct as fct
import sys
import sqlite3

from lib.decorators import metrics, log

@metrics
def sqlite3_db_connect(morpy_trace: dict, app_dict: dict, db_path: str) -> dict:

    r"""
    Establishes a connection to a SQLite database. Creates the database file if it does not exist.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The mpy-specific global dictionary.
    :param db_path: The path to the database to be addressed or altered.

    :return: dict
        conn - sqlite3.Connection object if successful
        error - Error details if the connection fails

    :example:
        sqlite3_db_connect(morpy_trace, app_dict, '/path/to/db.sqlite')
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'sqlite3'
    operation = 'sqlite3_db_connect(~)'
    morpy_trace = fct.tracing(module, operation, morpy_trace)

    # Connecting to SQLite database.
    log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["sqlite3_db_connect_conn"]}\n'
            f'{app_dict["loc"]["morpy"]["sqlite3_db_connect_Path"]}: {db_path}')

    conn = None
    try:
        conn = sqlite3.connect(db_path)

        # SQLite database connected.
        log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["sqlite3_db_connect_ready"]}\n'
                f'conn: {conn}')

        return conn

    except Exception as e:
        log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

@metrics
def sqlite3_db_disconnect(morpy_trace: dict, app_dict: dict, db_path: str) -> dict:

    r"""
    Disconnects a SQLite database.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The mpy-specific global dictionary.
    :param db_path: The path to the database to be addressed or altered.

    :return: dict
        status - Success or failure status
        message - Details about the disconnection process

    :example:
        sqlite3_db_disconnect(morpy_trace, app_dict, '/path/to/db.sqlite')
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'sqlite3'
    operation = 'sqlite3_db_disconnect(~)'
    morpy_trace = fct.tracing(module, operation, morpy_trace)

    try:

        # Disconnecting from SQLite database.
        log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["sqlite3_db_disconnect_discon"]}\n'
                f'{app_dict["loc"]["morpy"]["sqlite3_db_disconnect_path"]}: {db_path}')

        conn = sqlite3.connect(db_path)

    except Exception as e:
        log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    finally:
        try:
            if conn:
                conn.close()

                # SQLite database disconnected.
                log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["sqlite3_db_disconnect_ready"]}\n'
                              f'conn: {conn}')

        except Exception as e:
            log(morpy_trace, app_dict, "error",
                lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

@metrics
def sqlite3_db_statement(morpy_trace: dict, app_dict: dict, db_path: str, db_smnt: str) -> dict:

    r"""
    Executes any SQLite3 statement provided.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The mpy-specific global dictionary.
    :param db_path: The path to the database to be addressed or altered.
    :param db_smnt: The SQLite statement to be executed.

    :return: dict
        check - Indicates whether the function executed successfully (True/False).
        result - Query results or details of the operation.
        error - Error details if the statement fails.

    :example:
        sqlite3_db_statement(morpy_trace, app_dict, '/path/to/db.sqlite', 'SELECT * FROM table_name')
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'sqlite3'
    operation = 'sqlite3_db_statement(~)'
    morpy_trace = fct.tracing(module, operation, morpy_trace)

    # Preparing Parameters
    db_smnt = f'{db_smnt}'
    check = False

    # Executing a SQLite3 statement.
    log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["sqlite3_db_statement_exec"]}\n'
            f'{app_dict["loc"]["morpy"]["sqlite3_db_statement_db"]}: {db_path}\n'
            f'{app_dict["loc"]["morpy"]["sqlite3_db_statement_smnt"]}: {db_smnt}')

    # Execution
    try:

        # Connect the database
        conn = sqlite3_db_connect(morpy_trace, app_dict, db_path)

        # Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

        c = conn.cursor()

        # Insert a new row and write to cell(s)
        c.execute(db_smnt)

        # Commit changes to the database and close the cursor
        conn.commit()
        c.close()

        # Disconnect from the database
        sqlite3_db_disconnect(morpy_trace, app_dict, db_path)

        # Statement executed.
        log(morpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["morpy"]["sqlite3_db_statement_ready"]}\n'
                      f'{app_dict["loc"]["morpy"]["sqlite3_db_statement_db"]}: {db_path}')

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check
        }

@metrics
def sqlite3_tbl_check(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str) -> dict:

    r"""
    Checks for the existence of a table in a given SQLite database.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The mpy-specific global dictionary.
    :param db_path: The path to the database to be addressed or altered.
    :param table_name: The name of the database table to check.

    :return: dict
        check - Indicates whether the function executed successfully (True/False).
        exists - Boolean indicating if the table exists in the database.
        error - Error details if the check fails.

    :example:
        sqlite3_tbl_check(morpy_trace, app_dict, '/path/to/db.sqlite', 'users_table')
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'sqlite3'
    operation = 'sqlite3_tbl_check(~)'
    morpy_trace = fct.tracing(module, operation, morpy_trace)

    table_name = f'{table_name}'
    check = False

    # Checking the existence of a SQLite database table.
    log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["sqlite3_tbl_check_start"]}\n'
            f'{app_dict["loc"]["morpy"]["sqlite3_tbl_check_db"]}: {db_path}\n'
            f'{app_dict["loc"]["morpy"]["sqlite3_tbl_check_tbl"]}: {table_name}')

    # Define the execution statement
    exec_statement = f'SELECT count(name) FROM sqlite_master WHERE type=\"table\" AND name=\"{table_name}\"'

    # Execution
    try:
        # Connect the database
        conn = sqlite3_db_connect(morpy_trace, app_dict, db_path)

        # Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

        c = conn.cursor()

        # Check for the existence of a table
        c.execute(exec_statement)

        # Check the count of found tables
        if c.fetchone()[0] == 1:
            check = True
            # Table exists.
            msg = app_dict["sqlite3_tbl_check_tbl_ex"]

        else:
            # Table does not exist.
            msg = app_dict["sqlite3_tbl_check_tbl_nex"]

            log(morpy_trace, app_dict, "debug",
                lambda: f'{msg}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_tbl_check_db"]}: {db_path}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_tbl_check_tbl"]}: {table_name}\n'
                    f'check: {check}')

        # Close the cursor
        c.close()

        # Disconnect from the database
        sqlite3_db_disconnect(morpy_trace, app_dict, db_path)

    except Exception as e:
        log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check
        }

@metrics
def sqlite3_tbl_create(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str) -> dict:

    r"""
    Creates a table in a given SQLite database.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The mpy-specific global dictionary.
    :param db_path: The path to the database to be addressed or altered.
    :param table_name: The name of the database table to be created.

    :return: dict
        check - Indicates whether the function executed successfully (True/False).
        message - Details about the table creation process.
        error - Error details if the table creation fails.

    :example:
        sqlite3_tbl_create(morpy_trace, app_dict, '/path/to/db.sqlite', 'new_table')
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'sqlite3'
    operation = 'sqlite3_tbl_create(~)'
    morpy_trace = fct.tracing(module, operation, morpy_trace)

    table_name = f'{table_name}'
    check = False

    # Creating a SQLite database table.
    log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["sqlite3_tbl_create_start"]}\n'
            f'{app_dict["loc"]["morpy"]["sqlite3_tbl_create_db"]}: {db_path}\n'
            f'{app_dict["loc"]["morpy"]["sqlite3_tbl_create_tbl"]}: {table_name}')

    # Define the execution statement
    exec_statement = f'CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY)'

    # Execution
    try:
        # Connect the database
        conn = sqlite3_db_connect(morpy_trace, app_dict, db_path)

        # Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

        # Create the actual table
        conn.execute(exec_statement)

        # Commit changes to the database
        conn.commit()

        # SQLite table created.
        log(morpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["morpy"]["sqlite3_tbl_create_ready"]}\n'
                f'{app_dict["loc"]["morpy"]["sqlite3_tbl_create_db"]}: {db_path}\n'
                f'{app_dict["loc"]["morpy"]["sqlite3_tbl_create_tbl"]}: {table_name}')

        # Disconnect from the database
        sqlite3_db_disconnect(morpy_trace, app_dict, db_path)

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check
        }

@metrics
def sqlite3_tbl_column_add(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str, columns: list, col_types: list ) -> dict:

    r"""
    Adds one or more columns to a table in a given SQLite database.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The mpy-specific global dictionary.
    :param db_path: The path to the database to be addressed or altered.
    :param table_name: The name of the database table to be altered.
    :param columns: List of column names to be added.
    :param col_types: List of data types for the new columns as specified for SQLite.

    :return: dict
        check - Indicates whether the function executed successfully (True/False).
        message - Details about the column addition process.
        error - Error details if the column addition fails.

    :example:
        sqlite3_tbl_column_add(morpy_trace, app_dict, '/path/to/db.sqlite', 'table_name', ['new_column1', 'new_column2'], ['TEXT', 'INTEGER'])
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'sqlite3'
    operation = 'sqlite3_tbl_column_add(~)'
    morpy_trace = fct.tracing(module, operation, morpy_trace)

    table_name = f'{table_name}'
    columns_str = f'{columns}'
    col_types_str = f'{col_types}'.upper()
    check = False
    plausible = False

    try:

        # Adding columns to a SQLite database table.
        log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_start"]}\n'
                f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_db"]}: {db_path}\n'
                f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_tbl"]}: {table_name}')

        # Compare items in columns and col_types
        i = 0
        for col in columns:
            i += 1

        # List data types as a string
        j = 0
        for clt in col_types:
            j += 1

        # Check input plausibility
        if i == j:
            plausible = True

            # Check the existence of the table
            check = sqlite3_tbl_check(morpy_trace, app_dict, db_path, table_name)

        # Proceed only if table exists and column count is plausible.
        if check:

            # Connect the database
            conn = sqlite3_db_connect(morpy_trace, app_dict, db_path)

            # Activate WAL mode to acces the database
            conn.execute('pragma journal_mode=wal;')

            k = 0
            try:

                for col in columns:

                    # Define the execution statement
                    exec_statement = f'ALTER TABLE {table_name} ADD COLUMN {columns[k]} {col_types[k]}'

                    # Insert a new row and write to cell(s)
                    conn.execute(exec_statement)

                    # Commit changes to the database and close the cursor
                    conn.commit()

                    # Iterate
                    k += 1

                # Columns added to SQLite table.
                log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_start"]}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_db"]}: {db_path}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_tbl"]}: {table_name}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_col"]}: {columns_str}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_datatype"]}: {col_types_str}')

                # Disconnect from the database
                sqlite3_db_disconnect(morpy_trace, app_dict, db_path)

            except Exception as e:
                log(morpy_trace, app_dict, "error",
                    lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{type(e).__name__}: {e}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_smnt"]}: {exec_statement}')

        # Log and print a denial
        if not check:
            # The table does not exist. Columns could not be inserted.
            log(morpy_trace, app_dict, "denied",
                lambda: f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_tbl_nex"]}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_db"]}: {db_path}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_tbl"]}: {table_name}\n'
                    f'check: {check}')

        # Log and print a denial
        if not plausible:
            # The number of columns does not match the number of datatypes handed over to the function.
            log(morpy_trace, app_dict, "denied",
                lambda: f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_mismatch"]}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_col"]}: {columns_str}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_numcol"]}: {i}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_datatype"]}: {col_types_str}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_tbl_column_add_numdatatype"]}: {j}')

    except Exception as e:
        log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'tbl_check' : tbl_check
        }

@metrics
def sqlite3_row_insert(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str, columns: list, cell_data: list) -> dict:

    r"""
    Inserts a row into a table in a given SQLite database.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The mpy-specific global dictionary.
    :param db_path: The path to the database to be addressed or altered.
    :param table_name: The name of the database table where the row will be inserted.
    :param columns: List of column names to be written into. The number of columns must match the number of data values.
    :param cell_data: List of data values to be written into the cells. The number of values must match the number of columns addressed.

    :return: dict
        check - Indicates whether the function executed successfully (True/False).
        row_id - ID of the row that was inserted.
        error - Error details if the row insertion fails.

    :example:
        sqlite3_row_insert(morpy_trace, app_dict, '/path/to/db.sqlite', 'example_table', ['column1', 'column2'], ['value1', 123])
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'sqlite3'
    operation = 'sqlite3_row_insert(~)'
    morpy_trace = fct.tracing(module, operation, morpy_trace)

    table_name = f'{table_name}'
    check = False
    plausible = False

    try:

        # Build strings from columns and data for SQLite
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

        # Define the execution statement
        exec_statement = f'INSERT INTO {table_name} ({col_formatted}) VALUES ({dat_formatted})'

        # Inserting a row into a SQLite database table.
        log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_start"]}\n'
                      f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_db"]}: {db_path}\n'
                      f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_tbl"]}: {table_name}')

        # Plausibility check for columns and according data.
        if i == j:
            plausible = True

            # Number of columns match data.
            log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_match"]}\n'
                    f'plausible: {plausible}')

            # Check the existence of the table
            check = sqlite3_tbl_check(morpy_trace, app_dict, db_path, table_name)

        # Proceed only if table exists and column count is plausible.
        if check:

            # Execution
            try:
                # Connect the database
                conn = sqlite3_db_connect(morpy_trace, app_dict, db_path)

                # Activate WAL mode to acces the database
                conn.execute('pragma journal_mode=wal;')

                c = conn.cursor()

                # Insert a new row and write to cell(s)
                c.execute(exec_statement)

                # Check for the last ID
                row_id = int(c.lastrowid)

                # Commit changes to the database and close the cursor
                conn.commit()
                c.close()

                # Disconnect from the database
                sqlite3_db_disconnect(morpy_trace, app_dict, db_path)

                # Row inserted into SQLite table.
                log(morpy_trace, app_dict, "info",
                    lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_ready"]}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_db"]}: {db_path}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_tbl"]}: {table_name}')

            except Exception as e:
                log(morpy_trace, app_dict, "error",
                    lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{type(e).__name__}: {e}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_smnt"]}: {exec_statement}')

        # Log and print a denial
        if not check:
            # The table does not exist.
            log(morpy_trace, app_dict, "denied",
                lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_tblnex"]}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_db"]}: {db_path}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_tbl"]}: {table_name}\n'
                    f'check: {check}')

        # Log and print a denial
        if not plausible:
            # The number of columns does not match the number of values handed to the function.
            log(morpy_trace, app_dict, "denied",
                lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_mismatch"]}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_col"]}: {col_formatted}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_numcol"]}: {i}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_insert_numval"]}: {j}')

    except Exception as e:
        log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'row_id' : row_id
        }

@metrics
def sqlite3_row_update(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str, columns: list, cell_data: list, row_id: int) -> dict:

    r"""
    Updates a row in a table in a given SQLite database. Only the specified columns will be updated.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The mpy-specific global dictionary.
    :param db_path: The path to the database to be addressed or altered.
    :param table_name: The name of the database table where the row will be updated.
    :param columns: List of column names to be updated.
    :param cell_data: List of data values to be written into the specified columns. The number of values must match the number of columns addressed.
    :param row_id: The ID (primary key) of the row to be updated.

    :return: dict
        check - Indicates whether the function executed successfully (True/False).
        message - Details about the update operation.
        error - Error details if the update operation fails.

    :example:
        sqlite3_row_update(morpy_trace, app_dict, '/path/to/db.sqlite', 'example_table', ['column1', 'column2'], ['new_value1', 456], 42)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'sqlite3'
    operation = 'sqlite3_row_update(~)'
    morpy_trace = fct.tracing(module, operation, morpy_trace)

    table_name = f'{table_name}'
    check = False
    plausible = False
    dat_sets = ''

    try:

        # Compare the amount of Columns and Cells
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

        # Plausibility check for columns and according data
        if i == j:
            plausible = True

            # Updating a row of a SQLite database table.
            log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_update_start"]}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_db"]}: {db_path}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_tbl"]}: {table_name}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_col"]}: {col_formatted}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_id"]}: {row_id}')

            # Check the existence of the table
            check = sqlite3_tbl_check(morpy_trace, app_dict, db_path, table_name)

        # Proceed only if table exists and column count is plausible.
        if check:

            # Execution
            try:
                # Build the datasets fo be updated
                k = 0

                for dat in columns:
                    if k:
                        dat_sets = f'{dat_sets}, \"{columns[k]})\" = \"{cell_data[k]}\"'
                    else:
                        dat_sets = f'\"{columns[k]}\" = \"{cell_data[k]}\"'
                    k += 1

                # Define the execution statement
                exec_statement = f'UPDATE {table_name} SET {dat_sets} WHERE ID = {row_id}'

                # Connect the database
                conn = sqlite3_db_connect(morpy_trace, app_dict, db_path)

                # Activate WAL mode to acces the database
                conn.execute('pragma journal_mode=wal;')

                c = conn.cursor()

                # Insert a new row and write to cell(s)
                c.execute(exec_statement)

                # Commit changes to the database and close the cursor
                conn.commit()
                c.close()

                # Disconnect from the database
                sqlite3_db_disconnect(morpy_trace, app_dict, db_path)

                # Updated a row of a SQLite table.
                log(morpy_trace, app_dict, "info",
                    lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_update_ready"]}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_row_update_db"]}: {db_path}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_row_update_tbl"]}: {table_name}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_row_update_col"]}: {col_formatted}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_row_update_id"]}: {row_id}')

            except Exception as e:
                log(morpy_trace, app_dict, "error",
                    lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{type(e).__name__}: {e}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_row_update_smnt"]}: {exec_statement}')

        # Log and print a denial
        if not check:
            # The table does not exist.
            log(morpy_trace, app_dict, "denied",
                lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_update_tbl_nex"]}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_db"]}: {db_path}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_tbl"]}: {table_name}\n'
                    f'check: {check}')

        # Log and print a denial
        if not plausible:
            # The number of columns does not match the number of values handed to the function.
            log(morpy_trace, app_dict, "denied",
                lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_update_mismatch"]}\n'
                          f'{app_dict["loc"]["morpy"]["sqlite3_row_update_col"]}: {col_formatted}\n'
                          f'{app_dict["loc"]["morpy"]["sqlite3_row_update_numcol"]}: {i}\n'
                          f'{app_dict["loc"]["morpy"]["sqlite3_row_update_numval"]}: {j}')

    except Exception as e:
        log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'row_id' : row_id
        }

@metrics
def sqlite3_row_update_where(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str, columns: list, cell_data: list, where: str) -> dict:

    r"""
    Updates one or more rows in a table in a given SQLite database based on a specified condition.
    Only the specified columns will be updated.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The mpy-specific global dictionary.
    :param db_path: The path to the database to be addressed or altered.
    :param table_name: The name of the database table where the row(s) will be updated.
    :param columns: List of column names to be updated.
    :param cell_data: List of data values to be written into the specified columns. The number of values must match the number of columns addressed.
    :param where: SQL condition to specify which rows will be updated.

    :return: dict
        check - Indicates whether the function executed successfully (True/False).
        message - Details about the update operation.
        error - Error details if the update operation fails.

    :example:
        sqlite3_row_update_where(morpy_trace, app_dict, '/path/to/db.sqlite', 'example_table', ['column1', 'column2'], ['new_value1', 456], "id = 42 AND status = 'active'"
        )
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'sqlite3'
    operation = 'sqlite3_row_update_where(~)'
    morpy_trace = fct.tracing(module, operation, morpy_trace)

    table_name = f'{table_name}'
    where = f'{where}'
    check = False
    plausible = False
    dat_sets = ''

    try:

        # Compare the amount of Columns and Cells
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

        # Plausibility check for columns and according data
        if i == j:
            plausible = True

            # Updating a row of a SQLite database table.
            log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_start"]}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_db"]}: {db_path}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_tbl"]}: {table_name}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_col"]}: {col_formatted}\n'
                    f'where: {where}')

            # Check the existence of the table
            check = sqlite3_tbl_check(morpy_trace, app_dict, db_path, table_name)

        if check and plausible:

            # Execution
            try:
                # Build the datasets fo be updated
                k = 0

                for dat in columns:
                    if k:
                        dat_sets = f'{dat_sets},\"{columns[k]}\" = \"{cell_data[k]}\"'
                    else:
                        dat_sets = f'\"{columns[k]}\" = \"{cell_data[k]}\"'
                    k += 1

                # Define the execution statement
                exec_statement = f'UPDATE {table_name} SET {dat_sets} WHERE {where}'

                # Connect the database
                conn = sqlite3_db_connect(morpy_trace, app_dict, db_path)

                # Activate WAL mode to acces the database
                conn.execute('pragma journal_mode=wal;')

                c = conn.cursor()

                # Insert a new row and write to cell(s)
                c.execute(exec_statement)

                # Commit changes to the database and close the cursor
                conn.commit()
                c.close()

                # Disconnect from the database
                sqlite3_db_disconnect(morpy_trace, app_dict, db_path)

                # Updated a row of a SQLite table.
                log(morpy_trace, app_dict, "info",
                    lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_ready"]}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_db"]}: {db_path}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_tbl"]}: {table_name}\n'
                        f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_col"]}: {col_formatted}\n'
                        f'where: {where}')

            except Exception as e:
                log(morpy_trace, app_dict, "error",
                    lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{type(e).__name__}: {e}')

        # Log and print a denial
        if not check:
            # The table does not exist.
            log(morpy_trace, app_dict, "denied",
                lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_tbl_nex"]}\n'
                          f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_db"]}: {db_path}\n'
                          f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_tbl"]}: {table_name}\n'
                          f'check: {check}')

        # Log and print a denial
        if not plausible:
            # The number of columns does not match the number of values handed to the function.
            log(morpy_trace, app_dict, "denied",
                lambda: f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_mismatch"]}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_col"]}: {col_formatted}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_numcol"]}: {i}\n'
                    f'{app_dict["loc"]["morpy"]["sqlite3_row_update_where_numval"]}: {j}')

    except Exception as e:
        log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace, \
        'check' : check , \
        'where' : where
        }