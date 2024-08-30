"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers functions to handle exiting the project.
"""

from mpy_decorators import metrics

@metrics
def exit(mpy_trace, prj_dict):

    import mpy_mt, mpy_fct, mpy_msg
    import sys, gc

    """ This is the mpy exit routine. It may be executed at any time after
        initialization.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
    :return
        -
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_exit'
    operation = 'exit(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Wait for all threads to finish their current tasks
    mpy_mt.mpy_threads_joinall(mpy_trace, prj_dict)

    # Evaluate the usage of mpy_xl
    if 'mpy_xl_loaded_wb_lst' in prj_dict:

        import mpy_xl

        # Clean up RAM: Close all MS Excel Workbooks
        mpy_xl.wb_close_all(mpy_trace, prj_dict)

    # Retrieve exit time and date
    datetime_exit = mpy_fct.datetime_now(mpy_trace)

    # determine runtime duration
    temp_duration = mpy_fct.runtime(mpy_trace, prj_dict["run"]["init_datetime_value"])

    # Correction of the exit occurrance counter for the very last message
    prj_dict["run"]["events_EXIT"] += 1
    prj_dict["run"]["events_total"] += 1

    # Determine leading spaces before prj_dict["mpy_exit_msg_total"] so the colons
    # of the exit message fall in one vertcal line.
    spaces_total = 9 - len(prj_dict["loc"]["mpy"]["mpy_exit_msg_total"])
    leading_total = f'{spaces_total * " "}'

    # Build the exit message
    exit_message =  (f'{prj_dict["loc"]["mpy"]["mpy_exit_msg_done"]}\n'
                    f'{prj_dict["loc"]["mpy"]["mpy_exit_msg_started"]}: {prj_dict["run"]["init_date"]} {prj_dict["loc"]["mpy"]["mpy_exit_msg_at"]} {prj_dict["run"]["init_time"]}\n'
                    f'{prj_dict["loc"]["mpy"]["mpy_exit_msg_exited"]}: {datetime_exit["date"]} {prj_dict["loc"]["mpy"]["mpy_exit_msg_at"]} {datetime_exit["time"]}\n'
                    f'{prj_dict["loc"]["mpy"]["mpy_exit_msg_duration"]}: {temp_duration["rnt_delta"]}\n\n'
                    f'{prj_dict["loc"]["mpy"]["mpy_exit_msg_occ"]}:\n'
                    f'     INIT: {prj_dict["run"]["events_INIT"]}\n'
                    f'    DEBUG: {prj_dict["run"]["events_DEBUG"]}\n'
                    f'     INFO: {prj_dict["run"]["events_INFO"]}\n'
                    f'  WARNING: {prj_dict["run"]["events_WARNING"]}\n'
                    f'   DENIED: {prj_dict["run"]["events_DENIED"]}\n'
                    f'    ERROR: {prj_dict["run"]["events_ERROR"]}\n'
                    f' CRITICAL: {prj_dict["run"]["events_CRITICAL"]}\n'
                    f'     EXIT: {prj_dict["run"]["events_EXIT"]}\n'
                    f'UNDEFINED: {prj_dict["run"]["events_UNDEFINED"]}\n'
                    f'{18 * "-"}\n'
                    f'{leading_total}{prj_dict["loc"]["mpy"]["mpy_exit_msg_total"]}: {prj_dict["run"]["events_total"]}')

    # Correction of the exit occurrance counter for the very last message
    prj_dict["run"]["events_EXIT"] = int(prj_dict["run"]["events_EXIT"]) - 1
    prj_dict["run"]["events_total"] = int(prj_dict["run"]["events_total"]) - 1

    # Create a log
    mpy_msg.log(mpy_trace, prj_dict, exit_message, 'exit')

    # Delete the project dictionary and trash
    del prj_dict
    del mpy_trace
    gc.collect()

    # Quit the program
    sys.exit()