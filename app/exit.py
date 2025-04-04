r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from lib.mp import join_or_task
from lib.decorators import metrics, log

import sys
from UltraDict import UltraDict

@metrics
def app_exit(morpy_trace: dict, app_dict: dict | UltraDict, app_run_return: dict) -> dict:
    r"""
    This function runs the exit workflow of the app.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_run_return: Return value (dict) of the app, returned by app_run.
        This dictionary is not shared with other processes by default.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        from app import init as app_init
        from app import run as app_run
        from app import exit as app_exit

        # Assuming app_dict is initialized correctly
        init_retval = app_init(morpy_trace, app_dict)
        run_retval = app_run(morpy_trace, app_dict, init_retval)
        app_exit(morpy_trace, app_dict, run_retval)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module: str = 'app.exit'
    operation: str = 'app_exit(~)'
    morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

    # OPTION enable/disable logging
    # ??? morpy_trace["log_enable"] = False

    check: bool = False

    try:
        # TODO: MY CODE
        check: bool = True

    except Exception as e:
        raise morPy.exception(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    finally:
        # Join all spawned processes before transitioning into the next phase.
        join_or_task(morpy_trace, app_dict, reset_trace=True, reset_w_prefix=f'{module}.{operation}')
        # Signal morPy orchestrator of app termination
        if isinstance(app_dict["morpy"], UltraDict):
            with app_dict["morpy"].lock:
                app_dict["morpy"]["exit"] = True
        else:
            app_dict["morpy"]["exit"] = True

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            }