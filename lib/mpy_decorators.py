"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields all decorators to be used with the morPy framework.
"""

import mpy_fct
from functools import wraps

def metrics(func):

    """
    Decorator used for metrics and performance analytics.
    
    :param func: Function to be decorated
    
    :return retval: Return value of the wrapped function
    
    :example:
        from mpy_decorators import metrics
        @metrics
        my_function_call(mpy_trace, prj_dict)
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        try:
            # Extract function arguments
            mpy_trace = args[0]
            prj_dict = args[1]
    
            if prj_dict is not None:
                enable = prj_dict.get("mpy_conf", {}).get("mpy_metrics_enable", False)
                perfmode = prj_dict.get("mpy_conf", {}).get("mpy_metrics_perfmode", False)
            else:
                enable = False
                perfmode = False
            
            # Perform metrics if switched on
            if enable:
                import time
                
                # Measure the runtime and call a function
                start_time = time.perf_counter()
                retval = func(*args, **kwargs)
                end_time = time.perf_counter()
                run_time = end_time - start_time
                
                # Perform metrics collection in Performance Mode
                if perfmode:
                    hlpfct_analytics_perfmode(mpy_trace, run_time)
                
                # Perform metrics collection in full mode
                else:
                    hlpfct_analytics_fullmode(retval, run_time)
                    
            # If metrics are disabled, execute the function normally
            else:
                retval = func(*args, **kwargs)
            
        except Exception as e:
            mpy_fct.handle_exception_decorator(e)
            raise
            
        return retval
    
    return wrapper

def hlpfct_analytics_perfmode(mpy_trace, run_time):

    """ This helper function makes use of the data collected by it's calling
        function metrics(~) and provides logging and formatting of the data.
        It performs all action in performance mode, which limits the data
        collected to function name, trace and runtime.
    :param
        mpy_trace - [dictionary] operation credentials and tracing
        run_time - Total run time of the wrapped function.
    :return
        -
    """
    
    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_decorators'
    # operation = 'hlpfct_analytics(~)'
    # mpy_trace = mpy.tracing(module, operation, mpy_trace)
    
def hlpfct_analytics_fullmode(retval, run_time):

    """ This helper function makes use of the data collected by it's calling
        function metrics(~) and provides logging and formatting of the data.
        It performs all action in performance mode, which limits the data
        collected to function name, trace and runtime.
    :param
        retval - [dictionary] operation credentials and tracing
        run_time - Total run time of the wrapped function.
    :return
        -
    """
    
    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_decorators'
    # operation = 'hlpfct_analytics(~)'
    # mpy_trace = mpy.tracing(module, operation, mpy_trace)