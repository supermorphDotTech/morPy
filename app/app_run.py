r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import mpy
import mpy_mp
import app_init
import sys

from mpy_decorators import metrics, log
from mpy import cl_progress
from math import sqrt


@metrics
def _run( mpy_trace: dict, app_dict: dict, app_init_return: dict) -> dict:

    r"""
    This function runs the main workflow of the app.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_init_return: Return value (dict) of the initialization process, returned by app_init

    :return: dict
        mpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_run_return: Return value (dict) of the app process, handed to app_exit

    :example:
        init_retval = _init(mpy_trace, app_dict)
        run_retval = _run(mpy_trace, app_dict, init_retval)
    """

    # App initialization
    app_init._init(mpy_trace, app_dict)

    # morPy credentials (see mpy_init.init_cred() for all dict keys)
    module = 'app_run'
    operation = '_run(~)'
    mpy_trace = mpy.tracing(module, operation, mpy_trace)

    check = False

    app_run_return = {}

    try:
        # TODO my code

        log(mpy_trace, app_dict, "info",
        lambda: f'Starting {module}.{operation}')
        task = (arbitrary_parallel_task, mpy_trace, app_dict)

        counter = 0
        while counter < 4:
            counter += 1
            mpy.process_q(task=task, priority=100)
            # new_process(mpy_trace, app_dict, counter)

        log(mpy_trace, app_dict, "info",
        lambda: f'Finished {module}.{operation}')

        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        'app_run_return' : app_run_return
        }

@metrics
def new_process(mpy_trace: dict, app_dict: dict, counter: int=0) -> dict:

    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param counter: Processes opened counter

    :return: dict
        mpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        new_process(mpy_trace, app_dict, counter)
    """

    # morPy credentials (see mpy_init.init_cred() for all dict keys)
    module = 'app_run'
    operation = 'new_process(~)'
    mpy_trace = mpy.tracing(module, operation, mpy_trace)

    check = False
    p = None

    try:
        log(mpy_trace, app_dict, "info",
        lambda: "New process starting...")

        task = (arbitrary_parallel_task, mpy_trace, app_dict)  # Memory reference to app_dict
        priority = 100
        mpy.process_q(task=task, priority=priority)

        task_dqued = app_dict["proc"]["mpy"]["process_q"].dequeue(mpy_trace, app_dict)

        mpy_mp.run_parallel(mpy_trace, app_dict, task=task_dqued["task"], priority=task_dqued["priority"])

        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        'process' : p
        }

@metrics
def arbitrary_parallel_task(mpy_trace, app_dict):

    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        mpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        arbitrary_parallel_task(mpy_trace, app_dict)
    """

    # morPy credentials (see mpy_init.init_cred() for all dict keys)
    module = 'app_run'
    operation = 'arbitrary_parallel_task(~)'
    mpy_trace = mpy.tracing(module, operation, mpy_trace)

    check = False

    try:
        if not mpy_trace or not app_dict:
            raise RuntimeError

        i = 0
        total = 10**5
        tmp_val = 0
        lst = []

        progress = cl_progress(mpy_trace, app_dict,
            description=f'P{mpy_trace["process_id"]} App Progress',
            total=total,
            ticks=25)

        while i < total:
            i += 1
            while tmp_val < total:
                tmp_val = (sqrt(sqrt(i)*i) / i) + tmp_val**2
            lst.append(i)
            # print(f'Progress {i} / {total} :: {tmp_val}')
            progress.update(mpy_trace, app_dict, current=i)

        # Writing to app_dict for shared memory test
        app_dict["global"]["app"]["parallel_finished"] = True

        log(mpy_trace, app_dict, "info",
        lambda: f'Parallel task executed.')

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }