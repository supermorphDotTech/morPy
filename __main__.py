r"""
Author: Bastian Neuwirth, https://www.supermorph.tech/
Date: 28.08.2024
Version: 1.0.0c

TODO Unittests
TODO Finish multiprocessing with shared memory
    > consider subprocess library
    > Further tighten app_dict and move stuff to app_dict["morpy"]
FIXME Interrupt and exit
    - interrupt/exit does not yet work in multiprocessing
    - Additional "wait_for_join()" that is lightweight and is not prone to recursion; also for log() itself.
TODO define dependencies in one of the supported manifest file types, like package.json or Gemfile.
    > This will enable GitHub to show a dependency graph
TODO check entire framework if context manager "with" is sufficiently used
TODO search for "or" statements and see if it can be replaced by any()
TODO check, if assert can be used somewhere
TODO class/instantiate sqlite3
TODO use pyinstaller to generate standalone application
    > specify application icon
    pyinstaller --icon=bulb.ico myscript.py
"""

from lib.exceptions import MorPyException

import sys

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
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

def main(morpy_trace, app_dict, orchestrator):
    r"""
    Run morPy.
    """
    orchestrator._run(morpy_trace, app_dict)

def finalize_morpy(morpy_trace, app_dict):
    r"""
    Finalize morPy components.
    """

    from lib.exit import _exit
    _exit(morpy_trace, app_dict)

    # Quit the program
    sys.exit()

if __name__ == '__main__':
    try:
        morpy_trace, app_dict, orchestrator, init_check = initialize_morpy()
        main(morpy_trace, app_dict, orchestrator)
    except Exception as e:
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")
    finally:
        try:
            finalize_morpy(morpy_trace, app_dict)
        except Exception as e:
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")