r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import lib.morPy as morPy
import lib.mp as mp
from lib.decorators import metrics, log

import sys


@metrics
def app_exit(morpy_trace: dict, app_dict: dict, app_run_return: dict, orchestrator) -> dict:

    r"""
    This function runs the exit workflow of the app.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_run_return: Return value (dict) of the app, returned by app_run
    :param orchestrator: Reference to the instantiated morPy orchestrator

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        from app import init as app_init
        from app import run as app_run
        from app import exit as app_exit

        orchestrator = app_dict["proc"]["morpy"]["cl_orchestrator"]
        init_retval = app_init(morpy_trace, app_dict)
        run_retval = app_run(morpy_trace, app_dict, init_retval)
        app_exit(morpy_trace, app_dict, run_retval, orchestrator)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app.exit'
    operation = 'app_exit(~)'
    morpy_trace = morPy.tracing(module, operation, morpy_trace)

    # OPTION enable/disable logging
    # ??? morpy_trace["log_enable"] = False

    check = False

    try:
        # TODO: first statement .join()
        # TODO: MY CODE
        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{type(e).__name__}: {e}')

    finally:
        # TODO .join()
        # Signal morPy orchestrator of app termination
        mp.join_processes(morpy_trace, app_dict)
        orchestrator._terminate = True

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            }