"""
Author:     AUTHOR
Date:       DATE
Version:    VERSION
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

def template(mpy_trace, prj_dict):

    """ This function does ???
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        TODO - ???
    :return - dictionary
        check - The function ended with no errors
    """

#   Import the morPy link
    import mpy
#   Import standard libraries
    import sys, gc
#   Import project modules
#   import ???

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = '???'
    operation = '???(~)'
    mpy_trace = mpy.tracing(module, operation, mpy_trace)

    # OPTION enable/disable logging
    # ??? mpy_trace['log_enable'] = False

#   Preparing parameters
    check = False

    try:

    #   -------------------
    #   TODO: MY CODE
    #   -------------------

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

    #   Return a dictionary
        return{
            'check' : check
            }