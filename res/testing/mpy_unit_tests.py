r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Unit tests for the morPy framework.
"""

import mpy_fct
import sys
import importlib

from mpy_decorators import metrics, log

@metrics
def unit_tests(
    mpy_trace: dict,
    app_dict: dict,
) -> dict:

    r"""
    This function calls morPy unit tests.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        check: Indicates whether the function ended without errors

    :example:
        unit_tests(mpy_trace, app_dict)
    """

    module = 'mpy_dbg'
    operation = 'unit_tests(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Operation preparation
    check = False

    try:
        # Run the unit tests per module
        ut_mpy_bulk_ops(mpy_trace, app_dict)
        ut_mpy_common(mpy_trace, app_dict)
        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }

@metrics
def call_unit_test(
    mpy_trace: dict,
    app_dict: dict,
    module_ut: str,
    operation_ut: str,
) -> dict:

    r"""
    This function calls unit tests for certain operations. This only works, if
    the nomenclature of modules and operations is followed.
    Test-Modules: MYMODULE_test.py
    Test-Operation: cl_ut_MYFCT()

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param module_ut: name of the original module to test
    :param operation_ut: name of the original operation to test

    :return: dict
        check: Indicates whether the function ended without errors

    :example:
        module_ut = "mpy_common"
        operation_ut = "dialog_sel_file"
        call_unit_test(mpy_trace, app_dict, module_ut, operation_ut)
    """

    module = 'mpy_dbg'
    operation = 'call_unit_test(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    try:
        check = False
        mod_fct = f'{module_ut}.{operation_ut}(~)'
        log(mpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["mpy_dbg"]["mpy_ut_call_start"]} {mod_fct}')


        # Import the test module
        o_module_ut = importlib.import_module(f'{module_ut}_test')
        # Get the operation function
        o_operation_ut = getattr(o_module_ut, f'cl_ut_{operation_ut}')
        # Call the operation function
        o_operation_ut()

        check = True
        log(mpy_trace, app_dict, "debug",
            lambda: (f'{app_dict["loc"]["mpy_dbg"]["mpy_ut_call_pass"]} {mod_fct}'
                if check else
                f'{app_dict["loc"]["mpy_dbg"]["mpy_ut_call_fail"]} {mod_fct}')

    except Exception as e:
        log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }

@metrics
def ut_mpy_bulk_ops(
    mpy_trace: dict,
    app_dict: dict,
) -> dict:

    r"""
    This function calls unit tests for mpy_bulk_ops.py.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        check: Indicates whether the function ended without errors

    :example:
        ut_mpy_bulk_ops(mpy_trace, app_dict)
    """

    module = 'mpy_dbg'
    operation = 'ut_mpy_bulk_ops(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    check = False

    try:
        module_ut = "mpy_bulk_ops"
        operation_ut = "find_replace_saveas"
        call_unit_test(mpy_trace, app_dict, module_ut, operation_ut)

        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }

@metrics
def ut_mpy_common(
    mpy_trace: dict,
    app_dict: dict,
) -> dict:

    r"""
    This function calls unit tests for mpy_common.py.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        check: Indicates whether the function ended without errors

    :example:
        ut_mpy_common(mpy_trace, app_dict)
    """

    module = 'mpy_dbg'
    operation = 'ut_mpy_common(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    check = False

    try:
        module_ut = "mpy_common"
        operation_ut = "decode_to_plain_text"
        call_unit_test(mpy_trace, app_dict, module_ut, operation_ut)

        module_ut = "mpy_common"
        operation_ut = "dialog_sel_file"
        call_unit_test(mpy_trace, app_dict, module_ut, operation_ut)

        module_ut = "mpy_common"
        operation_ut = "dialog_sel_dir"
        call_unit_test(mpy_trace, app_dict, module_ut, operation_ut)

        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }