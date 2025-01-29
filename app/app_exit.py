r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
import sys

import lib.mp as mp
from lib.decorators import metrics, log

@metrics
def _exit(morPy_trace: dict, app_dict: dict, app_run_return: dict, orchestrator) -> dict:

    r"""
    This function runs the exit workflow of the app.

    :param morPy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_run_return: Return value (dict) of the app, returned by app_run
    :param orchestrator: Reference to the instantiated morPy orchestrator

    :return: dict
        morPy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        orchestrator = app_dict["proc"]["morPy"]["cl_orchestrator"]
        init_retval = _init(morPy_trace, app_dict)
        run_retval = _run(morPy_trace, app_dict, init_retval)
        _exit(morPy_trace, app_dict, run_retval, orchestrator)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app_exit'
    operation = '_exit(~)'
    morPy_trace = morPy.tracing(module, operation, morPy_trace)

    # OPTION enable/disable logging
    # ??? morPy_trace["log_enable"] = False

    check = False

    try:
        # TODO: first statement .join()
        # TODO: MY CODE
        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    finally:
        # TODO .join()
        # Signal morPy orchestrator of app termination
        mp.join_processes(morPy_trace, app_dict)
        orchestrator._terminate = True

        return{
            'morPy_trace' : morPy_trace,
            'check' : check,
            }