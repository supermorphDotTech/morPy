"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Unit tests for the morPy framework.
"""

import mpy_fct
import mpy_msg
from mpy_decorators import metrics

import mpy_bulk_ops_test
import mpy_common_test

import sys

@metrics
def mpy_ut(
    mpy_trace: str,
    prj_dict: dict,
) -> dict:

    """ 
    This function calls morPy unit tests.
    
    :param mpy_trace: operation credentials and tracing information
    :param prj_dict: morPy global dictionary containing project configurations

    :return: dict
        check: Indicates whether the function ended without errors
    
    :example:
        mpy_ut(mpy_trace, prj_dict)
    """

    module = 'mpy_dbg'
    operation = 'mpy_ut(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Operation preparation
    check = False 

    try:
        mpy_ut_init(mpy_trace, prj_dict)
        ut_mpy_bulk_ops(mpy_trace, prj_dict)
        ut_mpy_common(mpy_trace, prj_dict)
        check = True

    except Exception as e:
        log_message = (
            f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}'
        )
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }

@metrics
def mpy_ut_init(
    mpy_trace: str,
    prj_dict: dict,
) -> dict:

    """ 
    This function initializes morPy unit tests.
    
    :param mpy_trace: operation credentials and tracing information
    :param prj_dict: morPy global dictionary containing project configurations

    :return: dict
        check: Indicates whether the function ended without errors
    
    :example:
        mpy_ut_init(mpy_trace, prj_dict)
    """

    module = 'mpy_dbg'
    operation = 'mpy_ut_init(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Operation preparation
    check = False 

    try:
        exec (f'import {prj_dict["conf"]["localization"]}') 
        exec(f'prj_dict["loc"]["mpy_dbg"].update({prj_dict["conf"]["localization"]}.loc_dbg())')
        check = True

    except Exception as e:
        log_message = (
            f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}'
        )
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }

@metrics
def ut_mpy_bulk_ops(
    mpy_trace: str,
    prj_dict: dict,
) -> dict:

    """ 
    This function calls unit tests for mpy_bulk_ops.py.
    
    :param mpy_trace: operation credentials and tracing information
    :param prj_dict: morPy global dictionary containing project configurations

    :return: dict
        check: Indicates whether the function ended without errors
    
    :example:
        ut_mpy_bulk_ops(mpy_trace, prj_dict)
    """

    module = 'mpy_dbg'
    operation = 'ut_mpy_bulk_ops(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    try:
        check = False
        mod_fct = "mpy_bulk_ops.find_replace_saveas(~)"
        log_message = f'{prj_dict["loc"]["mpy_dbg"]["test_call_start"]} {mod_fct}'
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')
        mpy_bulk_ops_test.cl_ut_find_replace_saveas()
        check = True
        if check:
            log_message = (f'{prj_dict["loc"]["mpy_dbg"]["test_call_pass"]} {mod_fct}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')
        else:
            log_message = (f'{prj_dict["loc"]["mpy_dbg"]["test_call_fail"]} {mod_fct}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')
        
    except Exception as e:
        log_message = (
            f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}'
        )
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }

@metrics
def ut_mpy_common(
    mpy_trace: str,
    prj_dict: dict,
) -> dict:

    """ 
    This function calls unit tests for mpy_common.py.
    
    :param mpy_trace: operation credentials and tracing information
    :param prj_dict: morPy global dictionary containing project configurations

    :return: dict
        check: Indicates whether the function ended without errors
    
    :example:
        ut_mpy_common(mpy_trace, prj_dict)
    """

    module = 'mpy_dbg'
    operation = 'ut_mpy_common(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    try:
        check = False
        mod_fct = "mpy_common.decode_to_plain_text(~)"
        log_message = f'{prj_dict["loc"]["mpy_dbg"]["test_call_start"]} {mod_fct}'
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')
        mpy_common_test.cl_ut_decode_to_plain_text()
        check = True
        if check:
            log_message = (f'{prj_dict["loc"]["mpy_dbg"]["test_call_pass"]} {mod_fct}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')
        else:
            log_message = (f'{prj_dict["loc"]["mpy_dbg"]["test_call_fail"]} {mod_fct}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')
        
    except Exception as e:
        log_message = (
            f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}'
        )
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')
        
    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }
