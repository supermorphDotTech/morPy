r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from lib.decorators import metrics, log

import sys

@metrics
def app_init(morpy_trace: dict, app_dict: dict) -> dict:

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

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app.init'
    operation = 'app_init(~)'
    morpy_trace = morPy.tracing(module, operation, morpy_trace)

    # OPTION enable/disable logging
    # ??? morpy_trace["log_enable"] = False

    check = False
    app_init_return = {}

    try:
        # TODO: MY CODE

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{type(e).__name__}: {e}')
    finally:
        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            'app_init_return' : app_init_return
            }