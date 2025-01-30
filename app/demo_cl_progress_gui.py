r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module demonstrates how to use lib.ui_tk.cl_progress_gui()
"""

import lib.morPy as morPy
from lib.decorators import metrics, log

import sys
from math import sqrt
from functools import partial

def run(morpy_trace: dict, app_dict: dict) -> dict:
    r"""
    This function runs the main workflow of the app.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_run_return: Return value (dict) of the app process, handed to app_exit

    :example:
        # Demonstrate how to use lib.ui_tk.cl_progress_gui()
        import app.demo_cl_progress_gui as demo_cl_progress_gui
        demo_cl_progress_gui.run(morpy_trace, app_dict)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app.run'
    operation = 'app_run(~)'
    morpy_trace = morPy.tracing(module, operation, morpy_trace)

    check = False
    app_run_return = {}

    try:
        # Define repetitions and iterations of progress GUI demo
        stages = 5
        total_rep = 10 ** 2

        # No localization for demo module
        log(morpy_trace, app_dict, "info",
            lambda: f'Starting {module}.{operation}')
        task = partial(arbitrary_parallel_task, morpy_trace, app_dict, stages=stages, total_rep=total_rep, gui=None)

        progress = morPy.cl_progress_gui(morpy_trace, app_dict,
                                         frame_title="Progress Demo",
                                         stages=stages,
                                         headline_stage="Stage 1",
                                         description_stage="Currently at 0",
                                         max_per_stage=total_rep,
                                         console=False,
                                         auto_close=True,
                                         work=task  # run task in a background thread
                                         )

        progress.run(morpy_trace, app_dict)

        # No localization for demo module
        log(morpy_trace, app_dict, "info",
            lambda: f'Finished {module}.{operation}')

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{type(e).__name__}: {e}')

    return {
        'morpy_trace': morpy_trace,
        'check': check,
        'app_run_return': app_run_return
    }

@metrics
def arbitrary_parallel_task(morpy_trace, app_dict, stages: int=0, total_rep: int=0, gui=None):
    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param stages: Number of stages/repetitions
    :param total_rep: Iterations per stage
    :param gui: GUI object (cl_progress_gui)

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        arbitrary_parallel_task(morpy_trace, app_dict)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'app.run'
    operation = 'arbitrary_parallel_task(~)'
    morpy_trace = morPy.tracing(module, operation, morpy_trace)

    check = False

    try:
        if not morpy_trace or not app_dict:
            raise RuntimeError

        tmp_val = 0
        lst = []

        for stage in range(1, stages + 1):
            i = 0
            # Start new stage
            gui.update_text(morpy_trace, app_dict, headline_stage=f'Stage {stage}', description_stage=f'Currently at {i} - tmp_val is {tmp_val}')
            gui.update_progress(morpy_trace, app_dict, current=0)
            while i < total_rep:
                i += 1
                tmp_val = 0
                while tmp_val < total_rep:
                    tmp_val += sqrt(i) + tmp_val
                    lst.append(tmp_val)
                    if gui:
                        gui.update_text(morpy_trace, app_dict, description_stage=f'Currently at {i} - tmp_val is {tmp_val}')
                if gui:
                    gui.update_text(morpy_trace, app_dict, description_stage=f'Currently at {i} - tmp_val is {tmp_val}')
                    gui.update_progress(morpy_trace, app_dict, current=i)

        # No localization for demo module
        log(morpy_trace, app_dict, "info",
        lambda: f'Parallel task executed.')

    except Exception as e:
        log(morpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        }