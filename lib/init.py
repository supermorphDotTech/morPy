r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module holds all functions used for initialization of the
            morPy framework.
"""

import lib.fct as morpy_fct
import lib.conf as conf

from lib.common import PriorityQueue
from lib.common import textfile_write
from lib.decorators import log_no_q
from lib.mp import cl_orchestrator

import sys
import os
import importlib

def init_cred() -> dict:
    r"""
    This function initializes the operation credentials and tracing.

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
        'process_id' : 0,
        'thread_id' : 0,
        'task_id' : 0,
        'log_enable' : False,
        'interrupt_enable' : False,
    }

    return morpy_trace

def init(morpy_trace) -> (dict, cl_orchestrator):
    r"""
    This function initializes the app dictionary and yields app
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
        init_dict = types_dict_build(morpy_trace_init, create=True)

        init_dict["proc"]["morpy"].update({"tasks_created" : morpy_trace_init["task_id"]})
        init_dict["proc"]["morpy"].update({"proc_available" : set()})
        init_dict["proc"]["morpy"].update({"proc_busy" : set(range(morpy_trace_init["process_id"]))})
        init_dict["proc"]["morpy"].update({"proc_refs" : {}})

        # Initialize the global interrupt flag and exit flag
        init_dict["global"]["morpy"]["interrupt"] = False
        init_dict["global"]["morpy"]["exit"] = False

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
                init_dict["global"]["morpy"]["logs_generate"].update({log_level : True})
            else:
                init_dict["global"]["morpy"]["logs_generate"].update({log_level : False})

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

        # Logging may start after this
        init_dict["proc"]["morpy"]["process_q"] = PriorityQueue(
            morpy_trace_init, init_dict, name="morPy priority queue", is_manager=True
        )

        # Initialize the morPy debug-specific localization
        init_dict["loc"]["morpy_dgb"].update(getattr(morpy_loc, 'loc_morpy_dbg')())
        log_no_q(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_dbg_loaded"]}')

        # Initialize the app-specific localization
        app_loc = importlib.import_module(f'loc.app_{init_dict["conf"]["language"]}')
        init_dict["loc"]["app"].update(getattr(app_loc, 'loc_app')())
        init_dict["loc"]["app_dbg"].update(getattr(app_loc, 'loc_app_dbg')())
        log_no_q(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_app_loaded"]}')

        # Localization initialized.
        log_no_q(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_finished"]}\n'
                f'{init_dict["loc"]["morpy"]["init_loc_lang"]}: {init_dict["conf"]["language"]}')

        # Load init_dict as a string
        if init_dict["conf"]["print_init_vars"] or init_dict["conf"]["ref_create"]:
            init_dict_str = morpy_fct.app_dict_to_string(init_dict)
        else:
            init_dict_str = ''

        # Print init_dict to console
        if init_dict["conf"]["print_init_vars"]:
            print(init_dict_str)

        # Initialize the morPy orchestrator
        init_dict["proc"]["morpy"]["cl_orchestrator"] = cl_orchestrator(morpy_trace_init, init_dict)

        # Activate priority queue
        init_dict["proc"]["morpy"]["process_q"]._init_mp(morpy_trace_init, init_dict)

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

        log_no_q(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_finished"]}\n'
            f'{init_dict["loc"]["morpy"]["init_duration"]}: {init_dict["run"]["init_rnt_delta"]}')

        # Lock and tighten nested dictionaries
        types_dict_finalize(morpy_trace_init, init_dict)

        # Write app_dict to file: initialized_app_dict.txt
        if init_dict["conf"]["ref_create"]:
            morpy_ref(morpy_trace_init, init_dict, init_dict_str)

        # Exit initialization
        retval = init_dict, init_dict["proc"]["morpy"]["cl_orchestrator"]
        return retval

    except Exception as e:
        morpy_fct.handle_exception_init(e)
        raise

def types_dict_build(morpy_trace: dict, create: bool=False) -> dict:
    r"""
    This function builds the app_dict. This is needed in spawned processes, too
    to successfully link the nested dictionaries.

    :param morpy_trace: operation credentials and tracing
    :param create: If True, a (nested) dictionary is created. Otherwise, purely
        references to the UltraDict.

    :return init_dict: morPy global dictionary containing app configurations

    :example:
    >>> init_dict = types_dict_build(morpy_trace, create=True)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'types_dict_build(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    # Check for GIL and decide for an app_dict structure.
    gil = has_gil(morpy_trace)
    init_dict = None

    try:
        # With GIL, use a flat app_dict referencing UltraDict instances and mask it as nested.
        # TODO remove branch force
        if gil or True:
            from lib.types_dict import FlatDict, MorPyDictUltra

            init_dict = FlatDict(
                name="app_dict",
                create=create
            )

            init_dict["conf"] = MorPyDictUltra(
                name="app_dict[conf]",
                create=create
            )

            init_dict["sys"] = MorPyDictUltra(
                name="app_dict[sys]",
                create=create
            )

            init_dict["run"] = MorPyDictUltra(
                name="app_dict[run]",
                create=create
            )

            init_dict["global"] = MorPyDictUltra(
                name="app_dict[global]",
                create=create
            )

            init_dict["global"]["morpy"] = MorPyDictUltra(
                name="app_dict[global][morPy]",
                create=create
            )

            init_dict["global"]["app"] = MorPyDictUltra(
                name="app_dict[global][app]",
                create=create
            )

            init_dict["proc"] = MorPyDictUltra(
                name="app_dict[proc]",
                create=create
            )

            init_dict["proc"]["morpy"] = MorPyDictUltra(
                name="app_dict[proc][morPy]",
                create=create
            )

            init_dict["proc"]["morpy"][f'P{morpy_trace["process_id"]}'] = MorPyDictUltra(
                name=f'app_dict[proc][morPy][P{morpy_trace["process_id"]}]',
                create=create
            )

            init_dict["proc"]["morpy"][f'P{morpy_trace["process_id"]}'][f'T{morpy_trace["thread_id"]}'] = MorPyDictUltra(
                name=f'app_dict[proc][morPy][P{morpy_trace["process_id"]}][T{morpy_trace["thread_id"]}]',
                create=create
            )

            init_dict["proc"]["app"] = MorPyDictUltra(
                name="app_dict[proc][app]",
                create=create
            )

            init_dict["proc"]["app"][f'P{morpy_trace["process_id"]}'] = MorPyDictUltra(
                name=f'app_dict[proc][app][P{morpy_trace["process_id"]}]',
                create=create
            )

            init_dict["proc"]["app"][f'P{morpy_trace["process_id"]}'][f'T{morpy_trace["thread_id"]}'] = MorPyDictUltra(
                name=f'app_dict[proc][app][P{morpy_trace["process_id"]}][T{morpy_trace["thread_id"]}]',
                create=create
            )

            init_dict["loc"] = MorPyDictUltra(
                name="app_dict[loc]",
                create=create
            )

            init_dict["loc"]["morpy"] = MorPyDictUltra(
                name="app_dict[loc][morPy]",
                create=create
            )

            init_dict["loc"]["morpy_dgb"] = MorPyDictUltra(
                name="app_dict[loc][mpy_dbg]",
                create=create
            )

            init_dict["loc"]["app"] = MorPyDictUltra(
                name="app_dict[loc][app]",
                create=create
            )

            init_dict["loc"]["app_dbg"] = MorPyDictUltra(
                name="app_dict[loc][app_dbg]",
                create=create
            )

            init_dict["global"]["morpy"]["logs_generate"] = MorPyDictUltra(
                name="app_dict[global][morPy][logs_generate]",
                create=create
            )
        # Without GIL, allow for true nesting
        else:
            from lib.types_dict import MorPyDict

            init_dict = MorPyDict(
                name="app_dict",
            )

            init_dict["conf"] = MorPyDict(
                name="app_dict[conf]",
            )

            init_dict["sys"] = MorPyDict(
                name="app_dict[sys]",
            )

            init_dict["run"] = MorPyDict(
                name="app_dict[run]",
            )

            init_dict["global"] = MorPyDict(
                name="app_dict[global]",
            )

            init_dict["global"]["morpy"] = MorPyDict(
                name="app_dict[global][morPy]",
            )

            init_dict["global"]["app"] = MorPyDict(
                name="app_dict[global][app]",
            )

            init_dict["proc"] = MorPyDict(
                name="app_dict[proc]",
            )

            init_dict["proc"]["morpy"] = MorPyDict(
                name="app_dict[proc][morPy]",
            )

            init_dict["proc"]["morpy"][f'P{morpy_trace["process_id"]}'] = MorPyDict(
                name=f'app_dict[proc][morPy][P{morpy_trace["process_id"]}]',
            )

            init_dict["proc"]["morpy"][f'P{morpy_trace["process_id"]}'][f'T{morpy_trace["thread_id"]}'] = MorPyDict(
                name=f'app_dict[proc][morPy][P{morpy_trace["process_id"]}][T{morpy_trace["thread_id"]}]',
            )

            init_dict["proc"]["app"] = MorPyDict(
                name="app_dict[proc][app]",
            )

            init_dict["proc"]["app"][f'P{morpy_trace["process_id"]}'] = MorPyDict(
                name=f'app_dict[proc][app][P{morpy_trace["process_id"]}]',
            )

            init_dict["proc"]["app"][f'P{morpy_trace["process_id"]}'][f'T{morpy_trace["thread_id"]}'] = MorPyDict(
                name=f'app_dict[proc][app][P{morpy_trace["process_id"]}][T{morpy_trace["thread_id"]}]',
            )

            init_dict["loc"] = MorPyDict(
                name="app_dict[loc]",
            )

            init_dict["loc"]["morpy"] = MorPyDict(
                name="app_dict[loc][morPy]",
            )

            init_dict["loc"]["morpy_dgb"] = MorPyDict(
                name="app_dict[loc][mpy_dbg]",
            )

            init_dict["loc"]["app"] = MorPyDict(
                name="app_dict[loc][app]",
            )

            init_dict["loc"]["app_dbg"] = MorPyDict(
                name="app_dict[loc][app_dbg]",
            )

            init_dict["global"]["morpy"]["logs_generate"] = MorPyDict(
                name="app_dict[global][morPy][logs_generate]",
            )

    # Error detection
    except Exception as e:
        morpy_fct.handle_exception_init(e)
        raise

    finally:
        return init_dict

def types_dict_finalize(morpy_trace: dict, init_dict: dict) -> None:
    r"""
    This function locks parts of the global dictionary to streamline the use
    of app_dict as designed.

    :param morpy_trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)

    :return:
        -

    :example:
    >>> types_dict_finalize(morpy_trace, init_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'types_dict_finalize(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    try:
        init_dict._update_self(_access="tightened")
        init_dict["conf"]._update_self(_access="locked")
        init_dict["sys"]._update_self(_access="locked")
        init_dict["run"]._update_self(_access="tightened")
        init_dict["global"]._update_self(_access="tightened")
        init_dict["global"]["morpy"]._update_self(_access="normal")
        init_dict["global"]["morpy"]["logs_generate"]._update_self(_access="locked")
        init_dict["proc"]._update_self(_access="tightened")
        init_dict["proc"]["morpy"]._update_self(_access="tightened")
        init_dict["proc"]["app"]._update_self(_access="tightened")
        init_dict["loc"]._update_self(_access="locked")
        init_dict["loc"]["morpy"]._update_self(_access="locked")
        init_dict["loc"]["morpy_dgb"]._update_self(_access="locked")
        init_dict["loc"]["app"]._update_self(_access="locked")
        init_dict["loc"]["app_dbg"]._update_self(_access="locked")

    # Error detection
    except Exception as e:
        log_no_q(morpy_trace, init_dict, "error",
        lambda: f'{init_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                f'{init_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{init_dict["loc"]["morpy"]["err_excp"]}: {e}')

def morpy_log_header(morpy_trace: dict, init_dict: dict) -> None:
    r"""
    This function writes the header for the logfile including app specific
    information.

    :param morpy_trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)

    :return:
        -

    :example:
    >>> morpy_log_header(morpy_trace, init_dict)
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

def morpy_ref(morpy_trace: dict, init_dict: dict, init_dict_str: str) -> None:
    r"""
    This function documents the initialized dictionary (reference). It is stored
    in the same path as __main__.py and serves development purposes.

    :param morpy_trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)
    :param init_dict_str: String of the init_dict

    :return:
        -

    :example:
    >>> morpy_ref(morpy_trace, init_dict)
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
        log_no_q(morpy_trace, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["ref_created"]}\n'
                f'{init_dict["loc"]["morpy"]["ref_path"]}: {morpy_ref_path}')

    except Exception as e:
        log_no_q(morpy_trace, init_dict, "error",
        lambda: f'{init_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                f'{init_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{init_dict["loc"]["morpy"]["err_excp"]}: {e}')

def has_gil(morpy_trace: dict) -> bool | None:
    r"""
    Return True if we detect a standard GIL-based Python runtime on a 'typical' operating system.
    Return False if we suspect a 'no-gil' or 'free-threading' build on Linux/macOS/Windows, or if
    we detect certain alternative Pythons. This is *heuristic* and not a guaranteed official check.

    :param morpy_trace: operation credentials and tracing information

    :return gil_detected: If True, Python environment has GIL implemented. Process forking not supported.

    :example:
    >>> gil = has_gil(morpy_trace)
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

    except Exception as e:
        morpy_fct.handle_exception_init(e)