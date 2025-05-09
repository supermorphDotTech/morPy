r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module includes operations used to massively repeat/automize
            workflows.
"""

import lib.fct as morpy_fct
import lib.common as common
from morPy import log
from lib.decorators import morpy_wrap


@morpy_wrap
def find_replace_save_as(trace: dict, app_dict: dict, search_obj, replace_tpl: tuple, save_as: str,
                        overwrite: bool=False) -> None:
    r"""
    Iterates through each line of the given text (converted to a string) to find and replace
    substrings according to provided tuples of (pattern, replacement). The resulting text is
    written to the specified file. If the target file exists and overwriting is disallowed,
    the operation is skipped.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param search_obj: Can be any given object to search in for regular expressions. Searches line by line.
    :param replace_tpl: Tuple of tuples. Includes every tuple of regular expressions and what they are supposed
                        to be replaced by.
    :param save_as: Complete path of the file to be saved.
    :param overwrite: True if new files shall overwrite existing ones, if there are any. False otherwise.
                      Defaults to False.

    :example:
        search_obj = "Let's replace1 and replace2!"
        replace_tpl = (("replace1", "with1"), ("replace2", "with2"))
        save_as = "C:\my_replaced_strings.txt"
        overwrite = True
        retval = morPy.find_replace_save_as(trace, app_dict, search_obj, replace_tpl, save_as, overwrite)
    """

    search_obj: str = f'{search_obj}'

    # Operation start.
    log(trace, app_dict, "debug",
        lambda: f'{app_dict["find_replace_save_as_start"]}')

    # Check if file exists
    file_exists = morpy_fct.pathtool(save_as)["file_exists"]

    # If file exists and overwrite is false, skip action.
    if file_exists and not overwrite:
        # File already exists. Operation skipped.
        log(trace, app_dict, "warning",
            lambda: f'{app_dict["find_replace_save_as_f_ex_skip"]}')
    else:
        # Delete the target file if it exists and overwrite is true.
        if file_exists:
            common.fso_delete_file(trace, app_dict, save_as)

        # Check for tuple and make one if necessary
        if not isinstance(replace_tpl, tuple):
            replace_tpl = (replace_tpl,)

        # Check for tuple of tuples and raise error if necessary
        if not isinstance(replace_tpl[0], tuple):
            # Wrong type. Input must be a tuple of tuples.
            log(trace, app_dict, "error",
                lambda: f'{app_dict["loc"]["morpy"]["find_replace_save_as_tpl_err"]}\n'
                        f'type(replace_tpl): {type(replace_tpl)}\n'
                        f'replace_tpl: {replace_tpl}\n'
                        f'type(replace_tpl[0]): {type(replace_tpl[0])}\n'
                        f'replace_tpl[0]: {replace_tpl[0]}')
        else:
            # Search line by line
            for line in search_obj.splitlines():
                # Loop through all replace tuples.
                for tpl in replace_tpl:
                    # Replace the actual findings
                    new_line = common.regex_replace(trace, app_dict, line, tpl[0], tpl[1])["result"]
                    common.textfile_write(trace, app_dict, save_as, new_line)
