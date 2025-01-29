r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields all decorators to be used with the morPy framework.
"""

import sys
import time

from functools import wraps, partial

def log(morPy_trace: dict, app_dict: dict, log_level: str, message_func: callable):

    r"""
    Wrapper for conditional logging based on log level. To benefit from
    this logic, it is necessary to construct "message" in the lambda shown
    in the example, whereas <message> refers to a localized string like

        f'{app_dict["loc"]["app"]["localized_message"]}\nVariable: '

    :param morPy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param level: Severity: debug/info/warning/error/critical/denied
    :param message_func: A callable (e.g., lambda or function) that returns the log message.

    :example:
        from lib.decorators import log
        log(morPy_trace, app_dict, level,
        lambda: <message>)
    """

    import lib.msg as msg
    import lib.fct as fct

    try:
        log_level = log_level.lower()

        if log_level in app_dict["global"]["morPy"]["logs_generate"]:
            if app_dict["global"]["morPy"]["logs_generate"][log_level] == True:
                # Evaluate the message only when logging is demanded
                message = message_func()

                try:
                    if app_dict["proc"]["morPy"]["process_q"]:
                        task = (msg.log, morPy_trace, app_dict, message, log_level)

                        # Enqueue the orchestrator task
                        app_dict["proc"]["morPy"]["process_q"].enqueue(
                            morPy_trace, app_dict, priority=-100, task=task, autocorrect=False, is_process=False
                        )
                except:
                    msg.log(morPy_trace, app_dict, message, log_level)

    except Exception as e:
        msg = (f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
               f'{type(e).__name__}: {e}\n'
               f'{app_dict["loc"]["morPy"]["trace"]}: {morPy_trace["tracing"]}\n'
               f'{app_dict["loc"]["morPy"]["process"]}: {morPy_trace["process_id"]}\n'
               f'{app_dict["loc"]["morPy"]["thread"]}: {morPy_trace["thread_id"]}\n'
               f'{app_dict["loc"]["morPy"]["task"]}: {morPy_trace["task_id"]}')

        fct.handle_exception_decorator(msg)

        # Quit the program
        sys.exit()

def log_no_q(morPy_trace: dict, app_dict: dict, log_level: str, message_func: callable):

    r"""
    Wrapper for conditional logging based on log level. This decorator does not enqueue
    logs and is intended for use by morPy orchestrator only.

        f'{app_dict["loc"]["app"]["localized_message"]}\nVariable: '

    :param morPy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param level: Severity: debug/info/warning/error/critical/denied
    :param message_func: A callable (e.g., lambda or function) that returns the log message.

    :example:
        from lib.decorators import log_no_q
        log_no_q(morPy_trace, app_dict, level,
        lambda: <message>)
    """

    import lib.msg as msg
    import lib.fct as fct

    try:
        log_level = log_level.lower()

        if log_level in app_dict["global"]["morPy"]["logs_generate"]:
            if app_dict["global"]["morPy"]["logs_generate"][log_level] == True:
                # Evaluate the message only when logging is demanded
                message = message_func()
                msg.log(morPy_trace, app_dict, message, log_level)

    except Exception as e:
        msg = (f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
               f'{type(e).__name__}: {e}\n'
               f'{app_dict["loc"]["morPy"]["trace"]}: {morPy_trace["tracing"]}\n'
               f'{app_dict["loc"]["morPy"]["process"]}: {morPy_trace["process_id"]}\n'
               f'{app_dict["loc"]["morPy"]["thread"]}: {morPy_trace["thread_id"]}\n'
               f'{app_dict["loc"]["morPy"]["task"]}: {morPy_trace["task_id"]}')

        fct.handle_exception_decorator(msg)

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
        my_function_call(morPy_trace, app_dict, *args, **kwargs)
    """

    import lib.fct as fct

    @wraps(func)
    def wrapper(*args, **kwargs):

        perf_mode = None
        enable_metrics = False
        morPy_trace = None
        app_dict = None
        len_args = len(args)

        # Skip metrics, if arguments morPy_trace or app_dict are missing
        if len_args < 2:
            raise IndexError("Missing arguments morPy_trace and/or app_dict!")
        else:
            # Assume the first arg might be `self` if not a dict
            offset = 0
            if len_args > 0 and not isinstance(args[0], dict):
                # Probably a bound method; skip `self`
                offset = 1

            # Attempt to extract morPy_trace & app_dict from positional args
            try:
                morPy_trace = args[offset]
                app_dict = args[offset + 1]

                # Now we decide if metrics are enabled
                # (only if we found both morPy_trace and app_dict)
                if isinstance(morPy_trace, dict) and isinstance(app_dict, dict):
                    enable_metrics = app_dict.get("conf", {}).get("metrics_enable", False)
                    perf_mode = app_dict.get("conf", {}).get("metrics_perfmode", False)

            except (IndexError, TypeError):
                # If we still don't have them, leave them as None
                pass
            except (KeyError):
                raise IndexError("Positional arguments morPy_trace and/or app_dict are missing or at wrong position!")

            try:
                if enable_metrics:
                    start_time = time.perf_counter()
                    retval = func(*args, **kwargs)
                    end_time = time.perf_counter()
                    run_time = end_time - start_time

                    # Performance Mode vs. Full Mode
                    if perf_mode:
                        metrics_perf(morPy_trace, run_time)
                    else:
                        metrics_full(morPy_trace, run_time)
                else:
                    retval = func(*args, **kwargs)

            except Exception as e:
                # If we actually got our tracing info, log a CRITICAL error
                if isinstance(morPy_trace, dict) and isinstance(app_dict, dict):
                    module = 'decorators'
                    operation = 'metrics.wrapper(~)'
                    morPy_trace_metrics = fct.tracing(module, operation, morPy_trace)
                    log(morPy_trace_metrics, app_dict, "critical",
                    lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                            f'{type(e).__name__}: {e}')
                else:
                    # fallback handler if no tracing
                    fct.handle_exception_decorator(f'{e}\nmorPy_trace: {morPy_trace}\n*args: {args}\n**kwargs: {kwargs}')

                # Quit the program
                sys.exit(1)

        return retval

    return wrapper

def metrics_perf(morPy_trace, run_time):

    r""" This helper function makes use of the data collected by it's calling
        function metrics(~) and provides logging and formatting of the data.
        It performs all action in performance mode, which limits the data
        collected to function name, trace and runtime.
    :param
        morPy_trace - [dictionary] operation credentials and tracing
        run_time - Total run time of the wrapped function.
    :return
        -
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module = 'decorators'
    # operation = 'metrics_perf(~)'
    # morPy_trace = morPy.tracing(module, operation, morPy_trace)

def metrics_full(morPy_trace, run_time):

    r""" This helper function makes use of the data collected by it's calling
        function metrics(~) and provides logging and formatting of the data.
        It performs all action in performance mode, which limits the data
        collected to function name, trace and runtime.
    :param
        morPy_trace - [dictionary] operation credentials and tracing
        run_time - Total run time of the wrapped function.
    :return
        -
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module = 'decorators'
    # operation = 'metrics_full(~)'
    # morPy_trace = morPy.tracing(module, operation, morPy_trace)
