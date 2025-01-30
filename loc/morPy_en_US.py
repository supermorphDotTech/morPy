r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module defines all descriptive, localized strings for use in the developed app.
            It is loaded during initialization.
"""

def loc_morpy() -> dict:
    r"""
    This dictionary defines all messages for morPy core functions localized to a
    specific language.

    :param:
        -

    :return: dict
        loc_morpy_dict: Localization dictionary for morPy core functions. All keys
            will be copied to app_dict during morPy initialization.

    :example:
        app_dict["loc"]["mpy"][KEY]
    """

    loc_morpy_dict = {

        # #################
        # Area: General messaging
        # #################

        # ERRORS - Common vocabulary
        'err_line' : 'Line',
        'err_module' : 'in module',
        'err_excp' : 'Exception',
        'priority' : 'priority',
        'trace' : 'trace',
        'process' : 'process',
        'thread' : 'thread',
        'task' : 'task',

        # ERRORS - Built-in error types
        'AssertionError' : 'Assertion failed.',
        'AttributeError' : 'Attribute assignment or reference failed.',
        'EOFError' : 'End of file.',
        'FloatingPointError' : 'Floating point operation failed.',
        'GeneratorExit' : 'Generator close() method failed.',
        'ImportError' : 'Imported module can not be found.',
        'IndexError' : 'Index of sequence is out of range.',
        'KeyError' : 'Key not found.',
        'KeyboardInterrupt' : 'Keyboard interrupt by user.',
        'MemoryError' : 'Out of memory.',
        'NameError' : 'Variable addressed not found.',
        'NotImplementedError' : 'Class is in development.',
        'OSError' : 'A system related error occurred.',
        'OverflowError' : 'Result of arithmetic operation too big to be represented.',
        'ReferenceError' : 'A weak reference proxy is used to access a garbage collected referent.',
        'RuntimeError' : 'A non-specific error occurred.',
        'StopIteration' : 'No further item can be returned by the next() iterator.',
        'SyntaxError' : 'The parser encountered a syntax error.',
        'IndentationError' : 'Incorrect indentation encountered.',
        'TabError' : 'Indentation consists of inconsistent tabs and spaces.',
        'SystemError' : 'The interpreter detected an internal error.',
        'SystemExit' : 'The operation sys.exit() encountered an error.',
        'TypeError' : 'A function or operation is applied to an object of an incorrect type.',
        'UnboundLocalError' : 'A reference is made to a local variable in a function or method, but no value has been bound to that variable.',
        'UnicodeError' : 'A Unicode-related encoding or decoding error occurred.',
        'UnicodeEncodeError' : 'A Unicode-related error occurred during encoding.',
        'UnicodeDecodeError' : 'A Unicode-related error occurred during decoding.',
        'UnicodeTranslateError' : 'A Unicode-related error occurred during translation.',
        'ValueError' : 'A function got an argument of correct type but improper value.',
        'ZeroDivisionError' : 'The second operand of a division or module operation is zero.',

        # #################
        # Area: lib.bulk_ops.py
        # #################

        # lib.bulk_ops.py - find_replace_saveas(~)
        'find_replace_saveas_start': 'Operation start.',
        'find_replace_saveas_f_ex_skip': 'File already exists. Operation skipped.',
        'find_replace_saveas_tpl_err': 'Wrong type. Input must be a tuple of tuples.',

        # #################
        # Area: lib.common.py
        # #################

        # common.py - cl_priority_queue.__init__(~)
        'cl_priority_queue_name' : 'Entity name',
        'cl_priority_queue_init_done' : 'Priority queue initialized.',

        # common.py - cl_priority_queue.enqueue(~)
        'cl_priority_queue_enqueue_task' : 'Task',
        'cl_priority_queue_enqueue_prio_corr' : 'Invalid argument given to process queue. Autocorrected.',
        'cl_priority_queue_enqueue_start' : 'Pushing task to',
        'cl_priority_queue_enqueue_priority' : 'Priority',
        'cl_priority_queue_enqueue_none' : 'Task can not be None. Skipping enqueue.',

        # common.py - cl_priority_queue.dequeue(~)
        'cl_priority_queue_dequeue_task' : 'Task',
        'cl_priority_queue_dequeue_start' : 'Pulling task from',
        'cl_priority_queue_dequeue_name' : 'Task name',
        'cl_priority_queue_dequeue_priority' : 'Priority',
        'cl_priority_queue_dequeue_cnt' : 'Counter',
        'cl_priority_queue_dequeue_void' : 'Can not dequeue from an empty priority queue. Skipped...',

        # common.py - cl_progress._init(~)
        'cl_progress_miss_total': 'Missing total count. Can not track progress if point of completion is unknown.',

        # common.py - cl_progress.update(~)
        'cl_progress_upd_stopped': 'Current progress exceeded total. Progress updates stopped.',
        'cl_progress_proc': 'Processing',

        # common.py - decode_to_plain_text(~)
        'decode_to_plain_text_from' : 'Decoded from',
        'decode_to_plain_text_to' : 'to plain text.',
        'decode_to_plain_text_msg' : 'Message',
        'decode_to_plain_text_not' : 'The Input is not encoded or not supported. No action taken.',
        'decode_to_plain_text_val_fail' : 'Validation of encoding failed.',

        # common.py - dialog_sel_file(~)
        'dialog_sel_file_nosel' : 'No file was chosen by the user.',
        'dialog_sel_file_choice' : 'Choice',
        'dialog_sel_file_cancel' : 'Cancel',
        'dialog_sel_file_asel' : 'A file was chosen by the user.',
        'dialog_sel_file_open' : 'Open',
        'dialog_sel_file_all_files' : 'All Files',
        'dialog_sel_file_select' : 'Select a File',
        'dialog_sel_file_path' : 'Path',

        # common.py - dialog_sel_dir(~)
        'dialog_sel_dir_nosel' : 'No directory was chosen by the user.',
        'dialog_sel_dir_choice' : 'Choice',
        'dialog_sel_dir_cancel' : 'Cancel',
        'dialog_sel_dir_asel' : 'A directory was chosen by the user.',
        'dialog_sel_dir_open' : 'Open',
        'dialog_sel_dir_select' : 'Select a Directory',
        'dialog_sel_dir_path' : 'Path',

        # common.py - fso_copy_file(~)
        'fso_copy_file_source' : 'Source',
        'fso_copy_file_dest' : 'Destination',
        'fso_copy_file_copy_ovwr' : 'A file has been copied and was overwritten.',
        'fso_copy_file_copy_not_ovwr' : 'A file was not copied because it already exists and no overwrite permission was given.',
        'fso_copy_file_copy' : 'A file has been copied.',
        'fso_copy_file_not_exist' : 'A file has been copied and was overwritten.',

        # common.py - fso_create_dir(~)
        'fso_create_dir_directory' : 'Directory',
        'fso_create_dir_direxist' : 'Directory exists',
        'fso_create_dir_not_created' : 'The directory already exists.',
        'fso_create_dir_created' : 'The directory has been created.',

        # common.py - fso_delete_dir(~)
        'fso_delete_dir_directory' : 'Directory',
        'fso_delete_dir_direxist' : 'Directory exists',
        'fso_delete_dir_deleted' : 'The directory has been deleted.',
        'fso_delete_dir_notexist' : 'The directory does not exist.',

        # common.py - fso_delete_file(~)
        'fso_delete_file_file' : 'File',
        'fso_delete_file_exist' : 'File exists',
        'fso_delete_file_deleted' : 'The file has been deleted.',
        'fso_delete_file_notexist' : 'The file does not exist.',

        # common.py - fso_walk(~)
        'fso_walk_path_done' : 'Directory analyzed.',
        'fso_walk_path_dir' : 'Directory',
        'fso_walk_path_notexist' : 'The directory does not exist.',

        # common.py - regex_findall(~)
        'regex_findall_init' : 'Searching for regular expressions.',
        'regex_findall_pattern' : 'Pattern',
        'regex_findall_result' : 'Result',
        'regex_findall_compl' : 'Search completed.',

        # common.py - regex_find1st(~)
        'regex_find1st_init' : 'Searching for regular expressions.',
        'regex_find1st_pattern' : 'Pattern',
        'regex_find1st_result' : 'Result',
        'regex_find1st_compl' : 'Search completed.',
        'regex_find1st_none' : 'String is NoneType. No Regex executed.',

        # common.py - regex_split(~)
        'regex_split_init' : 'Splitting a string by a given delimiter.',
        'regex_split_delimiter' : 'Delimiter',
        'regex_split_result' : 'Result',
        'regex_split_compl' : 'String has been split.',
        'regex_split_none' : 'String is NoneType. No Split executed.',

        # common.py - regex_replace(~)
        'regex_replace_init' : 'Changing a string by given parameters.',
        'regex_replace_compl' : 'String substituted.',
        'regex_replace_result' : 'Result',

        # common.py - regex_remove_special(~)
        'regex_remove_special_init' : 'Removing special characters of a string and replacing them.',
        'regex_remove_special_compl' : 'String substituted.',
        'regex_remove_special_result' : 'Result',
        'regex_remove_special_tuple' : 'Tuple',
        'regex_remove_special_special' : 'Special',
        'regex_remove_special_replacer' : 'Replacer',

        # common.py - textfile_write(~)
        'textfile_write_appended' : 'Textfile has been appended to.',
        'textfile_write_created' : 'Textfile has been created.',
        'textfile_write_content' : 'Content',

        # common.py - wait_for_input(~)
        'wait_for_input_compl' : 'A user input was made.',
        'wait_for_input_message' : 'Message',
        'wait_for_input_usr_inp' : 'User input',

        # common.py - wait_for_select(~)
        'wait_for_select_compl' : 'A user input was made.',
        'wait_for_select_message' : 'Message',
        'wait_for_select_usr_inp' : 'User input',
        "wait_for_select_yes_selector": "y",
        "wait_for_select_yes": "yes",
        "wait_for_select_quit_selector": "q",
        "wait_for_select_quit": "quit",
        "wait_for_select_selection_invalid": "Invalid selection. Repeat?",

        # #################
        # Area: lib.csv.py
        # #################

        # csv.py - csv_read(~)
        'csv_read_start': 'Started processing CSV-file.',
        'csv_read_done': 'CSV file processed. Keys in dictionary',
        'csv_read_not_done': 'File does not exist or is not a CSV file.',
        'csv_read_file_exist': 'File exists',
        'csv_read_isfile': 'Is file',
        'csv_read_file_ext': 'File extension',
        'csv_read_file_path': 'File path',
        'csv_read_no_return': 'Delimiters could not be determined or data is corrupted. No return dictionary created.',

        # csv.py - csv_dict_to_excel(~)
        'csv_dict_to_excel_prog_fail': 'Missing row count in csv_dict. Skipping progress logging.',
        'csv_dict_to_excel_xl_ovwr': 'MS Excel file exists. Overwritten.',
        'csv_dict_to_excel_path': 'File Path',
        'csv_dict_to_excel_ovwr': 'Overwrite',
        'csv_dict_to_excel_xl_novwr': 'MS Excel file exists. Operation skipped.',
        'csv_dict_to_excel_missing_xl': 'Missing path to MS Excel file. Operation skipped.',
        'csv_dict_to_excel_inval_xl': 'Invalid path to MS Excel file. Operation skipped.',
        'csv_dict_to_excel_missing_data': 'Missing data book from csv file. operation skipped.',
        'csv_dict_to_excel_data': 'csv_dict',
        'csv_dict_to_excel_start': 'Writing data to MS Excel file.',
        'csv_dict_to_excel_prog_descr': 'Writing CSV to Excel',

        # #################
        # Area: lib.exit.py
        # #################

        # exit.py - exit(~)
        'exit_msg_done': 'App exited.',
        'exit_msg_started': 'Started',
        'exit_msg_at': 'at',
        'exit_msg_exited': 'Exited',
        'exit_msg_duration': 'Duration',
        'exit_msg_events': 'Events',
        'exit_msg_total': 'Total',

        # #################
        # Area: lib.init.py
        # #################

        # init.py - init(~)
        'events_total_descr' : 'Total number of logged events.',
        'events_DEBUG_descr' : 'Number of occurrences with the log level "debug".',
        'events_INFO_descr' : 'Number of occurrences with the log level "info".',
        'events_WARNING_descr' : 'Number of occurrences with the log level "warning".',
        'events_DENIED_descr' : 'Number of occurrences with the log level "denied".',
        'events_ERROR_descr' : 'Number of occurrences with the log level "error".',
        'events_CRITICAL_descr' : 'Number of occurrences with the log level "critical".',
        'events_UNDEFINED_descr' : 'Number of occurrences with the log level "undefined".',
        'events_INIT_descr' : 'Number of occurrences with the log level "init".',
        'events_EXIT_descr' : 'Number of occurrences with the log level "exit".',
        'init_loc_dbg_loaded' : 'morPy debug localization loaded.',
        'init_loc_app_loaded' : 'App localization loaded.',
        'init_loc_finished' : 'Localization initialized.',
        'init_loc_lang' : 'Language',
        'init_finished' : 'Initialization process finished.',
        'init_duration' : 'Duration',

        # init.py - morpy_log_header(~)
        'log_header_start' : 'START',
        'log_header_author' : 'Author',
        'log_header_app' : 'App',
        'log_header_timestamp' : 'Timestamp',
        'log_header_user' : 'User',
        'log_header_system' : 'System',
        'log_header_version' : 'Version',
        'log_header_architecture' : 'Architecture',
        'log_header_threads' : 'Threads',
        'log_header_begin' : 'BEGIN',

        # init.py - morpy_ref(~)
        'ref_descr' : 'This file shows the parameters set in lib.conf.py as well as the most important system and app related information. All of these are addressable through the app_dict which is available throughout all functions and modules of this framework. This reference is meant to be used for development only.',
        'ref_created' : 'The init_dict was written to textfile.',
        'ref_path' : 'Filepath',

        # #################
        # Area: lib.mp.py
        # #################

        # mp.py - cl_orchestrator._init(~)
        'cl_orchestrator_init_not_bool': 'Value is not a boolean. Check lib.conf.py for correction.',
        'cl_orchestrator_init_not_int': 'Value is not an integer. Check lib.conf.py for correction.',
        'cl_orchestrator_init_not_float': 'Value is not a float. Check lib.conf.py for correction.',
        'cl_orchestrator_init_not_str': 'Value is not a string. Check lib.conf.py for correction.',
        'cl_orchestrator_init_rel_math_corr': 'Rounding corrected.',
        'cl_orchestrator_init_cpus_determined': 'Maximum amount of parallel processes determined.',
        'cl_orchestrator_init_memory_set': 'Maximum memory set.',
        'cl_orchestrator_init_done': 'Multiprocessing initialized.',

        # mp.py - cl_orchestrator._run(~)
        'cl_orchestrator_run_app_start': 'App starting.',

        # mp.py - join_processes(~)
        'join_processes_start': 'Joining processes',

        # mp.py - watcher(~)
        'watcher_is_alive': 'Process Watcher: Process still alive.',
        'watcher_end': 'Process Watcher: Process ended, cleaning up process',

        # mp.py - run_parallel(~)
        'run_parallel_task': 'Task',
        'run_parallel_task_sys_id': 'Task ID',
        'run_parallel_start': 'Parallel process starting. ID',
        'run_parallel_exit': 'Parallel process created. ID',
        'run_parallel_call_err': 'Task provided is not callable.',
        'run_parallel_id_abort': 'Could not get process ID. Task was enqueued again.',
        'run_parallel_issues': 'Issues encountered:',
        'run_parallel_id_err_avl': 'Process ID conflict. Possible concurrent process creation. Process creation skipped.',
        'run_parallel_id_err_busy': 'Process ID conflict. ID# seemed available, is busy. Process creation skipped.',
        'run_parallel_id_err_dict': 'Process ID conflict. A process may have terminated dirty. Process creation skipped.',
        'run_parallel_requeue_err': 'Task could not be enqueued again. Task ID still in queue. Data loss possible.',
        'run_parallel_proc_busy': 'Processes busy',
        'run_parallel_proc_avl': 'Processes available',
        'run_parallel_start_w_arg': 'Starting process control with arguments',
        'run_parallel_search_p_id': 'Searching for available process ID.',
        'run_parallel_search_iter_end': 'Process ID determined.',
        'run_parallel_clean_up_remnants': 'Process remnant found.Cleaning up after supposed process crash.',

        # #################
        # Area: lib.msg.py
        # #################

        # msg.py - log(~)
        'log_crit_fail': 'Severe morPy logging error.',

        # msg.py - log_msg_builder(~)
        'log_msg_builder_trace': 'Trace',
        'log_msg_builder_process_id': 'Process',
        'log_msg_builder_thread_id': 'Thread',
        'log_msg_builder_task_id': 'Task',

        # msg.py - log_interrupt(~)
        'msg_print_intrpt': '>>> INTERRUPT <<< Press Enter to continue...',

        # msg.py - log_db_connect(~)
        'log_db_connect_excpt': 'The database could not be found and/or connected.',

        # msg.py - log_db_disconnect(~)
        'log_db_disconnect_excpt': 'The database could not be found and/or disconnected.',

        # msg.py - log_db_table_create(~)
        'log_db_table_create_excpt': 'The log table for runtime could not be created.',
        'log_db_table_create_stmt': 'Statement',

        # msg.py - log_db_table_add_column(~)
        'log_db_table_add_column_excpt': 'The log table could not be edited.',
        'log_db_table_add_column_stmt': 'Statement',
        'log_db_table_add_column_failed': 'The log table could not be found. Logging not possible.',

        # msg.py - log_db_row_insert(~)
        'log_db_row_insert_excpt': 'The log entry could not be created.',
        'log_db_row_insert_stmt': 'Statement',
        'log_db_row_insert_failed': 'The log table could not be found. Logging not possible.',

        # #################
        # Area: lib.sqlite3.py
        # #################

        # sqlite3.py - sqlite3_db_connect(~)
        'sqlite3_db_connect_conn': 'Connecting to SQLite database.',
        'sqlite3_db_connect_Path': 'Path',
        'sqlite3_db_connect_ready': 'SQLite database connected.',

        # sqlite3.py - sqlite3_db_disconnect(~)
        'sqlite3_db_disconnect_discon': 'Disconnecting from SQLite database.',
        'sqlite3_db_disconnect_path': 'Path',
        'sqlite3_db_disconnect_ready': 'SQLite database disconnected.',

        # sqlite3.py - sqlite3_db_statement(~)
        'sqlite3_db_statement_exec': 'Executing a SQLite3 statement.',
        'sqlite3_db_statement_db': 'Database',
        'sqlite3_db_statement_smnt': 'Statement',
        'sqlite3_db_statement_ready': 'Statement executed.',

        # sqlite3.py - sqlite3_tbl_check(~)
        'sqlite3_tbl_check_start': 'Checking the existence of a SQLite database table.',
        'sqlite3_tbl_check_db': 'Database',
        'sqlite3_tbl_check_tbl': 'Table',
        'sqlite3_tbl_check_tbl_ex': 'Table exists.',
        'sqlite3_tbl_check_tbl_nex': 'Table does not exist.',
        'sqlite3_tbl_check_smnt': 'Statement',

        # sqlite3.py - sqlite3_tbl_create(~)
        'sqlite3_tbl_create_start': 'Creating a SQLite database table.',
        'sqlite3_tbl_create_db': 'Database',
        'sqlite3_tbl_create_tbl': 'Table',
        'sqlite3_tbl_create_ready': 'SQLite table created.',
        'sqlite3_tbl_create_smnt': 'Statement',

        # sqlite3.py - sqlite3_tbl_column_add(~)
        'sqlite3_tbl_column_add_start': 'Adding columns to a SQLite database table.',
        'sqlite3_tbl_column_add_db': 'Database',
        'sqlite3_tbl_column_add_tbl': 'Table',
        'sqlite3_tbl_column_add_col': 'Columns',
        'sqlite3_tbl_column_add_numcol': 'Number of columns',
        'sqlite3_tbl_column_add_datatype': 'Datatypes',
        'sqlite3_tbl_column_add_numdatatype': 'Number of datatypes',
        'sqlite3_tbl_column_add_ready': 'Columns added to SQLite table.',
        'sqlite3_tbl_column_add_smnt': 'Statement',
        'sqlite3_tbl_column_add_tbl_nex': 'The table does not exist. Columns could not be inserted.',
        'sqlite3_tbl_column_add_mismatch': 'The number of columns does not match the number of datatypes handed over to the function.',

        # sqlite3.py - sqlite3_row_insert(~)
        'sqlite3_row_insert_start': 'Inserting a row into a SQLite database table.',
        'sqlite3_row_insert_db': 'Database',
        'sqlite3_row_insert_tbl': 'Table',
        'sqlite3_row_insert_match': 'Number of columns match data.',
        'sqlite3_row_insert_ready': 'Row inserted into SQLite table.',
        'sqlite3_row_insert_col': 'Columns',
        'sqlite3_row_insert_numcol': 'Number of columns',
        'sqlite3_row_insert_val': 'Values',
        'sqlite3_row_insert_numval': 'Number of values',
        'sqlite3_row_insert_data': 'Data',
        'sqlite3_row_insert_smnt': 'Statement',
        'sqlite3_row_insert_tblnex': 'The table does not exist.',
        'sqlite3_row_insert_mismatch': 'The number of columns does not match the number of values handed to the function.',

        # sqlite3.py - sqlite3_row_update(~)
        'sqlite3_row_update_start': 'Updating a row of a SQLite database table.',
        'sqlite3_row_update_db': 'Database',
        'sqlite3_row_update_tbl': 'Table',
        'sqlite3_row_update_col': 'Columns',
        'sqlite3_row_update_numcol': 'Number of columns',
        'sqlite3_row_update_data': 'Data',
        'sqlite3_row_update_val': 'Values',
        'sqlite3_row_update_numval': 'Number of Values',
        'sqlite3_row_update_id': 'Row ID',
        'sqlite3_row_update_ready': 'Updated a row of a SQLite table.',
        'sqlite3_row_update_smnt': 'Statement',
        'sqlite3_row_update_tbl_nex': 'The table does not exist.',
        'sqlite3_row_update_mismatch': 'The number of columns does not match the number of values handed to the function.',

        # sqlite3.py - sqlite3_row_update_where(~)
        'sqlite3_row_update_where_start': 'Updating a row of a SQLite database table.',
        'sqlite3_row_update_where_db': 'Database',
        'sqlite3_row_update_where_tbl': 'Table',
        'sqlite3_row_update_where_col': 'Columns',
        'sqlite3_row_update_where_numcol': 'Number of columns',
        'sqlite3_row_update_where_data': 'Data',
        'sqlite3_row_update_where_val': 'Values',
        'sqlite3_row_update_where_numval': 'Number of Values',
        'sqlite3_row_update_where_id': 'Row ID',
        'sqlite3_row_update_where_ready': 'Updated a row of a SQLite table.',
        'sqlite3_row_update_where_smnt': 'Statement',
        'sqlite3_row_update_where_tbl_nex': 'The table does not exist.',
        'sqlite3_row_update_where_mismatch': 'The number of columns does not match the number of values handed to the function.',

        # #################
        # Area: lib.types_dict.py
        # #################

        # types_dict.py - cl_attr_guard(~)
        'cl_attr_guard' : {
            'cl_attr_guard_no_mod' : 'can not modify an attribute of',
            'cl_attr_guard_no_del': 'Deletion prohibited!',
        },

        # types_dict.py - cl_morpy_dict(~)
        'cl_morpy_dict' : {
            'cl_morpy_dict_denied' : 'Prohibited method',
            'cl_morpy_dict_new_key' : 'Keys can not be added.',
            'cl_morpy_dict_del_key' : 'Keys can not be deleted.',
            'cl_morpy_dict_clear' : 'Dictionary can not be cleared.',
            'cl_morpy_dict_lock' : 'Dictionary is locked.',
            'cl_morpy_dict_item' : 'Item',
            'cl_morpy_dict_key' : 'Key',
            'cl_morpy_dict_val' : 'Value',
            "cl_morpy_dict_key_str" : "Keys must be strings.",
            "cl_morpy_dict_empty" : "Dictionary is empty.",
            "cl_morpy_dict_err_unlink" : "Error unlinking UltraDict instance",
        },

        # #################
        # Area: lib.ui_tk.py
        # #################

        # ui_tk.py - cl_progress_gui._init(~)
        'cl_progress_gui_prog': 'Progress',
        'cl_progress_gui_overall': 'Overall Progress',
        'cl_progress_gui_curr': 'Current Stage',
        'cl_progress_gui_abort': 'Abort',
        'cl_progress_gui_close': 'Close',
        'cl_progress_gui_done': 'All operations finished successfully.',
        'cl_progress_gui_start_work_thread_err': 'Exception in the worker thread.',

        # #################
        # Area: lib.xl.py
        # #################

        # xl.py - cl_xl_workbook._init(~)
        'cl_xl_workbook_inst': 'MS Excel workbook instantiated.',
        'cl_xl_workbook_wb': 'Workbook',
        'cl_xl_workbook_path_invalid': 'The path to the workbook is invalid.',
        'cl_xl_workbook_path': 'Path',
        'cl_xl_workbook_inst_abort': 'Instance construction aborted.',
        'cl_xl_workbook_not_create': 'File does not exist and was not created.',
        'cl_xl_workbook_create': 'Create',

        # xl.py - cl_xl_workbook._create_workbook(~)
        'create_workbook_done': 'MS Excel workbook created.',

        # xl.py - cl_xl_workbook._cell_ref_autoformat(~)
        'cell_ref_autoformat_1cell' : 'A single cell was added to the dictionary.',
        'cell_ref_autoformat_cl' : 'Cell',
        'cell_ref_autoformat_done' : 'A range of cells was added to the dictionary.',
        'cell_ref_autoformat_rng' : 'Range',
        'cell_ref_autoformat_invalid' : 'The cell value is invalid. Autoformatting aborted.',
        'cell_ref_autoformat_cls' : 'Cells',

        # xl.py - cl_xl_workbook.close_workbook(~)
        'close_workbook_done': 'The workbook object was closed.',
        'close_workbook_path': 'Path',

        # xl.py - cl_xl_workbook.activate_worksheet(~)
        'activate_worksheet_done': 'The worksheet was successfully activated.',
        'activate_worksheet_nfnd': 'The requested sheet was not found.',
        'activate_worksheet_file': 'Workbook',
        'activate_worksheet_req_sht': 'Sheet requested',

        # xl.py - cl_xl_workbook.read_cells(~)
        'read_cells_file' : 'File',
        'read_cells_sht' : 'Sheet',
        'read_cells_nfnd' : 'Could not find the requested worksheet.',
        'read_cells_av_shts' : 'Available Sheets',
        'read_cells_read' : 'The worksheet was read from.',
        'read_cells_cls' : 'Cells',
        'read_cells_no_range' : 'Missing cell range. Skipped reading cells.',

        # xl.py - cl_xl_workbook.write_cells(~)
        'write_cells_done': 'Cells written to.',
        'write_cells_range': 'Range',

        # xl.py - cl_xl_workbook.edit_worksheet(~)
        'edit_worksheet_found' : 'The requested worksheet was found.',
        'edit_worksheet_nfnd' : 'Could not find the requested worksheet.',
        'edit_worksheet_file' : 'File',
        'edit_worksheet_sht' : 'Sheet',
        'edit_worksheet_name' : 'Sheet Name',
        'edit_worksheet_old_name' : 'Old Sheet Name',
        'edit_worksheet_new_name' : 'New Sheet Name',
        'edit_worksheet_position' : 'Worksheet Position',
        'edit_worksheet_dup_name' : 'Duplicate Name',
        'edit_worksheet_shts' : 'Sheets in Workbook',
        'edit_worksheet_create_sheet_done' : 'Worksheet created.',
        'edit_worksheet_rename_sheet_done' : 'Worksheet renamed.',
        'edit_worksheet_duplicate_sheet_done' : 'Worksheet duplicated.',

        # xl.py - cl_xl_workbook.get_table_attributes(~)
        'get_table_attributes_retr' : 'Retrieved all values of an MS Excel table.',
        'get_table_attributes_path' : 'Path',
        'get_table_attributes_sheet' : 'Sheet',
        'get_table_attributes_tbl' : 'Table',

        # xl.py - openpyxl_table_data_dict(~)
        'openpyxl_table_data_dict_conv' : 'Converted an openpyxl data-book into a list specific to the attributes of the MS Excel table.',
        'openpyxl_table_data_dict_tbl' : 'Table',
        'openpyxl_table_data_dict_attr' : 'Attributes',
    }

    return loc_morpy_dict

def loc_morpy_dbg() -> dict:
    r"""
    This dictionary defines all messages for morPy core functions debugging localized to a
    specific language.

    :param:
        -

    :return: dict
        loc_morpy_dbg_dict: Localization dictionary for morPy unit tests. All keys
            will be copied to app_dict during unit testing instead of morPy
            initialization.

    :example:
        app_dict["loc"]["dbg"][KEY]
    """

    loc_morpy_dbg_dict = {}

    return loc_morpy_dbg_dict