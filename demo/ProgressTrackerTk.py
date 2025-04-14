r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module demonstrates how to use lib.ui_tk.ProgressTrackerTk()
"""

import morPy
from lib.decorators import morpy_wrap

from math import sqrt
from functools import partial


@morpy_wrap
def run(trace: dict, app_dict: dict) -> None:
    r"""
    This is a demo of ProgressTrackerTk(), a preconfigured GUI for progress
    tracking. At it's base, it uses tkinter to render the Window displayed.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :example:
        # Demonstrate how to use lib.ui_tk.ProgressTrackerTk()s
        import app.demo_ProgressTrackerTk as demo_ProgressTrackerTk
        demo_ProgressTrackerTk.run(trace, app_dict)
    """

    # Define repetitions and iterations of progress GUI demo
    stages = 5
    total_rep = 10 ** 2

    # Starting
    morPy.log(trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["app"]["demo_starting"]} {trace["module"]}.{trace["operation"]}')

    task = partial(arbitrary_task, trace, app_dict, stages=stages, total_rep=total_rep, gui=None)

    progress = morPy.ProgressTrackerTk(trace, app_dict,
                                     frame_title=f'{app_dict["loc"]["app"]["demo_title"]}',
                                     stages=stages,
                                     detail_description_on=True,
                                     console=False,
                                     auto_close=True,
                                     work=task  # run task in a background thread
                                     )

    progress.run(trace, app_dict)

    # Finished
    morPy.log(trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["app"]["demo_finished"]} {trace["module"]}.{trace["operation"]}')


@morpy_wrap
def arbitrary_task(trace: dict, app_dict: dict, stages: int=0, total_rep: int=0, gui=None) -> None:
    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param stages: Number of stages/repetitions
    :param total_rep: Iterations per stage
    :param gui: GUI object (ProgressTrackerTk)

    :example:
        arbitrary_task(trace, app_dict)
    """

    if not trace or not app_dict:
        raise RuntimeError

    for stage in range(1, stages + 1):
        # Beginning stage
        headline = f'{app_dict["loc"]["app"]["demo_begin_stage"]} {stage}'
        description = f'{app_dict["loc"]["app"]["demo_starting"]}...'
        if gui:
            gui.begin_stage(trace, app_dict, stage_limit=total_rep, headline_stage=headline,
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
                        trace, app_dict,
                        detail_description=f'{app_dict["loc"]["app"]["demo_step"]} {i} :: {tmp_val=}'
                    )
            if gui:
                gui.update_text(
                    trace, app_dict,
                    detail_description=f'{app_dict["loc"]["app"]["demo_step"]} {i} :: {tmp_val=}'
                )
                gui.update_progress(trace, app_dict)

    # Parallel task executed.
    morPy.log(trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["app"]["demo_executed"]}')
