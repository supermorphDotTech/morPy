r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields all decorators to be used with the morPy framework.
"""

import time
from functools import wraps
from UltraDict import UltraDict

def log(morpy_trace: dict, app_dict: dict, log_level: str, message: callable, verbose: bool=False):
    r"""
    Wrapper for conditional logging based on log level. To benefit from
    this logic, it is necessary to construct "message" in the lambda shown
    in the example, whereas <message> refers to a localized string like

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_level: Severity: debug/info/warning/error/critical/denied
    :param message: A callable (e.g., lambda or function) that returns the log message.
    :param verbose: If True, message is only logged in verbose mode.

    :example:
        from lib.decorators import log
        log(morpy_trace, app_dict, "info",
        lambda: "Hello world!")
    """

    import lib.msg as msg

    # Skip logging, if message is verbose and verbose is disabled
    if verbose and not app_dict["morpy"]["conf"].get("msg_verbose", False):
        return
    else:
        log_level = log_level.lower()

        if message and app_dict["morpy"]["logs_generate"].get(log_level, False):
            msg.log(morpy_trace, app_dict, log_level, message(), verbose)

def metrics(func):
    r"""
    Decorator used for metrics and performance analytics. in morPy this
    is the outermost decorator.

    :param func: Function to be decorated

    :return retval: Return value of the wrapped function

    :example:
        from lib.decorators import metrics
        @metrics
        my_function_call(morpy_trace, app_dict, *args, **kwargs)
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        perf_mode = None
        enable_metrics = False
        morpy_trace: dict = None
        len_args = len(args)

        # Skip metrics, if arguments morpy_trace or app_dict are missing
        if len_args < 2:
            raise IndexError("Missing arguments morpy_trace and/or app_dict!")
        else:
            # Assume the first arg might be `self` if not a dict
            offset = 0
            if len_args > 0 and not isinstance(args[0], dict):
                # Probably a bound method; skip `self`
                offset = 1

            # Attempt to extract morpy_trace & app_dict from positional args
            try:
                morpy_trace: dict = args[offset]
                app_dict = args[offset + 1]

                # Now we decide if metrics are enabled
                # (only if we found both morpy_trace and app_dict)
                if isinstance(morpy_trace, dict) and isinstance(app_dict, (UltraDict, dict)):
                    enable_metrics = app_dict.get("lib.conf", {}).get("metrics_enable", False)
                    perf_mode = app_dict.get("lib.conf", {}).get("metrics_perfmode", False)

            except (IndexError, TypeError):
                # If we still don't have them, leave them as None
                pass
            except KeyError:
                raise IndexError("Positional arguments morpy_trace and/or app_dict are missing or at the wrong position!")

            if enable_metrics:
                start_time = time.perf_counter()
                retval = func(*args, **kwargs)
                end_time = time.perf_counter()
                run_time = end_time - start_time

                # Performance Mode vs. Full Mode
                if perf_mode:
                    metrics_perf(morpy_trace, run_time)
                else:
                    metrics_full(morpy_trace, run_time)
            else:
                retval = func(*args, **kwargs)

        return retval

    return wrapper

<<<<<<< Updated upstream
def metrics_perf(morpy_trace, run_time):
=======

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
>>>>>>> Stashed changes
    r"""
    (Placeholder) Intended to process and log performance metrics in performance‑only mode;
    implementation details to be added.

    :param morpy_trace: operation credentials and tracing
    :param run_time: Total run time of the wrapped function.
<<<<<<< Updated upstream

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
=======
>>>>>>> Stashed changes
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module: str = 'decorators'
    # operation: str = 'metrics_perf(~)'
    # morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

<<<<<<< Updated upstream
def metrics_full(morpy_trace, run_time):
=======

def metrics_full(trace, run_time) -> None:
>>>>>>> Stashed changes
    r"""
    (Placeholder) Intended to process and log detailed performance metrics; implementation
    details to be added.

    :param morpy_trace: operation credentials and tracing
    :param run_time: Total run time of the wrapped function.
<<<<<<< Updated upstream

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module: str = 'decorators'
    # operation: str = 'metrics_full(~)'
    # morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)
=======
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
>>>>>>> Stashed changes
