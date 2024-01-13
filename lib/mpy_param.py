"""
Author:     Bastian Neuwirth
Date:       15.03.2022
Version:    0.1
Descr.:     This module yields all basic parameters of the morPy fork. The
            parameters are meant to be tempered with.
"""

def parameters(param_dict):

    import pathlib, os

    """ This function defines the paramaters to be initialized. These
        parameters are meant to be tinkered with and added on to. Have in mind,
        that the return dictionary eventually needs to be altered. The
        morPy framework is preconfigured to support the change of these parameters
        during runtime, although that may be done within prj_dict directly.
    :param
        param_dict - Dictionary object to hand initialized variables to parameters(~)
    :return - dictionary
        language - Defines the localized dictionary to be initialized by referencing
                   the related language with two capital letters, e.g. en_US.
        mpy_priv_required - Defines wether elevated privileges are required.
                        If required, the privileges will be tested and __main__ will be
                        restarted.
        mpy_ref_create - Store the initialized project dictionary in the
                      main path of the project ...\mpy_reference.txt except localization.
        mpy_print_init_vars - Print the initialized project dictionary to console.
        mpy_log_db_enable - Enable logging to a database (for the path see log_db_path).
        mpy_log_txt_enable - Enable logging to a textfile (for the path see log_txt_path).
        mpy_log_txt_header_enable - Enable the prepared header for the logging textfile.
        path_divider - System specific character or string used to
                       divide folders in a path.
        prj_path - Path to the project folder.
        log_path - Path to the logfile folder.
        log_db_path - Path to the database holding all logs.
        log_txt_path - Path to the textfile holding all logs.
        modules_path - Path to the modules folder.
        main_db_path - Path to the main database of the project.

    #TODO
    update return parameters in description
    """

    """
>>> LOCALIZATION <<<
    """

#   Choose the language of the project (See ...\loc\ for available dictionaries).
#   Called by mpy_init.init(~)
    language = 'en_US'

    """
>>> PRIVILEGES <<<
    """

#   Defines, wether elevated privileges are required.
#   Called by mpy_init.init(~)
    mpy_priv_required = True

    """
>>> LOGGING & DEBUGGING <<<
    """

#   Enable logging. If mpy_log_db_enable and mpy_log_txt_enable both are set false,
#   then log_enable will be overwritten to be False in mpy_init.init(~). Log messages
#   may still be printed to console.
#   Called by mpy_init.init(~)
    mpy_log_enable = True

#   Store the initialized system parameters relevant to a developer in a text file.
#   Called by mpy_init.mpy_ref(~)
    mpy_ref_create = False

#   Enable logging to database.
#   Called by mpy_msg.log(~)
    mpy_log_db_enable = True

#   Enable logging to a textfile.
#   Called by mpy_msg.log(~)
    mpy_log_txt_enable = False

#   Enable the prepared header for the logging textfile.
#   Called by mpy_init.init(~)
    mpy_log_txt_header_enable = mpy_log_txt_enable

#   Enable printouts of logs to console. This option works, even if log_enable is false.
#   Called throughout mpy_msg operations.
    mpy_msg_print = True

#   Print the initialized project dictionary to console.
#   Called by mpy_init.init(~)
    mpy_print_init_vars = True

#   List object to exclude certain log levels from being logged to DB or text file.
#   These log levels may still be printed to console.
#   Called throughout mpy_msg operations.
#   All log levels: ["INIT", "DEBUG", "INFO", "WARNING", "DENIED", "ERROR", "CRITICAL", "EXIT", "UNDEFINED]
#   Default: ["DEBUG"]
    mpy_log_lvl_nolog = []

#   List object to exclude certain log levels from being printed to ui or console.
#   These log levels may still be logged to DB or text file.
#   Called by mpy_msg.mpy_msg_print(~)
#   All log levels: ["INIT", "DEBUG", "INFO", "WARNING", "DENIED", "ERROR", "CRITICAL", "EXIT", "UNDEFINED]
    mpy_log_lvl_noprint = ["DEBUG"]

