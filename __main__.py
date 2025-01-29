r"""
Author: Bastian Neuwirth, https://www.supermorph.tech/
Date: 28.08.2024
Version: 1.0.0c

TODO IN PROGRESS
- Unit tests
    > common.py | common_test.py

TODO improve error handling to be specific, rather than excessive/graceful

TODO Finish multiprocessing with shared memory
    > consider subprocess library
    > make app_dict flat under the hood, if GIL

TODO Threading orchestrator: 1 for logs, 1 for dequeue, 1 for app_dict
TODO Interrupt and exit overhaul
    - provide function to check for interrupt/exit
    - interrupt when logging: move from mp to the log decorator
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
init_check = False

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

    init_check = False

    try:
        from lib import init
        morpy_trace = init.init_cred()
        app_dict, orchestrator = init.init(morpy_trace)
        if app_dict and orchestrator:
            init_check = True
        return morpy_trace, app_dict, orchestrator, init_check

    except Exception as e:
        import lib.fct as fct
        fct.handle_exception_main(e, init=init_check)

def main(morpy_trace, app_dict, orchestrator):
    r"""
    Run morPy.
    """
    orchestrator._run(morpy_trace, app_dict)

def finalize_morpy(morpy_trace, app_dict):
    r"""
    Finalize morPy components.
    """
    import lib.exit as exit
    exit._exit(morpy_trace, app_dict)

    # Quit the program
    sys.exit()

if __name__ == '__main__':
    add_paths() # Add system paths for enhanced compatibility

    try:
        morpy_trace, app_dict, orchestrator, init_check = initialize_morpy()
        main(morpy_trace, app_dict, orchestrator)
    except Exception as e:
        import lib.fct as fct
        fct.handle_exception_main(e, init=init_check)
    finally:
        try:
            finalize_morpy(morpy_trace, app_dict)
        except Exception as e:
            fct.handle_exception_main(e, init=init_check)