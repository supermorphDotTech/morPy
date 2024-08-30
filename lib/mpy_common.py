"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers generally useful functions.
"""

import mpy_fct
import mpy_msg
import sys
import gc
import chardet
import io

from tkinter import Tk
from tkinter import filedialog
from mpy_decorators import metrics

@metrics
def decode_to_plain_text(
    mpy_trace: str,
    prj_dict: dict,
    src_input: str,
    encoding: str,
) -> dict:
    """
    This function decodes different types of data and returns
    a plain text to work with in python. The return result behaves
    like using the open(file, 'r') method.
    
    :param mpy_trace: operation credentials and tracing
    :param prj_dict: morPy global dictionary
    :param src_input: Any kind of data to be decoded. Binary expected.
    :param encoding: String that defines encoding. Leave empty to auto detect.
    
    :return: dict
        result: Decoded result. Buffered object that my be used with the
            readlines() method.
        encoding: String containing the encoding of src_input.
        lines: Number of lines in the file.
        mpy_trace: Operation credentials and tracing
    
    :example:
        src_input = open(src_file, 'rb')
        encoding = 'utf-16-le'
        retval = decode_to_plain_text(mpy_trace, prj_dict, src_input, encoding)
    """

    module = 'mpy_common'
    operation = 'decode_to_plain_text(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    result = 'VOID'
    src_copy = b''
    decode = False
    lines = 0
    if encoding is None: encoding = ''

    try:
        # Copy all contents
        src_copy = src_input.read()
        lines = src_copy.count(b'\n') + 1

        # Auto detect encoding if not provided
        if not encoding:
            try:
                encoding = chardet.detect(src_copy)["encoding"]
                decode = True

        #   Warning if src_copy is of wrong format or not encoded.
            except Exception as e:
                log_message = (
                    f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{prj_dict["decode_to_plain_text_msg"]}: {e}'
                )
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')
                
        # Validate provided encoding
        else:
            try:
                chardet.detect(src_copy)["encoding"]
                decode = True

        #   Not encoded if an exception is raised
            except Exception as e:
                log_message = (
                    f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{prj_dict["decode_to_plain_text_msg"]}: {e}'
                )
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')
                
        # Decode the content
        if decode:
            result = io.StringIO(src_copy.decode(encoding))
            # Decoded from ### to plain text.
            log_message = (
                f'{prj_dict["loc"]["mpy"]["decode_to_plain_text_from"]} {encoding}) '
                f'{prj_dict["loc"]["mpy"]["decode_to_plain_text_to"]}\n'
                f'encoding: {encoding}'
            )
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        # Handle unsupported or non-encoded input
        else:
            result = io.StringIO(src_copy.decode('utf-8', errors='ignore'))
            # The Input is not decoded or not supported. No action taken.
            log_message = (
                f'{prj_dict["loc"]["mpy"]["decode_to_plain_text_not"]}\n'
                f'encoding: {encoding}'
            )
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    except Exception as e:
        log_message = (
            f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}'
        )
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return {
        'mpy_trace': mpy_trace,
        'result': result,
        'encoding': encoding,
        'lines': lines,
    }

@metrics
def dialog_sel_file(
    mpy_trace: str,
    prj_dict: dict,
    init_dir: str,
    ftypes: str,
    title: str,
) -> dict:
    """
    This function opens a dialog for the user to select a file.
    
    :param mpy_trace: operation credentials and tracing
    :param prj_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param ftypes: This tuple of 2-tuples specifies, which filetypes will be
        selsectable in the dialog box.
    :param title: Title of the open file dialog
    
    :return: dict
        mpy_trace: [dictionary] operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        sel_file: Path of the selected file
        file_selected: True, if file was selected. False, if canceled.
        
    :example:
        init_dir = prj_dict["sys"]["homedir"]
        ftypes = (('PDF','*.pdf'),('Textfile','*.txt'),('All Files','*.*'))
        title = 'Select a file...'
        sel_file = dialog_sel_file(mpy_trace, prj_dict, init_dir, ftypes, title)
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'dialog_sel_file(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    check = False
    file_selected = False

    try:
        # Invoke the Tkinter root window and withdraw it to force the
        # dialog to be opened in the foreground
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        # Open the actual dialog in the foreground and store the chosen folder
        sel_file = filedialog.askopenfilename(
            parent = root,
            title = f'{title}',
            initialdir = init_dir,
            filetypes = ftypes,
        )

        if not sel_file:
            # No file was chosen by the user.
            log_message = (
                f'{prj_dict["loc"]["mpy"]["dialog_sel_file_nosel"]}\n'
                f'sel_file: VOID\n'
                f'{prj_dict["loc"]["mpy"]["dialog_sel_file_choice"]}: {prj_dict["loc"]["mpy"]["dialog_sel_file_cancel"]}'
            )
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:
            file_selected = True
            # A file was chosen by the user.
            log_message = (
                f'{prj_dict["loc"]["mpy"]["dialog_sel_file_asel"]}\n'
                f'sel_file: {sel_file}\n'
                f'{prj_dict["loc"]["mpy"]["dialog_sel_file_choice"]}: {prj_dict["loc"]["mpy"]["dialog_sel_file_open"]}'
            )
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

            # Create a path object
            mpy_fct.pathtool(mpy_trace, sel_file)

        check = True

    # Error detection
    except Exception as e:
        log_message = (
            f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}'
        )
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    # Return a dictionary
    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        'sel_file' : sel_file,
        'file_selected' : file_selected,
        }

@metrics
def dialog_sel_dir(
    mpy_trace: str,
    prj_dict: dict,
    init_dir: str,
    title: str,
) -> dict:
    """
    This function opens a dialog for the user to select a directory.
    
    :param mpy_trace: operation credentials and tracing
    :param prj_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param title: Title of the open directory dialog
        
    :return: dict
        mpy_trace: [dictionary] operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        sel_dir: Path of the selected directory
        dir_selected: True, if directory was selected. False, if canceled.
        
    :example:
        init_dir = prj_dict["sys"]["homedir"]
        title = 'Select a file...'
        sel_dir = dialog_sel_dir(mpy_trace, prj_dict, init_dir, title)
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'dialog_sel_dir(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    check = False
    dir_selected = False

    try:
        # Invoke the Tkinter root window and withdraw it to force the
        # dialog to be opened in the foreground
        root = Tk()
        root.withdraw()

        # Open the actual dialog in the foreground and store the chosen folder
        root.dirname = filedialog.askdirectory(
            parent = root,
            title = f'{title}',
            initialdir = init_dir,
        )
        sel_dir = root.dirname

        if not sel_dir:
            # No directory was chosen by the user.
            log_message = (
                f'{prj_dict["loc"]["mpy"]["dialog_sel_dir_nosel"]}\n'
                f'sel_dir: VOID\n'
                f'{prj_dict["loc"]["mpy"]["dialog_sel_dir_choice"]}: {prj_dict["dialog_sel_dir_cancel"]}'
            )
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:
            dir_selected = True
            # A directory was chosen by the user.
            log_message = (
                f'{prj_dict["loc"]["mpy"]["dialog_sel_dir_asel"]}\n'
                f'sel_dir: {sel_dir}\n'
                f'{prj_dict["loc"]["mpy"]["dialog_sel_dir_choice"]}: {prj_dict["loc"]["mpy"]["dialog_sel_dir_open"]}'
            )
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

            # Create a path object
            mpy_fct.pathtool(mpy_trace, sel_dir)

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
        'sel_dir' : sel_dir,
        'dir_selected' : dir_selected,
        }

@metrics
def fso_copy_file(mpy_trace, prj_dict, source, dest, ovwr_perm):

    """ This function is used to copy a single file from source to destination.
        A file check is already included and will be performed.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        source - Complete path to the source file including the file extension
        dest - Complete path to the destination file including the file extension
        ovwr_perm - If TRUE, the destination file may be overwritten.
    :return - dictionary
        check - The function ended with no errors
        source - Path to the source file as a path object
        dest - Path to the destination file as a path object
        mpy_trace - [dictionary] operation credentials and tracing
    """

    import mpy_msg, mpy_fct
    import sys, gc, shutil

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'fso_copy_file(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False

    try:

        # Check the source file
        source_eval = mpy_fct.pathtool(mpy_trace, source)
        source_exist = source_eval["file_exists"]
        source = source_eval["out_path"]

        # Check the destination file
        dest_eval = mpy_fct.pathtool(mpy_trace, dest)
        dest_exist = dest_eval["file_exists"]
        dest = dest_eval["out_path"]

        # Evaluate the existence of the source
        if source_exist:

            # Evaluate the existence of the destination and overwrite permission
            if dest_exist and ovwr_perm:

                shutil.copyfile(source, dest)

                # Create a log
                # A file has been copied and the original was overwritten.
                log_message = (f'{prj_dict["loc"]["mpy"]["fso_copy_file_copy_ovwr"]}\n'
                              f'{prj_dict["loc"]["mpy"]["fso_copy_file_source"]}: {source}\n'
                              f'{prj_dict["loc"]["mpy"]["fso_copy_file_dest"]}: {dest}\n'
                              f'dest_exist: {dest_exist}\n'
                              f'ovwr_perm: {ovwr_perm}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

            # Evaluate the existence of the destination and overwrite permission
            if dest_exist and not ovwr_perm:

                shutil.copyfile(source, dest)

                # Create a log
                # A file was not copied because it already exists and no overwrite permission was given.
                log_message = (f'{prj_dict["loc"]["mpy"]["fso_copy_file_copy_not_ovwr"]}\n'
                              f'{prj_dict["loc"]["mpy"]["fso_copy_file_source"]}: {source}\n'
                              f'{prj_dict["loc"]["mpy"]["fso_copy_file_dest"]}: {dest}\n'
                              f'dest_exist: {dest_exist}\n'
                              f'ovwr_perm: {ovwr_perm}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

            if dest_exist:

                shutil.copyfile(source, dest)

                # Create a log
                # A file has been copied.
                log_message = (f'{prj_dict["loc"]["mpy"]["fso_copy_file_copy"]}\n'
                              f'{prj_dict["loc"]["mpy"]["fso_copy_file_source"]}: {source}\n'
                              f'{prj_dict["loc"]["mpy"]["fso_copy_file_dest"]}: {dest}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

            check = True

        else:

            # Create a log
            # A file could not be copied, because it does not exist.
            log_message = (f'{prj_dict["loc"]["mpy"]["fso_copy_file_not_exist"]}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_copy_file_source"]}: {source}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_copy_file_dest"]}: {dest}\n'
                          f'source_exist: {source_exist}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}\n'
                      f'{prj_dict["loc"]["mpy"]["fso_copy_file_source"]}: {source}\n'
                      f'{prj_dict["loc"]["mpy"]["fso_copy_file_dest"]}: {dest}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'mpy_trace' : mpy_trace, \
            'check' : check, \
            'source' : source, \
            'dest' : dest
            }

@metrics
def fso_create_dir(mpy_trace, prj_dict, mk_dir):

    """ This function creates a directory as well as it's parents
        recursively.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        mk_dir - Path to the directory/tree to be created

    :return - dictionary
        check - The function ended with no errors
        mpy_trace - [dictionary] operation credentials and tracing
    """

    import mpy_msg, mpy_fct
    import sys, gc, os

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'fso_create_dir(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False

    try:

        # Check the directory
        dir_eval = mpy_fct.pathtool(mpy_trace, mk_dir)
        dir_exist = dir_eval["dir_exists"]
        mk_dir = dir_eval["out_path"]

        if dir_exist:

            # Create a log
            # The directory already exists.
            log_message = (f'{prj_dict["loc"]["mpy"]["fso_create_dir_not_created"]}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_create_dir_directory"]}: {mk_dir}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_create_dir_direxist"]}: {dir_exist}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

            os.makedirs(mk_dir)

            # Create a log
            # The directory has been created.
            log_message = (f'{prj_dict["loc"]["mpy"]["fso_create_dir_created"]}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_create_dir_directory"]}: {mk_dir}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}\n'
                      f'{prj_dict["loc"]["mpy"]["fso_create_dir_directory"]}: {mk_dir}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'mpy_trace' : mpy_trace, \
            'check' : check
            }

@metrics
def fso_delete_dir(mpy_trace, prj_dict, del_dir):

    """ This function is used to delete an entire directory including it's
        contents. A directory check is already included and will be performed.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        del_dir - Path to the directory to be deleted
    :return - dictionary
        check - The function ended with no errors
        mpy_trace - [dictionary] operation credentials and tracing
    """

    import mpy_msg, mpy_fct
    import sys, shutil, gc

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'fso_delete_dir(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False

    try:

        # Check the directory
        dir_eval = mpy_fct.pathtool(mpy_trace, del_dir)
        dir_exist = dir_eval["dir_exists"]
        del_dir = dir_eval["out_path"]

        if dir_exist:

            shutil.rmtree(del_dir)

            # Create a log
            # The directory has been deleted.
            log_message = (f'{prj_dict["loc"]["mpy"]["fso_delete_dir_deleted"]}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_create_dir_directory"]}: {del_dir}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

            # Create a log
            # The directory does not exist.
            log_message = (f'{prj_dict["loc"]["mpy"]["fso_delete_dir_notexist"]}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_create_dir_directory"]}: {del_dir}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_create_dir_direxist"]}: {dir_exist}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}\n'
                      f'{prj_dict["loc"]["mpy"]["fso_delete_dir_directory"]}: {del_dir}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'mpy_trace' : mpy_trace, \
            'check' : check
            }

@metrics
def fso_delete_file(mpy_trace, prj_dict, del_file):

    """ This function is used to delete a file. A path check is
        already included and will be performed.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        del_file - Path to the directory to be deleted

    :return - dictionary
        check - The function ended with no errors
        mpy_trace - [dictionary] operation credentials and tracing
    """

    import mpy_msg, mpy_fct
    import sys, os, gc

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'fso_delete_file(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False

    try:

        # Check the directory
        file_eval = mpy_fct.pathtool(mpy_trace, del_file)
        file_exist = file_eval["file_exists"]
        del_file = file_eval["out_path"]

        if file_exist:

            os.remove(del_file)

            # Create a log
            # The file has been deleted.
            log_message = (f'{prj_dict["loc"]["mpy"]["fso_delete_file_deleted"]}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_delete_file_file"]}: {del_file}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

            # Create a log
            # The file does not exist.
            log_message = (f'{prj_dict["loc"]["mpy"]["fso_delete_file_notexist"]}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_delete_file_file"]}: {del_file}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_delete_file_exist"]}: {file_exist}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}\n'
                      f'{prj_dict["loc"]["mpy"]["fso_delete_file_file"]}: {del_file}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'mpy_trace' : mpy_trace, \
            'check' : check
            }

@metrics
def fso_walk(mpy_trace, prj_dict, path, depth):

    """ This function returns the contents of a directory.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
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

    import mpy_msg, mpy_fct
    import sys, os, gc

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'fso_delete_file(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False
    walk_dict = {}
    root = r""
    dirs = []
    files = []
    cnt_roots = 0

    try:

        # Check the directory
        if mpy_fct.pathtool(mpy_trace, path)["dir_exists"]:

            for root, dirs, files in os.walk(path):
                
                # Exit if depth is reached
                if cnt_roots > depth:
                    
                    break
                    
                walk_dict.update({f'root{cnt_roots}' : {'root' : root, 'dirs' : dirs, 'files' : files}})
                
                cnt_roots += 1

            # Create a log
            # Directory analyzed.
            log_message = (f'{prj_dict["loc"]["mpy"]["fso_walk_path_done"]}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_walk_path_dir"]}: {path}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

            # Create a log
            # The directory does not exist.
            log_message = (f'{prj_dict["loc"]["mpy"]["fso_walk_path_notexist"]}\n'
                          f'{prj_dict["loc"]["mpy"]["fso_walk_path_dir"]}: {path}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'mpy_trace' : mpy_trace, \
            'check' : check, \
            'walk_dict' : walk_dict
            }

@metrics
def regex_findall(mpy_trace, prj_dict, search_obj, pattern):

    """ This function searches for regular expression in any given object and returns a list of found expressions.'
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        pattern - The regular expression to search for
    :return - dictionary
        result - The list of expressions found in the input. Is None, if nothing was found.
        mpy_trace - [dictionary] operation credentials and tracing
    """

    import mpy_fct, mpy_msg
    import sys, re, gc

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'regex_findall(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Apply standard formats
    search_obj = f'{search_obj}'
    pattern =    f'{pattern}'
    result = None

    # Create a log
    # Searching for regular expressions.
    log_message = (f'{prj_dict["loc"]["mpy"]["regex_findall_init"]}\n'
                  f'{prj_dict["loc"]["mpy"]["regex_findall_pattern"]}: {pattern}\n'
                  f'search_obj: {search_obj}')
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    try:
        # Search for the pattern
        result_match = re.findall(pattern, search_obj)
        result = result_match.group() if result_match else None

        # Create a log
        # Search completed.
        log_message = (f'{prj_dict["loc"]["mpy"]["regex_findall_compl"]}\n'
                      f'{prj_dict["loc"]["mpy"]["regex_findall_result"]}: {result}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'mpy_trace' : mpy_trace, \
            'result' : result
            }

@metrics
def regex_find1st(mpy_trace, prj_dict, search_obj, pattern):

    """ This function searches for regular expression in any given object and returns the first match.'
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        pattern - The regular expression to search for

    :return - list
        result - The list of expressions found in the input. Is None, if nothing was found.
    """

    import mpy_fct, mpy_msg
    import sys, re, gc

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'regex_find1st(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False

    try:
    
        # Apply standard formats
        search_string = f'{search_obj}'
        pattern = f'{pattern}'
        result = None
    
        # Create a log
        # Searching for regular expressions.
        log_message = (f'{prj_dict["loc"]["mpy"]["regex_find1st_init"]}\n'
                      f'{prj_dict["loc"]["mpy"]["regex_find1st_pattern"]}: {pattern}\n'
                      f'search_obj: {search_string}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        if search_string is not None:

            result_match = re.search(pattern, search_string)
            result = result_match.group() if result_match else None

                # Create a log
                # Search completed.
            log_message = (f'{prj_dict["loc"]["mpy"]["regex_find1st_compl"]}\n'
                          f'{prj_dict["loc"]["mpy"]["regex_find1st_result"]}: {result}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

            result = [search_obj]

                # Create a log
                # String is NoneType. No Regex executed.
            log_message = (f'{prj_dict["loc"]["mpy"]["regex_find1st_none"]}\n'
                          f'{prj_dict["loc"]["mpy"]["regex_find1st_result"]}: {result}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')
            
        check = True

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'mpy_trace' : mpy_trace, \
            'check' : check, \
            'result' : result
            }

@metrics
def regex_split(mpy_trace, prj_dict, search_obj, delimiter):

    """ This function splits an object into a list by a given delimiter.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        delimiter - The character or string used to split the search_obj into a list. Have
                    in mind, that special characters may need a backslash preceding them (e.g. '\.' to use
                    '.' as a delimiter).
    :return - list
        result - The list of parts split from the input
    """

    import mpy_fct, mpy_msg
    import sys, re, gc

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'regex_split(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False

    try:
    
        # Apply standard formats
        search_string = f'{search_obj}'
        delimiter =    f'{delimiter}'
    
        # Create a log
        # Splitting a string by a given delimiter.
        log_message = (f'{prj_dict["loc"]["mpy"]["regex_split_init"]}\n'
                      f'{prj_dict["loc"]["mpy"]["regex_split_delimiter"]}: {delimiter}\n'
                      f'search_obj: {search_string}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        if search_string is not None:

            result = re.split(delimiter, search_string)

                # Create a log
                # String has been split.
            log_message = (f'{prj_dict["loc"]["mpy"]["regex_split_compl"]}\n'
                          f'{prj_dict["loc"]["mpy"]["regex_split_result"]}: {result}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

            result = [search_obj]

                # Create a log
                # String is NoneType. No Split executed.
            log_message = (f'{prj_dict["loc"]["mpy"]["regex_split_none"]}\n'
                          f'{prj_dict["loc"]["mpy"]["regex_split_result"]}: {result}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')
            
            check = True

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'mpy_trace' : mpy_trace, \
            'check' : check, \
            'result' : result
            }

@metrics
def regex_replace(mpy_trace, prj_dict, search_obj, search_for, replace_by):

    """ This function substitutes characters or strings in an input object.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        search_for - The character or string to be replaced
        replace_by - The character or string to substitute

    :return
        result - The substituted character or string
    """

    import mpy_fct, mpy_msg
    import sys, re, gc

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'regex_replace(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False

    try:
            
        # Apply standard formats
        search_obj = f'{search_obj}'
        search_for = f'{search_for}'
        replace_by = f'{replace_by}'
    
        # Create a log
        # Changing a string by given parameters.
        log_message = (f'{prj_dict["loc"]["mpy"]["regex_replace_init"]}\n'
                      f'search_for: {search_for}\n'
                      f'replace_by: {replace_by}\n'
                      f'search_obj: {search_obj}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        result = re.sub(search_for, replace_by, search_obj)

            # Create a log
            # String substituted.
        log_message = (f'{prj_dict["loc"]["mpy"]["regex_replace_compl"]}\n'
                      f'{prj_dict["loc"]["mpy"]["regex_replace_result"]}: {result}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')
        
        check = True

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'mpy_trace' : mpy_trace, \
            'check' : check, \
            'result' : result
            }

@metrics
def regex_remove_special(mpy_trace, prj_dict, inp_string, spec_lst):

    """ This function removes special characters of a given string and instead inserts
        any character if defined. The spec_lst is a list consiting of tuples
        consisting of special characters and what they are supposed to get exchanged
        with. Using a blank list will invoke a standard list where specials will be
        removed and not replaced by any other character. This function may even be used
        to perform a number of regex_replace actions on the same string, because it
        will replace what ever is given to the tuples-list. Essentially, you can use
        any valid regular expression instead of the special character.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        inp_string - The string to be altered
        spec_lst - List consisting of 2-tuples as a definition of which special character
                   is to be replaced by which [(special1,replacement1),...]. Set the
                   list to [('','')] to invoke the standard replace list.
    :return
        result - The substituted chracter or string
    """

    import mpy_fct, mpy_msg
    import sys, re, gc

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'regex_remove_special(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False

    try:
    
        # Define the standard special character removal list. The special characters will
        # later be converted to a raw string with repr(). You may use this list as a
        # guideline of how to define special and replacement characters.
        spec_lst_std =  [ \
                        (' ',''), \
                        ('¤',''), \
                        ('¶',''), \
                        ('§',''), \
                        ('!',''), \
                        ('\"',''), \
                        ('#',''), \
                        ('\$',''), \
                        ('%',''), \
                        ('&',''), \
                        ('\'',''), \
                        ('\(',''), \
                        ('\)',''), \
                        ('\*',''), \
                        ('\+',''), \
                        (',',''), \
                        ('-',''), \
                        ('\.',''), \
                        ('/',''), \
                        (':',''), \
                        (';',''), \
                        ('=',''), \
                        ('>',''), \
                        ('<',''), \
                        ('\?',''), \
                        ('@',''), \
                        ('\[',''), \
                        ('\]',''), \
                        ('\\\\',''), \
                        ('\^',''), \
                        ('_',''), \
                        ('`',''), \
                        ('´',''), \
                        ('{',''), \
                        ('}',''), \
                        ('\|',''), \
                        ('~','')
                        ]

        # Preparing parameters
        load_std = False
        inp_string = f'{inp_string}'

        # Evaluate the length of spec_lst
        lst_len = len(spec_lst)

        # Invoke the standard set of specials to be removed
        if spec_lst[0] == ('','') and lst_len < 2:

            spec_lst = spec_lst_std
            load_std = True

        # Create a log
        # Removing special characters of a string and replacing them.
        log_message = (f'{prj_dict["loc"]["mpy"]["regex_remove_special_init"]}\n'
                      f'inp_string: {inp_string}\n'
                      f'spec_lst: {spec_lst}\n'
                      f'load_std: {load_std}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        # Initialize the resulting string
        result = inp_string

        # Loop through the tuples list and remove/replace characters of the
        # input string
        for tpl in spec_lst:

            # Convert specials to raw string and perform search/replace
            result = re.sub(f'{tpl[0]}', f'{tpl[1]}', result)

            # Create a log
            # String substituted.
        log_message = (f'{prj_dict["loc"]["mpy"]["regex_remove_special_compl"]}\n'
                      f'inp_string: {inp_string}\n'
                      f'{prj_dict["loc"]["mpy"]["regex_remove_special_result"]}: {result}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')
        
        check = True

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}\n'
                      f'inp_string: {inp_string}\n'
                      f'{prj_dict["loc"]["mpy"]["regex_remove_special_result"]}: {result}\n'
                      f'{prj_dict["loc"]["mpy"]["regex_remove_special_tuple"]}: {tpl}\n'
                      f'{prj_dict["loc"]["mpy"]["regex_remove_special_special"]}: {tpl[0]}\n'
                      f'{prj_dict["loc"]["mpy"]["regex_remove_special_replacer"]}: {tpl[1]}\n'
                      f'load_std: {load_std}\n'
                      f'spec_lst: {spec_lst}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    # Return a dictionary
    return{
        'mpy_trace' : mpy_trace, \
        'check' : check, \
        'result' : result
        }

@metrics
def textfile_write(mpy_trace, prj_dict, filepath, content):

    """ This function appends any textfile and creates it, if there
        is no such file.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        filepath - Path to the textfile including its name and filetype
        content - Something that will be printed as a string.

    :return
        -
    """

    import mpy_fct, mpy_msg
    import sys, os.path, gc

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'textfile_write(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False

    try:
    
        # Apply standard formats
        content = f'{content}'
        filepath = os.path.abspath(filepath)

        # Append to a textfile
        if os.path.isfile(filepath):

            with open(filepath, 'a') as ap:
                ap.write(f'\n{content}')

            # Create a log
            # Textfile has been appended to.
            log_message = (f'{prj_dict["loc"]["mpy"]["textfile_write_appended"]}\n'
                          f'{prj_dict["loc"]["mpy"]["textfile_write_content"]}: {content}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        # Create and write a textfile
        else:
            with open(filepath, 'w') as wr:
                wr.write(content)

            # Create a log
            # Textfile has been created.
            log_message = (f'{prj_dict["loc"]["mpy"]["textfile_write_created"]}\n'
                          f'{prj_dict["loc"]["mpy"]["textfile_write_content"]}: {content}')
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')
            
        check = True

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }

@metrics
def testprint(mpy_trace, prj_dict, input):

    # import mpy_fct

    """ This function prints any value given. It is intended to be used for debugging.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        input - Something that will be printed as a string.
    :return
        -
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_common'
    # operation = 'testprint(~)'
    # mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    value     = f'{input}'
    intype    = f'{type(input)}'

    print(f'<TEST> value: {value}\n'
          f'<TEST> type: {intype}\n')

@metrics
def wait_for_input(mpy_trace, prj_dict, msg_text):

    """ This function makes the program wait until a user input was made.
        The user input can be returned to the calling module.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        msg_text - The text to be displayed before user input
    :return
        usr_input - Returns the input of the user
    """

    import mpy_fct, mpy_msg
    import sys, gc

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'wait_for_input(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Preparing parameters
    check = False

    try:

        usr_input = input(f'{msg_text}\n')

        # Create a log
        # A user input has been made.
        log_message = (f'{prj_dict["loc"]["mpy"]["wait_for_input_compl"]}\n'
                      f'{prj_dict["loc"]["mpy"]["wait_for_input_messsage"]}: {msg_text}\n'
                      f'{prj_dict["loc"]["mpy"]["wait_for_input_usr_inp"]}: {usr_input}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

    # Error detection
    except Exception as e:
        log_message = (f'{prj_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["loc"]["mpy"]["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')
        
    # Return a dictionary
    return{
        'mpy_trace' : mpy_trace, \
        'check' : check, \
        'usr_input' : usr_input
        }