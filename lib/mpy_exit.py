"""
Author:     Bastian Neuwirth
Date:       28.06.2021
Version:    0.1
Descr.:     This module delivers functions to handle exiting the project.
"""

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

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_exit'
    operation = 'exit(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Wait for all threads to finish their current tasks
    mpy_mt.mpy_threads_joinall(mpy_trace, prj_dict)

#   Evaluate the usage of mpy_xl
    if 'mpy_xl_loaded_wb_lst' in prj_dict:

        import mpy_xl

    #   Clean up RAM: Close all MS Excel Workbooks
        mpy_xl.wb_close_all(mpy_trace, prj_dict)

#   Retrieve exit time and date
    datetime_exit = mpy_fct.datetime_now(mpy_trace)

#   determine runtime duration
    temp_duration = mpy_fct.runtime(mpy_trace, prj_dict["init_datetime_value"])

#   Correction of the exit occurrance counter for the very last message
    prj_dict["events_EXIT"] += 1
    prj_dict["events_total"] += 1

#   Determine leading spaces before prj_dict["mpy_exit_msg_total"] so the colons
#   of the exit message fall in one vertcal line.
    spaces_total = 9 - len(prj_dict["mpy_exit_msg_total"])
    leading_total = f'{spaces_total * " "}'

#   Build the exit message
    exit_message =  (f'{prj_dict["mpy_exit_msg_done"]}\n'
                    f'{prj_dict["mpy_exit_msg_started"]}: {prj_dict["init_date"]} {prj_dict["mpy_exit_msg_at"]} {prj_dict["init_time"]}\n'
                    f'{prj_dict["mpy_exit_msg_exited"]}: {datetime_exit["date"]} {prj_dict["mpy_exit_msg_at"]} {datetime_exit["time"]}\n'
                    f'{prj_dict["mpy_exit_msg_duration"]}: {temp_duration["rnt_delta"]}\n\n'
                    f'{prj_dict["mpy_exit_msg_occ"]}:\n'
                    f'     INIT: {prj_dict["events_INIT"]}\n'
                    f'    DEBUG: {prj_dict["events_DEBUG"]}\n'
                    f'     INFO: {prj_dict["events_INFO"]}\n'
                    f'  WARNING: {prj_dict["events_WARNING"]}\n'
                    f'   DENIED: {prj_dict["events_DENIED"]}\n'
                    f'    ERROR: {prj_dict["events_ERROR"]}\n'
                    f' CRITICAL: {prj_dict["events_CRITICAL"]}\n'
                    f'     EXIT: {prj_dict["events_EXIT"]}\n'
                    f'UNDEFINED: {prj_dict["events_UNDEFINED"]}\n'
                    f'{18 * "-"}\n'
                    f'{leading_total}{prj_dict["mpy_exit_msg_total"]}: {prj_dict["events_total"]}')

#   Correction of the exit occurrance counter for the very last message
    prj_dict["events_EXIT"] = int(prj_dict["events_EXIT"]) - 1
    prj_dict["events_total"] = int(prj_dict["events_total"]) - 1

#   Create a log
    mpy_msg.log(mpy_trace, prj_dict, exit_message, 'exit')

#   Delete the project dictionary and trash
    del prj_dict
    del mpy_trace
    gc.collect()

#   Quit the program
    sys.exit()