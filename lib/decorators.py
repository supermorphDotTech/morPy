r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields all decorators to be used with the morPy framework.
"""

from lib.fct import tracing
import time
from functools import wraps
from UltraDict import UltraDict

def morpy_wrap(func):
    r"""
    Decorator to fit an operation (function or method) into the morPy
    framework. Enables features like 'metrics' and 'tracing' to effectively
    lift logging to serve as an audit trail. If 'trace' is not detected
    in the signature of 'func', an exception is raised. If 'app_dict' is
    missing, only the trace will be updated.

    :param func: morPy compatible function. Needs to at least carry the morPy specific 'trace'
        in its signature.

    :return retval: Return value of the wrapped function

    :example:
        from lib.decorators import morpy_wrap
        @morpy_wrap
        my_function_call(trace, app_dict, *args, **kwargs)
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        got_trace: bool                     = False
        got_app_dict: bool                  = False
        trace_pos: int | None               = None
        trace: dict | None                  = None
        app_dict: dict | UltraDict | None   = None

        # Search for 'trace' and 'app_dict' in the function signature.
        for count, arg in enumerate(args):
            if not trace:
                got_trace: bool = evaluate_trace(arg)
                if got_trace:
                    trace = arg
                    trace_pos = count
                    continue
            if not app_dict:
                got_app_dict: bool = evaluate_app_dict(arg)
                if got_app_dict:
                    app_dict = arg
                    break

        # Skip metrics, if arguments trace or app_dict are missing
        if not got_trace:
            raise IndexError("CRITICAL missing 'trace'. This is not a morPy compatible operation!")

        # Update the trace
        module: str         = func.__module__
        operation: str      = f'{func.__name__}()'
        trace: dict         = tracing(module, operation, trace)

        # Insert new 'trace' into the signature
        args = args[:trace_pos] + (trace,) + args[trace_pos+1:]

        if got_app_dict:
            metrics_enable = app_dict["morpy"]["conf"]["metrics_enable"]
            perf_mode = app_dict["morpy"]["conf"]["metrics_perf_mode"]

            if metrics_enable:
                start_time = time.perf_counter()
                retval = func(*args, **kwargs)
                end_time = time.perf_counter()
                run_time = end_time - start_time

                # Performance Mode vs. Full Mode
                if perf_mode:
                    metrics_perf(trace, run_time)
                else:
                    metrics_full(trace, run_time)
                return retval
            else:
                return func(*args, **kwargs)

        # If no 'app_dict' was detected
        return func(*args, **kwargs)

    return wrapper

def metrics_perf(trace, run_time):
    r"""
    This helper function makes use of the data collected by it calling
    function metrics(~) and provides logging and formatting of the data.
    It performs all action in performance mode, which limits the data
    collected to function name, trace and runtime.

    :param trace: operation credentials and tracing
    :param run_time: Total run time of the wrapped function.

    :return: dict
        trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module: str = 'decorators'
    # operation: str = 'metrics_perf(~)'
    # trace: dict = morPy.tracing(module, operation, trace)

def metrics_full(trace, run_time):
    r"""
    This helper function makes use of the data collected by it calling
    function metrics(~) and provides logging and formatting of the data.
    It performs all action in performance mode, which limits the data
    collected to function name, trace and runtime.

    :param trace: operation credentials and tracing
    :param run_time: Total run time of the wrapped function.

    :return: dict
        trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module: str = 'decorators'
    # operation: str = 'metrics_full(~)'
    # trace: dict = morPy.tracing(module, operation, trace)

def evaluate_trace(obj) -> bool:
    r"""
    Helper function which compares any object with the morPy specific 'trace' dictionary
    to identify 'trace' reliably.

    :param obj: Any object

    :return: True, if the object is a morpy trace.
    """

    # Hard coded for performance
    trace_pattern: dict = {
        "module" : str(),
        "operation" : str(),
        "tracing" : str(),
        "process_id" : int(),
        "thread_id" : int(),
        "task_id" : int(),
        "log_enable" : bool(),
        "interrupt_enable" : bool(),
    }

    if not isinstance(obj, type(trace_pattern)):
        return False

    for key in trace_pattern.keys():
        try:
            if not isinstance(obj[key], type(trace_pattern[key])):
                return False
        except KeyError:
            # Not a morpy 'trace'
            return False
    return True

def evaluate_app_dict(obj) -> bool:
    r"""
    Helper function which compares any object with the morPy specific 'app_dict' dictionary
    to identify 'app_dict' reliably.

    :param obj: Any object

    :return: True, if the object is a morpy trace.
    """

    # Evaluation for single process mode
    if isinstance(obj, dict):
        try:
            if not isinstance(obj["morpy"], dict):
                return False
            if not isinstance(obj["morpy"]["conf"], dict):
                return False
            if not isinstance(obj["loc"], dict):
                return False
            return True
        except KeyError:
            return False

    # Evaluation for shared dictionary
    elif isinstance(obj, UltraDict):
        try:
            if not isinstance(obj["morpy"], UltraDict):
                return False
            if not isinstance(obj["morpy"]["conf"], UltraDict):
                return False
            if not isinstance(obj["loc"], UltraDict):
                return False
            return True
        except KeyError:
            return False
    return False