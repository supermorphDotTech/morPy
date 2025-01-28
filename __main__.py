r"""
Author: Bastian Neuwirth, https://www.supermorph.tech/
Date: 28.08.2024
Version: 1.0.0c

TODO IN PROGRESS
- Unit tests
    > mpy_common.py | mpy_common_test.py

TODO improve error handling to be specific, rather than excessive/graceful

TODO Finish multiprocessing with shared memory
    > consider subprocess library
    > make app_dict flat under the hood, if GIL

TODO Threading orchestrator: 1 for logs, 1 for dequeue, 1 for app_dict
TODO Interrupt and exit overhaul
    - provide function to check for interrupt/exit
    - interrupt when logging: move from mpy_mp to the log decorator
    - exit option to log decorator
    - Provide an exit if CRITICAL and dump app_dict and priority queue, offer to pick up on it next restart

TODO define dependencies in one of the supported manifest file types, like package.json or Gemfile.
    > This will enable GitHub to show a dependency graph
    
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

TODO use pyinstaller to generate standalone application
    > specify application icon
    pyinstaller --icon=bulb.ico myscript.py
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

    mpy_init_check = False
    app_dict = None
    orchestrator = None

    try:
        from lib import mpy_init
        mpy_trace = mpy_init.init_cred()
        app_dict, orchestrator = mpy_init.init(mpy_trace)
        if app_dict and orchestrator:
            mpy_init_check = True
        return mpy_trace, app_dict, orchestrator, mpy_init_check

    except Exception as e:
        import mpy_fct
        mpy_fct.handle_exception_main(e, init=mpy_init_check)

def main(mpy_trace, app_dict, orchestrator):
    r"""
    Run morPy.
    """
    orchestrator._run(mpy_trace, app_dict)

def finalize_morpy(mpy_trace, app_dict):
    r"""
    Finalize morPy components.
    """
    import lib.mpy_exit as mpy_exit
    mpy_exit._exit(mpy_trace, app_dict)

    # Quit the program
    sys.exit()

if __name__ == '__main__':
    add_paths() # Add system paths for enhanced compatibility

    try:
        mpy_trace, app_dict, orchestrator, mpy_init_check = initialize_morpy()
        main(mpy_trace, app_dict, orchestrator)
    except Exception as e:
        import mpy_fct
        mpy_fct.handle_exception_main(e, init=mpy_init_check)
    finally:
        try:
            finalize_morpy(mpy_trace, app_dict)
        except Exception as e:
            mpy_fct.handle_exception_main(e, init=mpy_init_check)