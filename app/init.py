r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from lib.mp import join_or_task
from lib.fct import tracing as init_tracing
from lib.decorators import metrics, log

import sys
from UltraDict import UltraDict

@metrics
def app_init(morpy_trace: dict, app_dict: dict | UltraDict) -> dict:
    r"""
    This function runs the initialization workflow of the app.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_init_return: Return value (dict) of the initialization process, handed to app_run

    :example:
        from app import init as app_init
        init_retval = app_init(morpy_trace, app_dict)
    """

    try:
        if isinstance(app_dict, UltraDict):
            with app_dict["morpy"]["orchestrator"].lock:
                mp = app_dict["morpy"]["orchestrator"]["mp"]
        else:
            mp = False
    except:
        # Gracefully pass in single-core mode
        pass

    # morPy credentials (see init.init_cred() for all dict keys)
    module: str = 'app.init'
    operation: str = 'app_init(~)'
    morpy_trace: dict = init_tracing(module, operation, morpy_trace, reset=mp)

    # OPTION enable/disable logging
    # ??? morpy_trace["log_enable"] = False

    check: bool = False
    app_init_return = {}

    try:
        # TODO: MY CODE

        check: bool = True

    except Exception as e:
        raise morPy.exception(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    finally:
        # Join all spawned processes before transitioning into the next phase.
        join_or_task(morpy_trace, app_dict, reset_trace=True, reset_w_prefix=f'{module}.{operation}')

        # Initialization complete flag
        # TODO Up until this point prints to console are mirrored on splash screen
        if isinstance(app_dict["run"], UltraDict):
            with app_dict["run"].lock:
                app_dict["run"]["init_complete"] = True
        else:
            app_dict["run"]["init_complete"] = True

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            'app_init_return' : app_init_return
            }