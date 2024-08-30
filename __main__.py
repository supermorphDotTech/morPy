"""
Author: Bastian Neuwirth
Date: 28.08.2024
Version: 1.0.0c

IN PROGRESS
- Call parameters from the sub-dictionary prj_dict['mpy_params']
    > Weiter mit 'mpy_log_lvl_noprint' : mpy_log_lvl_noprint, \
    
TODO
- Can I create a macro for logs?
- Add :example to the headers
- Note the datatype in the headers
- Split the prj_dict deeper into a core-section

DONE:
- !! Always return function credentials for the metrics wrapper 'mpy_trace', 'module', 'operation'
"""

import sys
import os
import pathlib
import logging

# Setup fallback-logging for __main__
logging.basicConfig(level=logging.CRITICAL)
mpy_init_check = False

# TODO develop pre-init metrics
def add_mpy_paths():
    """
    Add morPy specific paths to sys.path.
    """
    base_path = pathlib.Path(__file__).parent.resolve()
    sys.path.append(os.path.join(base_path, 'lib'))
    sys.path.append(os.path.join(base_path, 'loc'))
    sys.path.append(os.path.join(base_path, 'prj'))
    sys.path.append(os.path.join(base_path, 'res'))

# TODO develop pre-init metrics
def initialize_morpy():
    """
    Initialize crucial morPy components.
    """
    import mpy_init
    mpy_trace = mpy_init.init_cred()
    prj_dict = mpy_init.init(mpy_trace)
    return mpy_trace, prj_dict

def main(mpy_trace, prj_dict):
    """
    Execute the main logic of the program.
    """
    # import prj_exec
    # prj_exec.prj_init(mpy_trace, prj_dict)
    # prj_exec.prj_run(mpy_trace, prj_dict)
    # prj_exec.prj_exit(mpy_trace, prj_dict)
    import mpy_dbg
    mpy_dbg.mpy_ut(mpy_trace, prj_dict)

def finalize_morpy(mpy_trace, prj_dict):
    """
    Finalize morPy components.
    """
    import mpy_exit
    mpy_exit.exit(mpy_trace, prj_dict)
    
if __name__ == '__main__':
    add_mpy_paths()

    try:
        mpy_trace, prj_dict = initialize_morpy()
        mpy_init_check = True
        main(mpy_trace, prj_dict)
    except Exception as e:
        import mpy_fct
        mpy_fct.handle_exception_main(e, mpy_init_check)
        raise
    finally:
        if mpy_init_check:
            finalize_morpy(mpy_trace, prj_dict)