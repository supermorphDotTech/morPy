r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from morPy import log
from lib.decorators import morpy_wrap

import sys
from UltraDict import UltraDict

@morpy_wrap
def app_run(morpy_trace: dict, app_dict: dict | UltraDict, app_dict_n_shared: dict) -> dict:
    r"""
    This function runs the main workflow of the app.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_dict_n_shared: App dictionary, which is not shared with child processes
        or the orchestrator. Efficient to share data in between app phases 'app.init',
        'app.run' and 'app.exit'.

    :return: dict
        trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_dict_n_shared: App dictionary, which is not shared with child processes
            or the orchestrator. Efficient to share data in between app phases 'app.init',
            'app.run' and 'app.exit'.

    :example:
        from app import init as app_init
        from app import run as app_run

        init_retval = app_init(trace, app_dict)
        run_retval = app_run(trace, app_dict, init_retval)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module: str = 'app.run'
    operation: str = 'app_run(~)'
    morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # FULL TEXT HERE
        # log(trace, app_dict, "info",
        # lambda: f'{app_dict["loc"]["app"]["MESSAGE_KEY"]}')

        # Demonstrate how to use lib.ui_tk.ProgressTrackerTk()
        from demo.ProgressTrackerTk import run as demo_ProgressTrackerTk
        demo_ProgressTrackerTk(morpy_trace, app_dict)

        # from morPy import process_q
        # for i in range(1, 40):
        #     task = (demo_ProgressTrackerTk, trace, app_dict)
        #     process_q(trace, app_dict, task=task)


        # from morPy import process_q
        # from functools import partial
        # import time
        #
        # for i in range(1, 40):
        #     task = partial(arbitrary_task, trace, app_dict, stages=3, total_rep=10 ** 5)
        #     process_q(trace, app_dict, task=task, priority=20)
        #
        #     task = [arbitrary_task, trace, app_dict, {"stages": 3, "total_rep": 10 ** 5}]
        #     process_q(trace, app_dict, task=task, priority=34)
        #
        #     task = (arbitrary_task, trace, app_dict, {"stages": 3, "total_rep": 10 ** 5})
        #     process_q(trace, app_dict, task=task, priority=56)
        #
        #     # task = [demo_ProgressTrackerTk, trace, app_dict]
        #     # process_q(trace, app_dict, task=task, priority=56)

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

        check: bool = True

    except Exception as e:
        raise morPy.MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    finally:
        return{
            'trace' : morpy_trace,
            'check' : check,
            'app_dict_n_shared' : app_dict_n_shared
            }

@morpy_wrap
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
        trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        arbitrary_task(trace, app_dict)
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
        lambda: f'P{morpy_trace["process_id"]} :: Parallel task executed.')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return {
        'trace': morpy_trace,
        'check': check,
    }