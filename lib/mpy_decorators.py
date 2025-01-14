r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields all decorators to be used with the morPy framework.
"""

import sys

from functools import wraps, partial

def log(mpy_trace: dict, app_dict: dict, log_level: str, message_func: callable):

    r"""
    Wrapper for conditional logging based on log level. To benefit from
    this logic, it is necessary to construct "message" in the lambda shown
    in the example, whereas <message> refers to a localized string like

        f'{app_dict["loc"]["app"]["localized_message"]}\nVariable: '

    :param mpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param level: Severity: debug/info/warning/error/critical/denied
    :param message_func: A callable (e.g., lambda or function) that returns the log message.

    :example:
        from mpy_decorators import log
        log(mpy_trace, app_dict, level,
        lambda: <message>)
    """

    import mpy_msg, mpy_fct

    try:
        log_level = log_level.lower()

        if log_level in app_dict["global"]["mpy"]["logs_generate"]:
            if app_dict["global"]["mpy"]["logs_generate"][log_level] == True:
                # Evaluate the message only when logging is demanded
                message = message_func()

                try:
                    if app_dict["proc"]["mpy"]["process_q"]:
                        task = (mpy_msg.log, mpy_trace, app_dict, message, log_level)

                        # Enqueue the orchestrator task
                        app_dict["proc"]["mpy"]["process_q"].enqueue(
                            mpy_trace, app_dict, priority=-100, task=task, autocorrect=False, is_process=False
                        )
                except:
                    mpy_msg.log(mpy_trace, app_dict, message, log_level)

    except Exception as e:
        msg = (f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}\n'
           f'{app_dict["loc"]["mpy"]["trace"]}: {mpy_trace["tracing"]}\n'
           f'{app_dict["loc"]["mpy"]["process"]}: {mpy_trace["process_id"]}\n'
           f'{app_dict["loc"]["mpy"]["thread"]}: {mpy_trace["thread_id"]}\n'
           f'{app_dict["loc"]["mpy"]["task"]}: {mpy_trace["task_id"]}')

        mpy_fct.handle_exception_decorator(msg)

        # Quit the program
        sys.exit()

def log_no_q(mpy_trace: dict, app_dict: dict, log_level: str, message_func: callable):

    r"""
    Wrapper for conditional logging based on log level. This decorator does not enqueue
    logs and is intended for use by morPy orchestrator only.

        f'{app_dict["loc"]["app"]["localized_message"]}\nVariable: '

    :param mpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param level: Severity: debug/info/warning/error/critical/denied
    :param message_func: A callable (e.g., lambda or function) that returns the log message.

    :example:
        from mpy_decorators import log_no_q
        log_no_q(mpy_trace, app_dict, level,
        lambda: <message>)
    """

    import mpy_msg, mpy_fct

    try:
        log_level = log_level.lower()

        if log_level in app_dict["global"]["mpy"]["logs_generate"]:
            if app_dict["global"]["mpy"]["logs_generate"][log_level] == True:
                # Evaluate the message only when logging is demanded
                message = message_func()
                mpy_msg.log(mpy_trace, app_dict, message, log_level)

    except Exception as e:
        msg = (f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}\n'
           f'{app_dict["loc"]["mpy"]["trace"]}: {mpy_trace["tracing"]}\n'
           f'{app_dict["loc"]["mpy"]["process"]}: {mpy_trace["process_id"]}\n'
           f'{app_dict["loc"]["mpy"]["thread"]}: {mpy_trace["thread_id"]}\n'
           f'{app_dict["loc"]["mpy"]["task"]}: {mpy_trace["task_id"]}')

        mpy_fct.handle_exception_decorator(msg)

        # Quit the program
        sys.exit()

def metrics(func):

    r"""
    Decorator used for metrics and performance analytics. in morPy this
    is the outermost decorator.

    :param func: Function to be decorated

    :return retval: Return value of the wrapped function

    :example:
        from mpy_decorators import metrics
        @metrics
        my_function_call(mpy_trace, app_dict, *args, **kwargs)
    """

    import mpy_fct

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            if func is not None:
                # Extract function arguments
                # Respect "self", if object is a method
                # TODO make it work for methods / when "self" is passed as arg[0]
                # TODO make the evaluation for mpy_trace and app_dict more elegant and robust

                # Extract function arguments
                mpy_args_check = False
                enable = False
                try:
                    mpy_trace = args[0]
                    app_dict = args[1]
                    if mpy_trace["process_id"] and mpy_trace["tracing"]:
                        mpy_args_check = True
                except:
                    mpy_trace = args[1]
                    app_dict = args[2]
                    mpy_args_check = True

                if mpy_args_check and mpy_trace is not None and app_dict is not None and not hasattr(func, '__wrapped__'):
                    enable = app_dict.get("conf", {}).get("mpy_metrics_enable", False)
                    perfmode = app_dict.get("conf", {}).get("mpy_metrics_perfmode", False)

                # Perform metrics if switched on
                if enable:
                    import time

                    # Measure the runtime and call a function
                    start_time = time.perf_counter()
                    retval = func(*args, **kwargs)
                    end_time = time.perf_counter()
                    run_time = end_time - start_time

                    # Metrics collection in performance Mode
                    if perfmode:
                        metrics_perf(mpy_trace, run_time)

                    # Metrics collection in full mode
                    else:
                        metrics_full(retval, run_time)

                # If metrics are disabled, execute the function normally
                else:
                    retval = func(*args, **kwargs)

            else:
                retval = None

        except Exception as e:
            if mpy_args_check and mpy_trace is not None and app_dict is not None:
                module = 'mpy_decorators'
                operation = 'metrics.wrapper(~)'
                mpy_trace_metrics = mpy_fct.tracing(module, operation, mpy_trace)
                log(mpy_trace_metrics, app_dict, "critical",
                lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

            else:
                mpy_fct.handle_exception_decorator(e)

            # Quit the program
            sys.exit()

        return retval

    return wrapper

def metrics_perf(mpy_trace, run_time):

    r""" This helper function makes use of the data collected by it's calling
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
    # operation = 'metrics_perf(~)'
    # mpy_trace = mpy.tracing(module, operation, mpy_trace)

def metrics_full(mpy_trace, run_time):

    r""" This helper function makes use of the data collected by it's calling
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
    # operation = 'metrics_full(~)'
    # mpy_trace = mpy.tracing(module, operation, mpy_trace)
