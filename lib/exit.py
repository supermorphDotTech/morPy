r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers functions to handle exiting the app.
"""

import lib.fct as morpy_fct
from lib.decorators import metrics, log_no_q

import sys

@metrics
def _exit(morpy_trace: dict=None, app_dict: dict=None):
    r"""
    This is the mpy exit routine. It is not intended to be used as part of an app, but it may be executed however,
    at any time after initialization.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: The mpy-specific global dictionary

    :return:
        -

    :example:
        exit._exit(morpy_trace, app_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'lib.exit'
    operation = '_exit(~)'
    morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

    try:
        # Retrieve exit time and date
        datetime_exit = morpy_fct.datetime_now()

        # determine runtime duration
        temp_duration = morpy_fct.runtime(app_dict["run"]["init_datetime_value"])

        # Correction of the exit occurrance counter for the very last message
        app_dict["run"]["events_EXIT"] += 1
        app_dict["run"]["events_total"] += 1

        # Determine leading spaces before app_dict["exit_msg_total"] so the colons
        # of the exit message fall in one vertcal line.
        spaces_total = 9 - len(app_dict["loc"]["morpy"]["exit_msg_total"])
        leading_total = f'{spaces_total * " "}'

        # Build the exit message
        log_no_q(morpy_trace, app_dict, "exit",
        lambda: f'{app_dict["loc"]["morpy"]["exit_msg_done"]}\n'
                f'{app_dict["loc"]["morpy"]["exit_msg_started"]}: {app_dict["run"]["init_date"]} {app_dict["loc"]["morpy"]["exit_msg_at"]} {app_dict["run"]["init_time"]}\n'
                f'{app_dict["loc"]["morpy"]["exit_msg_exited"]}: {datetime_exit["date"]} {app_dict["loc"]["morpy"]["exit_msg_at"]} {datetime_exit["time"]}\n'
                f'{app_dict["loc"]["morpy"]["exit_msg_duration"]}: {temp_duration["rnt_delta"]}\n\n'
                f'{5 * "-"} {app_dict["loc"]["morpy"]["exit_msg_events"]} {5 * "-"}\n'
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
                f'{leading_total}{app_dict["loc"]["morpy"]["exit_msg_total"]}: {app_dict["run"]["events_total"]}')

    except Exception as e:
        log_no_q(morpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')