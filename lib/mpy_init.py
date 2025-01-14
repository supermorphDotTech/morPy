r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module holds all functions used for initialization of the
            morPy framework.
"""

import mpy_fct
import mpy_conf
import mpy_mp
import sys
import os
import importlib

# from mpy_dict_BACKUP import cl_mpy_dict
from mpy_common import cl_priority_queue
from mpy_decorators import log_no_q


def init_cred():

    r""" This function initializes the operation credentials and tracing.
    :param
        -
    :return - dictionary
        mpy_trace - operation credentials and tracing
    """

    # Initialize operation credentials and tracing.
    # Each operation/function/object will fill the dictionary with data
    # by executing mpy_trace = mpy.tracing(module, operation, mpy_trace)
    # as a first step before execution.
    mpy_trace = {
        'module' : '__main__',
        'operation' : '',
        'tracing' : '__main__',
        'process_id' : 0,
        'thread_id' : 0,
        'task_id' : 0,
        'log_enable' : False,
        'interrupt_enable' : False,
    }

    return mpy_trace

def init(mpy_trace):

    r""" This function initializes the app dictionary and yields app
        specific information to be handed down through called functions.
    :param
        mpy_trace - operation credentials and tracing
    :return - dictionary
        app_dict - morPy global dictionary containing app configurations

    TODO init log_db and store connection in app_dict
    TODO provide cleanups of log_db lock (conn) in exit functions
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_init'
    operation = 'init(~)'
    mpy_trace_init = mpy_fct.tracing(module, operation, mpy_trace)

    try:
        # ############################################
        # START Single-threaded initialization
        # ############################################

        # Build the app_dict
        init_dict = mpy_dict_build(mpy_trace_init)

        init_dict["proc"]["mpy"].update({"tasks_created" : mpy_trace_init["task_id"]})
        init_dict["proc"]["mpy"].update({"proc_available" : set()})
        init_dict["proc"]["mpy"].update({"proc_busy" : set(range(mpy_trace_init["process_id"]))})
        init_dict["proc"]["mpy"].update({"proc_refs" : []})

        # Initialize the global interrupt flag
        init_dict["global"]["mpy"].update({"mpy_interrupt" : False})

        # Set an initialization complete flag
        init_dict["run"]["init_complete"] = False

        # Retrieve the starting time of the program
        init_datetime = mpy_fct.datetime_now(mpy_trace_init)

        # Store the start time and timestamps in the dictionary
        for time_key in init_datetime:
            init_dict["run"][f'init_{time_key}'] = init_datetime[f'{time_key}']

        # Update the initialize dictionary with the parameters dictionary
        init_dict["conf"].update(mpy_conf.parameters(start_time=init_dict["run"]["init_datetimestamp"]))

        # Evaluate log_enable
        if not init_dict["conf"]["mpy_log_db_enable"] and not init_dict["conf"]["mpy_log_txt_enable"]:
            init_dict["conf"]["mpy_log_enable"] = False

        # Pass down the log enabling parameter
        mpy_trace["log_enable"] = init_dict["conf"]["mpy_log_enable"]
        mpy_trace_init["log_enable"] = init_dict["conf"]["mpy_log_enable"]

        # Import the morPy core functions localization into init_dict.
        mpy_loc = importlib.import_module(init_dict["conf"]["localization"])
        init_dict["loc"]["mpy"].update(getattr(mpy_loc, 'loc_mpy')())

        # Build nested dictionary for log generation
        log_levels = ("init", "debug", "info", "warning", "denied", "error", "critical", "exit")
        for log_level in log_levels:
            if (
                (init_dict["conf"]["mpy_log_enable"] and
                 not (log_level in init_dict["conf"]["mpy_log_lvl_nolog"])
                 ) or (
                init_dict["conf"]["mpy_msg_print"] and
                 not (log_level in init_dict["conf"]["mpy_log_lvl_noprint"]))
            ):
                init_dict["global"]["mpy"]["logs_generate"].update({log_level : True})
            else:
                init_dict["global"]["mpy"]["logs_generate"].update({log_level : False})

        # Retrieve system information
        sysinfo = mpy_fct.sysinfo(mpy_trace_init)

        # Update init_dict with system information
        for sys_key in sysinfo:
            init_dict["sys"][sys_key] = sysinfo[sys_key]

        # Test for elevated privileges
        mpy_fct.privileges_handler(mpy_trace_init, init_dict)

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
        if (init_dict["conf"]["mpy_log_txt_header_enable"] and
            mpy_trace_init["log_enable"] and
            init_dict["conf"]["mpy_log_txt_enable"]
        ):
            mpy_log_header(mpy_trace_init, init_dict)

        # TODO Initialize the priority queue and Multithreading
        # Logging may start after this
        init_dict["proc"]["mpy"]["process_q"] = cl_priority_queue(
            mpy_trace_init, init_dict, name="morPy priority queue", is_manager=True
        )
        # TODO Threading
        # mpy_mt.mt_init(mpy_trace_init, init_dict)

        # Initialize the morPy debug-specific localization
        init_dict["loc"]["mpy_dbg"].update(getattr(mpy_loc, 'loc_mpy_dbg')())
        log_no_q(mpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["mpy"]["init_loc_dbg_loaded"]}')

        # Initialize the app-specific localization
        init_dict["loc"]["app"].update(getattr(mpy_loc, 'loc_app')())
        init_dict["loc"]["app_dbg"].update(getattr(mpy_loc, 'loc_app_dbg')())
        log_no_q(mpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["mpy"]["init_loc_app_loaded"]}')

        # Localization initialized.
        log_no_q(mpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["mpy"]["init_loc_finished"]}')

        # Load init_dict as a string
        if (init_dict["conf"]["mpy_print_init_vars"] or init_dict["conf"]["mpy_ref_create"]):
            init_dict_str = mpy_fct.app_dict_to_string(init_dict)

        # Print init_dict to console
        if init_dict["conf"]["mpy_print_init_vars"]:
            print(init_dict_str)

        # Initialize the morPy orchestrator
        init_dict["proc"]["mpy"]["cl_orchestrator"] = mpy_mp.cl_orchestrator(mpy_trace_init, init_dict)

        # Activate priority queue
        init_dict["proc"]["mpy"]["process_q"]._init_mp(mpy_trace_init, init_dict)

        # Initialize Multiprocessing dictionary
        if init_dict["proc"]["mpy"]["cl_orchestrator"].processes_max > 1:
            # TODO finish Multiprocessing dictionary
            # TODO initialize Multiprocessing dictionary
            pass

        # ############################################
        # END Single-threaded initialization
        # START Multi-threaded initialization
        # ############################################

        # task = mpy.testprint(mpy_trace_init, "Message")
        # mpy_mp.run_parallel(mpy_task, app_dict, task)

        # ############################################
        # END Multi-threaded initialization
        # ############################################

        # Calculate the runtime of the initialization routine
        init_duration = mpy_fct.runtime(mpy_trace_init, init_dict["run"]["init_datetime_value"])

        # Record the duration of the initialization
        init_dict["run"]["init_rnt_delta"] = init_duration["rnt_delta"]

        log_no_q(mpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["mpy"]["init_finished"]}\n'
            f'{init_dict["loc"]["mpy"]["init_duration"]}: {init_dict["run"]["init_rnt_delta"]}')

        # Lock and tighten nested dictionaries
        mpy_dict_finalize(mpy_trace_init, init_dict)

        # Write app_dict to file: initialized_app_dict.txt
        if init_dict["conf"]["mpy_ref_create"]:
            mpy_ref(mpy_trace_init, init_dict, init_dict_str)

        # Set an initialization complete flag
        init_dict["run"]["init_complete"] = True

        # Exit initialization
        retval = init_dict, init_dict["proc"]["mpy"]["cl_orchestrator"]
        return retval

    except Exception as e:
        mpy_fct.handle_exception_init(e)
        raise

