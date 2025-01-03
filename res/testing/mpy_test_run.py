r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION

Annotations for Spyder:
    TODO
    FIXME
    XXX
    HINT
    TIP
    @todo
    HACK
    BUG
    OPTIMIZE
    !!!
    ???
"""

import mpy
import sys
import os

from mpy_decorators import metrics, log

@metrics
def template(
    mpy_trace: dict,
    app_dict: dict
) -> dict:

    r"""
    This function does ???

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        mpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        template(mpy_trace, app_dict)
    """

    # morPy credentials (see mpy_init.init_cred() for all dict keys)
    module = '???'
    operation = '???(~)'
    mpy_trace = mpy.tracing(module, operation, mpy_trace)

    # OPTION enable/disable logging
    # ??? mpy_trace["log_enable"] = False

    # Operation preparation
    check = False

    # Add paths for testing to the environment
    base_path = app_dict["conf"]["main_path"]
    sys.path.append(os.path.join(app_dict["conf"][""], 'res', 'testing'))
    sys.path.append(os.path.join(base_path, 'res', 'testing', 'ut'))

    try:
        # TODO: MY CODE
        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }