r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers operations to track performance, occurances of any
            kind, benchmarks and analysis of runtime.

            TODO:
                Tasks (finished / started)
                Threads (finished / started)
                Processes (finished / started)
"""

def init_metrics(mpy_trace, app_dict):

    r""" This function initializes the metrics functionality if set in the parameters.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    # Import the morPy link
    import mpy_msg, mpy_fct
    # Import standard libraries
    import sys, gc

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = '???'
    operation = '???(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False

    try:

# =============================================================================
#
    # TODO: MY CODE
#
# =============================================================================

        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    # Return a dictionary
    return{
        'check' : check
        }