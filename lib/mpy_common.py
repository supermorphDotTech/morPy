"""
Author:     Bastian Neuwirth
Date:       06.11.2021
Version:    0.1
Descr.:     This module delivers generally useful functions.
"""

def decode_to_plain_text(mpy_trace, prj_dict, src_input, encoding):

    """ This function decodes different types of data and returns
        a plain text to work with in python. The return result behaves
        like using the open(file, 'r') method.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        src_input - Any kind of data to be decoded. Binary expected. Example:
                    src_input = open(src_file, 'rb')
        encoding - String that defines encoding. Leave empty to auto detect. Examples:
                   '' - Empty. Encoding will be determined automatically. May be incorrect.
                   'utf-16-le' - Decode UTF-16 LE to buffered text.
    :return - dictionary
        result - Decoded result. Bufferd object that my be used with the readlines() method.
        encoding - String containing the encoding of src_input.
        lines - Number of lines in the file.
    """

    import mpy_fct, mpy_msg
    import sys, gc, chardet, io

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'decode_to_plain_text(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparation
    result = 'VOID'
    src_copy = b''
    decode = False
    lines = 0

    try:

    #   Loop through the input line by line to copy all contents
        for ln in src_input:

            src_copy += ln
            lines += 1

    #   Determine auto detection of encoding
        if encoding == '':

        #   Detect encoding
            try:

                encoding = chardet.detect(src_input)['encoding']
                decode = True

        #   Log a warning if src_input is of wrong format or not encoded at all.
            except Exception as e:

                log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                              + prj_dict['decode_to_plain_text_msg'] + ': {}'. format(e)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')

    #   Use given encoding and check, if it exists.
        else:

        #   Check encoding
            try:

                chardet.detect(src_copy)['encoding']
                decode = True

        #   Not encoded if an exception is raised
            except Exception as e:

                log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                              + prj_dict['decode_to_plain_text_msg'] + ': {}'. format(e)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')

    #   Decode
        if decode == True:

            result = io.StringIO(src_copy.decode(encoding))

        #   Create a log
        #   Decoded from ### to plain text.
            log_message = prj_dict['decode_to_plain_text_1'] \
                          + ' ' + str(encoding) + ' ' \
                          + prj_dict['decode_to_plain_text_2'] + '\n' \
                          + 'encoding: ' + encoding
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Input is not encoded or not supported.
        else:

            result = io.StringIO(src_input)

        #   Create a log
        #   The Input is not decoded or not supported. No action taken.
            log_message = prj_dict['decode_to_plain_text_not'] + '\n' \
                          + 'encoding: ' + encoding
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return{
            'result' : result, \
            'encoding' : encoding, \
            'lines' : lines
            }

def dialog_sel_file(mpy_trace, prj_dict, init_dir, ftypes):

    """ This function opens a dialog for the user to select a file.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        init_dir - The directory in which the dialog will initially be opened
        ftypes - This tuple of 2-tuples specifies, which filetypes will be
                displayed by the dialog box, e.g.
                (('type1','*.t1'),('All Files','*.*'),...)
    :return - dictionary
        check - The function ended with no errors and a file was chosen
        sel_file - Path of the selected file
    """

    import mpy_msg, mpy_fct
    import sys
    from tkinter import Tk
    from tkinter import filedialog

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'dialog_sel_file(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False

    try:

    #   Invoke the Tkinter root window and withdraw it to force the
    #   dialog to be opened in the foreground
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)

    #   Open the actual dialog in the foreground and store the chosen folder
        root.filename = filedialog.askopenfilename( \
                            parent = root, \
                            initialdir = init_dir, \
                            filetypes = ftypes)
        sel_file = root.filename

        if len(sel_file) == 0:

        #   Create a log
        #   No file was chosen by the user.
            log_message =   prj_dict['dialog_sel_file_nosel'] + '\n' \
                            + 'sel_file: VOID\n' \
                            + prj_dict['dialog_sel_file_choice'] + ': ' + prj_dict['dialog_sel_file_cancel']
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

        #   Create a log
        #   A file was chosen by the user.
            log_message =   prj_dict['dialog_sel_file_asel'] + '\n' \
                            + 'sel_file: ' + str(sel_file) + '\n' \
                            + prj_dict['dialog_sel_file_choice'] + ': ' + prj_dict['dialog_sel_file_open']
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Create a path object
            mpy_fct.pathtool(mpy_trace, sel_file)

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'check' : check, \
        'sel_file' : sel_file
        }

def dialog_sel_dir(mpy_trace, prj_dict, init_dir):

    """ This function opens a dialog for the user to select a directory.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        init_dir - The directory in which the dialog will initially be opened

    :return - dictionary
        check - The function ended with no errors and a file was chosen
        sel_dir - Path of the selected directory
    """

    import mpy_msg, mpy_fct
    import sys
    from tkinter import Tk
    from tkinter import filedialog

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'dialog_sel_dir(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False

    try:

    #   Invoke the Tkinter root window and withdraw it to force the
    #   dialog to be opened in the foreground
        root = Tk()
        root.withdraw()

    #   Open the actual dialog in the foreground and store the chosen folder
        root.dirname = filedialog.askdirectory( \
                            parent = root, \
                            initialdir = init_dir)
        sel_dir = root.dirname

        if len(sel_dir) == 0:

        #   Create a log
        #   No directory was chosen by the user.
            log_message = prj_dict['dialog_sel_dir_nosel'] + '\n' \
                          + 'sel_dir: VOID\n' \
                          + prj_dict['dialog_sel_dir_choice'] + ': ' + prj_dict['dialog_sel_dir_cancel']
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

        #   Create a log
        #   A directory was chosen by the user.
            log_message = prj_dict['dialog_sel_dir_asel'] + '\n' \
                            + 'sel_dir: ' + str(sel_dir) + '\n' \
                            + prj_dict['dialog_sel_dir_choice'] + ': ' + prj_dict['dialog_sel_dir_open']
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Create a path object
            mpy_fct.pathtool(mpy_trace, sel_dir)

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'check' : check, \
        'sel_dir' : sel_dir
        }

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
    """

    import mpy_msg, mpy_fct
    import sys, shutil

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'fso_copy_file(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False

    try:

    #   Check the source file
        source_eval = mpy_fct.pathtool(mpy_trace, source)
        source_exist = source_eval['file_exists']
        source = source_eval['out_path']

    #   Check the destination file
        dest_eval = mpy_fct.pathtool(mpy_trace, dest)
        dest_exist = dest_eval['file_exists']
        dest = dest_eval['out_path']

    #   Evaluate the existence of the source
        if source_exist == True:

        #   Evaluate the existence of the destination and overwrite permission
            if dest_exist == True and ovwr_perm == True:

                shutil.copyfile(source, dest)

            #   Create a log
            #   A file has been copied and the original was overwritten.
                log_message = prj_dict['fso_copy_file_copy_ovwr'] + '\n' \
                              + prj_dict['fso_copy_file_source'] + ': ' + str(source) + '\n' \
                              + prj_dict['fso_copy_file_dest'] + ': ' + str(dest) + '\n' \
                              + 'dest_exist: ' + str(dest_exist) + '\n' \
                              + 'ovwr_perm: ' + str(ovwr_perm)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Evaluate the existence of the destination and overwrite permission
            if dest_exist == True and ovwr_perm == False:

                shutil.copyfile(source, dest)

            #   Create a log
            #   A file was not copied because it already exists and no overwrite permission was given.
                log_message = prj_dict['fso_copy_file_copy_not_ovwr'] + '\n' \
                              + prj_dict['fso_copy_file_source'] + ': ' + str(source) + '\n' \
                              + prj_dict['fso_copy_file_dest'] + ': ' + str(dest) + '\n' \
                              + 'dest_exist: ' + str(dest_exist) + '\n' \
                              + 'ovwr_perm: ' + str(ovwr_perm)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

            if dest_exist == False:

                shutil.copyfile(source, dest)

            #   Create a log
            #   A file has been copied.
                log_message = prj_dict['fso_copy_file_copy'] + '\n' \
                              + prj_dict['fso_copy_file_source'] + ': ' + str(source) + '\n' \
                              + prj_dict['fso_copy_file_dest'] + ': ' + str(dest)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

            check = True

        else:

        #   Create a log
        #   A file could not be copied, because it does not exist.
            log_message = prj_dict['fso_copy_file_not_exist'] + '\n' \
                          + prj_dict['fso_copy_file_source'] + ': ' + str(source) + '\n' \
                          + prj_dict['fso_copy_file_dest'] + ': ' + str(dest) + '\n' \
                          + 'source_exist: ' + str(source_exist)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                      + prj_dict['fso_copy_file_source'] + ': {}'. format(source) + '\n' \
                      + prj_dict['fso_copy_file_dest'] + ': {}'. format(dest)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'check' : check, \
        'source' : source, \
        'dest' : dest
        }

def fso_create_dir(mpy_trace, prj_dict, mk_dir):

    """ This function creates a directory as well as it's parents
        recursively.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        mk_dir - Path to the directory/tree to be created

    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_msg, mpy_fct
    import sys, os

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'fso_create_dir(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False

    try:

    #   Check the directory
        dir_eval = mpy_fct.pathtool(mpy_trace, mk_dir)
        dir_exist = dir_eval['dir_exists']
        mk_dir = dir_eval['out_path']

        if dir_exist == True:

        #   Create a log
        #   The directory already exists.
            log_message = prj_dict['fso_create_dir_not_created'] + '\n' \
                          + prj_dict['fso_create_dir_directory'] + ': ' + str(mk_dir) + '\n' \
                          + prj_dict['fso_create_dir_direxist'] + ': ' + str(dir_exist)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

            os.makedirs(mk_dir)

        #   Create a log
        #   The directory has been created.
            log_message = prj_dict['fso_create_dir_created'] + '\n' \
                          + prj_dict['fso_create_dir_directory'] + ': ' + str(mk_dir)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                      + prj_dict['fso_create_dir_directory'] + ': {}'. format(mk_dir)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'check' : check
        }

def fso_delete_dir(mpy_trace, prj_dict, del_dir):

    """ This function is used to delete an entire directory including it's
        contents. A directory check is already included and will be performed.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        del_dir - Path to the directory to be deleted
    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_msg, mpy_fct
    import sys, shutil, gc

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'fso_delete_dir(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False

    try:

    #   Check the directory
        dir_eval = mpy_fct.pathtool(mpy_trace, del_dir)
        dir_exist = dir_eval['dir_exists']
        del_dir = dir_eval['out_path']

        if dir_exist == True:

            shutil.rmtree(del_dir)

        #   Create a log
        #   The directory has been deleted.
            log_message = prj_dict['fso_delete_dir_deleted'] + '\n' \
                          + prj_dict['fso_create_dir_directory'] + ': ' + str(del_dir)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

        #   Create a log
        #   The directory does not exist.
            log_message = prj_dict['fso_delete_dir_notexist'] + '\n' \
                          + prj_dict['fso_create_dir_directory'] + ': ' + str(del_dir) + '\n' \
                          + prj_dict['fso_create_dir_direxist'] + ': ' + str(dir_exist)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                      + prj_dict['fso_delete_dir_directory'] + ': {}'. format(del_dir)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return{
            'check' : check
            }

def fso_delete_file(mpy_trace, prj_dict, del_file):

    """ This function is used to delete a file. A path check is
        already included and will be performed.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        del_file - Path to the directory to be deleted

    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_msg, mpy_fct
    import sys, os, gc

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'fso_delete_file(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False

    try:

    #   Check the directory
        file_eval = mpy_fct.pathtool(mpy_trace, del_file)
        file_exist = file_eval['file_exists']
        del_file = file_eval['out_path']

        if file_exist == True:

            os.remove(del_file)

        #   Create a log
        #   The file has been deleted.
            log_message = prj_dict['fso_delete_file_deleted'] + '\n' \
                          + prj_dict['fso_delete_file_file'] + ': ' + str(del_file)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

        #   Create a log
        #   The file does not exist.
            log_message = prj_dict['fso_delete_file_notexist'] + '\n' \
                          + prj_dict['fso_delete_file_file'] + ': ' + str(del_file) + '\n' \
                          + prj_dict['fso_delete_file_exist'] + ': ' + str(file_exist)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                      + prj_dict['fso_delete_file_file'] + ': {}'. format(del_file)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return{
            'check' : check
            }

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
    """

    import mpy_msg, mpy_fct
    import sys, os, gc

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'fso_delete_file(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False
    walk_dict = {}
    root = r""
    dirs = []
    files = []
    cnt_roots = 0

    try:

    #   Check the directory
        if mpy_fct.pathtool(mpy_trace, path)["dir_exists"]:

            for root, dirs, files in os.walk(path):
                
            #   Exit if depth is reached
                if cnt_roots > depth:
                    
                    break
                    
                walk_dict.update({'root' + str(cnt_roots) : {'root' : root, 'dirs' : dirs, 'files' : files}})
                
                cnt_roots += 1

        #   Create a log
        #   Directory analyzed.
            log_message = prj_dict['fso_walk_path_done'] + '\n' \
                          + 'Directory: ' + str(path)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

        #   Create a log
        #   The directory does not exist.
            log_message = prj_dict['fso_walk_path_notexist'] + '\n' \
                          + 'Directory: ' + str(path)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return{
            'check' : check, \
            'walk_dict' : walk_dict
            }

def regex_findall(mpy_trace, prj_dict, search_obj, pattern):

    """ This function searches for regular expression in any given object and returns a list of found expressions.'
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

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'regex_findall(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    search_obj = str(search_obj)
    pattern =    str(pattern)
    result = None

#   Create a log
#   Searching for regular expressions.
    log_message = prj_dict['regex_findall_init'] + '\n' \
                  + prj_dict['regex_findall_pattern'] + ': ' + str(pattern) + '\n' \
                  + 'search_obj: ' + str(search_obj)
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    try:
    #   Search for the pattern
        result_match = re.findall(pattern, search_obj)
        result = result_match.group() if result_match else None

    #   Create a log
    #   Search completed.
        log_message = prj_dict['regex_findall_compl'] + '\n' \
                      + prj_dict['regex_findall_result'] + ': ' + str(result)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return result

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

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'regex_find1st(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    search_string = str(search_obj)
    pattern = str(pattern)
    result = None

#   Create a log
#   Searching for regular expressions.
    log_message = prj_dict['regex_find1st_init'] + '\n' \
                  + prj_dict['regex_find1st_pattern'] + ': ' + str(pattern) + '\n' \
                  + 'search_obj: ' + search_string
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    try:

        if search_string is not None:

            result_match = re.search(pattern, search_string)
            result = result_match.group() if result_match else None

            #   Create a log
            #   Search completed.
            log_message = prj_dict['regex_find1st_compl'] + '\n' \
                          + prj_dict['regex_find1st_result'] + ': ' + str(result)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

            result = [search_obj]

            #   Create a log
            #   String is NoneType. No Regex executed.
            log_message = prj_dict['regex_find1st_none'] + '\n' \
                          + prj_dict['regex_find1st_result'] + ': ' + str(result)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return result

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

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'regex_split(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    search_string = str(search_obj)
    delimiter =    str(delimiter)

#   Create a log
#   Splitting a string by a given delimiter.
    log_message = prj_dict['regex_split_init'] + '\n' \
                  + prj_dict['regex_split_delimiter'] + ': ' + str(delimiter) + '\n' \
                  + 'search_obj: ' + search_string
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    try:

        if search_string is not None:

            result = re.split(delimiter, search_string)

            #   Create a log
            #   String has been split.
            log_message = prj_dict['regex_split_compl'] + '\n' \
                          + prj_dict['regex_split_result'] + ': ' + str(result)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        else:

            result = [search_obj]

            #   Create a log
            #   String is NoneType. No Split executed.
            log_message = prj_dict['regex_split_none'] + '\n' \
                          + prj_dict['regex_split_result'] + ': ' + str(result)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return result

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

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'regex_replace(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    search_obj = str(search_obj)
    search_for = str(search_for)
    replace_by = str(replace_by)