#   List object to have certain log levels raise an interrupt. This will also freeze
#   running threads and processes and eventually abort the program (depending on
#   further implementation of UI). An interrupt is only raised, if mpy_msg_print
#   or mpy_log_enable is true. If an item is part of this list, it will override being
#   part of the list mpy_log_lvl_nolog.
#   Called by mpy_msg.mpy_msg_print(~)
#   All log levels: ["INIT", "DEBUG", "INFO", "WARNING", "DENIED", "ERROR", "CRITICAL", "EXIT", "UNDEFINED]
    mpy_log_lvl_interrupts = ["DENIED","ERROR","CRITICAL"]

    """
>>> MULTITHREADING <<<
    """

#   Enable or disable multthreading. Have in mind, that during initialization
#   the available threads will be determined and this option may be overwritten
#   if there is only a single thread available.
    mt_enabled = True

#   Select how the maximum threads will be determined. If true, you must set
#   an integer value greater than 1 for mt_max_threads_cnt_abs. Ultimately,
#   if the relative determination is chosen, an absolute maximum thread count
#   will be determined during initialization and mt_max_threads will
#   always be adressed after initialization.
    mt_max_threads_set_abs = True

#   Set the absolute maximum amount of threads which shall be utilized. This needs
#   mt_max_threads_set_abs = True in order to have any effect. Have in mind, that
#   your project still needs to utilize these threads by keeping enough tasks in
#   the priority queue.
    mt_max_threads_cnt_abs = 2

#   Set the relative maximum amount of threads which shall be utilized, where
#   1 resembles 100% utilization and 0 resembles 0% utilization. This needs
#   mt_max_threads_set_abs = False in order to have any effect. Have in mind, that
#   your project still needs to utilize these threads by keeping enough tasks in
#   the priority queue.
    mt_max_threads_cnt_rel = 1.0

#   If the relative determination of maximum threads is enabled, it is necessary
#   to set whether the maximum thread count should be rounded up or down, since
#   not in every case the result will be an integer value.
    mt_max_threads_rel_floor = False

    """
>>> PATHS <<<
    """

#   System specific character or string used to divide folders in a path
    path_divider = os.sep

#   Path to the project folder
    prj_path = pathlib.Path(__file__).parent.parent.resolve()

#   Path to the logfile folder
    log_path = pathlib.Path(os.path.join(f'{prj_path}', 'log'))

#   Path to the database holding all logs.
    log_db_path = pathlib.Path(os.path.join(f'{prj_path}', 'log', 'log.db'))

#   Path to the textfile holding all logs
    log_txt_path = os.path.join(f'{log_path}', f'{param_dict["temp_datetime"]}.log')

#   Path to the modules folder
    prjFiles_path = pathlib.Path(__file__).parent.parent.parent.resolve()

#   Path to the main database of the project
    main_db_path = pathlib.Path(os.path.join(f'{prj_path}', 'db', 'main.db'))

    return{
        'language' : language, \
        'localization' : f'mpy_{language}', \
        'mpy_priv_required' : mpy_priv_required, \
        'mpy_log_enable' : mpy_log_enable, \
        'mpy_ref_create' : mpy_ref_create, \
        'mpy_log_db_enable' : mpy_log_db_enable, \
        'mpy_log_txt_enable' : mpy_log_txt_enable, \
        'mpy_log_txt_header_enable' : mpy_log_txt_header_enable, \
        'mpy_msg_print' : mpy_msg_print, \
        'mpy_print_init_vars' : mpy_print_init_vars, \
        'mpy_log_lvl_nolog' : mpy_log_lvl_nolog, \
        'mpy_log_lvl_noprint' : mpy_log_lvl_noprint, \
        'mpy_log_lvl_interrupts' : mpy_log_lvl_interrupts, \
        'mt_enabled' : mt_enabled, \
        'mt_max_threads_set_abs' : mt_max_threads_set_abs, \
        'mt_max_threads_cnt_abs' : mt_max_threads_cnt_abs, \
        'mt_max_threads_cnt_rel' : mt_max_threads_cnt_rel, \
        'mt_max_threads_rel_floor' : mt_max_threads_rel_floor, \
        'path_divider' : f'{path_divider}', \
        'prj_path' : prj_path, \
        'log_path' : log_path, \
        'log_db_path' : log_db_path, \
        'log_txt_path' : log_txt_path, \
        'prjFiles_path' : prjFiles_path, \
        'main_db_path' : main_db_path, \
    }