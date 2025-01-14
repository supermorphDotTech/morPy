r"""
Author:     Bastian Neuwirth
Date:       12.08.2023
Version:    0.1
Descr.:     This module is the interface to the morPy framework.
    TODO Finish formatting in morPy standard
"""

import lib.mpy_bulk_ops as mpy_bulk_ops
import lib.mpy_common as mpy_common
import lib.mpy_csv as mpy_csv
import lib.mpy_fct as mpy_fct
import lib.mpy_mt as mpy_mt
import lib.mpy_ui_tk as mpy_ui_tk
# import lib.mpy_wscraper as mpy_wscraper
# TODO fix webscraper
import lib.mpy_xl as mpy_xl
from lib.mpy_decorators import log

import sys

def cl_priority_queue(mpy_trace: dict, app_dict: dict, name: str=None):

    r"""
    This class delivers a priority queue solution. Any task may be enqueued.
    When dequeueing, the highest priority task (lowest number) is dequeued
    first. In case there is more than one, the oldest is dequeued.

    :param mpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param name: Name or description of the instance

    :example:
        from functools import partial
        # Create queue instance
        queue = mpy.cl_priority_queue(mpy_trace, app_dict, name="example_queue")
        # Add a task to the queue
        queue.enqueue(mpy_trace, app_dict, priority=25, task=partial(task, mpy_trace, app_dict))
        # Fetch a task and run it
        task = queue.dequeue(mpy_trace, app_dict)['task']
        task()
    """

    try:
        return mpy_common.cl_priority_queue(mpy_trace, app_dict, name)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'cl_priority_queue(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def cl_progress(mpy_trace: dict, app_dict: dict, description: str=None, total: float=None, ticks: float=None):

    r"""
    This class instanciates a progress counter. If ticks, total or counter
    are floats, a progress of 100 % may not be displayed.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param description: Describe, what is being processed (i.e. file path or calculation)
    :param total: Mandatory - The total count for completion
    :param ticks: Mandatory - Percentage of total to log the progress. I.e. at ticks=10.7 at every
        10.7% progress exceeded the exact progress will be logged.

    .update()
        Method to update current progress and log progress if tick is passed.

        :return .update(): dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors
            prog_rel: Relative progress, float between 0 and 1
            message: Message generated. None, if no tick was hit.

    :example:
        progress = cl_progress(mpy_trace, app_dict, description='App Progress', total=total_count, ticks=10)
        progress.update(mpy_trace, app_dict, current=current_count)
    """

    try:
        return mpy_common.cl_progress(mpy_trace, app_dict, description, total, ticks)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'cl_progress(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def csv_read(mpy_trace: dict, app_dict: dict, src_file_path: str, delimiter: str, print_csv_dict: bool) -> dict:

    r"""
    This function reads a csv file and returns a dictionary of
    dictionaries. The header row, first row of data and delimiter
    is determined automatically.

    :param mpy_trace: Operation credentials and tracing
    :param app_dict: morPy global dictionary containing app configurations
    :param src_file_path: Path to the csv file.
    :param delimiter: Delimiters used in the csv. None = Auto detection
    :param print_csv_dict: If true, the csv_dict will be printed to console. Should only
        be used for debugging with small example csv files. May take very long to complete.

    :return: dict
        mpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        csv_dict: Dictionary containing all tags. The line numbers of data are
            the keys of the parent dictionary, and the csv header consists of
            the keys of every sub-dictionary.
            Pattern:
                {DATA1 :
                     delimiter : [str]
                     header : [tuple] (header(1), header(2), ...)
                     columns : [int] header columns
                     rows : [int] number of rows in data
                     ROW1 : [dict]
                         {header(1) : data(1, 1),
                          header(2) : data(2, 1),
                          ...}
                     ROW2 : [dict]
                         {header(1) : data(1, 2),
                         header(2) : data(2, 2),
                                 ...}
                 DATA2 :
                     ...
                 }

    :example:
        src_file_path = 'C:\myfile.csv'
        delimiter = '' # Delimiter auto detection
        print_csv_dict = True # Print data tables to console
        csv_dict = mpy_csv.csv_read(mpy_trace, app_dict, src_file_path, delimiter, print_csv_dict=False)
    """

    try:
        return mpy_csv.csv_read(mpy_trace, app_dict, src_file_path, delimiter, print_csv_dict)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'csv_read(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def decode_to_plain_text(mpy_trace: dict, app_dict: dict, src_input: str, encoding: str) -> dict:

    r""" This function decodes different types of data and returns
        a plain text to work with in python. The return result behaves
        like using the open(file, 'r') method.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        src_input - Any kind of data to be decoded. Binary expected. Example:
                    src_input = open(src_file, 'rb')
        encoding - String that defines encoding. Leave empty to auto detect. Examples:
                   '' - Empty. Encoding will be determined automatically. May be incorrect.
                   'utf-16-le' - Decode UTF-16 LE to buffered text.
    :return - dictionary
        result - Decoded result. Buffered object that my be used with the readlines() method.
        encoding - String containing the encoding of src_input.
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.decode_to_plain_text(mpy_trace, app_dict, src_input, encoding)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'decode_to_plain_text(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def dialog_sel_file(mpy_trace: dict, app_dict: dict, init_dir: str, ftypes: str, title: str) -> dict:

    r""" This function opens a dialog for the user to select a file.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        init_dir - The directory in which the dialog will initially be opened
        ftypes - This tuple of 2-tuples specifies, which filetypes will be
                displayed by the dialog box, e.g.
                (('type1','*.t1'),('All Files','*.*'),...)
        title - Title of the open file dialog
    :return - dictionary
        check - The function ended with no errors and a file was chosen
        sel_file - Path of the selected file
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.dialog_sel_file(mpy_trace, app_dict, init_dir, ftypes, title)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'dialog_sel_file(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def dialog_sel_dir(mpy_trace: dict, app_dict: dict, init_dir: str, title: str) -> dict:

    r"""
    This function opens a dialog for the user to select a directory.

    :param mpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param title: Title of the open directory dialog

    :return: dict
        mpy_trace: [dictionary] operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        sel_dir: Path of the selected directory
        dir_selected: True, if directory was selected. False, if canceled.

    :example:
        init_dir = app_dict["sys"]["homedir"]
        title = 'Select a file...'
        sel_dir = dialog_sel_dir(mpy_trace, app_dict, init_dir, title)
    """

    try:
        return mpy_common.dialog_sel_dir(mpy_trace, app_dict, init_dir, title)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'dialog_sel_dir(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def fso_copy_file(mpy_trace, app_dict, source, dest, ovwr_perm):

    r""" This function is used to copy a single file from source to destination.
        A file check is already included and will be performed.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        source - Complete path to the source file including the file extension
        dest - Complete path to the destination file including the file extension
        ovwr_perm - If TRUE, the destination file may be overwritten.
    :return - dictionary
        check - The function ended with no errors
        source - Path to the source file as a path object
        dest - Path to the destination file as a path object
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.fso_copy_file(mpy_trace, app_dict, source, dest, ovwr_perm)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'fso_copy_file(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def fso_create_dir(mpy_trace, app_dict, mk_dir):

    r""" This function creates a directory as well as it's parents
        recursively.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        mk_dir - Path to the directory/tree to be created
    :return - dictionary
        check - The function ended with no errors
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.fso_create_dir(mpy_trace, app_dict, mk_dir)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'fso_create_dir(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def fso_delete_dir(mpy_trace, app_dict, del_dir):

    r""" This function is used to delete an entire directory including it's
        contents. A directory check is already included and will be performed.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        del_dir - Path to the directory to be deleted
    :return - dictionary
        check - The function ended with no errors
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.fso_delete_dir(mpy_trace, app_dict, del_dir)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'fso_delete_dir(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def fso_delete_file(mpy_trace, app_dict, del_file):

    r"""
    This function is used to delete a file. A path check is
    already included and will be performed.

    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        del_file - Path to the directory to be deleted

    :return - dictionary
        check - The function ended with no errors
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.fso_delete_file(mpy_trace, app_dict, del_file)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'fso_delete_file(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def fso_walk(mpy_trace, app_dict, path, depth):

    r""" This function returns the contents of a directory.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        path - Path to be analyzed
        depth - Limits the depth to be analyzed
                -1 - No Limit
                0 - path only
    :return - dictionary
        check - The function ended with no errors
        walk_dict - Dictionary of root directories and it's contents. Example:
                {'root0' : {'root' : root, \
                            'dirs' : [dir list], \
                            'files' : [file list]}
                 'root1' : {'root' : root, \
                            'dirs' : [dir list], \
                            'files' : [file list]}
                 ...
                }
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.fso_walk(mpy_trace, app_dict, path, depth)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'fso_walk(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def process_q(task: tuple, priority: int=100, autocorrect: bool=True):

    r"""
    This function enqueues a task in the morPy multiprocessing queue. The task is a
    tuple, that demands the positional arguments (func, mpy_trace, app_dict, *args, **kwargs).

    :param task: Tuple of a callable, *args and **kwargs
    :param priority: Integer representing task priority (lower is higher priority)
    :param autocorrect: If False, priority can be smaller than zero. Priority
        smaller zero is reserved for the morPy Core. However, it is a devs choice
        to make.

    :return: process_qed: If True, process was queued successfully. If False, an error occurred.

    :example:
        from mpy import process_q
        message = "Gimme 5"
        def gimme_5(mpy_trace, app_dict, message):
            print(message)
            return message
        a_number = (gimme_5, mpy_trace, app_dict, message) # Tuple of a callable, *args and **kwargs
        enqueued = process_q(task=a_number, priority=20) #
        if not enqueued:
            print("No, thank you sir!")
    """

    process_qed = False

    try:
        mpy_trace = task[1]
        app_dict = task[2]
        try:
            app_dict["proc"]["mpy"]["process_q"].enqueue(
                mpy_trace, app_dict, priority=priority, task=task, autocorrect=autocorrect
            )

            process_qed = True

        except Exception as e:
            # Define operation credentials (see mpy_init.init_cred() for all dict keys)
            module = 'mpy'
            operation = 'process_q(~)'
            mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

            log(mpy_trace, app_dict, "critical",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    except:
        raise RuntimeError

    finally:
        return process_qed

def regex_findall(mpy_trace, app_dict, search_obj, pattern):

    r""" This function searches for regular expression in any given object and returns a list of found expressions.'
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        pattern - The regular expression to search for
    :return - list
        result - The list of expressions found in the input
    """

    try:
        return mpy_common.regex_findall(mpy_trace, app_dict, search_obj, pattern)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'regex_findall(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def regex_find1st(mpy_trace, app_dict, search_obj, pattern):

    r""" This function searches for regular expression in any given object and returns the first match.'
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        pattern - The regular expression to search for

    :return - list
        result - The list of expressions found in the input
    """

    try:
        return mpy_common.regex_find1st(mpy_trace, app_dict, search_obj, pattern)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'regex_find1st(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def regex_split(mpy_trace, app_dict, search_obj, delimiter):

    r""" This function splits an object into a list by a given delimiter.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        delimiter - The character or string used to split the search_obj into a list. Have
                    in mind, that special characters may need a backslash preceding them (e.g. '\.' to use
                    '.' as a delimiter).
    :return - list
        result - The list of parts split from the input
    """

    try:
        return mpy_common.regex_split(mpy_trace, app_dict, search_obj, delimiter)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'regex_split(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def regex_replace(mpy_trace, app_dict, search_obj, search_for, replace_by):

    r""" This function substitutes characters or strings in an input object.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        search_for - The character or string to be replaced
        replace_by - The character or string to substitute

    :return
        result - The substituted chracter or string
    """

    try:
        return mpy_common.regex_replace(mpy_trace, app_dict, search_obj, search_for, replace_by)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'regex_replace(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def regex_remove_special(mpy_trace, app_dict, inp_string, spec_lst):

    r""" This function removes special characters of a given string and instead inserts
        any character if defined. The spec_lst is a list consiting of tuples
        consisting of special characters and what they are supposed to get exchanged
        with. Using a blank list will invoke a standard list where specials will be
        removed and not replaced by any other character. This function may even be used
        to perform a number of regex_replace actions on the same string, because it
        will replace what ever is given to the tuples-list. Essentially, you can use
        any valid regular expression instead of the special character.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        inp_string - The string to be altered
        spec_lst - List consisting of 2-tuples as a definition of which special character
                   is to be replaced by which [(special1,replacement1),...]. Set the
                   list to [('','')] to invoke the standard replace list.
    :return
        result - The substituted chracter or string
    """

    try:
        return mpy_common.regex_remove_special(mpy_trace, app_dict, inp_string, spec_lst)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'regex_remove_special(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def textfile_write(mpy_trace, app_dict, filepath, content):

    r""" This function appends any textfile and creates it, if there
        is no such file.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        filepath - Path to the textfile including its name and filetype
        content - Something that will be printed as a string.

    :return
        -
    """

    try:
        return mpy_common.textfile_write(mpy_trace, app_dict, filepath, content)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'textfile_write(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def testprint(mpy_trace, input):

    r""" This function prints any value given. It is intended to be used for debugging.
    :param
        mpy_trace - operation credentials and tracing
        input - Something that will be printed as a string.
    :return
        -
    """

    return mpy_common.testprint(mpy_trace, input)

def wait_for_input(mpy_trace, app_dict, msg_text):

    r""" This function makes the program wait until a user input was made.
        The user input can be returned to the calling module.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        msg_text - The text to be displayed before user input
    :return
        usr_input - Returns the input of the user
    """

    try:
        return mpy_common.wait_for_input(mpy_trace, app_dict, msg_text)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'wait_for_input(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def datetime_now(mpy_trace):

    r""" This function reads the current date and time and returns formatted
        stamps.
    :param
        mpy_trace - operation credentials and tracing
    :return - dictionary
        datetime_value - Date and time in the format YYYY-MM-DD hh:mm:ss.ms as value
                        (used to determine runtime).
        date - Date DD.MM.YYY as a string.
        datestamp - Datestamp YYYY-MM-DD as a string.
        time - Time hh:mm:ss as a string.
        timestamp - Timestamp hhmmss as a string.
        datetimestamp - Date- and timestamp YYY-MM-DD_hhmmss as a string.
        loggingstamp - Date- and timestamp for logging YYYMMDD_hhmmss as a string.
    """

    return mpy_fct.datetime_now(mpy_trace)

def runtime(mpy_trace, in_ref_time):

    r""" This function calculates the actual runtime and returns it.
    :param
        mpy_trace - operation credentials and tracing
        in_ref_time - Value of the reference time to calculate the actual runtime
    :return - dictionary
        rnt_delta - Value of the actual runtime.
    """

    import mpy_fct

    return mpy_fct.runtime(mpy_trace, in_ref_time)

def sysinfo(mpy_trace):

    r""" This function returns various informations about the hardware and operating system.
    :param
        mpy_trace - operation credentials and tracing
    :return - dictionary
        system - Operating system.
        release - Major version of the operating system.
        version - Major and subversions of the operating system.
        arch - Architecture of the operating system.
        processor - Processor running the code.
        logical_cpus - Amount of processes, that could run in parallel.
        sys_memory_bytes - Physical system memory in bytes
        username - Returns the username.
        homedir - Returns the home directory.
        hostname - Returns the host name.
    """

    import mpy_fct

    return mpy_fct.sysinfo(mpy_trace)

def pathtool(mpy_trace, in_path):

    r""" This function takes a string and converts it to a path. Additionally,
        it returns path components and checks.
    :param
        mpy_trace - operation credentials and tracing
        in_path - Path to be converted
    :return - dictionary
        out_path - Same as the input, but converted to a path.
        is_file - The path is a file path.
        file_exists - The file has been found under the given path.
        file_name - This is the actual file name.
        file_ext - This is the file extension or file type.
        is_dir - The path is a directory.
        dir_exists - The directory has been found under the given path.
        dir_name - This is the actual directory name.
        parent_dir - Path of the parent directory.
    """

    import mpy_fct

    return mpy_fct.pathtool(mpy_trace, in_path)

def path_join(mpy_trace, path_parts, file_extension):

    r""" This function joins components of a tuple to an OS path.
    :param
        mpy_trace - operation credentials and tracing
        path_parts - Tuple of parts to be joined. Exact order is critical. Examples:
                     ('C:', 'This', 'is', 'my', 'path', '.txt') - C:\This\is\my\path.txt
                     ('T:This_Fol', 'der_Will_Be_Split', 'this_Way') - T:\This_Fol\der_Will_Be_Split\this_Way
                     ('Y:', 'myFile.txt') - Y:\myFile.txt
        file_extension - String of the file extension (i.e. '.txt'). Leave
                         empty if path is a directory (None or '') or if the tuple already includes the
                         file extension.
    :return
        path_obj - OS path object of the joined path parts.
    """

    import mpy_fct

    return mpy_fct.path_join(mpy_trace, path_parts, file_extension)

def perfinfo(mpy_trace):

    r""" This function returns performance metrics.
    :param
        mpy_trace - operation credentials and tracing
    :return - dictionary
        boot_time - Timestamp of the latest recorded boot process.
        cpu_count_phys - Return the number of physical CPUs in the system.
        cpu_count_log - Return the number of logical CPUs in the system.
        cpu_freq_max - Return the maximum CPU frequency expressed in Mhz.
        cpu_freq_min - Return the minimum CPU frequency expressed in Mhz.
        cpu_freq_comb - Return the combined CPU frequency expressed in Mhz.
        cpu_perc_comb - Returns the current combined system-wide CPU utilization as a percentage.
        cpu_perc_indv - Returns the current individual system-wide CPU utilization as a percentage.
        mem_total_MB - Total physical memory in MB (exclusive swap).
        mem_available_MB - Memory in MB that can be given instantly to processes without the system going into swap.
        mem_used_MB - Memory used in MB.
        mem_free_MB - Memory not being used at all (zeroed) that is readily available in MB.
    """

    import mpy_fct

    return mpy_fct.perfinfo(mpy_trace)

def app_dict_to_string(app_dict):

    r""" This function prints the entire app dictionary in Terminal.
    :param
        app_dict - morPy global dictionary
    :return
        -
    """

    import mpy_fct

    return mpy_fct.app_dict_to_string(app_dict)

def tracing(module, operation, mpy_trace):

    r""" This function formats the trace to any given operation. This function is
        necessary to alter the mpy_trace as a pass down rather than pointing to the
        same mpy_trace passed down by the calling operation. If mpy_trace is to altered
        in any way (i.e. 'log_enable') it needs to be done after calling this function.
        This is why this function is called at the top of any operation.
    :param
        module - Name of the module, the operation is defined in (i.e. 'mpy_common')
        operation - Name of the operation executed (i.e. 'tracing(~)')
        mpy_trace - operation credentials and tracing
    :return
        mpy_trace_passdown - operation credentials and tracing
    """

    import mpy_fct

    return mpy_fct.tracing(module, operation, mpy_trace)

def mpy_thread_queue(mpy_trace, app_dict, name, priority, task):

    r""" This function handles the task queue (instance 'mpy_mt_priority_queue' of cl_mtPriorityQueue)
        of this framework. Its main purpose is to provide an easy handling of multithreaded
        programming in the way, that the developer just needs to fill the queue with tasks
        and tailor the multithreading parameters to the apps needs. However, when being
        bound to single threaded execution the queue will just execute sequentially, while
        prioritizing the tasks.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        name - Name of the task/thread.
        priority - Integer value. Sets the priority of the given task. Lower numbers indicate
                   a higher priority. Negative integers should be avoided.
        task - Statement, function or class/module to be run by the thread. A string
               is expected and will be executed via the exec()-function. The module has
               got to be referenced (if any) in order to work. Example:

                   task = 'app_module1.app_function1([mpy_trace], [app_dict], [...], [log])'
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        return mpy_mt.mpy_thread_queue(mpy_trace, app_dict, name, priority, task)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'mpy_thread_queue(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def mpy_threads_joinall(mpy_trace, app_dict):

    r""" This function stops execution of the code until all threads have finished their work.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        return mpy_mt.mpy_threads_joinall(mpy_trace, app_dict)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'mpy_threads_joinall(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def mpy_mt_abort(mpy_trace, app_dict):

    r""" This function aborts all pending tasks. However, the priority queue still exists and new threads
        would eventually pick up the aborted tasks.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        return mpy_mt.mpy_mt_abort(mpy_trace, app_dict)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'mpy_mt_abort(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def cl_read(mpy_trace, app_dict, wb_path, wb_sht, cells, dat, vba):

    r""" This function reads the cells of MS Excel workbooks.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        wb_path - Path to the MS Excel workbook
        wb_sht - Name of the sheet, to copy cells from
        cells - The cell or range of cells to read from. Two datatypes
                are accepted, either a single cell or a range, as shown:
                ["A1"] or ["A1:ZZ1000"] (letters are not case sensitive)
                Since 'cells' is a list, you may add as many items to the
                list, as you wish.
        dat - True means cells with formulae will only be represented by
            their calculated values. Notice that you need to close the
            loaded workbook and open it again if you want this behaviour
            to change.
        vba - True means any Visual Basic elements are preserved. If they
            are preserved they are still not editable. Notice that you
            need to close the loaded workbook and open it again if you
            want this behaviour to change.
    :return - dictionary
        check - The function ended with no errors
        cl_dict - Dictionary where cells are keys with copied arguments
                    {'cell1' : 'copied value 1' ,
                     'cell2' : 'copied value 2' ,
                     ...}
    """

    try:
        return mpy_xl.cl_read(mpy_trace, app_dict, wb_path, wb_sht, cells, dat, vba)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'cl_read(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def wb_close(mpy_trace, app_dict, wb_path):

    r""" This function closes an MS Excel workbook. It is advisory to
        only use the morPy functions to open and close a workbook, since a
        wb_close routine is implemented for various cases (i.e. Exceptions).
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        wb_path - Path to the MS Excel workbook
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        return mpy_xl.wb_close(mpy_trace, app_dict, wb_path)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'wb_close(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def wb_close_all(mpy_trace, app_dict):

    r""" This function closes all MS Excel workbooks opened by this app. It is
        advisory to only use the morPy functions to open and close a workbook, since
        a wb_close routine is implemented for various cases (i.e. Exceptions).
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        return mpy_xl.wb_close_all(mpy_trace, app_dict)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'wb_close_all(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def wb_create(mpy_trace, app_dict, xl_path):

    r""" This function creates a new empty excel workbook at a path handed
        to this function.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        return mpy_xl.wb_create(mpy_trace, app_dict, xl_path)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'wb_create(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def wb_load(mpy_trace, app_dict, wb_path, dat, vba):

    r""" This function connects to an MS Excel workbook. It is advisory to
        only use the morPy functions to open and close a workbook, since a
        wb_close routine is implemented for various cases (i.e. Exceptions).
        The workbook path will be connected to the object in RAM by creating
        a key in a dedicated dictionary as shown:
        >   app_dict["mpy_xl_loaded_wb_lst"] = {wb_path : wb_obj}
        This way a once opened Excel workbook may not be adressed twice.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        wb_path - Path to the MS Excel workbook
        dat - True means cells with formulae will only be represented by
            their calculated values. Notice that you need to close the
            loaded workbook and open it again if you want this behaviour
            to be changed.
        vba - True means any Visual Basic elements are preserved. If they
            are preserved they are still not editable. Notice that you
            need to close the loaded workbook and open it again if you
            want this behaviour to be changed.
    :return - dictionary
        check - The function ended with no errors
        wb_obj - The workbook object which was loaded
        wb_path - Path-object to the MS Excel workbook
        wb_sheets - List of the sheets in the loaded workbook
        sht_active - Name of the active sheet after opening the workbook
    """

    try:
        return mpy_xl.wb_load(mpy_trace, app_dict, wb_path, dat, vba)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'wb_load(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def wb_tbl_attributes(mpy_trace, app_dict, wb_path, tbl):

    r""" This function retrieves all attributes of an MS Excel table. To achieve
        it, the function openpyxl module will be called. If you are fine with
        only the most basic paramters of an MS Excel table, use wb_tbl_inquiry
        instead.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        wb_path - Path to the MS Excel workbook
        tbl - Name of the table to be analyzed
    :return - dictionary
        check - The function ended with no errors
        wb_obj - The workbook object which was loaded
        tbl_attr - List of the table's attributes
    """

    try:
        return mpy_xl.wb_tbl_attributes(mpy_trace, app_dict, wb_path, tbl)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'wb_tbl_attributes(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def wb_tbl_inquiry(mpy_trace, app_dict, wb_path):

    r""" This function inquires all tables of a worksheet. The result is a
        dictionary containing a number of datatypes.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        wb_path - Path to the MS Excel workbook
    :return - dictionary
        check - The function ended with no errors
        wb_obj - The workbook object which was loaded
        wb_sheets - List of the sheets in the loaded workbook
        tbl_lst - List of tables in the entire workbook
        tbl_rng - List of tuples of tables and their ranges
        tbl_sht - List of tuples of tables and the sheets they are on
    """

    try:
        return mpy_xl.wb_tbl_inquiry(mpy_trace, app_dict, wb_path)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'wb_tbl_inquiry(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def tk_progbar_indeterminate(mpy_trace, app_dict, GUI_dict):

    r""" This function invokes a window with an indeterminate progress bar
        and status messages.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - The mpy-specific global dictionary
        GUI_dict - Dictionary holding all needed parameters:

            GUI_dict = {'frame_title' : 'TITLE' , \
                        'frame_width' : 450 , \
                        'frame_height' : 300 , \
                        'headline_txt' : 'HEADLINE' , \
                        'headline_font_size' : 35 , \
                        'status_font_size' : 25
                        }

    :return - dictionary
        check - The function ended with no errors and a file was chosen
    """

    try:
        return mpy_ui_tk.tk_progbar_indeterminate(mpy_trace, app_dict, GUI_dict)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'tk_progbar_indeterminate(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def find_replace_saveas(mpy_trace, app_dict, search_obj, replace_tpl, save_as, overwrite):

    r""" This function finds and replaces strings in a readable object
        line by line. This may be text or csv files, but even strings
        would be converted so they are read line by line. This function
        does not repeat, but it's easy to iterate it. Once every line
        was evaluated and regular expressions got replaced, a file
        will be saved including all changes.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        search_obj - Any given object to search in for regular
                     expressions.
        replace_tpl - Tuple of tuples. Includes every tuple of regular
                      expressions and what they are supposed to be
                      replaced by. Example:
                    ((replace 1, by 1), (replace 2, by 2), ...)
        save_as - Complete path of the file to be saved.
        overwrite - True, if new files shall overwrite existing ones,
                    if there are any. False otherwise.
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        return mpy_bulk_ops.find_replace_saveas(mpy_trace, app_dict, search_obj, replace_tpl, save_as, overwrite)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'find_replace_saveas(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def web_request(mpy_trace, app_dict, URL, req_dict):

    r""" This function connects to an URL and delivers the responses requested. Data
        of spreadsheets and other media may be extracted with this method.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - The mpy-specific global dictionary
        URL - Link to the webpage
        req_dict - Dictionary to determine which responses are requested. It
                   is fine to only address the requests needed. THis is the
                   dictionary:

                        req_dict =  {'apparent_encoding' : False , \
                                    'content' : False , \
                                    'cookies' : False , \
                                    'elapsed' : False , \
                                    'encoding' : False , \
                                    'headers' : False , \
                                    'history' : False , \
                                    'is_permanent_redirect' : False , \
                                    'is_redirect' : False , \
                                    'links' : False , \
                                    'next' : False , \
                                    'ok' : False , \
                                    'reason' : False , \
                                    'request' : False , \
                                    'status_code' : False , \
                                    'text' : False , \
                                    'url' : False
                                    }

    :return - dictionary
        check - The function ended with no errors and a file was chosen
        html_code - Holds the 3 digit identifier for the html response
        response_dict - Returns the responses requested. The response includes
                        the same keys as the (full) req_dict.
    """

    try:
        return mpy_wscraper.web_request(mpy_trace, app_dict, URL, req_dict)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'dialog_sel_file(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')