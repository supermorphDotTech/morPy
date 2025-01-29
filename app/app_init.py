r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import lib.morPy as morPy
from lib.decorators import metrics, log

import sys

@metrics
def _init(morPy_trace: dict, app_dict: dict) -> dict:

    r"""
    This function runs the initialization workflow of the app.

    :param morPy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        morPy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_init_return: Return value (dict) of the initialization process, handed to app_run

    :example:
        init_retval = _init(morPy_trace, app_dict)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app_init'
    operation = '_init(~)'
    morPy_trace = morPy.tracing(module, operation, morPy_trace)

    # OPTION enable/disable logging
    # ??? morPy_trace["log_enable"] = False

    check = False
    app_init_return = {}

    try:
        # TODO: MY CODE

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')
    finally:
        return{
            'morPy_trace' : morPy_trace,
            'check' : check,
            'app_init_return' : app_init_return
            }