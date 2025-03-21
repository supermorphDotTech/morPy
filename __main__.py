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

TODO make use of the "with" statement
    > Optimize own classes to be supported by with (i.e. __exit__() methods)

TODO class/instantiate logging and sqlite3
TODO class/instantiate file operations

TODO use pyinstaller to generate standalone application
    > specify application icon
    pyinstaller --icon=bulb.ico myscript.py
"""

import sys
import logging

# Setup fallback-logging for __main__
logging.basicConfig(level=logging.CRITICAL)
init_check: bool = False

def initialize_morpy():
    r"""
    Initialize the morPy framework.
    """

    init_check: bool = False

    try:
        from lib import init
        morpy_trace: dict = init.init_cred()
        app_dict, orchestrator = init.init(morpy_trace)
        if app_dict and orchestrator:
            init_check: bool = True
        return morpy_trace, app_dict, orchestrator, init_check

    except Exception as e:
        import lib.fct as morpy_fct
        morpy_fct.handle_exception_main(e, init=init_check)

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
    try:
        morpy_trace, app_dict, orchestrator, init_check = initialize_morpy()
        main(morpy_trace, app_dict, orchestrator)
    except Exception as e:
        import lib.fct as morpy_fct
        morpy_fct.handle_exception_main(e, init=init_check)
    finally:
        try:
            finalize_morpy(morpy_trace, app_dict)
        except Exception as e:
            morpy_fct.handle_exception_main(e, init=init_check)