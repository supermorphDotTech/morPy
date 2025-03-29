r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from lib.mp import join_processes_for_transition
from lib.decorators import metrics, log

import sys

@metrics
def app_run(morpy_trace: dict, app_dict: dict, app_init_return: dict) -> dict:
    r"""
    This function runs the main workflow of the app.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_init_return: Return value (dict) of the initialization process, returned by app_init

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_run_return: Return value (dict) of the app process, handed to app_exit

    :example:
        from app import init as app_init
        from app import run as app_run

        init_retval = app_init(morpy_trace, app_dict)
        run_retval = app_run(morpy_trace, app_dict, init_retval)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module: str = 'app.run'
    operation: str = 'app_run(~)'
    morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

    check: bool = False
    app_run_return = {}

    try:
        # Demonstrate how to use lib.ui_tk.ProgressTrackerTk()
        import demo.ProgressTrackerTk as demo_ProgressTrackerTk
        demo_ProgressTrackerTk.run(morpy_trace, app_dict)

        check: bool = True

    except Exception as e:
        raise morPy.exception(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    finally:
        # Join all spawned processes before transitioning into the next phase.
        join_processes_for_transition(morpy_trace, app_dict)

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            'app_run_return' : app_run_return
            }