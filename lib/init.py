r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module holds all functions used for initialization of the
            morPy framework.
"""

import lib.fct as morpy_fct
import lib.conf as conf
from lib.common import textfile_write
from lib.decorators import log
from lib.mp import MorPyOrchestrator

import importlib
import sys
import os
import os.path
from UltraDict import UltraDict

def init_cred() -> dict:
    r"""
    Initializes the operation credentials and tracing.

    :param:
        -

    :return: dict
        morpy_trace - operation credentials and tracing
    """

    # Initialize operation credentials and tracing.
    # Each operation/function/object will fill the dictionary with data
    # by executing morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)
    # as a first step before execution.
    morpy_trace: dict = {
        'module' : '__main__',
        'operation' : '',
        'tracing' : '__main__',
        'process_id' : int(0),
        'thread_id' : int(0),
        'task_id' : int(0),
        'log_enable' : False,
        'interrupt_enable' : False,
    }

    return morpy_trace

def init(morpy_trace) -> (dict | UltraDict, MorPyOrchestrator):
    r"""
    Initializes the app dictionary and yields app
    specific information to be handed down through called functions.

    :param morpy_trace: operation credentials and tracing

    :return app_dict: morPy global dictionary containing app configurations
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'init(~)'
    morpy_trace_init = morpy_fct.tracing(module, operation, morpy_trace)

    try:
        # ############################################
        # START Single-threaded initialization
        # ############################################

        # Build the app_dict
        init_dict = build_app_dict(morpy_trace_init, create=True)

        init_dict["morpy"].update({"tasks_created" : morpy_trace_init["task_id"]})
        init_dict["morpy"].update({"proc_available" : set()})
        init_dict["morpy"].update({"proc_busy" : {morpy_trace_init["process_id"],}})
        init_dict["morpy"]["proc_joined"] = True
        init_dict["morpy"].update({"proc_master" : morpy_trace['process_id']})

        # Initialize the global interrupt flag and exit flag
        init_dict["morpy"]["interrupt"] = False
        init_dict["morpy"]["exit"] = False

        # Set an initialization complete flag
        init_dict["run"]["init_complete"] = False

        # Retrieve the starting time of the program
        init_datetime = morpy_fct.datetime_now()

        # Store the start time and timestamps in the dictionary
        for time_key in init_datetime:
            init_dict["run"][f'init_{time_key}'] = init_datetime[f'{time_key}']

        # Update the initialize dictionary with the parameters dictionary
        init_dict["conf"].update(conf.settings(start_time=init_dict["run"]["init_datetimestamp"]))

        # Evaluate log_enable
        if not init_dict["conf"]["log_db_enable"] and not init_dict["conf"]["log_txt_enable"]:
            init_dict["conf"]["log_enable"] = False

        # Pass down the log enabling parameter
        morpy_trace["log_enable"] = init_dict["conf"]["log_enable"]
        morpy_trace_init["log_enable"] = init_dict["conf"]["log_enable"]

        # Import the morPy core functions localization into init_dict.
        morpy_loc = importlib.import_module(init_dict["conf"]["localization"])
        init_dict["loc"]["morpy"].update(getattr(morpy_loc, 'loc_morpy')())

        # Build nested dictionary for log generation
        log_levels = ("init", "debug", "info", "warning", "denied", "error", "critical", "exit")
        for log_level in log_levels:
            if (
                (init_dict["conf"]["log_enable"] and
                 not (log_level in init_dict["conf"]["log_lvl_nolog"])
                 ) or (
                init_dict["conf"]["msg_print"] and
                 not (log_level in init_dict["conf"]["log_lvl_noprint"]))
            ):
                init_dict["morpy"]["logs_generate"].update({log_level : True})
            else:
                init_dict["morpy"]["logs_generate"].update({log_level : False})

        # Retrieve system information
        sysinfo = morpy_fct.sysinfo()

        # Update init_dict with system information
        for sys_key in sysinfo:
            init_dict["sys"][sys_key] = sysinfo[sys_key]

        # Test for elevated privileges
        # TODO make an elevation handler

        # Prepare log levels
        init_dict["run"]["events_total"] = 0
        init_dict["run"]["events_DEBUG"] = 0
        init_dict["run"]["events_INFO"] = 0
        init_dict["run"]["events_WARNING"] = 0
        init_dict["run"]["events_DENIED"] = 0
        init_dict["run"]["events_ERROR"] = 0
        init_dict["run"]["events_CRITICAL"] = 0
        init_dict["run"]["events_UNDEFINED"] = 0
        init_dict["run"]["events_INIT"] = 0
        init_dict["run"]["events_EXIT"] = 0

        # Create first log in txt-file including the app header
        if (init_dict["conf"]["log_txt_header_enable"] and
            morpy_trace_init["log_enable"] and
            init_dict["conf"]["log_txt_enable"]
        ):
            morpy_log_header(morpy_trace_init, init_dict)

        # Initialize the morPy debug-specific localization
        init_dict["loc"]["morpy_dgb"].update(getattr(morpy_loc, 'loc_morpy_dbg')())
        log(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_dbg_loaded"]}')

        # Initialize the app-specific localization
        app_loc = importlib.import_module(f'loc.app_{init_dict["conf"]["language"]}')
        init_dict["loc"]["app"].update(getattr(app_loc, 'loc_app')())
        init_dict["loc"]["app_dbg"].update(getattr(app_loc, 'loc_app_dbg')())
        log(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_app_loaded"]}')

        # Localization initialized.
        log(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_finished"]}\n'
                f'{init_dict["loc"]["morpy"]["init_loc_lang"]}: {init_dict["conf"]["language"]}')

        # Load init_dict as a string
        if init_dict["conf"]["print_init_vars"] or init_dict["conf"]["ref_create"]:
            init_dict_str = morpy_fct.app_dict_to_string(init_dict)
        else:
            init_dict_str = ""

        # Print init_dict to console
        if init_dict["conf"]["print_init_vars"]:
            print(init_dict_str)

        # Initialize the morPy orchestrator
        orchestrator = MorPyOrchestrator(morpy_trace_init, init_dict)

        # ############################################
        # END Single-threaded initialization
        # START Multi-threaded initialization
        # ############################################

        # task = morPy.testprint(morpy_trace_init, "Message")
        # mp.run_parallel(mpy_task, app_dict, task)

        # ############################################
        # END Multi-threaded initialization
        # ############################################

        # Calculate the runtime of the initialization routine
        init_duration = morpy_fct.runtime(init_dict["run"]["init_datetime_value"])

        # Record the duration of the initialization
        init_dict["run"]["init_rnt_delta"] = init_duration["rnt_delta"]

        log(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_finished"]}\n'
            f'{init_dict["loc"]["morpy"]["init_duration"]}: {init_dict["run"]["init_rnt_delta"]}')

        # Write app_dict to file: initialized_app_dict.txt
        if init_dict["conf"]["ref_create"]:
            morpy_ref(morpy_trace_init, init_dict, init_dict_str)

        # Exit initialization
        retval = init_dict, orchestrator
        return retval

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, init_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

def build_app_dict(morpy_trace: dict, create: bool=False) -> dict:
    r"""
    This function builds the app_dict in accordance to multiprocessing and whether GIL
    is included in the Python environment.

    :param morpy_trace: operation credentials and tracing
    :param create: If True, a (nested) dictionary is created. Otherwise, purely
        references to the UltraDict.

    :return init_dict: morPy global dictionary containing app configurations

    :example:
        init_dict = build_app_dict(morpy_trace, create=True)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'build_app_dict(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    # Check for GIL and decide for an app_dict structure.
    gil = has_gil(morpy_trace)
    init_dict = None
    init_mem = 1_000_000 # TODO get memory from config
    min_mem = 1_000

    try:
        # FIXME
        # if gil:
        if True:
            from lib.mp import shared_dict

            def mem_evaluation(mem, min_mem) -> int:
                mem = mem if mem > min_mem else min_mem
                return mem

            mem = mem_evaluation(init_mem, min_mem)
            init_dict = shared_dict(
                name="app_dict",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["conf"] = shared_dict(
                name="app_dict[conf]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem // 10, min_mem)
            init_dict["morpy"] = shared_dict(
                name="app_dict[morpy]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem // 1_000, min_mem)
            init_dict["morpy"]["logs_generate"] = shared_dict(
                name="app_dict[global][morPy][logs_generate]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["morpy"]["orchestrator"] = shared_dict(
                name="app_dict[morpy][orchestrator]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["morpy"]["proc_refs"] = shared_dict(
                name="app_dict[morpy][proc_refs]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem // 10, min_mem)
            init_dict["morpy"]["proc_waiting"] = shared_dict(
                name="app_dict[morpy][proc_waiting]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem // 10, min_mem)
            init_dict["sys"] = shared_dict(
                name="app_dict[sys]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem // 10, min_mem)
            init_dict["run"] = shared_dict(
                name="app_dict[run]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem // 1_000, min_mem)
            init_dict["loc"] = shared_dict(
                name="app_dict[loc]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem, min_mem)
            init_dict["loc"]["morpy"] = shared_dict(
                name="app_dict[loc][morPy]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["loc"]["morpy_dgb"] = shared_dict(
                name="app_dict[loc][mpy_dbg]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem, min_mem)
            init_dict["loc"]["app"] = shared_dict(
                name="app_dict[loc][app]",
                create=create,
                size=mem,
                recurse=False
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["loc"]["app_dbg"] = shared_dict(
                name="app_dict[loc][app_dbg]",
                create=create,
                size=mem,
                recurse=False
            )

        # Without GIL, allow for true nesting
        else:
            init_dict = {}

            init_dict["conf"] = {}
            init_dict["morpy"] = {}
            init_dict["morpy"]["logs_generate"] = {}
            init_dict["morpy"]["orchestrator"] = {}
            init_dict["morpy"]["proc_refs"] = {}
            init_dict["sys"] = {}
            init_dict["run"] = {}
            init_dict["loc"] = {}
            init_dict["loc"]["morpy"] = {}
            init_dict["loc"]["morpy_dgb"] = {}
            init_dict["loc"]["app"] = {}
            init_dict["loc"]["app_dbg"] = {}

        return init_dict

    # Error detection
    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

def morpy_log_header(morpy_trace: dict, init_dict: dict | UltraDict) -> None:
    r"""
    This function writes the header for the logfile including app specific
    information.

    :param morpy_trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)

    :return:
        -

    :example:
        morpy_log_header(morpy_trace, init_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'log_header(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    # Create the app header
    content = (
        f'== {init_dict["loc"]["morpy"]["log_header_start"]}{3*" =="}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_author"]}: Bastian Neuwirth\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_app"]}: {init_dict["conf"]["main_path"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_timestamp"]}: {init_dict["run"]["init_datetimestamp"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_user"]}: {init_dict["sys"]["username"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_system"]}: {init_dict["sys"]["os"]} {init_dict["sys"]["os_release"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_version"]}: {init_dict["sys"]["os_version"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_architecture"]}: {init_dict["sys"]["os_arch"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_threads"]}: {init_dict["sys"]["threads"]}\n'
        f'== {init_dict["loc"]["morpy"]["log_header_begin"]}{3*" =="}\n'
    )

    # Write to the logfile
    filepath = init_dict["conf"]["log_txt_path"]
    textfile_write(morpy_trace, init_dict, filepath, content)

    # Clean up
    del morpy_trace

def morpy_ref(morpy_trace: dict, init_dict: dict | UltraDict, init_dict_str: str) -> None:
    r"""
    This function documents the initialized dictionary (reference). It is stored
    in the same path as __main__.py and serves development purposes.

    :param morpy_trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)
    :param init_dict_str: String of the init_dict

    :return:
        -

    :example:
        morpy_ref(morpy_trace, init_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'ref(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    try:
        morpy_ref_path = os.path.join(f'{init_dict["conf"]["main_path"]}', 'initialized_app_dict.txt')
        init_dict_txt = open(morpy_ref_path,'w')

        # Write init_dict to file
        init_dict_txt.write(f'{init_dict["loc"]["morpy"]["ref_descr"]}\n\n')
        init_dict_txt.write(init_dict_str)

        # Close the file
        init_dict_txt.close()

        # The init_dict was written to textfile.
        log(morpy_trace, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["ref_created"]}\n'
                f'{init_dict["loc"]["morpy"]["ref_path"]}: {morpy_ref_path}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, init_dict, e, sys.exc_info()[-1].tb_lineno, "error")

def has_gil(morpy_trace: dict) -> bool | None:
    r"""
    Return True if we detect a standard GIL-based Python runtime on a 'typical' operating system.
    Return False if we suspect a 'no-gil' or 'free-threading' build on Linux/macOS/Windows, or if
    we detect certain alternative Pythons. This is *heuristic* and not a guaranteed official check.

    :param morpy_trace: operation credentials and tracing information

    :return gil_detected: If True, Python environment has GIL implemented. Process forking not supported.

    :example:
        gil = has_gil(morpy_trace)
    """

    # module: str = 'lib.init'
    # operation: str = 'has_gil(~)'
    # morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    try:
        if sys.version_info >= (3, 13):
            status = sys._is_gil_enabled()
            if status:
                return True
            else:
                return False
        else:
            return True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, None, e, sys.exc_info()[-1].tb_lineno, "error")
