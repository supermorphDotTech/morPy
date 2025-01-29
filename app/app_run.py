r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import mpy
import mpy_mp
import lib.mpy_fct as mpy_fct
import app_init
from mpy_decorators import metrics, log
from mpy import cl_progress
import lib.mpy_common as mpy_common


import sys
import time

from math import sqrt
from functools import partial

import queue
import threading
import traceback
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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
        log(mpy_trace, app_dict, "info",
        lambda: f'Starting {module}.{operation}')
        task = partial(arbitrary_parallel_task, mpy_trace, app_dict, gui=None)

        progress = mpy.cl_progress_gui(mpy_trace, app_dict,
            frame_title="Progress Demo",
            stages=2,
            headline_stage="Stage 1",
            description_stage="Currently at 0",
            max_per_stage=10**2,
            console=True,
            work=task  # run in a background thread
        )

        progress.run(mpy_trace, app_dict)

        log(mpy_trace, app_dict, "info",
        lambda: f'Finished {module}.{operation}')

        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

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
                f'{type(e).__name__}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        'process' : p
        }

@metrics
def arbitrary_parallel_task(mpy_trace, app_dict, gui=None):

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
                    gui.update_text(mpy_trace, app_dict, description_stage=f'Currently at {i}')
                    gui.update_progress(mpy_trace, app_dict, current=i)

            # Start new stage
            gui.update_text(mpy_trace, app_dict, headline_stage="Stage 2", description_stage=f'Currently at 0')
            gui.update_progress(mpy_trace, app_dict, current=0)

        # Writing to app_dict for shared memory test
        app_dict["global"]["app"]["parallel_finished"] = True

        log(mpy_trace, app_dict, "info",
        lambda: f'Parallel task executed.')

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }