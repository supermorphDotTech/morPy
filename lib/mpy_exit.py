r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers functions to handle exiting the app.
"""

import mpy_fct
import sys

from mpy_decorators import metrics, log_no_q

@metrics
def _exit(mpy_trace: dict=None, app_dict: dict=None):

    r"""
    This is the mpy exit routine. It may be executed at any time after
    initialization.

    :param mpy_trace: operation credentials and tracing
    :param app_dict: The mpy-specific global dictionary

    :return:
        -

    :example:
        mpy_exit._exit(mpy_trace, app_dict)
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_exit'
    operation = '_exit(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    try:
        # Wait for all threads to finish their current tasks
        # TODO wait for mp and mt processes to finish up
        # TODO implement a timeout, as all tasks should be finished at this point anyway
        # mpy_mt.mpy_threads_joinall(mpy_trace, app_dict)

        # Retrieve exit time and date
        datetime_exit = mpy_fct.datetime_now(mpy_trace)

        # determine runtime duration
        temp_duration = mpy_fct.runtime(mpy_trace, app_dict["run"]["init_datetime_value"])

        # Correction of the exit occurrance counter for the very last message
        app_dict["run"]["events_EXIT"] += 1
        app_dict["run"]["events_total"] += 1

        # Determine leading spaces before app_dict["mpy_exit_msg_total"] so the colons
        # of the exit message fall in one vertcal line.
        spaces_total = 9 - len(app_dict["loc"]["mpy"]["mpy_exit_msg_total"])
        leading_total = f'{spaces_total * " "}'

        # Build the exit message
        log_no_q(mpy_trace, app_dict, "exit",
        lambda: f'{app_dict["loc"]["mpy"]["mpy_exit_msg_done"]}\n'
                f'{app_dict["loc"]["mpy"]["mpy_exit_msg_started"]}: {app_dict["run"]["init_date"]} {app_dict["loc"]["mpy"]["mpy_exit_msg_at"]} {app_dict["run"]["init_time"]}\n'
                f'{app_dict["loc"]["mpy"]["mpy_exit_msg_exited"]}: {datetime_exit["date"]} {app_dict["loc"]["mpy"]["mpy_exit_msg_at"]} {datetime_exit["time"]}\n'
                f'{app_dict["loc"]["mpy"]["mpy_exit_msg_duration"]}: {temp_duration["rnt_delta"]}\n\n'
                f'{5 * "-"} {app_dict["loc"]["mpy"]["mpy_exit_msg_events"]} {5 * "-"}\n'
                f'     INIT: {app_dict["run"]["events_INIT"]}\n'
                f'    DEBUG: {app_dict["run"]["events_DEBUG"]}\n'
                f'     INFO: {app_dict["run"]["events_INFO"]}\n'
                f'  WARNING: {app_dict["run"]["events_WARNING"]}\n'
                f'   DENIED: {app_dict["run"]["events_DENIED"]}\n'
                f'    ERROR: {app_dict["run"]["events_ERROR"]}\n'
                f' CRITICAL: {app_dict["run"]["events_CRITICAL"]}\n'
                f'     EXIT: {app_dict["run"]["events_EXIT"]}\n'
                f'UNDEFINED: {app_dict["run"]["events_UNDEFINED"]}\n'
                f'{18 * "-"}\n'
                f'{leading_total}{app_dict["loc"]["mpy"]["mpy_exit_msg_total"]}: {app_dict["run"]["events_total"]}')

    except Exception as e:
        log_no_q(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')