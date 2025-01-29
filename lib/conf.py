r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields all basic parameters of the morPy fork. The
            parameters are meant to be tempered with.

TODO remake paramters() as settings() and provide as json
"""

def parameters(start_time=None):

    import pathlib, os

    r""" This function defines the paramaters to be initialized. These
        parameters are meant to be tinkered with and added on to. Have in mind,
        that the return dictionary eventually needs to be altered. The
        morPy framework is preconfigured to support the change of these parameters
        during runtime, although that may be done within app_dict directly, rather
        than initializing the parameters again. There are exceptions though, which
        are pointed out with ">REINITIALIZE<", as an indicator, that the JSON file
        containing all parameters needs to be updated before a change can have an
        effect. To do so, simply execute param_to_json(~) after altering the
        parameters in app_dict like so:
            app_dict["conf"]['my_param'] = 'my_value'
            param_to_json(morPy_trace, app_dict)
    :param
        start_time - Datetime stamp of runtime start
    :return - dictionary
        language - Defines the localized dictionary to be initialized by referencing
                   the related language with two capital letters, e.g. en_US.
        mpy_priv_required - Defines wether elevated privileges are required.
                        If required, the privileges will be tested and __main__ will be
                        restarted.
        mpy_ref_create - Store the initialized app dictionary in the
                      main path of the app ...\init_dict.txt except localization.
        mpy_print_init_vars - Print the initialized app dictionary to console.
        mpy_log_db_enable - Enable logging to a database (for the path see log_db_path).
        mpy_log_txt_enable - Enable logging to a textfile (for the path see log_txt_path).
        mpy_log_txt_header_enable - Enable the prepared header for the logging textfile.
        path_divider - System specific character or string used to
                       divide folders in a path.
        main_path - Path to the app folder.
        log_path - Path to the logfile folder.
        log_db_path - Path to the database holding all logs.
        log_txt_path - Path to the textfile holding all logs.
        modules_path - Path to the modules folder.
        main_db_path - Path to the main database of the app.

    TODO update return parameters in description
    TODO change variable names and remove "morPy" from it (dict nesting circumvents name collisions)
    """

    r"""
>>> LOCALIZATION <<<
    """

    # Choose the language of the app (See ...\loc\ for available dictionaries).
    # Called by: init.init(~)
    language = 'en_US'

    r"""
>>> PRIVILEGES <<<
    """

    # Defines, wether elevated privileges are required.
    # Called by: init.init(~)
    mpy_priv_required = False

    r"""
>>> LOGGING & DEBUGGING <<<
    Log Levels: init, debug, info, warning, denied, error, critical, exit, undefined
    """

    # Enable logging. If mpy_log_db_enable and mpy_log_txt_enable both are set false,
    # then log_enable will be overwritten to be False in init.init(~). Log messages
    # may still be printed to console.
    # Called by: init.init(~)
    mpy_log_enable = True

    # Store the initialized system parameters relevant to a developer in a text file.
    # This is for checking initialized app_dict prior to app execution.
    # Called by: init.mpy_ref(~)
    mpy_ref_create = False

    # Enable logging to database.
    # Called by: msg.log(~)
    mpy_log_db_enable = True

    # Enable logging to a textfile.
    # Called by: msg.log(~)
    mpy_log_txt_enable = False

    # Enable the prepared header for the logging textfile.
    # Called by: init.init(~)
    mpy_log_txt_header_enable = mpy_log_txt_enable

    # Enable printouts of logs to console. This option works, even if log_enable is false.
    # Called by: throughout msg operations
    msg_print = True

    # Set the messages to verbose. THis means, that the full logg message will contain technical
    # data helpful for tracing and context. This option comes with additional storage requirement
    # for logging. If logging to db is activated, there is no need for this option, as all
    # relevant data is stored in the db. When logging to textfile, verbose messages are the only way
    # to get a detailed context of a log message.
    msg_verbose = True

    # Print the initialized app dictionary to console.
    # Called by: init.init(~)
    mpy_print_init_vars = False

    # List object to exclude certain log levels from being logged to DB or text file.
    # These log levels may still be printed to console.
    # Called by: throughout msg operations
    # Default: ["debug"]
    mpy_log_lvl_nolog = ["debug"]

    # List object to exclude certain log levels from being printed to ui or console.
    # These log levels may still be logged to DB or text file.
    # Called by: msg.msg_print(~)
    # Default: ["debug"]
    mpy_log_lvl_noprint = ["debug", "warning"]

    # List object to have certain log levels raise an interrupt. This will also freeze
    # running threads and processes and eventually abort the program (depending on
    # further implementation of UI). An interrupt is only raised, if msg_print
    # or mpy_log_enable is true. If an item is part of this list, it will override being
    # part of the list mpy_log_lvl_nolog.
    # Called by: msg.msg_print(~)
    # Default: ["denied","error","critical"]
    mpy_log_lvl_interrupts = ["denied","error","critical"]

    r"""
