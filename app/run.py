r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from lib.mp import join_or_task
from lib.decorators import metrics, log

import sys
from UltraDict import UltraDict

@metrics
def app_run(morpy_trace: dict, app_dict: dict | UltraDict, app_init_return: dict) -> dict:
    r"""
    This function runs the main workflow of the app.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_init_return: Return value (dict) of the initialization process, returned by app_init.
        This dictionary is not shared with other processes by default.

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
    module: str = 'app.run'
    operation: str = 'app_run(~)'
    morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

    check: bool = False
    app_run_return = {}

    try:
        # Demonstrate how to use lib.ui_tk.ProgressTrackerTk()
        # from demo.ProgressTrackerTk import run as demo_ProgressTrackerTk
        # demo_ProgressTrackerTk(morpy_trace, app_dict)

        from morPy import process_q
        from functools import partial
        import time

        for i in range(1, 40):
            task = partial(arbitrary_task, morpy_trace, app_dict, stages=3, total_rep=10 ** 5)
            process_q(morpy_trace, app_dict, task=task, priority=20)

            task = [arbitrary_task, morpy_trace, app_dict, {"stages": 3, "total_rep": 10 ** 5}]
            process_q(morpy_trace, app_dict, task=task, priority=34)

            task = (arbitrary_task, morpy_trace, app_dict, {"stages": 3, "total_rep": 10 ** 5})
            process_q(morpy_trace, app_dict, task=task, priority=56)

            # task = [demo_ProgressTrackerTk, morpy_trace, app_dict]
            # process_q(morpy_trace, app_dict, task=task, priority=56)

        check: bool = True
        time.sleep(2)

    except Exception as e:
        raise morPy.exception(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    finally:
        # Join all spawned processes before transitioning into the next phase.
        join_or_task(morpy_trace, app_dict, reset_trace=True, reset_w_prefix=f'{module}.{operation}')

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            'app_run_return' : app_run_return
            }

@metrics
def arbitrary_task(morpy_trace: dict, app_dict: dict, stages: int = 5, total_rep: int = 10**6, gui=None):
    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param stages: Number of stages/repetitions
    :param total_rep: Iterations per stage
    :param gui: GUI object (ProgressTrackerTk)

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        arbitrary_task(morpy_trace, app_dict)
    """

    from math import sqrt

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app.run'
    operation = 'arbitrary_task(~)'
    morpy_trace = morPy.tracing(module, operation, morpy_trace)

    check = False

    try:
        if not morpy_trace or not app_dict:
            raise RuntimeError

        for stage in range(1, stages + 1):
            # Begin a stage
            headline = f'Running Stage {stage}'
            description = "Starting stage..."
            if gui:
                gui.begin_stage(morpy_trace, app_dict, stage_limit=total_rep, headline_stage=headline,
                                detail_description=description)

            # Prepare the list to append to
            lst = []

            for i in range(1, total_rep + 1):
                tmp_val = 0
                while tmp_val < total_rep:
                    tmp_val += sqrt(i) + tmp_val
                    lst.append(tmp_val)
                    if gui:
                        gui.update_text(morpy_trace, app_dict,
                                        detail_description=f'Currently at {i} - tmp_val is {tmp_val}')
                if gui:
                    gui.update_text(morpy_trace, app_dict,
                                    detail_description=f'Currently at {i} - tmp_val is {tmp_val}')
                    gui.update_progress(morpy_trace, app_dict)

        # No localization for demo module
        log(morpy_trace, app_dict, "info",
        lambda: f'P{morpy_trace["process_id"]} :: Parallel task executed.\n{morpy_trace["task_id"]=}\n'
                f'{app_dict["morpy"]["tasks_created"]=}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return {
        'morpy_trace': morpy_trace,
        'check': check,
    }