#   Create a log
#   Changing a string by given parameters.
    log_message = prj_dict['regex_replace_init'] + '\n' \
                  + 'search_for: ' + str(search_for) + '\n' \
                  + 'replace_by: ' + str(replace_by) + '\n' \
                  + 'search_obj: ' + str(search_obj)
    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    try:
        result = re.sub(search_for, replace_by, search_obj)

        #   Create a log
        #   String substituted.
        log_message = prj_dict['regex_replace_compl'] + '\n' \
                      + prj_dict['regex_replace_result'] + ': ' + str(result)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return result

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

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'regex_remove_special(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Define the standard special character removal list. The special characters will
#   later be converted to a raw string with repr(). You may use this list as a
#   guideline of how to define special and replacement characters.
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

    try:

    #   Preparing parameters
        load_std = False
        inp_string = str(inp_string)

    #   Evaluate the length of spec_lst
        lst_len = len(spec_lst)

    #   Invoke the standard set of specials to be removed
        if spec_lst[0] == ('','') and lst_len < 2:

            spec_lst = spec_lst_std
            load_std = True

    #   Create a log
    #   Removing special characters of a string and replacing them.
        log_message = prj_dict['regex_remove_special_init'] + '\n' \
                      + 'inp_string: ' + str(inp_string) + '\n' \
                      + 'spec_lst: ' + str(spec_lst) + '\n' \
                      + 'load_std: ' + str(load_std)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Initialize the resulting string
        result = inp_string

    #   Loop through the tuples list and remove/replace characters of the
    #   input string
        for tpl in spec_lst:

        #   Convert specials to raw string and perform search/replace
            result = re.sub(str(tpl[0]), str(tpl[1]), result)

        #   Create a log
        #   String substituted.
        log_message = prj_dict['regex_remove_special_compl'] + '\n' \
                      + 'inp_string: ' + str(inp_string) + '\n' \
                      + prj_dict['regex_remove_special_result'] + ': ' + str(result)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                      + 'inp_string: {}'. format(inp_string) + '\n' \
                      + prj_dict['regex_remove_special_result'] + ': {}'. format(result) + '\n' \
                      + prj_dict['regex_remove_special_tuple'] + ': {}'. format(tpl) + '\n' \
                      + prj_dict['regex_remove_special_special'] + ': {}'. format(tpl[0]) + '\n' \
                      + prj_dict['regex_remove_special_replacer'] + ': {}'. format(tpl[1]) + '\n' \
                      + 'load_std: {}'. format(load_std) + '\n' \
                      + 'spec_lst: {}'. format(spec_lst)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return result

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

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'textfile_write(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Apply standard formats
    content = str(content)
    filepath = os.path.abspath(filepath)

    try:

    #   Append to a textfile
        if os.path.isfile(filepath) == True:

            with open(filepath, 'a') as ap:
                ap.write('\n' + content)

        #   Create a log
        #   Textfile has been appended to.
            if mpy_trace['log_enable'] == True:
                log_message = prj_dict['textfile_write_appended'] + '\n' \
                              + prj_dict['textfile_write_content'] + ': ' + str(content)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Create and write a textfile
        else:
            with open(filepath, 'w') as wr:
                wr.write(content)

        #   Create a log
        #   Textfile has been created.
            if mpy_trace['log_enable'] == True:
                log_message = prj_dict['textfile_write_created'] + '\n' \
                              + prj_dict['textfile_write_content'] + ': ' + str(content)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

def testprint(mpy_trace, input):

    # import mpy_fct

    """ This function prints any value given. It is intended to be used for debugging.
    :param
        mpy_trace - operation credentials and tracing
        input - Something that will be printed as a string.
    :return
        -
    """

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_common'
    # operation = 'testprint(~)'
    # mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    value     = str(input)
    intype    = str(type(input))

    print('<TEST> value: ' + value + '\n' + '<TEST> type: ' + intype + '\n')

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

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_common'
    operation = 'wait_for_input(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    try:

        usr_input = input(str(msg_text) + '\n')

    #   Create a log
    #   A user input has been made.
        log_message = prj_dict['wait_for_input_compl'] + '\n' \
                      + prj_dict['wait_for_input_messsage'] + ': ' + str(msg_text) + '\n' \
                      + prj_dict['wait_for_input_usr_inp'] + ': ' + str(usr_input)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return usr_input