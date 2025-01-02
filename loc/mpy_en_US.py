r"""
Author:     Bastian Neuwirth
Date:       29.06.2021
Version:    0.1
Descr.:     This module defines all descriptive strings as a dictionary. This
            dictionary will be initialized, if localization was set accordingly
            in mpy_param.py. The function localization_mpy() is reserved for the
            morPy framework. You may add app specific definitions,
            explanations and whatever you need within the function
            localization_app(). Both of the dictionaries will be initialized
            and may be accessed via app_dict throughout the program.

            The main idea and purpose of this module is to provide a single file
            for later translation that may be translated to other languages.

            The dictionaries defined here are not intended to hold larger texts.
            You may create your own modules for that purpose.
"""

def loc_mpy() -> dict:

    r"""
    This dictionary defines all messages for morPy core functions localized to a
    specific language.

    :param:
        -

    :return: dict
        loc_mpy_dict: Localization dictionary for morPy core functions. All keys
            will be copied to app_dict during morPy initialization.

    :example:
        app_dict["loc"]["mpy"][KEY]
    """

    mpy_language = 'en-US'

    loc_mpy_dict = {

        # morPy specific area - BEGIN

        # ERRORS
        'err_line' : 'Line',
        'err_excp' : 'Exception',
        'priority' : 'priority',
        'trace' : 'trace',
        'process' : 'process',
        'thread' : 'thread',
        'task' : 'task',

        # mpy_init.py - init(~)
        'events_total_descr' : 'Total number of logged events.',
        'events_DEBUG_descr' : 'Number of occurences with the log level "debug".',
        'events_INFO_descr' : 'Number of occurences with the log level "info".',
        'events_WARNING_descr' : 'Number of occurences with the log level "warning".',
        'events_DENIED_descr' : 'Number of occurences with the log level "denied".',
        'events_ERROR_descr' : 'Number of occurences with the log level "error".',
        'events_CRITICAL_descr' : 'Number of occurences with the log level "critical".',
        'events_UNDEFINED_descr' : 'Number of occurences with the log level "undefined".',
        'events_INIT_descr' : 'Number of occurences with the log level "init".',
        'events_EXIT_descr' : 'Number of occurences with the log level "exit".',
        'init_loc_dbg_loaded' : 'morPy debug localization loaded.',
        'init_loc_app_loaded' : 'App localization loaded.',
        'init_loc_finished' : f'Localization initialized.\nLanguage: {mpy_language}',
        'init_finished' : 'Initialization process finished.',
        'init_duration' : 'Duration',

        # mpy_init.py - mpy_log_header(~)
        'mpy_log_header_start' : 'START',
        'mpy_log_header_author' : 'Author',
        'mpy_log_header_app' : 'App',
        'mpy_log_header_timestamp' : 'Timestamp',
        'mpy_log_header_user' : 'User',
        'mpy_log_header_system' : 'System',
        'mpy_log_header_version' : 'Version',
        'mpy_log_header_architecture' : 'Architecture',
        'mpy_log_header_threads' : 'Threads',
        'mpy_log_header_begin' : 'BEGIN',

        # mpy_init.py - mpy_ref(~)
        'mpy_ref_descr' : 'This file shows the parameters set in mpy_param.py as well as the most important system and app related information. All of these are adressable through the app_dict which is available throughout all functions and modules of this framework. This reference is meant to be used for development only.',
        'mpy_ref_created' : 'The init_dict was written to textfile.',
        'mpy_ref_path' : 'Filepath',

        # mpy_fct.py - privileges_handler(~)
        'mpy_priv_handler_eval' : 'Program started with elevated Privileges.',

        # mpy_fct.py - datetime_now(~)
        'datetime_value_descr' : 'Date and time in the format YYYY-MM-DD hh:mm:ss.ms as value (used to determine runtime).',
        'date_descr' : 'Date DD.MM.YYY as a string.',
        'datestamp_descr' : 'Datestamp YYYY-MM-DD as a string.',
        'time_descr' : 'Time hh:mm:ss as a string.',
        'timestamp_descr' : 'Timestamp hhmmss as a string.',
        'datetimestamp_descr' : 'Date- and timestamp YYY-MM-DD_hhmmss as a string.',
        'loggingstamp_descr' : 'Date- and timestamp for logging YYYMMDD_hhmmss as a string.',

        # mpy_fct.py - runtime(~)
        'rnt_delta_descr' : 'Value of the actual runtime.',

        # mpy_fct.py - sysinfo(~)
        'system_descr' : 'Operating system.',
        'system_release_descr' : 'Major version of the operating system.',
        'system_version_descr' : 'Major and subversions of the operating system.',
        'system_arch_descr' : 'Architecture of the operating system.',
        'processor_descr' : 'Processor running the code.',
        'threads_descr' : 'Total threads available to the machine.',
        'username_descr' : 'Returns the username.',
        'homedir_descr' : 'Returns the home directory.',
        'hostname_descr' : 'Returns the host name.',

        # mpy_fct.py - pathtool(~)
        'out_path_descr' : 'Same as the input, but converted to a path.',
        'is_file_descr' : 'The path is a file path.',
        'file_exists_descr' : 'The file has been found under the given path.',
        'file_name_descr' : 'This is the actual file name.',
        'file_ext_descr' : 'This is the file extension or file type.',
        'is_dir_descr' : 'The path is a directory.',
        'dir_exists_descr' : 'The directory has been found under the given path.',
        'dir_name_descr' : 'This is the actual directory name.',
        'parent_dir_descr' : 'Path of the parent directory.',

        # mpy_fct.py - perfinfo(~)
        'boot_time_descr' : 'Timestamp of the latest recorded boot process.',
        'cpu_count_phys_descr' : 'Return the number of physical CPUs in the system.',
        'cpu_count_log_descr' : 'Return the number of logical CPUs in the system.',
        'cpu_freq_max_descr' : 'Return the maximum CPU frequency expressed in Mhz.',
        'cpu_freq_min_descr' : 'Return the minimum CPU frequency expressed in Mhz.',
        'cpu_freq_comb_descr' : 'Return the combined CPU frequency expressed in Mhz.',
        'cpu_perc_comb_descr' : 'Returns the current combined system-wide CPU utilization as a percentage.',
        'cpu_perc_indv_descr' : 'Returns the current individual system-wide CPU utilization as a percentage.',
        'mem_total_MB_descr' : 'Total physical memory in MB (exclusive swap).',
        'mem_available_MB_descr' : 'Memory in MB that can be given instantly to processes without the system going into swap.',
        'mem_used_MB_descr' : 'Memory used in MB.',
        'mem_free_MB_descr' : 'Memory not being used at all (zeroed) that is readily available in MB.',

        # mpy_dict.py - cl_attr_guard(~)
        'cl_attr_guard' : {
            'cl_attr_guard_no_mod' : 'can not modify an attribute of',
            'cl_attr_guard_no_del': 'Deletion prohibited!',
        },

        # mpy_dict.py - cl_shared_dict(~)
        'cl_shared_dict' : {
            'cl_shared_dict_unk_pref': 'Unknown prefix in data',
            'cl_shared_dict_mem_full': 'Shared memory block is full.',
            'cl_shared_dict_key_str': 'Keys must be strings.',
            'cl_shared_dict_empty': 'Dictionary is empty.',
        },

        # mpy_dict.py - mpy_dict_nesting(~)
        'mpy_dict_nesting_done' : 'Dictionary referenced for nesting.',

        # mpy_dict.py - cl_mpy_dict(~)
        'cl_mpy_dict' : {
            'cl_mpy_dict_denied' : 'Prohibited method',
            'cl_mpy_dict_new_key' : 'Keys can not be added.',
            'cl_mpy_dict_del_key' : 'Keys can not be deleted.',
            'cl_mpy_dict_clear' : 'Dictionary can not be cleared.',
            'cl_mpy_dict_lock' : 'Dictionary is locked.',
            'cl_mpy_dict_item' : 'Item',
            'cl_mpy_dict_key' : 'Key',
            'cl_mpy_dict_val' : 'Value',
            "cl_mpy_dict_key_str" : "Keys must be strings.",
            "cl_mpy_dict_empty" : "Dictionary is empty.",
            "cl_mpy_dict_err_unlink" : "Error unlinking UltraDict instance",
        },

        # mpy_msg.py - log_msg_builder(~)
        'log_msg_builder_trace' : 'Trace',
        'log_msg_builder_process_id' : 'Process',
        'log_msg_builder_thread_id' : 'Thread',
        'log_msg_builder_task_id' : 'Task',

        # mpy_msg.py - mpy_msg_print(~)
        'mpy_msg_print_intrpt' : '>>> INTERRUPT <<< Press Enter to continue...',

        # mpy_msg.py - log_db_connect(~)
        'log_db_connect_excpt' : 'The database could not be found and/or connected.',

        # mpy_msg.py - log_db_disconnect(~)
        'log_db_disconnect_excpt' : 'The database could not be found and/or disconnected.',

        # mpy_msg.py - log_db_table_create(~)
        'log_db_table_create_excpt' : 'The log table for runtime could not be created.',
        'log_db_table_create_stmt' : 'Statement',

        # mpy_msg.py - log_db_table_add_column(~)
        'log_db_table_add_column_excpt' : 'The log table could not be edited.',
        'log_db_table_add_column_stmt' : 'Statement',
        'log_db_table_add_column_failed' : 'The log table could not be found. Logging not possible.',

        # mpy_msg.py - log_db_row_insert(~)
        'log_db_row_insert_excpt' : 'The log entry could not be created.',
        'log_db_row_insert_stmt' : 'Statement',
        'log_db_row_insert_failed' : 'The log table could not be found. Logging not possible.',

        # mpy_common.py - cl_priority_queue.__init__(~)
        'cl_priority_queue_name' : 'Entity name',
        'cl_priority_queue_init_done' : 'Priority queue initialized.',

        # mpy_common.py - cl_priority_queue.enqueue(~)
        'cl_priority_queue_enqueue_task' : 'Task',
        'cl_priority_queue_enqueue_prio_corr' : 'Invalid argument given to process queue. Autocorrected.',
        'cl_priority_queue_enqueue_start' : 'Pushing task to',
        'cl_priority_queue_enqueue_priority' : 'Priority',
        'cl_priority_queue_enqueue_none' : 'Task can not be None. Skipping enqueue.',

        # mpy_common.py - cl_priority_queue.dequeue(~)
        'cl_priority_queue_dequeue_task' : 'Task',
        'cl_priority_queue_dequeue_start' : 'Pulling task from',
        'cl_priority_queue_dequeue_name' : 'Task name',
        'cl_priority_queue_dequeue_priority' : 'Priority',
        'cl_priority_queue_dequeue_cnt' : 'Counter',
        'cl_priority_queue_dequeue_void' : 'Can not dequeue from an empty priority queue. Skipped...',

        # mpy_common.py - decode_to_plain_text(~)
        'decode_to_plain_text_from' : 'Decoded from',
        'decode_to_plain_text_to' : 'to plain text.',
        'decode_to_plain_text_msg' : 'Message',
        'decode_to_plain_text_not' : 'The Input is not encoded or not supported. No action taken.',

        # mpy_common.py - dialog_sel_file(~)
        'dialog_sel_file_nosel' : 'No file was chosen by the user.',
        'dialog_sel_file_choice' : 'Choice',
        'dialog_sel_file_cancel' : 'Cancel',
        'dialog_sel_file_asel' : 'A file was chosen by the user.',
        'dialog_sel_file_open' : 'Open',

        # mpy_common.py - dialog_sel_dir(~)
        'dialog_sel_dir_nosel' : 'No directory was chosen by the user.',
        'dialog_sel_dir_choice' : 'Choice',
        'dialog_sel_dir_cancel' : 'Cancel',
        'dialog_sel_dir_asel' : 'A directory was chosen by the user.',
        'dialog_sel_dir_open' : 'Open',

        # mpy_common.py - fso_copy_file(~)
        'fso_copy_file_source' : 'Source',
        'fso_copy_file_dest' : 'Destination',
        'fso_copy_file_copy_ovwr' : 'A file has been copied and was overwritten.',
        'fso_copy_file_copy_not_ovwr' : 'A file was not copied because it already exists and no overwrite permission was given.',
        'fso_copy_file_copy' : 'A file has been copied.',
        'fso_copy_file_not_exist' : 'A file has been copied and was overwritten.',

        # mpy_common.py - fso_create_dir(~)
        'fso_create_dir_directory' : 'Directory',
        'fso_create_dir_direxist' : 'Directory exists',
        'fso_create_dir_not_created' : 'The directory already exists.',
        'fso_create_dir_created' : 'The directory has been created.',

        # mpy_common.py - fso_delete_dir(~)
        'fso_delete_dir_directory' : 'Directory',
        'fso_create_dir_direxist' : 'Directory exists',
        'fso_delete_dir_deleted' : 'The directory has been deleted.',
        'fso_delete_dir_notexist' : 'The directory does not exist.',

        # mpy_common.py - fso_delete_file(~)
        'fso_delete_file_file' : 'File',
        'fso_delete_file_exist' : 'File exists',
        'fso_delete_file_deleted' : 'The file has been deleted.',
        'fso_delete_file_notexist' : 'The file does not exist.',

        # mpy_common.py - fso_walk(~)
        'fso_walk_path_done' : 'Directory analyzed.',
        'fso_walk_path_dir' : 'Directory',
        'fso_walk_path_notexist' : 'The directory does not exist.',

        # mpy_common.py - print_progress(~)
        'cl_progress_proc' : 'Processing',

        # mpy_common.py - regex_findall(~)
        'regex_findall_init' : 'Searching for regular expressions.',
        'regex_findall_pattern' : 'Pattern',
        'regex_findall_result' : 'Result',
        'regex_findall_compl' : 'Search completed.',

        # mpy_common.py - regex_find1st(~)
        'regex_find1st_init' : 'Searching for regular expressions.',
        'regex_find1st_pattern' : 'Pattern',
        'regex_find1st_result' : 'Result',
        'regex_find1st_compl' : 'Search completed.',
        'regex_find1st_none' : 'String is NoneType. No Regex executed.',

        # mpy_common.py - regex_split(~)
        'regex_split_init' : 'Splitting a string by a given delimiter.',
        'regex_split_delimiter' : 'Delimiter',
        'regex_split_result' : 'Result',
        'regex_split_compl' : 'String has been split.',
        'regex_split_none' : 'String is NoneType. No Split executed.',

        # mpy_common.py - regex_replace(~)
        'regex_replace_init' : 'Changing a string by given parameters.',
        'regex_replace_compl' : 'String substituted.',
        'regex_replace_result' : 'Result',

        # mpy_common.py - regex_remove_special(~)
        'regex_remove_special_init' : 'Removing special characters of a string and replacing them.',
        'regex_remove_special_compl' : 'String substituted.',
        'regex_remove_special_result' : 'Result',
        'regex_remove_special_tuple' : 'Tuple',
        'regex_remove_special_special' : 'Special',
        'regex_remove_special_replacer' : 'Replacer',

        # mpy_common.py - textfile_write(~)
        'textfile_write_appended' : 'Textfile has been appended to.',
        'textfile_write_created' : 'Textfile has been created.',
        'textfile_write_content' : 'Content',

        # mpy_common.py - wait_for_input(~)
        'wait_for_input_compl' : 'A user input was made.',
        'wait_for_input_messsage' : 'Message',
        'wait_for_input_usr_inp' : 'User input',

        # mpy_csv.py - csv_read(~)
        'csv_read_start' : 'Started processing CSV-file.',
        'csv_read_done' : 'CSV file processed. Keys in dictionary',
        'csv_read_not_done' : 'File does not exist or is not a CSV file.',
        'csv_read_file_exist' : 'File exists',
        'csv_read_isfile' : 'Is file',
        'csv_read_file_ext' : 'File extension',
        'csv_read_file_path' : 'File path',
        'csv_read_no_return' : 'Delimiters could not be determined or data is corrupted. No return dictionary created.',

        # mpy_exit.py - exit(~)
        'mpy_exit_msg_done' : 'App exited.',
        'mpy_exit_msg_started' : 'Started',
        'mpy_exit_msg_at' : 'at',
        'mpy_exit_msg_exited' : 'Exited',
        'mpy_exit_msg_duration' : 'Duration',
        'mpy_exit_msg_events' : 'Events',
        'mpy_exit_msg_total' : 'Total',

        # mpy_xl.py - cl_autof_rd(~)
        'cl_autof_rd_1cell' : 'A single cell was added to the dictionary.',
        'cl_autof_rd_cl' : 'Cell',
        'cl_autof_rd_done' : 'A range of cells was added to the dictionary.',
        'cl_autof_rd_rng' : 'Range',
        'cl_autof_rd_invalid' : 'The cell value is invalid. Autoformatting aborted.',
        'cl_autof_rd_cls' : 'Cells',

        # mpy_xl.py - cl_read(~)
        'cl_read_sht_active' : 'The requested sheet is active.',
        'cl_read_file' : 'File',
        'cl_read_sht' : 'Sheet',
        'cl_read_sht_activated' : 'Activated requested sheet.',
        'cl_read_nfnd' : 'Could not find the requested workbook sheet.',
        'cl_read_av_shts' : 'Available Sheets',
        'cl_read_copied' : 'The cells and/or ranges were copied.',
        'cl_read_cls' : 'Cells',
        'cl_read_dat' : 'Data only',

        # mpy_xl.py - sht_edit(~)
        'sht_edit_found' : 'The requested workbook sheet was found.',
        'sht_edit_nfnd' : 'Could not find the requested workbook sheet.',
        'sht_edit_file' : 'File',
        'sht_edit_sht' : 'Sheet',
        'sht_edit_name' : 'Sheet Name',
        'sht_edit_old_name' : 'Old Sheet Name',
        'sht_edit_new_name' : 'New Sheet Name',
        'sht_edit_position' : 'Worksheet Position',
        'sht_edit_dup_name' : 'Duplicate Name',
        'sht_edit_shts' : 'Sheets in Workbook',
        'sht_edit_create_sheet_done' : 'Workbook sheet created.',
        'sht_edit_rename_sheet_done' : 'Workbook sheet renamed.',
        'sht_edit_duplicate_sheet_done' : 'Workbook sheet duplicated.',

        # mpy_xl.py - wb_close(~)
        'wb_close_lst_occupied' : 'The dedicated list for MS Excel workbook objects appears to be occupied by a user variable (type mismatch: dictionary expected).',
        'wb_close_lst_type' : 'Object Type',
        'wb_close_lst_content' : 'Object',
        'wb_close_done' : 'The workbook object was closed.',
        'wb_close_nfnd' : 'The workbook object could not be found.',
        'wb_close_obj_loaded' : 'Objects loaded',
        'wb_close_no_wb' : 'The workbook does not exist.',
        'wb_close_no_lst' : 'No workbook object list was created. No loaded workbooks could be found and closed.',

        # mpy_xl.py - wb_close_all(~)
        'wb_close_all_cls_del' : 'Closing all open workbooks. Deleting the list.',
        'wb_close_all_del' : 'Deleting the list.',
        'wb_close_all_lst_fnd' : 'A workbook object list was found. ',
        'wb_close_all_obj_loaded' : 'Objects loaded',
        'wb_close_all_nothing' : 'No workbooks list has been created. Nothing to be closed.',

        # mpy_xl.py - wb_create(~)
        'wb_create_done' : 'New workbook created.',

        # mpy_xl.py - wb_load(~)
        'wb_load_wblst_mismatch' : 'The dedicated list for MS Excel workbook objects appears to be occupied by a user variable.',
        'wb_load_wb_exists' : 'The workbook is already a loaded object. No action required.',
        'wb_load_path' : 'Path',
        'wb_load_obj' : 'Object',
        'wb_load_wb_loaded' : 'MS Excel workbook loaded.',
        'wb_load_no_file' : 'The file does not exist.',
        'wb_load_dat' : 'Data only',

        # mpy_xl.py - wb_tbl_attributes(~)
        'wb_tbl_attributes_retr' : 'Retrieved all values of an MS Excel table.',
        'wb_tbl_attributes_path' : 'Path',
        'wb_tbl_attributes_sheet' : 'Sheet',
        'wb_tbl_attributes_tbl' : 'Table',

        # mpy_xl.py - wb_tbl_inquiry(~)
        'wb_tbl_inquiry_retr' : 'Retrieved all tables of a workbook.',
        'wb_tbl_inquiry_Path' : 'Path',
        'wb_tbl_inquiry_tbl_wksh' : 'Tables and worksheets',
        'wb_tbl_inquiry_tbl_rng' : 'Tables and ranges',

        # mpy_xl.py - opyxl_tbl_datb_dict(~)
        'opyxl_tbl_datb_dict_conv' : 'Converted an openpyxl databook into a list specific to the attributes of the MS Excel table.',
        'opyxl_tbl_datb_dict_tbl' : 'Table',
        'opyxl_tbl_datb_dict_attr' : 'Attributes',

        # mpy_sqlite3.py - sqlite3_db_connect(~)
        'sqlite3_db_connect_conn' : 'Connecting to SQLite database.',
        'sqlite3_db_connect_Path' : 'Path',
        'sqlite3_db_connect_ready' : 'SQLite database connected.',

        # mpy_sqlite3.py - sqlite3_db_disconnect(~)
        'sqlite3_db_disconnect_discon' : 'Disconnecting from SQLite database.',
        'sqlite3_db_disconnect_path' : 'Path',
        'sqlite3_db_disconnect_ready' : 'SQLite database disconnected.',

        # mpy_sqlite3.py - sqlite3_db_statement(~)
        'sqlite3_db_statement_exec' : 'Executing a SQLite3 statement.',
        'sqlite3_db_statement_db' : 'Database',
        'sqlite3_db_statement_smnt' : 'Statement',
        'sqlite3_db_statement_ready' : 'Statement executed.',

        # mpy_sqlite3.py - sqlite3_tbl_check(~)
        'sqlite3_tbl_check_start' : 'Checking the existence of a SQLite database table.',
        'sqlite3_tbl_check_db' : 'Database',
        'sqlite3_tbl_check_tbl' : 'Table',
        'sqlite3_tbl_check_tbl_ex' : 'Table exists.',
        'sqlite3_tbl_check_tbl_nex' : 'Table does not exist.',
        'sqlite3_tbl_check_smnt' : 'Statement',

        # mpy_sqlite3.py - sqlite3_tbl_create(~)
        'sqlite3_tbl_create_start' : 'Creating a SQLite database table.',
        'sqlite3_tbl_create_db' : 'Database',
        'sqlite3_tbl_create_tbl' : 'Table',
        'sqlite3_tbl_create_ready' : 'SQLite table created.',
        'sqlite3_tbl_create_smnt' : 'Statement',

        # mpy_sqlite3.py - sqlite3_tbl_column_add(~)
        'sqlite3_tbl_column_add_start' : 'Adding columns to a SQLite database table.',
        'sqlite3_tbl_column_add_db' : 'Database',
        'sqlite3_tbl_column_add_tbl' : 'Table',
        'sqlite3_tbl_column_add_col' : 'Columns',
        'sqlite3_tbl_column_add_numcol' : 'Number of columns',
        'sqlite3_tbl_column_add_datatype' : 'Datatypes',
        'sqlite3_tbl_column_add_numdatatype' : 'Number of datatypes',
        'sqlite3_tbl_column_add_ready' : 'Columns added to SQLite table.',
        'sqlite3_tbl_column_add_smnt' : 'Statement',
        'sqlite3_tbl_column_add_tbl_nex' : 'The table does not exist. Columns could not be inserted.',
        'sqlite3_tbl_column_add_mismatch' : 'The number of columns does not match the number of datatypes handed over to the function.',

        # mpy_sqlite3.py - sqlite3_row_insert(~)
        'sqlite3_row_insert_start' : 'Inserting a row into a SQLite database table.',
        'sqlite3_row_insert_db' : 'Database',
        'sqlite3_row_insert_tbl' : 'Table',
        'sqlite3_row_insert_match' : 'Number of columns match data.',
        'sqlite3_row_insert_ready' : 'Row inserted into SQLite table.',
        'sqlite3_row_insert_col' : 'Columns',
        'sqlite3_row_insert_numcol' : 'Number of columns',
        'sqlite3_row_insert_val' : 'Values',
        'sqlite3_row_insert_numval' : 'Number of values',
        'sqlite3_row_insert_data' : 'Data',
        'sqlite3_row_insert_smnt' : 'Statement',
        'sqlite3_row_insert_tblnex' : 'The table does not exist.',
        'sqlite3_row_insert_mismatch' : 'The number of columns does not match the number of values handed to the function.',

        # mpy_sqlite3.py - sqlite3_row_update(~)
        'sqlite3_row_update_start' : 'Updating a row of a SQLite database table.',
        'sqlite3_row_update_db' : 'Database',
        'sqlite3_row_update_tbl' : 'Table',
        'sqlite3_row_update_col' : 'Columns',
        'sqlite3_row_update_numcol' : 'Number of columns',
        'sqlite3_row_update_data' : 'Data',
        'sqlite3_row_update_val' : 'Values',
        'sqlite3_row_update_numval' : 'Number of Values',
        'sqlite3_row_update_id' : 'Row ID',
        'sqlite3_row_update_ready' : 'Updated a row of a SQLite table.',
        'sqlite3_row_update_smnt' : 'Statement',
        'sqlite3_row_update_tbl_nex' : 'The table does not exist.',
        'sqlite3_row_update_mismatch' : 'The number of columns does not match the number of values handed to the function.',

        # mpy_sqlite3.py - sqlite3_row_update_where(~)
        'sqlite3_row_update_where_start' : 'Updating a row of a SQLite database table.',
        'sqlite3_row_update_where_db' : 'Database',
        'sqlite3_row_update_where_tbl' : 'Table',
        'sqlite3_row_update_where_col' : 'Columns',
        'sqlite3_row_update_where_numcol' : 'Number of columns',
        'sqlite3_row_update_where_data' : 'Data',
        'sqlite3_row_update_where_val' : 'Values',
        'sqlite3_row_update_where_numval' : 'Number of Values',
        'sqlite3_row_update_where_id' : 'Row ID',
        'sqlite3_row_update_where_ready' : 'Updated a row of a SQLite table.',
        'sqlite3_row_update_where_smnt' : 'Statement',
        'sqlite3_row_update_where_tbl_nex' : 'The table does not exist.',
        'sqlite3_row_update_where_mismatch' : 'The number of columns does not match the number of values handed to the function.',

        # mpy_mp.py - cl_orchestrator._init(~)
        'cl_orchestrator_init_not_bool' : 'Value is not a boolean. Check mpy_conf.py for correction.',
        'cl_orchestrator_init_not_int' : 'Value is not an integer. Check mpy_conf.py for correction.',
        'cl_orchestrator_init_not_float' : 'Value is not a float. Check mpy_conf.py for correction.',
        'cl_orchestrator_init_not_str' : 'Value is not a string. Check mpy_conf.py for correction.',
        'cl_orchestrator_init_rel_math_corr' : 'Rounding corrected.',
        'cl_orchestrator_init_cpus_determined' : 'Maximum amount of parallel processes determined.',
        'cl_orchestrator_init_memory_set' : 'Maximum memory set.',
        'cl_orchestrator_init_done' : 'Multiprocessing initialized.',

        # mpy_mp.py - cl_orchestrator._run(~)
        'cl_orchestrator_run_app_start': 'App starting.',

        # mpy_mp.py - join_processes(~)
        'join_processes_start': 'Joining processes',

        # mpy_mp.py - watcher(~)
        'watcher_is_alive': 'Process Watcher: Process still alive.',
        'watcher_end': 'Process Watcher: Process ended, cleaning up process',

        # mpy_decorators.py - run_parallel(~)
        'run_parallel_task' : 'Task',
        'run_parallel_task_sys_id' : 'Task ID',
        'run_parallel_start' : 'Parallel process starting. ID',
        'run_parallel_exit' : 'Parallel process created. ID',
        'run_parallel_call_err' : 'Task provided is not callable.',
        'run_parallel_id_abort' : 'Could not get process ID. Task was enqueued again.',
        'run_parallel_issues' : 'Issues encountered:',
        'run_parallel_id_err_avl' : 'Process ID conflict. Possible concurrent process creation. Process creation skipped.',
        'run_parallel_id_err_busy' : 'Process ID conflict. ID# seemed available, is busy. Process creation skipped.',
        'run_parallel_id_err_dict' : 'Process ID conflict. A process may have terminated dirty. Process creation skipped.',
        'run_parallel_requeue_err' : 'Task could not be enqueued again. Task ID still in queue. Data loss possible.',
        'run_parallel_proc_busy' : 'Processes busy',
        'run_parallel_proc_avl' : 'Processes available',
        'run_parallel_start_w_arg' : 'Starting process control with arguments',
        'run_parallel_search_p_id' : 'Searching for available process ID.',
        'run_parallel_search_iter_end' : 'Process ID determined.',
        'run_parallel_clean_up_remnants' : 'Process remnant found.Cleaning up after supposed process crash.',

        # mpy_mt.py - cl_thread.__init__(~)
        'cl_thread_init_start' : 'A worker thread is being created.',
        'cl_thread_init_done' : 'Worker thread created. ID reserved.',
        'cl_thread_lock' : 'Thread lock',
        'cl_thread_name' : 'Name',
        'cl_thread_prio' : 'Priority',
        'cl_thread_id' : 'Identifier',
        'cl_thread_counter' : 'Counter',

        # mpy_mt.py - cl_thread.run(~)
        'cl_thread_run_start' : 'A task is starting. Thread has been locked.',
        'cl_thread_run_task' : 'Task',
        'cl_thread_run_task_id' : 'Task identifier',
        'cl_thread_run_task_fetched' : 'Fetched a new task. Thread renamed with the task name.',
        'cl_thread_run_tasks_total' : 'Total tasks initiated',
        'cl_thread_run_modules' : 'Modules were imported.',
        'cl_thread_run_nomodules' : 'No modules had to get imported.',
        'cl_thread_run_end' : 'Task ended.',

        # mpy_mt.py - prio_correction(~)
        'prio_correction_warn' : 'The priority of a task has been corrected.',
        'prio_correction_prio_in' : 'Initial priority',
        'prio_correction_prio_out' : 'Corrected priority',
        'prio_correction_err' : 'The priority of a morPy-task has been corrected.',

        # mpy_mt.py - mpy_mt_abort(~)
        'mpy_mt_abort_start' : 'Aborting threaded execution of tasks. Continuing main thread.',

        # mpy_mt.py - thread_imports(~)
        'thread_imports_start' : 'Task split to identify module imports.',
        'thread_imports_yes' : 'The calling thread imported a module.',
        'thread_imports_no' : 'No module got imported by the calling thread.',

        # mpy_mt.py - mit_init(~)
        'mt_init_done' : 'Multithreading initialized.',
        'mt_init_enabled_yes' : 'Multithreading enabled.',
        'mt_init_enabled_no' : 'Multithreading disabled. Fallback to single threaded mode.',
        'mt_init_thr_available' : 'Threads available',
        'mt_init_thr_max' : 'Maximum threads configured',

        # mpy_mt.py - thread_id(~)
        'thread_id_init' : 'Reserving an ID for a new thread/task.',
        'thread_id_done' : 'Reserved an ID for a new thread/task.',
        'thread_id_err' : 'Overflow in thread ID list. ID exceeds maximum threads utilized.',

        # mpy_mt.py - mpy_thread_queue(~)
        'mpy_thread_queue_enqueue' : 'Enqueing task.',
        'mpy_thread_queue_dbg_enqueue_done' : 'Task successfully enqueued. Thread created.',
        'mpy_thread_queue_dbg_thread_skip' : 'No free thread available. Skipping thread invoke.',
        'mpy_thread_queue_dbg_enq_new_done' : 'New Thread ID list created. Task successfully enqueued.',
        'mpy_thread_queue_task' : 'Task',
        'mpy_thread_queue_priority' : 'Priority',
        'cl_priority_queue_enqueue_id_conflict' : 'Task not enqueued. Task ID mismatch or conflict.',
        'cl_priority_queue_enqueue_task_duplicate' : 'Task is already enqueued. Referencing in queue.',
        'mpy_thread_queue_enqueue_err' : 'Enqueing failed.',
        'mpy_thread_queue_dbg_threads_available' : 'Checking threads availability.',
        'mpy_thread_queue_dbg_threads_used' : 'Threads in use',
        'mpy_thread_queue_dbg_threads_max' : 'Threads total',
        'mpy_thread_queue_thread_err' : 'A new thread could not be initiated.',

        # mpy_mt.py - mpy_threads_joinall(~)
        'mpy_threads_joinall_start' : 'Waiting for all threads to finish up their work.',
        'mpy_threads_joinall_eval' : 'Threads running',
        'mpy_threads_joinall_end' : 'All threads/tasks finished.',

        # mpy_bulk_ops.py - find_replace_saveas(~)
        'find_replace_saveas_start' : 'Operation start.',
        'find_replace_saveas_f_ex_skip' : 'File already exists. Operation skipped.',
        'find_replace_saveas_tpl_err' : 'Wrong type. Input must be a tuple of tuples.',

        # morPy specific area - END
    }

    return loc_mpy_dict

def loc_mpy_dbg() -> dict:

    r"""
    This dictionary defines all messages for morPy core functions debugging localized to a
    specific language.

    :param:
        -

    :return: dict
        loc_mpy_dbg_dict: Localization dictionary for morPy unit tests. All keys
            will be copied to app_dict during unit testing instead of morPy
            initialization.

    :example:
        app_dict["loc"]["dbg"][KEY]
    """

    loc_mpy_dbg_dict = {

        # Debug specific area - BEGIN

        # debug.py - dbg_mpy_param(~)
        'dbg_mpy_param_start' : 'Start debugging of the mpy_param.py module.',
        'dbg_mpy_param_end' : 'Debugging of mpy_param.py finished.',

        # debug.py - dbg_mpy_mt(~)
        'dbg_mpy_mt_start' : 'Start debugging of the mpy_mt.py module.',
        'dbg_mpy_mt_next' : 'Starting a parallel prioritized task.',
        'dbg_mpy_mt_name' : 'Name',
        'dbg_mpy_mt_priority' : 'Priority',
        'dbg_mpy_mt_task' : 'Task',
        'dbg_mpy_mt_end' : 'Debugging of mpy_mt.py finished.',

        # debug.py - dbg_mpy_fct(~)
        'dbg_mpy_fct_start' : 'Start debugging of the mpy_fct.py module.',
        'dbg_mpy_fct_end' : 'Debugging of mpy_fct.py finished.',

        # debug.py - dbg_mpy_msg(~)
        'dbg_mpy_msg_start' : 'Start debugging of the mpy_msg.py module.',
        'dbg_mpy_msg_interrupt' : 'Simple Test of the interrupt functionality.',
        'dbg_mpy_msg_end' : 'Debugging of mpy_msg.py finished.',

        # debug.py - dbg_mpy_common(~)
        'dbg_mpy_common_start' : 'Start debugging of the mpy_common.py module.',
        'dbg_mpy_common_end' : 'Debugging of mpy_common.py finished.',

        # debug.py - dbg_mpy_ui_tk(~)
        'dbg_mpy_ui_tk_start' : 'Start debugging of the mpy_ui_tk.py module.',
        'dbg_mpy_ui_tk_end' : 'Debugging of mpy_ui_tk.py finished.',

        # debug.py - dbg_mpy_sqlite3(~)
        'dbg_mpy_sqlite3_start' : 'Start debugging of the mpy_sqlite3.py module.',
        'dbg_mpy_sqlite3_end' : 'Debugging of mpy_sqlite3.py finished.',

        # debug.py - dbg_mpy_xl(~)
        'dbg_mpy_xl_start' : 'Start debugging of the mpy_xl.py module.',
        'dbg_mpy_xl_end' : 'Debugging of mpy_xl.py finished.',

        # debug.py - dbg_mpy_wscraper(~)
        'dbg_mpy_wscraper_start' : 'Start debugging of the mpy_wscraper.py module.',
        'dbg_mpy_wscraper_end' : 'Debugging of mpy_wscraper.py finished.',

        # debug.py - dummy_process_list_append(~)
        'dummy_process_list_append_start' : 'Start appending to a list. Simple benchmark.\nItems total',
        'dummy_process_list_append_dict_conn' : 'Testing global dictionary connection. This number is supposed to always increment by 1.',
        'dummy_process_list_append_items' : 'Items appended',
        'dummy_process_list_append_progress' : 'Progress',
        'dummy_process_list_append_end' : 'Finished appending to a list.',

        # debug.py - dummy_process_math(~)
        'dummy_process_math_start' : 'Start simple math benchmark.\nComplexity',
        'dummy_process_math_end' : 'Finished simple math benchmark.',

        # mpy_dbg.py - mpy_ut_call_test_op(~)
        'mpy_ut_call_start' : 'START unit test of:',
        'mpy_ut_call_pass' : 'PASSED:',
        'mpy_ut_call_fail' : 'FAILED:',

        # App specific area - END
    }

    return loc_mpy_dbg_dict

def loc_app() -> dict:

    r"""
    This dictionary defines all messages for app functions localized to a
    specific language.

    :param:
        -

    :return: dict
        loc_app_dict: Localization dictionary for app functions. All keys
            will be copied to app_dict during morPy initialization.

    :example:
        app_dict["loc"]["app"][KEY]
    """

    loc_app_dict = {

        # App specific area - BEGIN

        # App specific area - END
    }

    return loc_app_dict

def loc_app_dbg() -> dict:

    r"""
    This dictionary defines all messages for debugging app functions localized to a
    specific language.

    :param:
        -

    :return: dict
        loc_app_dbg_dict: Localization dictionary for app functions. All keys
            will be copied to app_dict during morPy initialization.

    :example:
        app_dict["loc"]["app"][KEY]
    """

    loc_app_dbg_dict = {

        # App specific area - BEGIN

        # App specific area - END
    }

    return loc_app_dbg_dict