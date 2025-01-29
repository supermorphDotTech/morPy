r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields all decorators to be used with the morPy framework.
"""

import sys
import time

from functools import wraps

def log(morpy_trace: dict, app_dict: dict, log_level: str, message_func: callable):
    r"""
    Wrapper for conditional logging based on log level. To benefit from
    this logic, it is necessary to construct "message" in the lambda shown
    in the example, whereas <message> refers to a localized string like

        f'{app_dict["loc"]["app"]["localized_message"]}\nVariable: '

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_level: Severity: debug/info/warning/error/critical/denied
    :param message_func: A callable (e.g., lambda or function) that returns the log message.

    :example:
        from lib.decorators import log
        log(morpy_trace, app_dict, "info",
        lambda: "Hello world!")
    """

    import lib.msg as msg
    import lib.fct as morpy_fct

    try:
        log_level = log_level.lower()

        if app_dict["global"]["morpy"]["logs_generate"].get(log_level, False):
            # Evaluate the message only when logging is demanded
            message = message_func()

            if app_dict["proc"]["morpy"]["process_q"]:
                task = (msg.log, morpy_trace, app_dict, message, log_level)

                # Enqueue the orchestrator task
                app_dict["proc"]["morpy"]["process_q"].enqueue(
                    morpy_trace, app_dict, priority=-100, task=task, autocorrect=False, is_process=False
                )

    except Exception as e:
        morpy_fct.handle_exception_decorator(e)

        # Quit the program
        sys.exit()

def log_no_q(morpy_trace: dict, app_dict: dict, log_level: str, message_func: callable):
    r"""
    Wrapper for conditional logging based on log level. This decorator does not enqueue
    logs and is intended for use by morPy orchestrator only.

        f'{app_dict["loc"]["app"]["localized_message"]}\nVariable: '

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_level: Severity: debug/info/warning/error/critical/denied
    :param message_func: A callable (e.g., lambda or function) that returns the log message.

    :example:
        from lib.decorators import log_no_q
        log_no_q(morpy_trace, app_dict, level,
        lambda: <message>)
    """

    import lib.msg as msg
    import lib.fct as morpy_fct

    try:
        log_level = log_level.lower()

        if app_dict["global"]["morpy"]["logs_generate"].get(log_level, False):
            msg.log(morpy_trace, app_dict, message_func(), log_level)

    except Exception as e:
        morpy_fct.handle_exception_decorator(e)

        # Quit the program
        sys.exit()

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

    import lib.fct as morpy_fct

    @wraps(func)
    def wrapper(*args, **kwargs):

        perf_mode = None
        enable_metrics = False
        morpy_trace = None
        app_dict = None
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
                morpy_trace = args[offset]
                app_dict = args[offset + 1]

                # Now we decide if metrics are enabled
                # (only if we found both morpy_trace and app_dict)
                if isinstance(morpy_trace, dict) and isinstance(app_dict, dict):
                    enable_metrics = app_dict.get("conf", {}).get("metrics_enable", False)
                    perf_mode = app_dict.get("conf", {}).get("metrics_perfmode", False)

            except (IndexError, TypeError):
                # If we still don't have them, leave them as None
                pass
            except KeyError:
                raise IndexError("Positional arguments morpy_trace and/or app_dict are missing or at wrong position!")

            try:
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

            except Exception as e:
                # If we actually got our tracing info, log a CRITICAL error
                if isinstance(morpy_trace, dict) and isinstance(app_dict, dict):
                    module = 'decorators'
                    operation = 'metrics.wrapper(~)'
                    morpy_trace_metrics = morpy_fct.tracing(module, operation, morpy_trace)
                    log(morpy_trace_metrics, app_dict, "critical",
                    lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                            f'{type(e).__name__}: {e}')
                else:
                    # fallback handler if no tracing
                    morpy_fct.handle_exception_decorator(e)

                # Quit the program
                sys.exit(1)

        return retval

    return wrapper

def metrics_perf(morpy_trace, run_time):
    r"""
    This helper function makes use of the data collected by it calling
    function metrics(~) and provides logging and formatting of the data.
    It performs all action in performance mode, which limits the data
    collected to function name, trace and runtime.

    :param morpy_trace: operation credentials and tracing
    :param run_time: Total run time of the wrapped function.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module = 'decorators'
    # operation = 'metrics_perf(~)'
    # morpy_trace = morPy.tracing(module, operation, morpy_trace)

def metrics_full(morpy_trace, run_time):
    r"""
    This helper function makes use of the data collected by it calling
    function metrics(~) and provides logging and formatting of the data.
    It performs all action in performance mode, which limits the data
    collected to function name, trace and runtime.

    :param morpy_trace: operation credentials and tracing
    :param run_time: Total run time of the wrapped function.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module = 'decorators'
    # operation = 'metrics_full(~)'
    # morpy_trace = morPy.tracing(module, operation, morpy_trace)
