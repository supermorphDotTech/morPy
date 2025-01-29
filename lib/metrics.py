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

def init_metrics(morpy_trace, app_dict):

    r""" This function initializes the metrics functionality if set in the parameters.
    :param
        morpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    # Import the morPy link
    import lib.msg as msg, fct
    # Import standard libraries
    import sys, gc

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = '???'
    operation = '???(~)'
    morpy_trace = fct.tracing(module, operation, morpy_trace)

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
        log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    # Return a dictionary
    return{
        'check' : check
        }