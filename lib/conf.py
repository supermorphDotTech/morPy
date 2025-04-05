r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Initialization parameters for the morPy framework.
"""

def settings(start_time=None):
    r"""
    Initialization parameters for the morPy framework. These settings are
    not meant to be tempered with during runtime.

    :param start_time: Datetime stamp of runtime start. Defaults to None.

    :return: dict
        > See through the function for detailed descriptions of every morPy setting.
    """

    import pathlib, os

    r"""
>>> LOCALIZATION <<<
    """

    # Choose the language of the app (See ...\loc\ for available dictionaries).
    # Called by: init.init(~)
    language: str = 'en_US'

    r"""
>>> PRIVILEGES <<<
    """

    # Defines, whether elevated privileges are required.
    # Called by: 
    run_elevated: bool = False

    r"""
>>> LOGGING & DEBUGGING <<<
    Log Levels: init, debug, info, warning, denied, error, critical, exit, undefined
    """

    # Enable logging. If log_db_enable and log_txt_enable both are set false,
    # then log_enable will be overwritten to be False in init.init(~). Log messages
    # may still be printed to console.
    # Called by: init.init(~)
    log_enable: bool = True

    # Store the initialized system parameters relevant to a developer in a text file.
    # This is for checking initialized app_dict prior to app execution.
    # Called by: init.mpy_ref(~)
    ref_create: bool = False

    # Enable logging to database.
    # Called by: msg.log(~)
    log_db_enable: bool = True

    # Enable logging to a textfile.
    # Called by: msg.log(~)
    log_txt_enable: bool = False

    # Enable the prepared header for the logging textfile.
    # Called by: init.init(~)
    log_txt_header_enable = log_txt_enable

    # Enable printouts of logs to console. This option works, even if log_enable is false.
    # Called by: throughout msg operations
    msg_print: bool = True

    # Activate verbose logging/printing. This means, that the full log message will contain technical
    # data helpful for tracing and context. This option comes with additional storage requirement
    # for logging. If logging to db is activated, there is no need for this option, as all
    # relevant data is stored in the db. When logging to textfile, verbose messages are the only way
    # to get a detailed context of a log message.
    msg_verbose: bool = True

    # Print the initialized app dictionary to console.
    # Called by: init.init(~)
    print_init_vars: bool = False

    # List object to exclude certain log levels from being logged to DB or text file.
    # These log levels may still be printed to console.
    # Called by: throughout msg operations
    # Default: ["debug"]
    log_lvl_nolog: list = []

    # List object to exclude certain log levels from being printed to ui or console.
    # These log levels may still be logged to DB or text file.
    # Called by: msg.msg_print(~)
    # Default: ["debug"]
    log_lvl_noprint: list = ["debug", "warning"]

    # List object to have certain log levels raise an interrupt. This will also freeze
    # running threads and processes and eventually abort the program (depending on
    # further implementation of UI). An interrupt is only raised, if msg_print
    # or log_enable is true. If an item is part of this list, it will override being
    # part of the list log_lvl_nolog.
    # Called by: msg.msg_print(~)
    # Default: ["denied","error","critical"]
    log_lvl_interrupts: list = ["denied","error","critical"]

    r"""
>>> METRICS <<<
    """

    # Turn on metrics for the code executed.
    # Data collected: function name, trace, runtime, start time, end time, process ID, task ID
    metrics_enable: bool = False

    # Perform metrics gathering in performance mode.
    # Data collected: function name, trace, runtime
    metrics_perfmode: bool = False

    r"""
>>> MEMORY <<<
    TODO implement memory management with UltraDict
    
    These settings only take effect in a multiprocessing context. With these settings
    memory can be claimed at initialization to prevent later memory buffer increases.
    In case of performance issues, memory may be increased.
    """

    # Select the way, how the available RAM is determined. If absolute, an integer
    # value will reflect the Megabytes of maximum memory. Otherwise, use relative.
    # Default: False or None
    memory_use_absolute: bool = False

    # Absolute amount of memory in MB. If None, all RAM can be utilized.
    # Default: None
    memory_absolute_mb: int = None

    # Set the relative amount of memory to be reserved, where 1 resembles 100%
    # of system memory and 0 resembles 0%. If None, automatically determined.
    # Default: None or 1.0
    memory_relative: float = None

    # Set the Minimum amount of memory in MB to be reserved at startup. If this threshold
    # can not be met, app will exit.
    # Default: None or 100
    memory_min_mb: int = None

    r"""
