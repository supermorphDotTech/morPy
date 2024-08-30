"""
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
    
from mpy_decorators import metrics

@metrics
def template(
    mpy_trace: str,
    prj_dict: dict
) -> dict:

    """ 
    This function does ???
    
    :param mpy_trace: operation credentials and tracing information
    :param prj_dict: morPy global dictionary containing project configurations

    :return: dict
        check: Indicates whether the function ended without errors
    
    :example:
        template(mpy_trace, prj_dict)
    """

    # morPy credentials (see mpy_init.init_cred() for all dict keys)
    module = '???'
    operation = '???(~)'
    mpy_trace = mpy.tracing(module, operation, mpy_trace)

    # OPTION enable/disable logging
    # ??? mpy_trace["log_enable"] = False

    # Operation preparation
    check = False 

    try:
        # TODO: MY CODE
        check = True

    except Exception as e:
        log_message = (
            f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}'
        )
        mpy.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }