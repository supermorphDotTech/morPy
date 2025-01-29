r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import lib.morPy as morPy
import lib.mp as mp
import lib.fct as fct
from lib.decorators import metrics, log
from lib.morPy import cl_progress
import lib.common as common
import app.app_init as app_init

import sys
import time

from math import sqrt
from functools import partial

@metrics
def _run( morPy_trace: dict, app_dict: dict, app_init_return: dict) -> dict:

    r"""
    This function runs the main workflow of the app.

    :param morPy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_init_return: Return value (dict) of the initialization process, returned by app_init

    :return: dict
        morPy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_run_return: Return value (dict) of the app process, handed to app_exit

    :example:
        init_retval = _init(morPy_trace, app_dict)
        run_retval = _run(morPy_trace, app_dict, init_retval)
    """

    # App initialization
    app_init._init(morPy_trace, app_dict)

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app_run'
    operation = '_run(~)'
    morPy_trace = morPy.tracing(module, operation, morPy_trace)

    check = False
    app_run_return = {}

    try:
        log(morPy_trace, app_dict, "info",
        lambda: f'Starting {module}.{operation}')
        task = partial(arbitrary_parallel_task, morPy_trace, app_dict, gui=None)

        progress = morPy.cl_progress_gui(morPy_trace, app_dict,
            frame_title="Progress Demo",
            stages=2,
            headline_stage="Stage 1",
            description_stage="Currently at 0",
            max_per_stage=10**2,
            console=True,
            work=task  # run in a background thread
        )

        progress.run(morPy_trace, app_dict)

        log(morPy_trace, app_dict, "info",
        lambda: f'Finished {module}.{operation}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        'app_run_return' : app_run_return
        }

@metrics
def new_process(morPy_trace: dict, app_dict: dict, counter: int=0) -> dict:

    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param morPy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param counter: Processes opened counter

    :return: dict
        morPy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        new_process(morPy_trace, app_dict, counter)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app_run'
    operation = 'new_process(~)'
    morPy_trace = morPy.tracing(module, operation, morPy_trace)

    check = False
    p = None

    try:
        log(morPy_trace, app_dict, "info",
        lambda: "New process starting...")

        task = (arbitrary_parallel_task, morPy_trace, app_dict)  # Memory reference to app_dict
        priority = 100
        morPy.process_q(task=task, priority=priority)

        task_dqued = app_dict["proc"]["morPy"]["process_q"].dequeue(morPy_trace, app_dict)

        mp.run_parallel(morPy_trace, app_dict, task=task_dqued["task"], priority=task_dqued["priority"])

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        'process' : p
        }

@metrics
def arbitrary_parallel_task(morPy_trace, app_dict, gui=None):

    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param morPy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        morPy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        arbitrary_parallel_task(morPy_trace, app_dict)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app_run'
    operation = 'arbitrary_parallel_task(~)'
    morPy_trace = morPy.tracing(module, operation, morPy_trace)

    check = False

    try:
        if not morPy_trace or not app_dict:
            raise RuntimeError

        i = 0
        total = 10**2
        tmp_val = 0
        lst = []

        for stage in range(1, 3):
            i = 0
            while i < total:
                i += 1
                while tmp_val < total:
                    tmp_val = (sqrt(sqrt(i)*i) / i) + tmp_val**2
                lst.append(i)
                # print(f'Progress {i} / {total} :: {tmp_val}')
                if gui:
                    gui.update_text(morPy_trace, app_dict, description_stage=f'Currently at {i}')
                    gui.update_progress(morPy_trace, app_dict, current=i)

            # Start new stage
            gui.update_text(morPy_trace, app_dict, headline_stage="Stage 2", description_stage=f'Currently at 0')
            gui.update_progress(morPy_trace, app_dict, current=0)

        # Writing to app_dict for shared memory test
        app_dict["global"]["app"]["parallel_finished"] = True

        log(morPy_trace, app_dict, "info",
        lambda: f'Parallel task executed.')

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        }