>>> METRICS <<<
    """

    # Turn on metrics for the code executed.
    # Data collected: function name, trace, runtime, start time, end time, process ID, task ID
    # >REINITIALIZE<
    metrics_enable = True

    # Perform metrics gathering in performance mode.
    # Data collected: function name, trace, runtime
    # >REINITIALIZE<
    metrics_perfmode = False

    r"""
>>> MEMORY <<<
    TODO
    """

    # Select the way, how the available RAM is determined. If absolute, an integer
    # value will reflect the Megabytes of maximum memory.
    # Default: False or None
    memory_count_absolute = False

    # Absolute amount of RAM to be utilized. This value will by default not exceed
    # the memory available on the system. If None, all RAM can be utilized.
    # Default: None
    memory_absolute = None

    # Set the relative maximum amount of RAM to be utilized, where 1 resembles 100%
    # utilization and 0 resembles 0% utilization. If None, all RAM can be utilized.
    # Default: None or 1.0
    memory_relative = None

    # Set the Minimum amount of memory in MB, that app_dict has to have reserved.
    # Default: None or 200
    memory_min_MB = None

    r"""
>>> MULTI-PROCESSING <<<
    """

    # Select the way, how the available CPUs are determined. If absolute, an integer
    # value will reflect the maximum number of logical cores to utilize in parallel.
    # Default: False or None
    processes_count_absolute = True

    # Absolute amount of processes to run parallel. This value will by default not exceed
    # the logical cores available on the system. If None, all CPUs can be utilized.
    # Default: None
    processes_absolute = 1

    # Set the relative maximum amount of processes to be utilized, where 1 resembles 100%
    # utilization and 0 resembles 0% utilization. If None, all CPUs can be utilized.
    # Default: None or 1.0
    processes_relative = None

    # If the relative determination of maximum processes is used, it is necessary
    # to set how the maximum thread count should be rounded in case process_relative
    # does not reflect an integer cpu count. Allowed is "round" (default), "floor" or
    # "ceil".
    processes_relative_math = "round"

    r"""
>>> MULTITHREADING <<<
    """

    # Enable or disable multthreading. Have in mind, that during initialization
    # the available threads will be determined and this option may be overwritten
    # if there is only a single thread available.
    mt_enabled = True

    # Select how the maximum threads will be determined. If true, you must set
    # an integer value greater than 1 for mt_max_threads_cnt_abs. Ultimately,
    # if the relative determination is chosen, an absolute maximum thread count
    # will be determined during initialization and mt_max_threads will
    # always be addressed after initialization.
    mt_max_threads_set_abs = True

    # Set the absolute maximum amount of threads which shall be utilized. This needs
    # mt_max_threads_set_abs = True in order to have any effect. Have in mind, that
    # your app still needs to utilize these threads by keeping enough tasks in
    # the priority queue.
    mt_max_threads_cnt_abs = 1

    # Set the relative maximum amount of threads which shall be utilized, where
    # 1 resembles 100% utilization and 0 resembles 0% utilization. This needs
    # mt_max_threads_set_abs = False in order to have any effect. Have in mind, that
    # your app still needs to utilize these threads by keeping enough tasks in
    # the priority queue.
    mt_max_threads_cnt_rel = 1.0

    # If the relative determination of maximum threads is enabled, it is necessary
    # to set whether the maximum thread count should be rounded up or down, since
    # not in every case the result will be an integer value.
    mt_max_threads_rel_floor = False

    r"""
>>> PATHS <<<
    """

    # Path to the app folder
    main_path = pathlib.Path(__file__).parent.parent.resolve()

    # Path to the logfile folder
    log_path = pathlib.Path(os.path.join(f'{main_path}', 'log'))
    # Create the path, if not existing.
    os.makedirs(log_path, exist_ok=True)

    # Path to the database holding all logs.
    log_db_path = pathlib.Path(os.path.join(f'{main_path}', 'log', 'log.db'))

    # Path to the textfile holding all logs
    log_txt_path = os.path.join(f'{log_path}', f'{start_time}.log')

    # Path to the modules folder
    app_files_path = pathlib.Path(os.path.join(f'{main_path}', 'data'))
    # Create the path, if not existing.
    os.makedirs(app_files_path, exist_ok=True)

    # Path to the main database of the app
    main_db_path = pathlib.Path(os.path.join(f'{main_path}', 'db', 'main.db'))

    # Path to the developed app
    app_path = pathlib.Path(os.path.join(f'{main_path}', 'app'))
    # Create the path, if not existing.
    os.makedirs(app_path, exist_ok=True)

    # Set the app icon
    app_icon = pathlib.Path(os.path.join(f'{main_path}', 'res', 'icons', 'smph.ico'))

    # Set the GUI background
    app_banner = pathlib.Path(os.path.join(f'{main_path}', 'res', 'banners', 'smph.png'))

    return{
        'language' : language,
        'localization' : f'morPy_{language}',
        'priv_required' : mpy_priv_required,
        'log_enable' : mpy_log_enable,
        'ref_create' : mpy_ref_create,
        'log_db_enable' : mpy_log_db_enable,
        'log_txt_enable' : mpy_log_txt_enable,
        'log_txt_header_enable' : mpy_log_txt_header_enable,
        'msg_print' : msg_print,
        'msg_verbose' : msg_verbose,
        'print_init_vars' : mpy_print_init_vars,
        'log_lvl_nolog' : mpy_log_lvl_nolog,
        'log_lvl_noprint' : mpy_log_lvl_noprint,
        'log_lvl_interrupts' : mpy_log_lvl_interrupts,
        'metrics_enable' : metrics_enable,
        'metrics_perfmode' : metrics_perfmode,
        'memory_count_absolute' : memory_count_absolute,
        'memory_absolute' : memory_absolute,
        'memory_relative' : memory_relative,
        'memory_min_MB' : memory_min_MB,
        'processes_count_absolute' : processes_count_absolute,
        'processes_absolute' : processes_absolute,
        'processes_relative' : processes_relative,
        'processes_relative_math' : processes_relative_math,
        'mt_enabled' : mt_enabled,
        'mt_max_threads_set_abs' : mt_max_threads_set_abs,
        'mt_max_threads_cnt_abs' : mt_max_threads_cnt_abs,
        'mt_max_threads_cnt_rel' : mt_max_threads_cnt_rel,
        'mt_max_threads_rel_floor' : mt_max_threads_rel_floor,
        'main_path' : main_path,
        'log_path' : log_path,
        'log_db_path' : log_db_path,
        'log_txt_path' : log_txt_path,
        'app_files_path' : app_files_path,
        'main_db_path' : main_db_path,
        'app_path' : app_path,
        'app_icon' : app_icon,
        'app_banner' : app_banner,
    }