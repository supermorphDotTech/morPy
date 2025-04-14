r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers functions to handle exiting the app.
"""

import lib.fct as morpy_fct
from morPy import log
from lib.decorators import core_wrap

import sys


@core_wrap
def end_runtime(trace: dict, app_dict: dict) -> None:
    r"""
    Finalizes the morPy runtime by retrieving the exit timestamp, calculating the total runtime,
    logging event counters and exit details, and then calling sys.exit() to terminate the application.

    :param trace: operation credentials and tracing
    :param app_dict: The mpy-specific global dictionary

    :example:
        from lib.exit import end_runtime
        end_runtime(trace, app_dict)
    """

    # Retrieve exit time and date
    datetime_exit = morpy_fct.datetime_now()

    # determine runtime duration
    temp_duration = morpy_fct.runtime(app_dict["morpy"]["init_datetime_value"])

    # Correction of the exit occurrence counter for the very last message
    app_dict["morpy"]["events_EXIT"] += 1
    app_dict["morpy"]["events_total"] += 1

    # Determine leading spaces before app_dict["exit_msg_total"] so the colons
    # of the exit message fall in one vertcal line.
    spaces_total = 9 - len(app_dict["loc"]["morpy"]["exit_msg_total"])

    # Build the exit message
    log(trace, app_dict, "exit",
        lambda: f'{app_dict["loc"]["morpy"]["exit_msg_done"]}\n'
                f'{app_dict["loc"]["morpy"]["exit_msg_started"]}: {app_dict["morpy"]["init_date"]} {app_dict["loc"]["morpy"]["exit_msg_at"]} {app_dict["morpy"]["init_time"]}\n'
                f'{app_dict["loc"]["morpy"]["exit_msg_exited"]}: {datetime_exit["date"]} {app_dict["loc"]["morpy"]["exit_msg_at"]} {datetime_exit["time"]}\n'
                f'{app_dict["loc"]["morpy"]["exit_msg_duration"]}: {temp_duration["rnt_delta"]}\n\n'
                f'{5 * "-"} {app_dict["loc"]["morpy"]["exit_msg_events"]} {5 * "-"}\n'
                f'     INIT: {app_dict["morpy"]["events_INIT"]}\n'
                f'    DEBUG: {app_dict["morpy"]["events_DEBUG"]}\n'
                f'     INFO: {app_dict["morpy"]["events_INFO"]}\n'
                f'  WARNING: {app_dict["morpy"]["events_WARNING"]}\n'
                f'   DENIED: {app_dict["morpy"]["events_DENIED"]}\n'
                f'    ERROR: {app_dict["morpy"]["events_ERROR"]}\n'
                f' CRITICAL: {app_dict["morpy"]["events_CRITICAL"]}\n'
                f'     EXIT: {app_dict["morpy"]["events_EXIT"]}\n'
                f'UNDEFINED: {app_dict["morpy"]["events_UNDEFINED"]}\n'
                f'{18 * "-"}\n'
                f'{spaces_total * " "}{app_dict["loc"]["morpy"]["exit_msg_total"]}: {app_dict["morpy"]["events_total"]}')

    sys.exit(0)