r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from lib.decorators import morpy_wrap

from UltraDict import UltraDict


@morpy_wrap
def run(trace: dict, app_dict: dict | UltraDict, app_dict_n_shared: dict) -> dict:
    r"""
    This function runs the main workflow of the app.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_dict_n_shared: App dictionary, which is not shared with child processes
        or the orchestrator. Efficient to share data in between app phases 'app.init',
        'app.run' and 'app.exit'.

    :return: dict
        app_dict_n_shared: App dictionary, which is not shared with child processes
            or the orchestrator. Efficient to share data in between app phases 'app.init',
            'app.run' and 'app.exit'.

    :example:
        from app import init as init
        from app import run as run

        init_retval = init(trace, app_dict)
        run_retval = run(trace, app_dict, init_retval)
    """

    # App starting.
    morPy.log(trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["morpy"]["app_run_start"]}')

    # Demonstrate how to use lib.ui_tk.ProgressTrackerTk()
    from demo.ProgressTrackerTk import run as demo_progress_gui
    demo_progress_gui(trace, app_dict)

    # from morPy import process_q
    # for i in range(1, 40):
    #     task = (demo_ProgressTrackerTk, trace, app_dict)
    #     process_q(trace, app_dict, task=task)


    from morPy import process_q
    from functools import partial

    for i in range(0, 40):
        task = partial(arbitrary_task, trace, app_dict, stages=3, total_rep=10 ** 5)
        process_q(trace, app_dict, task=task, priority=20)

        task = [arbitrary_task, trace, app_dict, {"stages": 3, "total_rep": 10 ** 5}]
        process_q(trace, app_dict, task=task, priority=34)

        task = (arbitrary_task, trace, app_dict, {"stages": 3, "total_rep": 10 ** 5})
        process_q(trace, app_dict, task=task, priority=56)

        morPy.join_or_task(trace, app_dict)

        # task = [demo_ProgressTrackerTk, trace, app_dict]
        # process_q(trace, app_dict, task=task, priority=56)

    # from morPy import FileDirSelectTk
    # selection_config = {
    #     "file_select" : {
    #         "is_dir" : False,
    #         "file_types" : (('Textfile','*.txt'), ('All Files','*.*')),
    #         "default_path" : app_dict["morpy"]["conf"]["data_path"]
    #     },
    #     "dir_select" : {
    #         "is_dir" : True,
    #         "default_path" : app_dict["morpy"]["conf"]["data_path"]
    #     }
    # }
    # gui = FileDirSelectTk(trace, app_dict, selection_config, title="Select...")
    # results = gui.run(trace, app_dict)["selections"]
    # file = results["file_select"]
    # directory = results["dir_select"]
    # print(f'{file=}\n{directory=}')
    return{
        'app_dict_n_shared' : app_dict_n_shared
        }


@morpy_wrap
def arbitrary_task(trace: dict, app_dict: dict, stages: int = 5, total_rep: int = 10**6, gui=None) -> None:
    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param stages: Number of stages/repetitions
    :param total_rep: Iterations per stage
    :param gui: GUI object (ProgressTrackerTk)

    :return: -

    :example:
        arbitrary_task(trace, app_dict)
    """

    from math import sqrt

    for stage in range(1, stages + 1):
        # Begin a stage
        headline = f'Running Stage {stage}'
        description = "Starting stage..."
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
                    gui.update_text(trace, app_dict,
                                    detail_description=f'Currently at {i} - tmp_val is {tmp_val}')
            if gui:
                gui.update_text(trace, app_dict,
                                detail_description=f'Currently at {i} - tmp_val is {tmp_val}')
                gui.update_progress(trace, app_dict)

    # No localization for demo module
    morPy.log(trace, app_dict, "info",
        lambda: f'P{trace["process_id"]} :: Parallel task executed.')
