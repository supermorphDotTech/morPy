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
    """

    # App starting.
    morPy.log(trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["morpy"]["app_run_start"]}')

    # --- DEMO ---
    # Multi-stage progressbar with GUI
    from demo import ProgressTrackerTk
    ProgressTrackerTk.run(trace, app_dict)

    # --- DEMO ---
    # Multiprocessing with task shelving. Lots of tiny tasks.
    # Configure processes in config.py
    from demo import tiny_benchmark as bench
    task: list = [bench.run, trace, app_dict]

    for _ in range(0, 250):
        morPy.process_q(trace, app_dict, task)

    return{
        'app_dict_n_shared' : app_dict_n_shared
        }
