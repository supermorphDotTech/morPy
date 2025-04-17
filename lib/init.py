r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Initialization of the morPy framework.
"""

import lib.fct as morpy_fct
import config
from morPy import log
from lib.decorators import core_wrap
from lib.common import textfile_write
from lib.mp import MorPyOrchestrator

import importlib
import sys
import os
import os.path
from UltraDict import UltraDict


def init_cred() -> dict:
    r"""
    Creates and returns a trace dictionary with default keys such as module, operation,
    process and thread IDs, and flags for logging and interruption. This dictionary is
    used to initiate tracing for morPy operations.

    :return: dict
        trace - operation credentials and tracing
    """

    # Initialize operation credentials and tracing.
    # Each operation/function/object will fill the dictionary with data
    # by executing trace: dict = morPy.tracing(module, operation, trace)
    # as a first step before execution.
    trace: dict = {
        "module" : "__main__",
        "operation" : "",
        "tracing" : "__main__",
        "process_id" : int(0),
        "thread_id" : int(0),
        "task_id" : int(0),
        "log_enable" : False,
        "interrupt_enable" : False,
    }

    return trace


@core_wrap
def init(trace) -> (dict | UltraDict, MorPyOrchestrator):
    r"""
    Performs initialization of the global app configuration dictionary (app_dict) by building
    nested shared dictionaries, setting up localization, logging options, and system properties.
    It then initializes the morPy orchestrator and returns a tuple of the updated trace,
    app_dict, and the orchestrator.

    :return app_dict: morPy global dictionary containing app configurations
    """

    # Build the app_dict
    init_dict, init_datetime = build_app_dict(trace, create=True)

    init_dict["morpy"].update({"tasks_created" : trace["task_id"]})
    init_dict["morpy"]["proc_joined"] = True
    init_dict["morpy"].update({"proc_master" : trace['process_id']})

    # Initialize the global interrupt flag and exit flag
    init_dict["morpy"]["interrupt"] = False
    init_dict["morpy"]["exit"] = False

    # Set an initialization complete flag
    init_dict["morpy"]["init_complete"] = False

    # Store the start time and timestamps in the dictionary
    for time_key in init_datetime:
        init_dict["morpy"][f'init_{time_key}'] = init_datetime[f'{time_key}']

    # Evaluate log_enable
    if not init_dict["morpy"]["conf"]["log_db_enable"] and not init_dict["morpy"]["conf"]["log_txt_enable"]:
        init_dict["morpy"]["conf"]["log_enable"] = False
    log_enable = init_dict["morpy"]["conf"]["log_enable"]

    # Pass down the log enabling parameter
    trace["log_enable"] = log_enable

    # Import the morPy core functions localization into init_dict.
    morpy_loc = importlib.import_module(init_dict["morpy"]["conf"]["localization"])
    init_dict["loc"]["morpy"].update(getattr(morpy_loc, 'loc_morpy')())

    # Build nested dictionary for log generation
    log_levels = ("init", "debug", "info", "warning", "denied", "error", "critical", "exit")
    for log_level in log_levels:
        if ((log_enable and not (log_level in init_dict["morpy"]["conf"]["log_lvl_nolog"]))
            or (init_dict["morpy"]["conf"]["msg_print"]
            and not (log_level in init_dict["morpy"]["conf"]["log_lvl_noprint"]))):

            init_dict["morpy"]["logs_generate"][log_level] = True
        else:
            init_dict["morpy"]["logs_generate"][log_level] = False

    # Prepare log levels
    init_dict["morpy"]["events_total"] = 0
    init_dict["morpy"]["events_DEBUG"] = 0
    init_dict["morpy"]["events_INFO"] = 0
    init_dict["morpy"]["events_WARNING"] = 0
    init_dict["morpy"]["events_DENIED"] = 0
    init_dict["morpy"]["events_ERROR"] = 0
    init_dict["morpy"]["events_CRITICAL"] = 0
    init_dict["morpy"]["events_UNDEFINED"] = 0
    init_dict["morpy"]["events_INIT"] = 0
    init_dict["morpy"]["events_EXIT"] = 0

    # Create first log in txt-file including the app header
    if (init_dict["morpy"]["conf"]["log_txt_header_enable"]
        and trace["log_enable"]
        and init_dict["morpy"]["conf"]["log_txt_enable"]):

        morpy_log_header(trace, init_dict)

    # Initialize log DB
    if (init_dict["morpy"]["conf"]["log_enable"]
        and init_dict["morpy"]["conf"]["log_db_enable"]):

        from lib.msg import log_db_init
        log_db_init(trace, init_dict)

    # Initialize the morPy debug-specific localization
    init_dict["loc"]["morpy_dgb"].update(getattr(morpy_loc, 'loc_morpy_dbg')())
    log(trace, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_dbg_loaded"]}')

    # Initialize the app-specific localization
    app_loc = importlib.import_module(f'loc.app_{init_dict["morpy"]["conf"]["language"]}')
    init_dict["loc"]["app"].update(getattr(app_loc, 'loc_app')())
    init_dict["loc"]["app_dbg"].update(getattr(app_loc, 'loc_app_dbg')())
    log(trace, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_app_loaded"]}')

    # Localization initialized.
    log(trace, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_finished"]}\n'
                f'{init_dict["loc"]["morpy"]["init_loc_lang"]}: {init_dict["morpy"]["conf"]["language"]}')

    # Load init_dict as a string
    if init_dict["morpy"]["conf"]["print_init_vars"] or init_dict["morpy"]["conf"]["ref_create"]:
        init_dict_str = morpy_fct.app_dict_to_string(init_dict)
    else:
        init_dict_str = ""

    # Print init_dict to console
    if init_dict["morpy"]["conf"]["print_init_vars"]:
        print(init_dict_str)

    # Initialize the morPy orchestrator
    orchestrator = MorPyOrchestrator(trace, init_dict)

    # Calculate the runtime of the initialization routine
    init_duration = morpy_fct.runtime(init_dict["morpy"]["init_datetime_value"])

    # Record the duration of the initialization
    init_dict["morpy"]["init_rnt_delta"] = init_duration["rnt_delta"]

    log(trace, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_finished"]}\n'
                f'{init_dict["loc"]["morpy"]["init_duration"]}: {init_dict["morpy"]["init_rnt_delta"]}')

    # Write app_dict to file: initialized_app_dict.txt
    if init_dict["morpy"]["conf"]["ref_create"]:
        morpy_ref(trace, init_dict, init_dict_str)

    # Exit initialization
    retval = trace, init_dict, orchestrator
    return retval


@core_wrap
def build_app_dict(trace: dict, create: bool=False) -> (dict | UltraDict, dict):
    r"""
    Constructs the morPy global configuration dictionary (app_dict) with support for
    multiprocessing. It collects system information, applies configuration settings from
    lib.conf, and returns the app_dict along with a datetime stamp dictionary.

    :param trace: operation credentials and tracing
    :param create: If True, a (nested) dictionary is created. Otherwise, purely
        references to the UltraDict.

    :return init_dict: morPy global dictionary containing app configurations

    :example:
        init_dict = build_app_dict(trace, create=True)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'build_app_dict(~)'
    trace: dict = morpy_fct.tracing(module, operation, trace)

    init_dict = None

    try:
        # Retrieve the starting time of the program
        init_datetime = morpy_fct.datetime_now()

        # Get project settings
        conf_dict = config.settings()

        # Collect system information
        sysinfo = morpy_fct.sysinfo()

        processes_max = init_max_processes(conf_dict, sysinfo["logical_cpus"])

        if processes_max > 1:
            from lib.mp import shared_dict

            memory_dict = nested_memory_sizes(conf_dict, processes_max)

            # app_dict
            init_dict = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_mem"],
                recurse=False
            )

            # app_dict["morpy"]
            init_dict["morpy"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_morpy_mem"],
                recurse=False
            )

            # app_dict["morpy"]["conf"]
            init_dict["morpy"]["conf"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_morpy_conf_mem"],
                recurse=False
            )

            # app_dict["morpy"]["heap_shelf"]
            init_dict["morpy"]["heap_shelf"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_morpy_heap_shelf_mem"],
                recurse=False
            )

            # app_dict["morpy"]["logs_generate"]
            init_dict["morpy"]["logs_generate"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_morpy_logs_generate_mem"],
                recurse=False
            )

            # app_dict["morpy"]["orchestrator"]
            init_dict["morpy"]["orchestrator"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_morpy_orchestrator_mem"],
                recurse=False
            )

            # app_dict["morpy"]["proc_available"]
            init_dict["morpy"]["proc_available"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_morpy_proc_available_mem"],
                recurse=False
            )

            # app_dict["morpy"]["proc_busy"]
            init_dict["morpy"]["proc_busy"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_morpy_proc_busy_mem"],
                recurse=False
            )
            # Insert master process ID
            init_dict["morpy"]["proc_busy"][trace["process_id"]] = "MASTER"

            # app_dict["morpy"]["proc_waiting"]
            init_dict["morpy"]["proc_waiting"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_morpy_proc_waiting_mem"],
                recurse=False
            )

            # app_dict["morpy"]["sys"]
            init_dict["morpy"]["sys"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_morpy_sys_mem"],
                recurse=False
            )

            # app_dict["loc"]
            init_dict["loc"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_loc_mem"],
                recurse=False
            )

            # app_dict["loc"]["morPy"]
            init_dict["loc"]["morpy"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_loc_morpy_mem"],
                recurse=False
            )

            # app_dict["loc"]["mpy_dbg"]
            init_dict["loc"]["morpy_dgb"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_loc_morpy_dbg_mem"],
                recurse=False
            )

            # app_dict["loc"]["app"]
            init_dict["loc"]["app"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_loc_app_mem"],
                recurse=False
            )

            # app_dict["loc"]["app_dbg"]
            init_dict["loc"]["app_dbg"] = shared_dict(
                name=obscure_shared_name(),
                create=create,
                size=memory_dict["app_dict_loc_app_dbg_mem"],
                recurse=False
            )

        # Without GIL, allow for true nesting
        else:
            init_dict = dict()
            init_dict["morpy"] = {}
            init_dict["morpy"]["conf"] = {}
            init_dict["morpy"]["logs_generate"] = {}
            init_dict["morpy"]["orchestrator"] = {}
            init_dict["morpy"]["sys"] = {}
            init_dict["loc"] = {}
            init_dict["loc"]["morpy"] = {}
            init_dict["loc"]["morpy_dgb"] = {}
            init_dict["loc"]["app"] = {}
            init_dict["loc"]["app_dbg"] = {}

        # Store configuration in init_dict
        for key, val in conf_dict.items():
            init_dict["morpy"]["conf"][key] = val

        # Store system information
        for sys_key, sys_val in sysinfo.items():
            init_dict["morpy"]["sys"][sys_key] = sys_val

        # Store maximum determined processes
        init_dict["morpy"]["processes_max"] = processes_max

        return init_dict, init_datetime

    # Error detection
    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(trace, init_dict, e, sys.exc_info()[-1].tb_lineno, "critical")


