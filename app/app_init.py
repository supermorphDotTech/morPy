r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import mpy
import sys

from mpy_decorators import metrics, log

@metrics
def _init(mpy_trace: dict, app_dict: dict) -> dict:

    r"""
    This function runs the initialization workflow of the app.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        mpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_init_return: Return value (dict) of the initialization process, handed to app_run

    :example:
        init_retval = _init(mpy_trace, app_dict)
    """

    # morPy credentials (see mpy_init.init_cred() for all dict keys)
    module = 'app_init'
    operation = '_init(~)'
    mpy_trace = mpy.tracing(module, operation, mpy_trace)

    # OPTION enable/disable logging
    # ??? mpy_trace["log_enable"] = False

    check = False
    app_init_return = {}

    try:
        # TODO: MY CODE

        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')
    finally:
        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            'app_init_return' : app_init_return
            }