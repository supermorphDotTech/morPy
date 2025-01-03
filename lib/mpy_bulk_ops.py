r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module includes operations used to massively repeat/automize
            workflows.
"""

import lib.mpy_fct as mpy_fct
import lib.mpy_common as mpy_common
from lib.mpy_decorators import metrics, log

import sys

@metrics
def find_replace_saveas(mpy_trace: dict, app_dict: dict, search_obj, replace_tpl: tuple, save_as: str, overwrite: bool) -> dict:

    r"""
    This function finds and replaces strings in a readable object
    line by line. The result is saved into a file specified.

    :param mpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param search_obj: Any given object to search in for regular expressions.
    :param replace_tpl: Tuple of tuples. Includes every tuple of regular
        expressions and what they are supposed to be replaced by.
    :param save_as: Complete path of the file to be saved.
    :param overwrite: True if new files shall overwrite existing ones,
        if there are any. False otherwise.

    :return: dictionary
        check - The function ended with no errors
        mpy_trace - operation credentials and tracing

    :example:
        search_obj = "Let's replace1 and replace2!"
        replace_tpl = (("replace1", "with1"), ("replace2", "with2"))
        save_as = "C:\my_replaced_strings.txt"
        overwrite = True
        retval = find_replace_saveas(mpy_trace, app_dict, search_obj, replace_tpl, save_as, overwrite)
    """

    module = 'mpy_bulk_ops'
    operation = 'find_replace_saveas(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    check = False
    search_obj = f'{search_obj}'

    try:
        # Operation start.
        log(mpy_trace, app_dict, "debug",
        lambda: f'{app_dict["find_replace_saveas_start"]}')

        # Check if file exists
        file_exists = mpy_fct.pathtool(mpy_trace, save_as)["file_exists"]

        # If file exists and overwrite is false, skip action.
        if file_exists and not overwrite:
            # File already exists. Operation skipped.
            log(mpy_trace, app_dict, "warning",
            lambda: f'{app_dict["find_replace_saveas_f_ex_skip"]}')
        else:
            # Delete the target file if it exists and overwrite is true.
            if file_exists:
                mpy_common.fso_delete_file(mpy_trace, app_dict, save_as)

            # Check for tuple and make one if necessary
            if not isinstance(replace_tpl, tuple):
                replace_tpl = (replace_tpl,)

            # Check for tuple of tuples and raise error if necessary
            if not isinstance(replace_tpl[0], tuple):
                # Wrong type. Input must be a tuple of tuples.
                log(mpy_trace, app_dict, "error",
                lambda: f'{app_dict["loc"]["mpy"]["find_replace_saveas_tpl_err"]}\n'
                        f'type(replace_tpl): {type(replace_tpl)}\n'
                        f'replace_tpl: {replace_tpl}\n'
                        f'type(replace_tpl[0]): {type(replace_tpl[0])}\n'
                        f'replace_tpl[0]: {replace_tpl[0]}')
            else:
                # Search line by line
                for line in search_obj.readlines():
                    # Loop through all replace tuples.
                    for tpl in replace_tpl:
                        # Replace the actual findings
                        new_line = mpy_common.regex_replace(mpy_trace, app_dict, line, tpl[0], tpl[1])
                        mpy_common.textfile_write(mpy_trace, app_dict, save_as, new_line)

                check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return {
        'mpy_trace': mpy_trace,
        'check': check,
    }