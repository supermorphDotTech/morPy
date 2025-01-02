r"""
Author: Bastian Neuwirth, https://www.supermorph.tech/
Date: 02.01.2025
Version: 1.0.0c
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