def mpy_dict_build(mpy_trace: dict):

    r"""
    This function builds the app_dict. This is needed in spawned processes, too
    to successfully link the nested dictionaries.

    :param mpy_trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)

    :return:
        init_dict

    :example:
        init_dict = mpy_init.mpy_dict_build(mpy_trace, create=True)
    """

    from lib.mpy_dict import cl_mpy_dict, cl_mpy_dict

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_init'
    operation = 'mpy_dict_build(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    try:
        init_dict = cl_mpy_dict(
            name="app_dict",
        )

        init_dict["conf"] = cl_mpy_dict(
            name="app_dict[conf]",
        )

        init_dict["sys"] = cl_mpy_dict(
            name="app_dict[sys]",
        )

        init_dict["run"] = cl_mpy_dict(
            name="app_dict[run]",
        )

        init_dict["global"] = cl_mpy_dict(
            name="app_dict[global]",
        )

        init_dict["global"]["mpy"] = cl_mpy_dict(
            name="app_dict[global][mpy]",
        )

        init_dict["global"]["app"] = cl_mpy_dict(
            name="app_dict[global][app]",
        )

        init_dict["proc"] = cl_mpy_dict(
            name="app_dict[proc]",
        )

        init_dict["proc"]["mpy"] = cl_mpy_dict(
            name="app_dict[proc][mpy]",
        )

        init_dict["proc"]["mpy"][f'P{mpy_trace["process_id"]}'] = cl_mpy_dict(
            name=f'app_dict[proc][mpy][P{mpy_trace["process_id"]}]',
        )

        init_dict["proc"]["mpy"][f'P{mpy_trace["process_id"]}'][f'T{mpy_trace["thread_id"]}'] = cl_mpy_dict(
            name=f'app_dict[proc][mpy][P{mpy_trace["process_id"]}][T{mpy_trace["thread_id"]}]',
        )

        init_dict["proc"]["app"] = cl_mpy_dict(
            name="app_dict[proc][app]",
        )

        init_dict["proc"]["app"][f'P{mpy_trace["process_id"]}'] = cl_mpy_dict(
            name=f'app_dict[proc][app][P{mpy_trace["process_id"]}]',
        )

        init_dict["proc"]["app"][f'P{mpy_trace["process_id"]}'][f'T{mpy_trace["thread_id"]}'] = cl_mpy_dict(
            name=f'app_dict[proc][app][P{mpy_trace["process_id"]}][T{mpy_trace["thread_id"]}]',
        )

        init_dict["loc"] = cl_mpy_dict(
            name="app_dict[loc]",
        )

        init_dict["loc"]["mpy"] = cl_mpy_dict(
            name="app_dict[loc][mpy]",
        )

        init_dict["loc"]["mpy_dbg"] = cl_mpy_dict(
            name="app_dict[loc][mpy_dbg]",
        )

        init_dict["loc"]["app"] = cl_mpy_dict(
            name="app_dict[loc][app]",
        )

        init_dict["loc"]["app_dbg"] = cl_mpy_dict(
            name="app_dict[loc][app_dbg]",
        )

        init_dict["global"]["mpy"]["logs_generate"] = cl_mpy_dict(
            name="app_dict[global][mpy][logs_generate]",
        )

    # Error detection
    except Exception as e:
        log_no_q(mpy_trace, init_dict, "error",
        lambda: f'{init_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{init_dict["loc"]["mpy"]["err_excp"]}: {e}')

    finally:
        return init_dict

def mpy_dict_finalize(mpy_trace: dict, init_dict: dict):

    r"""
    This function locks parts of the global dictionary to streamline the use
    of app_dict as designed.

    :param mpy_trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)

    :return:
        -

    :example:
        mpy_init.mpy_dict_finalize(mpy_trace, init_dict)
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_init'
    operation = 'mpy_dict_finalize(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    try:
        init_dict._update_self(_access="tightened")
        init_dict["conf"]._update_self(_access="locked")
        init_dict["sys"]._update_self(_access="locked")
        init_dict["run"]._update_self(_access="tightened")
        init_dict["global"]._update_self(_access="tightened")
        init_dict["global"]["mpy"]._update_self(_access="normal")
        init_dict["global"]["mpy"]["logs_generate"]._update_self(_access="locked")
        init_dict["proc"]._update_self(_access="tightened")
        init_dict["proc"]["mpy"]._update_self(_access="tightened")
        init_dict["proc"]["app"]._update_self(_access="tightened")
        init_dict["loc"]._update_self(_access="locked")
        init_dict["loc"]["mpy"]._update_self(_access="locked")
        init_dict["loc"]["mpy_dbg"]._update_self(_access="locked")
        init_dict["loc"]["app"]._update_self(_access="locked")
        init_dict["loc"]["app_dbg"]._update_self(_access="locked")

    # Error detection
    except Exception as e:
        log_no_q(mpy_trace, init_dict, "error",
        lambda: f'{init_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{init_dict["loc"]["mpy"]["err_excp"]}: {e}')

def mpy_log_header(mpy_trace: dict, init_dict: dict):

    r"""
    This function writes the header for the logfile including app specific
    information.

    :param mpy_trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)

    :return:

    :example:
        mpy_log_header(mpy_trace, init_dict)
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_init'
    operation = 'mpy_log_header(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Create the app header
    content = (
        f'== {init_dict["loc"]["mpy"]["mpy_log_header_start"]}{3*" =="}\n\t'
        f'{init_dict["loc"]["mpy"]["mpy_log_header_author"]}: Bastian Neuwirth\n\t'
        f'{init_dict["loc"]["mpy"]["mpy_log_header_app"]}: {init_dict["conf"]["main_path"]}\n\t'
        f'{init_dict["loc"]["mpy"]["mpy_log_header_timestamp"]}: {init_dict["run"]["init_datetimestamp"]}\n\t'
        f'{init_dict["loc"]["mpy"]["mpy_log_header_user"]}: {init_dict["sys"]["username"]}\n\t'
        f'{init_dict["loc"]["mpy"]["mpy_log_header_system"]}: {init_dict["sys"]["os"]} {init_dict["sys"]["os_release"]}\n\t'
        f'{init_dict["loc"]["mpy"]["mpy_log_header_version"]}: {init_dict["sys"]["os_version"]}\n\t'
        f'{init_dict["loc"]["mpy"]["mpy_log_header_architecture"]}: {init_dict["sys"]["os_arch"]}\n\t'
        f'{init_dict["loc"]["mpy"]["mpy_log_header_threads"]}: {init_dict["sys"]["threads"]}\n'
        f'== {init_dict["loc"]["mpy"]["mpy_log_header_begin"]}{3*" =="}\n'
    )

    # Write to the logfile
    filepath = init_dict["conf"]["log_txt_path"]
    mpy_fct.txt_wr(mpy_trace, init_dict, filepath, content)

    # Clean up
    del mpy_trace

def mpy_ref(mpy_trace: dict, init_dict: dict, init_dict_str: str):

    r"""
    This function documents the initialized dictionary (reference). It is stored
    in the same path as __main__.py and serves development purposes.

    :param mpy_trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)
    :param init_dict_str: String of the init_dict

    :return:

    :example:
        mpy_ref(mpy_trace, init_dict)
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_init'
    operation = 'mpy_ref(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    try:
        mpy_ref_path = os.path.join(f'{init_dict["conf"]["main_path"]}', 'initialized_app_dict.txt')
        mpy_init_dict = open(mpy_ref_path,'w')

        # Write init_dict to file
        mpy_init_dict.write(f'{init_dict["loc"]["mpy"]["mpy_ref_descr"]}\n\n')
        mpy_init_dict.write(init_dict_str)

        # Close the file
        mpy_init_dict.close()

        # The init_dict was written to textfile.
        log_no_q(mpy_trace, init_dict, "init",
        lambda: f'{init_dict["loc"]["mpy"]["mpy_ref_created"]}\n'
            f'{init_dict["loc"]["mpy"]["mpy_ref_path"]}: {mpy_ref_path}')

    except Exception as e:
        log_no_q(mpy_trace, init_dict, "error",
        lambda: f'{init_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{init_dict["loc"]["mpy"]["err_excp"]}: {e}')