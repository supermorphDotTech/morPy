r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module demonstrates how to use lib.ui_tk.ProgressTrackerTk()
"""

import morPy
from morPy import log
from lib.decorators import morpy_wrap

import sys
from math import sqrt
from functools import partial

def run(morpy_trace: dict, app_dict: dict) -> dict:
    r"""
    This is a demo of ProgressTrackerTk(), a preconfigured GUI for progress
    tracking. At it's base, it uses tkinter to render the Window displayed.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_run_return: Return value (dict) of the app process, handed to app_exit

    :example:
        # Demonstrate how to use lib.ui_tk.ProgressTrackerTk()
        import app.demo_ProgressTrackerTk as demo_ProgressTrackerTk
        demo_ProgressTrackerTk.run(trace, app_dict)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'demo.ProgressTrackerTk'
    operation = 'run(~)'
    morpy_trace = morPy.tracing(module, operation, morpy_trace)

    app_run_return = {}

    try:
        # Define repetitions and iterations of progress GUI demo
        stages = 5
        total_rep = 10 ** 2

        # Starting
        log(morpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["app"]["demo_starting"]} {module}.{operation}')

        task = partial(arbitrary_task, morpy_trace, app_dict, stages=stages, total_rep=total_rep, gui=None)

        progress = morPy.ProgressTrackerTk(morpy_trace, app_dict,
                                         frame_title=f'{app_dict["loc"]["app"]["demo_title"]}',
                                         stages=stages,
                                         detail_description_on=True,
                                         console=True,
                                         auto_close=True,
                                         work=task  # run task in a background thread
                                         )

        progress.run(morpy_trace, app_dict)

        # Finished
        log(morpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["app"]["demo_finished"]} {module}.{operation}')

        check = True

    except Exception as e:
        raise morPy.MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return {
        'trace': morpy_trace,
        'check': check,
        'app_run_return': app_run_return
    }

@morpy_wrap
def arbitrary_task(morpy_trace: dict, app_dict: dict, stages: int=0, total_rep: int=0, gui=None):
    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param stages: Number of stages/repetitions
    :param total_rep: Iterations per stage
    :param gui: GUI object (ProgressTrackerTk)

    :return: dict
        trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        arbitrary_task(trace, app_dict)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'demo.ProgressTrackerTk'
    operation = 'arbitrary_task(~)'
    morpy_trace = morPy.tracing(module, operation, morpy_trace)

    check = False

    try:
        if not morpy_trace or not app_dict:
            raise RuntimeError

        for stage in range(1, stages + 1):
            # Beginning stage
            headline = f'{app_dict["loc"]["app"]["demo_begin_stage"]} {stage}'
            description = f'{app_dict["loc"]["app"]["demo_starting"]}...'
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
                        gui.update_text(
                            morpy_trace, app_dict,
                            detail_description=f'{app_dict["loc"]["app"]["demo_step"]} {i} :: {tmp_val=}'
                        )
                if gui:
                    gui.update_text(
                        morpy_trace, app_dict,
                        detail_description=f'{app_dict["loc"]["app"]["demo_step"]} {i} :: {tmp_val=}'
                    )
                    gui.update_progress(morpy_trace, app_dict)

        # Parallel task executed.
        log(morpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["app"]["demo_executed"]}')

    except Exception as e:
        raise morPy.MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'trace' : morpy_trace,
        'check' : check,
        }