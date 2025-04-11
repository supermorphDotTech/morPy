r"""
Author: Bastian Neuwirth, https://www.supermorph.tech/
Date: 28.08.2024
Version: 1.0.0c

TODO Unittests
TODO find and provide an easy way for locks
    > A ternary statement is used right now to see, if memory needs locking
    > It should be simpler and more scalable
TODO provide a general purpose lock
    > Find a way to lock file objects and dirs
    > Skip in single process mode
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
    pyinstaller --icon=bulb.ico my_script.py
"""

from lib.exceptions import MorPyException

import sys

def initialize_morpy():
    r""" Initialize the morPy framework """

    check: bool = False
    init_trace: dict | None = None
    init_dict: dict | None = None

    try:
        from lib import init
        init_trace: dict = init.init_cred()
        init_dict, init_orch = init.init(init_trace)

        if init_dict and init_orch:
            check: bool = True
        return init_trace, init_dict, init_orch, check

    except Exception as init_e:
        init_trace = init_trace if init_trace else None
        init_dict = init_dict if init_dict else None
        raise MorPyException(init_trace, init_dict, init_e, sys.exc_info()[-1].tb_lineno, "critical")

def main(main_trace, main_dict, main_orch):
    r""" Run morPy """

    main_orch.run(main_trace, main_dict)

def finalize_morpy(final_trace, final_dict):
    r""" Finalize morPy runtime """

    from lib.exit import exit
    exit(final_trace, final_dict)

    # Quit the program
    sys.exit()

if __name__ == '__main__':
    try:
        morpy_trace, app_dict, orchestrator, init_check = initialize_morpy()
        main(morpy_trace, app_dict, orchestrator)
    except Exception as e:
        # noinspection PyUnboundLocalVariable
        morpy_trace = morpy_trace if morpy_trace else None
        # noinspection PyUnboundLocalVariable
        app_dict = app_dict if app_dict else None
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")
    finally:
        try:
            finalize_morpy(morpy_trace, app_dict)
        except Exception as e:
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")