r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from lib.decorators import metrics, log

import sys

@metrics
def app_run(morpy_trace: dict, app_dict: dict, app_init_return: dict) -> dict:
    r"""
    This function runs the main workflow of the app.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_init_return: Return value (dict) of the initialization process, returned by app_init

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_run_return: Return value (dict) of the app process, handed to app_exit

    :example:
        from app import init as app_init
        from app import run as app_run

        init_retval = app_init(morpy_trace, app_dict)
        run_retval = app_run(morpy_trace, app_dict, init_retval)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app.run'
    operation = 'app_run(~)'
    morpy_trace = morPy.tracing(module, operation, morpy_trace)

    check = False
    app_run_return = {}

    try:
        # Demonstrate how to use lib.ui_tk.ProgressTrackerTk()
        import demo.ProgressTrackerTk as demo_ProgressTrackerTk
        demo_ProgressTrackerTk.run(morpy_trace, app_dict)

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'app_run_return' : app_run_return
        }

@metrics
def new_process(morpy_trace: dict, app_dict: dict, counter: int=0) -> dict:
    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param counter: Processes opened counter

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        new_process(morpy_trace, app_dict, counter)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app.run'
    operation = 'new_process(~)'
    morpy_trace = morPy.tracing(module, operation, morpy_trace)

    check = False
    p = None

    try:
        # TODO port to it's own demo module
        # log(morpy_trace, app_dict, "info",
        # lambda: "New process starting...")
        #
        # task = (arbitrary_parallel_task, morpy_trace, app_dict)  # Memory reference to app_dict
        # priority = 100
        # morPy.process_q(task=task, priority=priority)
        #
        # task_dqued = app_dict["proc"]["morpy"]["process_q"].dequeue(morpy_trace, app_dict)
        #
        # mp.run_parallel(morpy_trace, app_dict, task=task_dqued["task"], priority=task_dqued["priority"])

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'process' : p
        }
