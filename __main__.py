r"""
Author: Bastian Neuwirth, https://www.supermorph.tech/
Date: 02.01.2025
Version: 1.0.0c

TODO IN PROGRESS
- Unit tests
    > mpy_common.py | mpy_common_test.py

TODO Finish multiprocessing with shared memory
    NEXT STEPS:
    - debug-messages for process_control wrapper
    - debug messages for run_parallel
    - debug-messages, where useful
TODO Threading orchestrator: 1 for logs, 1 for dequeue, 1 for app_dict
TODO Interrupt and exit overhaul
    - provide function to check for interrupt/exit
    - interrupt when logging: move from mpy_mp to the log decorator
    - exit option to log decorator
    - Provide an exit if CRITICAL and dump app_dict and priority queue, offer to pick up on it next restart

TODO Make exit() more dynamic, so it is used instead of sys.exit
    - Needed i.e. to release the log.db lock and other cleanups
    - Needed also to release any db lock

TODO chatGPT: make use of the "with" statement
    > Optimize own classes to be supported by with (i.e. __exit__() methods)
TODO class/instantiate logging and sqlite3
TODO class/instantiate excel
TODO class/instantiate file operations
TODO Check and complete function signatures

TODO use app_exit and morPy exit accordingly (usually app_exit the exit point for .join() and terminate)
    > search for sys.exit() and substitute it
    > search for .exit and evaluate it
"""

import sys
import os
import pathlib
import logging

# Setup fallback-logging for __main__
logging.basicConfig(level=logging.CRITICAL)
mpy_init_check = False

def add_paths():
    r"""
    Add morPy specific paths to sys.path.
    """
    base_path = pathlib.Path(__file__).parent.resolve()
    sys.path.append(os.path.join(base_path, 'lib'))
    sys.path.append(os.path.join(base_path, 'loc'))
    sys.path.append(os.path.join(base_path, 'app'))
    sys.path.append(os.path.join(base_path, 'res'))

def initialize_morpy():
    r"""
    Initialize the morPy framework.
    """
    from lib import mpy_init
    mpy_trace = mpy_init.init_cred()
    app_dict, orchestrator = mpy_init.init(mpy_trace)
    return mpy_trace, app_dict, orchestrator

def main(mpy_trace, app_dict, orchestrator):
    r"""
    Run morPy.
    """
    orchestrator._run(mpy_trace, app_dict)

def finalize_morpy(mpy_trace, app_dict):
    r"""
    Finalize morPy components.
    """
    import mpy_exit
    mpy_exit._exit(mpy_trace, app_dict)

    # Quit the program
    sys.exit()

if __name__ == '__main__':
    add_paths() # Add system paths for enhanced compatibility

    try:
        mpy_trace, app_dict, orchestrator = initialize_morpy()
        main(mpy_trace, app_dict, orchestrator)
    except Exception as e:
        import mpy_fct
        mpy_fct.handle_exception_main(e, mpy_init_check)
        raise
    finally:
        try:
            finalize_morpy(mpy_trace, app_dict)
        except Exception as e:
            print(f'CRITICAL missing app_dict. Exit dirty.\n{e}')
