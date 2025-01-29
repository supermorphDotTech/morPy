r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import mpy
import sys

import mpy_mp
from mpy_decorators import metrics, log

@metrics
def _exit(mpy_trace: dict, app_dict: dict, app_run_return: dict, orchestrator) -> dict:

    r"""
    This function runs the exit workflow of the app.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_run_return: Return value (dict) of the app, returned by app_run
    :param orchestrator: Reference to the instantiated morPy orchestrator

    :return: dict
        mpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        orchestrator = app_dict["proc"]["mpy"]["cl_orchestrator"]
        init_retval = _init(mpy_trace, app_dict)
        run_retval = _run(mpy_trace, app_dict, init_retval)
        _exit(mpy_trace, app_dict, run_retval, orchestrator)
    """

    # morPy credentials (see mpy_init.init_cred() for all dict keys)
    module = 'app_exit'
    operation = '_exit(~)'
    mpy_trace = mpy.tracing(module, operation, mpy_trace)

    # OPTION enable/disable logging
    # ??? mpy_trace["log_enable"] = False

    check = False

    try:
        # TODO: first statement .join()
        # TODO: MY CODE
        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    finally:
        # TODO .join()
        # Signal morPy orchestrator of app termination
        mpy_mp.join_processes(mpy_trace, app_dict)
        orchestrator._terminate = True

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }