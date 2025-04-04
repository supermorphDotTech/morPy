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
        import demo.ProgressTrackerTk as demo_ProgressTrackerTk
        demo_ProgressTrackerTk.run(morpy_trace, app_dict)

        # import time
        #
        # def fibonacci(n):
        #     n = n * 50
        #     if n <= 0:
        #         return []  # Return an empty list if n is non-positive.
        #     elif n == 1:
        #         return [0]
        #
        #     sequence = [0, 1]
        #     while len(sequence) < n:
        #         # Append the sum of the last two numbers in the sequence.
        #         sequence.append(sequence[-1] + sequence[-2])
        #     return sequence
        #
        # def parallel_task(app_dict):
        #     """ Task to be run in parallel with writes to app_dict """
        #     import time
        #     from math import sqrt
        #     try:
        #         if not app_dict:
        #             raise RuntimeError("No connection to app_dict.")
        #
        #         i = 0
        #         total = 10 ** 5
        #         tmp_val = 0
        #
        #         # Hold on until all processes are ready
        #         while not app_dict["lets_go"]:
        #             time.sleep(.1)
        #
        #         while i < total:
        #             i += 1
        #             fib_seq = fibonacci(i)
        #             # Read and write app_dict and nested dictionaries
        #             with app_dict.lock:
        #                 app_dict["test_count"] += 1
        #
        #             with app_dict["nested_udict"].lock:
        #                 app_dict["nested_udict"]["test_count"] += 1
        #
        #             print(
        #                 f'root={app_dict["test_count"]} :: nested={app_dict["nested_udict"]["test_count"]} :: fibonacci={len(fib_seq)} :: pid {morpy_trace["process_id"]}\n')
        #             while tmp_val < total:
        #                 tmp_val = (sqrt(sqrt(i) * i) / i) + tmp_val ** 2
        #
        #     except Exception as e:
        #         print(f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n')
        #
        # app_dict["test_count"] = 0
        # app_dict["nested_udict"] = {}
        # app_dict["nested_udict"]["test_count"] = 0
        # app_dict["lets_go"] = False
        # task = [parallel_task, app_dict]
        # morPy.process_q(morpy_trace, app_dict, task=task)
        # morPy.process_q(morpy_trace, app_dict, task=task)
        # morPy.process_q(morpy_trace, app_dict, task=task)
        # morPy.process_q(morpy_trace, app_dict, task=task)
        # morPy.process_q(morpy_trace, app_dict, task=task)
        # morPy.process_q(morpy_trace, app_dict, task=task)
        # app_dict["lets_go"] = True
        # time.sleep(2)

        check: bool = True

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