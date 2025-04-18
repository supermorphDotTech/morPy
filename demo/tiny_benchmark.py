r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     DESCRIPTION
"""

import morPy
from lib.decorators import morpy_wrap


@morpy_wrap
def run(trace: dict, app_dict: dict, stages: int = 1, total_rep: int = 10**2, gui=None) -> None:
    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param stages: Number of stages/repetitions
    :param total_rep: Iterations per stage
    :param gui: GUI object (ProgressTrackerTk)

    :example:
        demo.tiny_benchmark.run(trace, app_dict)
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