>>> MULTI-PROCESSING <<<
    """

    # Select the way, how the available CPUs are determined. If absolute, an integer
    # value will reflect the maximum number of logical cores to utilize in parallel.
    # Default: False or None
    processes_count_absolute: bool = False

    # Absolute amount of processes to run parallel. This value will by default not exceed
    # the logical cores available on the system. If None, all CPUs can be utilized.
    # Default: None
    processes_absolute: int = 1

    # Set the relative maximum amount of processes to be utilized, where 1 resembles 100%
    # utilization and 0 resembles 0% utilization. If None, all CPUs can be utilized.
    # Default: None or 1.0
    processes_relative: float = 0.92

    # If the relative determination of maximum processes is used, it is necessary
    # to set how the maximum thread count should be rounded in case process_relative
    # does not reflect an integer cpu count. Allowed is "round" (default), "floor" or
    # "ceil".
    processes_relative_math: str = "floor"

    r"""
>>> PATHS <<<
    """

    # Path to the app folder
    main_path = pathlib.Path(__file__).parent.parent.resolve()

    # Path to the logfile folder
    log_path = pathlib.Path(os.path.join(f'{main_path}', 'log'))
    # Create the path, if not existing.
    os.makedirs(log_path, exist_ok=True)

    # Path to the logging database.
    log_db_path = pathlib.Path(os.path.join(f'{log_path}', 'log.db'))

    # Path to the logging textfile.
    log_txt_path = os.path.join(f'{log_path}', f'{start_time}.log')

    # Path to the data folder
    data_path = pathlib.Path(os.path.join(f'{main_path}', 'data'))
    # Create the path, if not existing.
    os.makedirs(data_path, exist_ok=True)

    # Path to the main database of the app
    main_db_path = pathlib.Path(os.path.join(f'{main_path}', 'db', 'main.db'))

    # Path to the developed app
    app_path = pathlib.Path(os.path.join(f'{main_path}', 'app'))
    # Create the path, if not existing.
    os.makedirs(app_path, exist_ok=True)

    # Set the app icon (must be .ico)
    app_icon = pathlib.Path(os.path.join(f'{main_path}', 'res', 'icons', 'smph.ico'))

    # Set a GUI banner
    app_banner = pathlib.Path(os.path.join(f'{main_path}', 'res', 'banners', 'supermorph.png'))

    return{
        'language' : language,
        'localization' : f'loc.morPy_{language}',
        'run_elevated' : run_elevated,
        'log_enable' : log_enable,
        'ref_create' : ref_create,
        'log_db_enable' : log_db_enable,
        'log_txt_enable' : log_txt_enable,
        'log_txt_header_enable' : log_txt_header_enable,
        'msg_print' : msg_print,
        'msg_verbose' : msg_verbose,
        'print_init_vars' : print_init_vars,
        'log_lvl_nolog' : log_lvl_nolog,
        'log_lvl_noprint' : log_lvl_noprint,
        'log_lvl_interrupts' : log_lvl_interrupts,
        'metrics_enable' : metrics_enable,
        'metrics_perfmode' : metrics_perfmode,
        'memory_use_absolute' : memory_use_absolute,
        'memory_relative' : memory_relative,
        'memory_absolute' : memory_absolute_mb,
        'memory_min_mb' : memory_min_mb,
        'processes_count_absolute' : processes_count_absolute,
        'processes_absolute' : processes_absolute,
        'processes_relative' : processes_relative,
        'processes_relative_math' : processes_relative_math,
        'main_path' : main_path,
        'log_path' : log_path,
        'log_db_path' : log_db_path,
        'log_txt_path' : log_txt_path,
        'data_path' : data_path,
        'main_db_path' : main_db_path,
        'app_path' : app_path,
        'app_icon' : app_icon,
        'app_banner' : app_banner,
    }