@core_wrap
def morpy_log_header(trace: dict, init_dict: dict | UltraDict) -> None:
    r"""
    Writes a header to the logging text file that includes key application metadata such as
    the author, application path, timestamp, user, system, OS version, architecture, and
    thread count.

    :param trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)

    :example:
        morpy_log_header(trace, init_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'log_header(~)'
    trace: dict = morpy_fct.tracing(module, operation, trace)

    # Create the app header
    content = (
        f'== {init_dict["loc"]["morpy"]["log_header_start"]}{3*" =="}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_author"]}: Bastian Neuwirth\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_app"]}: {init_dict["morpy"]["conf"]["main_path"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_timestamp"]}: {init_dict["morpy"]["init_datetimestamp"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_user"]}: {init_dict["morpy"]["sys"]["username"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_system"]}: {init_dict["morpy"]["sys"]["os"]} {init_dict["morpy"]["sys"]["os_release"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_version"]}: {init_dict["morpy"]["sys"]["os_version"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_architecture"]}: {init_dict["morpy"]["sys"]["os_arch"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_threads"]}: {init_dict["morpy"]["sys"]["threads"]}\n'
        f'== {init_dict["loc"]["morpy"]["log_header_begin"]}{3*" =="}\n'
    )

    # Write to the logfile
    filepath = init_dict["morpy"]["conf"]["log_txt_path"]
    textfile_write(trace, init_dict, filepath, content)

    # Clean up
    del trace


@core_wrap
def morpy_ref(trace: dict, init_dict: dict | UltraDict, init_dict_str: str) -> None:
    r"""
    Writes a string representation of the initialized app_dict to a reference file in the
    main path. This document is intended for development purposes only.

    :param trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)
    :param init_dict_str: String of the init_dict

    :example:
        morpy_ref(trace, init_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'ref(~)'
    trace: dict = morpy_fct.tracing(module, operation, trace)

    try:
        morpy_ref_path = os.path.join(f'{init_dict["morpy"]["conf"]["main_path"]}', 'initialized_app_dict.txt')
        init_dict_txt = open(morpy_ref_path,'w')

        # Write init_dict to file
        init_dict_txt.write(f'{init_dict["loc"]["morpy"]["ref_descr"]}\n\n')
        init_dict_txt.write(init_dict_str)

        # Close the file
        init_dict_txt.close()

        # The init_dict was written to textfile.
        log(trace, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["ref_created"]}\n'
                f'{init_dict["loc"]["morpy"]["ref_path"]}: {morpy_ref_path}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(trace, init_dict, e, sys.exc_info()[-1].tb_lineno, "error")


def init_max_processes(conf_dict: dict, system_logical_cpus: int) -> int:
    r"""
    Calculates the maximum number of processes allowed for runtime, based on configuration settings
    (absolute or relative) and the number of logical CPUs. Returns the maximum process count as an
    integer.

    :param conf_dict: Dictionary equal to lib.conf.settings()
    :param system_logical_cpus: Logical CPUs of the machine.

    :return max_processes: Maximum processes evaluated for runtime.
    """

    # Set up multiprocessing
    processes_min: int = 1
    processes_max: int = processes_min
    processes_count_absolute: bool = conf_dict["processes_count_absolute"]
    conf_processes_absolute: int = conf_dict["processes_absolute"]
    conf_processes_relative: float = conf_dict["processes_relative"]
    processes_relative_math: str = conf_dict["processes_relative_math"]

    # Evaluate absolute/relative processes calculation. Fallback to absolute.
    processes_count_absolute: bool = processes_count_absolute if isinstance(processes_count_absolute, bool) else True

    # +--- Calculate maximum processes ---+
    if processes_count_absolute:
        # Determine absolute process count. Fallback to half of system logical CPUs or 1.
        if isinstance(conf_processes_absolute, int):
            processes_max: int = max(processes_min, min(conf_processes_absolute, system_logical_cpus))
        else:
            from math import floor
            processes_max: int = max(1, floor(0.5 * system_logical_cpus))
    else:
        # Determine relative process count. Fallback to half of system logical CPUs or 1.
        if isinstance(conf_processes_relative, float):
            processes_relative: float = max(float(processes_min), min(conf_processes_relative * system_logical_cpus, system_logical_cpus))
        else:
            processes_relative: float = max(1.0, 0.5 * system_logical_cpus)

        # Determine relative calculation method.
        if isinstance(processes_relative_math, str):
            if processes_relative_math not in ("round", "floor", "ceil"):
                processes_relative_math: str = "floor"
        else:
            processes_relative_math: str = "floor"

        match processes_relative_math:
            case "round":
                processes_max: int = round(processes_relative)
            case "floor":
                from math import floor
                processes_max: int = floor(processes_relative)
            case "ceil":
                from math import ceil
                processes_max: int = ceil(processes_relative)

    return processes_max


def init_memory_size(conf_dict: dict, max_processes: int) -> tuple:
    r"""
    Computes the total memory (in bytes) to be allocated for shared dictionaries by converting
    configuration values (in MB) to bytes. It checks that the minimum required memory does not
    exceed system memory and returns a tuple containing the target initialization memory, the
    minimal required bytes, and total system memory.

    :param conf_dict: Dictionary equal to lib.conf.settings()
    :param max_processes: Maximum processes evaluated for runtime.

    :return init_memory: Memory in bytes
    :return memory_min_bytes: Minimum bytes from lib.conf.settings()["memory_min_mb"]
    :return sys_memory_bytes: System total memory
    """

    import psutil

    memory_min_mb: int = conf_dict["memory_min_mb"]

    # Get system memory
    sys_memory_bytes: int = int(psutil.virtual_memory().total)

    # Minimum memory. Change unit from MB to Byte. Fallback to 20 MB per process.
    memory_min_bytes: int = memory_min_mb * 1024 * 1024 if isinstance(memory_min_mb, int) else 20 * 1024 * 1024 * max_processes

    if memory_min_bytes > sys_memory_bytes:
        sys_memory_mb: float = sys_memory_bytes / 1024 / 1024
        raise RuntimeError(f'Insufficient system memory.\nSystem: {sys_memory_mb:.2f} MB\n'
                           f'Required per Configuration: {memory_min_mb:.2f} MB')

    # Evaluate absolute/relative memory calculation. Fallback to absolute.
    memory_use_absolute: bool = conf_dict["memory_use_absolute"]
    memory_use_absolute = memory_use_absolute if isinstance(memory_use_absolute, bool) else True

    if memory_use_absolute:
        # Absolute Target memory. Change unit from MB to Byte. Fallback to 20 MB per process.
        memory_absolute_mb: int = conf_dict["memory_absolute"]
        init_memory = memory_absolute_mb * 1024 * 1024 if isinstance(memory_absolute_mb, int) else 20 * 1024 * 1024 * max_processes
    else:
        from math import floor
        # Relative Target memory. Fallback to 0.002% per process.
        memory_relative: float = conf_dict["memory_relative"]
        memory_relative = memory_relative if isinstance(memory_relative, float) else 0.0002
        init_memory = floor(memory_relative * sys_memory_bytes) * max_processes

    # Proactive autocorrection of memory
    init_memory = max(memory_min_bytes, min(init_memory, sys_memory_bytes))

    retval = int(init_memory), int(memory_min_bytes), int(sys_memory_bytes)
    return retval


def nested_memory_sizes(conf_dict: dict, max_processes: int) -> dict:
    r"""
    Determines the memory sizes for each nested shared dictionary (e.g. for ‘morpy’, ‘conf’, ‘logs_generate’, etc.)
    based on the maximum number of processes. Returns a dictionary mapping each UltraDict’s purpose to its allocated
    memory size in bytes.

    !! ATTENTION !!
    The most heavily used dictionary in multiprocessing context is `app_dict["morpy"]`.
    If a warning shows up like
    >>> 'WARNING:root:Full dumps too fast full_dump_counter=0 full_dump_counter_remote=5. Consider increasing buffer_size.'
    increase buffer sizes, starting with `app_dict_morpy_mem`, which is the buffer size for
    `app_dict["morpy"]`.

    :param conf_dict: Dictionary equal to lib.conf.settings()
    :param max_processes: Maximum processes evaluated for runtime.

    :return: dict
        app_dict_mem                        - Memory for UltraDict: app_dict
        app_dict_morpy_mem                  - Memory for UltraDict: app_dict["morpy"]
        app_dict_morpy_conf_mem             - Memory for UltraDict: app_dict["morpy"]["conf"]
        app_dict_morpy_heap_shelf_mem       - Memory for UltraDict: app_dict["morpy"]["heap_shelf"]
        app_dict_morpy_logs_generate_mem    - Memory for UltraDict: app_dict["morpy"]["logs_generate"]
        app_dict_morpy_orchestrator_mem     - Memory for UltraDict: app_dict["morpy"]["orchestrator"]
        app_dict_morpy_proc_available_mem   - Memory for UltraDict: app_dict["morpy"]["proc_available"]
        app_dict_morpy_proc_busy_mem        - Memory for UltraDict: app_dict["morpy"]["proc_busy"]
        app_dict_morpy_proc_waiting_mem     - Memory for UltraDict: app_dict["morpy"]["proc_waiting"]
        app_dict_morpy_sys_mem              - Memory for UltraDict: app_dict["morpy"]["sys"]
        app_dict_loc_mem                    - Memory for UltraDict: app_dict["loc"]
        app_dict_loc_morpy_mem              - Memory for UltraDict: app_dict["loc"]["morpy"]
        app_dict_loc_morpy_dbg_mem          - Memory for UltraDict: app_dict["loc"]["morpy_dbg"]
        app_dict_loc_app_mem                - Memory for UltraDict: app_dict["loc"]["app"]
        app_dict_loc_app_dbg_mem            - Memory for UltraDict: app_dict["loc"]["app_dbg"]
    """

    from math import ceil

    init_memory, memory_min_bytes, sys_memory_bytes = init_memory_size(conf_dict, max_processes)

    # Determine minimum memories for morPy core first
    app_dict_morpy_mem: int                 = 2 * 1024 * 1024 * ceil(1 + 0.5 * max_processes)
    app_dict_morpy_heap_shelf_mem: int      = 5 * 1024 * 1024 * max_processes
    app_dict_morpy_orchestrator_mem: int    = 1 * 1024 * 1024
    app_dict_morpy_proc_available_mem: int  = 1 * 1024 * 1024 * ceil(1 + 0.2 * max_processes)
    app_dict_morpy_proc_busy_mem: int       = 1 * 1024 * 1024 * ceil(1 + 0.2 * max_processes)
    app_dict_morpy_proc_waiting_mem: int    = 1 * 1024 * 1024 * ceil(1 + 0.2 * max_processes)
    app_dict_morpy_logs_generate_mem: int   = 1 * 1024 * 1024

    app_dict_morpy_conf_mem: int  = 1 * 1024 * 1024
    app_dict_morpy_sys_mem: int   = 2 * 1024 * 1024
    app_dict_loc_mem: int         = 1 * 1024 * 1024

    app_dict_loc_morpy_mem: int     = 2 * 1024 * 1024
    app_dict_loc_morpy_dbg_mem: int = 1 * 1024 * 1024

    # Combined size of morPy core memory
    morpy_core_memory: int = sum(
        (app_dict_morpy_mem,
        app_dict_morpy_heap_shelf_mem,
        app_dict_morpy_orchestrator_mem,
        app_dict_morpy_proc_available_mem,
        app_dict_morpy_proc_busy_mem,
        app_dict_morpy_proc_waiting_mem,
        app_dict_morpy_logs_generate_mem,
        app_dict_morpy_conf_mem,
        app_dict_morpy_sys_mem,
        app_dict_loc_morpy_mem,
        app_dict_loc_morpy_dbg_mem)
    )

    # If memory for morPy core is greater than system memory, exit
    if morpy_core_memory > sys_memory_bytes:
        sys_memory_mb: float = sys_memory_bytes / 1024 / 1024
        morpy_core_memory_mb: float = morpy_core_memory / 1024 / 1024
        raise RuntimeError(f'Insufficient system memory.\nSystem: {sys_memory_mb:.2f} MB\n'
                           f'morPy required: {morpy_core_memory_mb:.2f} MB')

    app_dict_loc_app_mem: int       = 10 * 1024 * 1024
    app_dict_loc_app_dbg_mem: int   = 2 * 1024 * 1024

    # Try assign left memory space to app_dict.
    app_dict_mem: int = init_memory - sum((morpy_core_memory, app_dict_loc_app_mem, app_dict_loc_app_dbg_mem))

    # If root shared memory size is too small, try to adjust.
    if app_dict_mem < 1 * 1024 * 1024:
        app_mem_byte = 3 * 1024 * 1024
        if  sys_memory_bytes > app_mem_byte + morpy_core_memory:
            app_dict_loc_app_mem: int       = 1 * 1024 * 1024
            app_dict_loc_app_dbg_mem: int   = 1 * 1024 * 1024
            app_dict_mem: int               = 1 * 1024 * 1024
        else:
            sys_memory_mb: float = sys_memory_bytes / 1024 / 1024
            morpy_core_memory_mb: float = morpy_core_memory / 1024 / 1024
            app_mem_mb: float = app_mem_byte / 3
            raise RuntimeError(f'Insufficient memory configuration.\nSystem: {sys_memory_mb:.2f} MB\n'
                               f'morPy required: {morpy_core_memory_mb:.2f} MB\n'
                               f'App required: {app_mem_mb:.2f} MB')

    return {
        "app_dict_mem" : app_dict_mem,
        "app_dict_morpy_mem" : app_dict_morpy_mem,
        "app_dict_morpy_conf_mem" : app_dict_morpy_conf_mem,
        "app_dict_morpy_heap_shelf_mem" : app_dict_morpy_heap_shelf_mem,
        "app_dict_morpy_logs_generate_mem" : app_dict_morpy_logs_generate_mem,
        "app_dict_morpy_orchestrator_mem" : app_dict_morpy_orchestrator_mem,
        "app_dict_morpy_proc_available_mem" : app_dict_morpy_proc_available_mem,
        "app_dict_morpy_proc_busy_mem" : app_dict_morpy_proc_busy_mem,
        "app_dict_morpy_proc_waiting_mem" : app_dict_morpy_proc_waiting_mem,
        "app_dict_morpy_sys_mem" : app_dict_morpy_sys_mem,
        "app_dict_loc_mem" : app_dict_loc_mem,
        "app_dict_loc_morpy_mem" : app_dict_loc_morpy_mem,
        "app_dict_loc_morpy_dbg_mem" : app_dict_loc_morpy_dbg_mem,
        "app_dict_loc_app_mem" : app_dict_loc_app_mem,
        "app_dict_loc_app_dbg_mem" : app_dict_loc_app_dbg_mem
    }


def obscure_shared_name() -> str:
    r"""
    Generates a random, unique string to serve as the name for a shared memory segment. This obfuscates
    the shared memory names to enhance security and reduce the risk of external attachment.

    :return shared_name: String with random signs and length.
    """

    import secrets
    import random
    from UltraDict import UltraDict

    shared_name: str = ''
    unique: bool = False
    min_len: int = 16
    max_len: int = 48

    # Loop to ensure that the dictionaries will not attach to a running app.
    while not unique:
        token_hex: str = secrets.token_hex(max_len)
        cut_off: int = random.randint(min_len, max_len) + min_len
        shared_name: str = token_hex[:cut_off]
        try:
            UltraDict(create=False, name=shared_name)
        except Exception as e:
            # Check if the caught exception is effectively a "CannotAttachSharedMemory"
            if e.__class__.__name__ == "CannotAttachSharedMemory":
                unique = True
            else:
                # Re-raise if it is an unexpected error
                raise

    return shared_name