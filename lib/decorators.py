r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields all decorators to be used with the morPy framework.
"""

from lib.fct import tracing
from lib.exceptions import MorPyException

import sys
import time
from functools import wraps
from UltraDict import UltraDict


def core_wrap(func):
    r"""
    Decorator for morPy core functionality. Exactly like 'morpy_wrap()', except for:
        > Exception log level is 'critical'

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
            raise IndexError("CRITICAL missing 'trace'. Operation is not morPy compatible!")

        # Detect, if operation is a class method and extract its name
        if trace_pos > 0:
            operation: str      = f'{type(args[0]).__name__}.{func.__name__}()'
        else:
            operation: str      = f'{func.__name__}()'

        # Update the trace
        module: str         = func.__module__
        trace: dict         = tracing(module, operation, trace)

        # Insert new 'trace' into the signature
        args = args[:trace_pos] + (trace,) + args[trace_pos+1:]

        if got_app_dict:
            metrics_enable = app_dict["morpy"]["conf"]["metrics_enable"]
            perf_mode = app_dict["morpy"]["conf"]["metrics_perf_mode"]

            if metrics_enable:
                start_time = time.perf_counter()

                try:
                    retval = func(*args, **kwargs)
                except Exception as e:
                    # Extract the innermost traceback line number.
                    tb = sys.exc_info()[2]
                    # Skip the wrapper’s frame if available.
                    if tb.tb_next is not None:
                        line_no = tb.tb_next.tb_lineno
                    else:
                        line_no = tb.tb_lineno
                    raise MorPyException(trace, app_dict, e, line_no, "critical") from e

                end_time = time.perf_counter()
                run_time = end_time - start_time

                # Metrics performance mode vs. full mode
                if perf_mode:
                    metrics_perf(trace, run_time)
                else:
                    metrics_full(trace, run_time)
                return retval
            else:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # Extract the innermost traceback line number.
                    tb = sys.exc_info()[2]
                    # Skip the wrapper’s frame if available.
                    if tb.tb_next is not None:
                        line_no = tb.tb_next.tb_lineno
                    else:
                        line_no = tb.tb_lineno
                    raise MorPyException(trace, app_dict, e, line_no, "critical") from e

        # If no 'app_dict' was detected
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Extract the innermost traceback line number.
            tb = sys.exc_info()[2]
            # Skip the wrapper’s frame if available.
            if tb.tb_next is not None:
                line_no = tb.tb_next.tb_lineno
            else:
                line_no = tb.tb_lineno
            raise MorPyException(trace, app_dict, e, line_no, "critical") from e

    return wrapper


def morpy_wrap(func):
    r"""
    Decorator that adapts a function or method to be morPy‑compatible. It verifies and updates the
    trace and app_dict, optionally measures performance metrics, and catches exceptions to re‑raise
    them as MorPyExceptions (with error severity by default).

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
            raise IndexError("ERROR missing 'trace'. Operation is not morPy compatible!")

        # Detect, if operation is a class method and extract its name
        if trace_pos > 0:
            operation: str      = f'{type(args[0]).__name__}.{func.__name__}()'
        else:
            operation: str      = f'{func.__name__}()'

        # Update the trace
        module: str         = func.__module__
        trace: dict         = tracing(module, operation, trace)

        # Insert new 'trace' into the signature
        args = args[:trace_pos] + (trace,) + args[trace_pos+1:]

        if got_app_dict:
            metrics_enable = app_dict["morpy"]["conf"]["metrics_enable"]
            perf_mode = app_dict["morpy"]["conf"]["metrics_perf_mode"]

            if metrics_enable:
                start_time = time.perf_counter()

                try:
                    retval = func(*args, **kwargs)
                except Exception as e:
                    # Extract the innermost traceback line number.
                    tb = sys.exc_info()[2]
                    # Skip the wrapper’s frame if available.
                    if tb.tb_next is not None:
                        line_no = tb.tb_next.tb_lineno
                    else:
                        line_no = tb.tb_lineno
                    raise MorPyException(trace, app_dict, e, line_no, "error") from e

                end_time = time.perf_counter()
                run_time = end_time - start_time

                # Metrics performance mode vs. full mode
                if perf_mode:
                    metrics_perf(trace, run_time)
                else:
                    metrics_full(trace, run_time)
                return retval
            else:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # Extract the innermost traceback line number.
                    tb = sys.exc_info()[2]
                    # Skip the wrapper’s frame if available.
                    if tb.tb_next is not None:
                        line_no = tb.tb_next.tb_lineno
                    else:
                        line_no = tb.tb_lineno
                    raise MorPyException(trace, app_dict, e, line_no, "error") from e

        # If no 'app_dict' was detected
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Extract the innermost traceback line number.
            tb = sys.exc_info()[2]
            # Skip the wrapper’s frame if available.
            if tb.tb_next is not None:
                line_no = tb.tb_next.tb_lineno
            else:
                line_no = tb.tb_lineno
            raise MorPyException(trace, app_dict, e, line_no, "error") from e

    return wrapper


def metrics_perf(trace, run_time) -> None:
    r"""
    (Placeholder) Intended to process and log performance metrics in performance‑only mode;
    implementation details to be added.

    :param trace: operation credentials and tracing
    :param run_time: Total run time of the wrapped function.
    """

    pass


def metrics_full(trace, run_time) -> None:
    r"""
    (Placeholder) Intended to process and log detailed performance metrics; implementation
    details to be added.

    :param trace: operation credentials and tracing
    :param run_time: Total run time of the wrapped function.
    """

    pass


def evaluate_trace(obj) -> bool:
    r"""
    Checks whether an object conforms to the morPy trace dictionary format (i.e. contains the
    expected keys and types). Returns True if valid.

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
    Determines whether the provided object is a valid morPy app_dict by verifying it contains
    the expected nested keys (whether it is a native dict or an UltraDict). Returns True if
    the structure is valid.

    :param obj: Any object

    :return: True, if the object is a morpy trace.
    """

    # Evaluation for single process mode
    if isinstance(obj, dict):
        try:
            if not isinstance(obj["morpy"]["conf"], dict):
                return False
            if not isinstance(obj["loc"]["morpy"], dict):
                return False
            return True
        except KeyError:
            return False

    # Evaluation for shared dictionary
    elif isinstance(obj, UltraDict):
        try:
            if not isinstance(obj["morpy"]["conf"], UltraDict):
                return False
            if not isinstance(obj["loc"]["morpy"], UltraDict):
                return False
            return True
        except KeyError:
            return False
    return False