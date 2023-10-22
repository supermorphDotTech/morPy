"""
Author:     Bastian Neuwirth
Date:       12.08.2023
Version:    0.1
Descr.:     This module links all routines and classes of the morPy framework.
            Linking provides the following advantages:
                - Shortens the code needed to adress a function
                - Framework is easier to understand, since all functions are
                  collected here
                - Only one module mpy.py needs to be adressed (imported) in
                  the code of the project
                - Only functions intended to be used are provided here
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
    """

    try:
        import sys, mpy_common
        return mpy_common.decode_to_plain_text(mpy_trace, prj_dict, src_input, encoding)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'decode_to_plain_text(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def dialog_sel_file(mpy_trace, prj_dict, init_dir, ftypes):

    """ This function opens a dialog for the user to select a file.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        init_dir - The directory in which the dialog will initially be opened
        ftypes - This tuple of 2-tuples specifies, which filetypes will be
                displayed by the dialog box, e.g.
                (('type1','*.t1'),('All Files','*.*'),...)
                ((NAME,TYPE),('All Files','*.*'),...)
    :return - dictionary
        check - The function ended with no errors and a file was chosen
        sel_file - Path of the selected file
    """

    try:
        import sys, mpy_common
        return mpy_common.dialog_sel_file(mpy_trace, prj_dict, init_dir, ftypes)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'dialog_sel_file(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

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

    try:
        import sys, mpy_common
        return mpy_common.dialog_sel_dir(mpy_trace, prj_dict, init_dir)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'dialog_sel_dir(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

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

    try:
        import sys, mpy_common
        return mpy_common.fso_copy_file(mpy_trace, prj_dict, source, dest, ovwr_perm)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'fso_copy_file(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

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

    try:
        import sys, mpy_common
        return mpy_common.fso_create_dir(mpy_trace, prj_dict, mk_dir)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'fso_create_dir(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

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

    try:
        import sys, mpy_common
        return mpy_common.fso_delete_dir(mpy_trace, prj_dict, del_dir)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'fso_delete_dir(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

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

    try:
        import sys, mpy_common
        return mpy_common.fso_delete_file(mpy_trace, prj_dict, del_file)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'fso_delete_file(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

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

    try:
        import sys, mpy_common
        return mpy_common.fso_walk(mpy_trace, prj_dict, path, depth)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'fso_walk(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def regex_findall(mpy_trace, prj_dict, search_obj, pattern):

    """ This function searches for regular expression in any given object and returns a list of found expressions.'
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        pattern - The regular expression to search for
    :return - list
        result - The list of expressions found in the input
    """

    try:
        import sys, mpy_common
        return mpy_common.regex_findall(mpy_trace, prj_dict, search_obj, pattern)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'regex_findall(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def regex_find1st(mpy_trace, prj_dict, search_obj, pattern):

    """ This function searches for regular expression in any given object and returns the first match.'
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        pattern - The regular expression to search for

    :return - list
        result - The list of expressions found in the input
    """

    try:
        import sys, mpy_common
        return mpy_common.regex_find1st(mpy_trace, prj_dict, search_obj, pattern)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'regex_find1st(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

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

    try:
        import sys, mpy_common
        return mpy_common.regex_split(mpy_trace, prj_dict, search_obj, delimiter)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'regex_split(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def regex_replace(mpy_trace, prj_dict, search_obj, search_for, replace_by):

    """ This function substitutes characters or strings in an input object.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        search_obj - Any given object to search in for a regular expression (will be converted to a string)
        search_for - The character or string to be replaced
        replace_by - The character or string to substitute

    :return
        result - The substituted chracter or string
    """

    try:
        import sys, mpy_common
        return mpy_common.regex_replace(mpy_trace, prj_dict, search_obj, search_for, replace_by)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'regex_replace(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

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

    try:
        import sys, mpy_common
        return mpy_common.regex_remove_special(mpy_trace, prj_dict, inp_string, spec_lst)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'regex_remove_special(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

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

    try:
        import sys, mpy_common
        return mpy_common.textfile_write(mpy_trace, prj_dict, filepath, content)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'textfile_write(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def testprint(mpy_trace, input):

    """ This function prints any value given. It is intended to be used for debugging.
    :param
        mpy_trace - operation credentials and tracing
        input - Something that will be printed as a string.
    :return
        -
    """

    import mpy_common
    return mpy_common.testprint(mpy_trace, input)

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

    try:
        import sys, mpy_common
        return mpy_common.wait_for_input(mpy_trace, prj_dict, msg_text)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'wait_for_input(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def datetime_now(mpy_trace):

    """ This function reads the current date and time and returns formatted
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

    import mpy_fct

    return mpy_fct.datetime_now(mpy_trace)

def runtime(mpy_trace, in_ref_time):

    """ This function calculates the actual runtime and returns it.
    :param
        mpy_trace - operation credentials and tracing
        in_ref_time - Value of the reference time to calculate the actual runtime
    :return - dictionary
        rnt_delta - Value of the actual runtime.
    """

    import mpy_fct

    return mpy_fct.runtime(mpy_trace, in_ref_time)

def sysinfo(mpy_trace):

    """ This function returns various informations about the hardware and operating system.
    :param
        mpy_trace - operation credentials and tracing
    :return - dictionary
        system - Operating system.
        release - Major version of the operating system.
        version - Major and subversions of the operating system.
        arch - Architecture of the operating system.
        processor - Processor running the code.
        threads - Total threads available to the machine.
        username - Returns the username.
        homedir - Returns the home directory.
        hostname - Returns the host name.
    """

    import mpy_fct

    return mpy_fct.sysinfo(mpy_trace)

def pathtool(mpy_trace, in_path):

    """ This function takes a string and converts it to a path. Additionally,
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

    """ This function joins components of a tuple to an OS path.
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

    """ This function returns performance metrics.
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

def print_prj_dict(prj_dict):

    """ This function prints the entire project dictionary in Terminal.
    :param
        prj_dict - morPy global dictionary
    :return
        -
    """

    import mpy_fct

    return mpy_fct.print_prj_dict(prj_dict)

def tracing(module, operation, mpy_trace):

    """ This function formats the trace to any given operation. This function is
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

def log(mpy_trace, prj_dict, log_message, level):

    """ This function writes an event to a specified file and/or prints it out
        according to it's severity (level).
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        log_message - The message to be logged
        level - Severity: debug/info/warning/error/critical/denied
    :return
        -
    """

    try:
        import mpy_msg, sys
        return mpy_msg.log(mpy_trace, prj_dict, log_message, level)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'log(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

def mpy_thread_queue(mpy_trace, prj_dict, name, priority, task):

    """ This function handles the task queue (instance 'mpy_PriorityQueue' of cl_mtPriorityQueue)
        of this framework. Its main purpose is to provide an easy handling of multithreaded
        programming in the way, that the developer just needs to fill the queue with tasks
        and tailor the multithreading parameters to the projects needs. However, when being
        bound to single threaded execution the queue will just execute sequentially, while
        prioritizing the tasks.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        name - Name of the task/thread.
        priority - Integer value. Sets the priority of the given task. Lower numbers indicate
                   a higher priority. Negative integers should be avoided.
        task - Statement, function or class/module to be run by the thread. A string
               is expected and will be executed via the exec()-function. The module has
               got to be referenced (if any) in order to work. Example:

                   task = 'prj_module1.prj_function1([mpy_trace], [prj_dict], [...], [log])'
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        import sys, mpy_mt
        return mpy_mt.mpy_thread_queue(mpy_trace, prj_dict, name, priority, task)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'mpy_thread_queue(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def mpy_threads_joinall(mpy_trace, prj_dict):

    """ This function stops execution of the code until all threads have finished their work.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        import sys, mpy_mt
        return mpy_mt.mpy_threads_joinall(mpy_trace, prj_dict)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'mpy_threads_joinall(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def mpy_mt_abort(mpy_trace, prj_dict):

    """ This function aborts all pending tasks. However, the priority queue still exists and new threads
        would eventually pick up the aborted tasks.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        import sys, mpy_mt
        return mpy_mt.mpy_mt_abort(mpy_trace, prj_dict)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'mpy_mt_abort(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def cl_read(mpy_trace, prj_dict, wb_path, wb_sht, cells, dat, vba):

    """ This function reads the cells of MS Excel workbooks.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        wb_path - Path to the MS Excel workbook
        wb_sht - Name of the sheet, to copy cells from
        cells - The cell or range of cells to read from. Two datatypes
                are accepted, either a single cell or a range, as shown:
                ['A1'] or ['A1:ZZ1000'] (letters are not case sensitive)
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
        import sys, mpy_xl
        return mpy_xl.cl_read(mpy_trace, prj_dict, wb_path, wb_sht, cells, dat, vba)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'cl_read(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def wb_close(mpy_trace, prj_dict, wb_path):

    """ This function closes an MS Excel workbook. It is advisory to
        only use the morPy functions to open and close a workbook, since a
        wb_close routine is implemented for various cases (i.e. Exceptions).
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        wb_path - Path to the MS Excel workbook
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        import sys, mpy_xl
        return mpy_xl.wb_close(mpy_trace, prj_dict, wb_path)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'wb_close(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def wb_close_all(mpy_trace, prj_dict):

    """ This function closes all MS Excel workbooks opened by this project. It is
        advisory to only use the morPy functions to open and close a workbook, since
        a wb_close routine is implemented for various cases (i.e. Exceptions).
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        import sys, mpy_xl
        return mpy_xl.wb_close_all(mpy_trace, prj_dict)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'wb_close_all(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def wb_create(mpy_trace, prj_dict, xl_path):

    """ This function creates a new empty excel workbook at a path handed
        to this function.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        import sys, mpy_xl
        return mpy_xl.wb_create(mpy_trace, prj_dict, xl_path)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'wb_create(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def wb_load(mpy_trace, prj_dict, wb_path, dat, vba):

    """ This function connects to an MS Excel workbook. It is advisory to
        only use the morPy functions to open and close a workbook, since a
        wb_close routine is implemented for various cases (i.e. Exceptions).
        The workbook path will be connected to the object in RAM by creating
        a key in a dedicated dictionary as shown:
        >   prj_dict['mpy_xl_loaded_wb_lst'] = {wb_path : wb_obj}
        This way a once opened Excel workbook may not be adressed twice.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
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
        import sys, mpy_xl
        return mpy_xl.wb_load(mpy_trace, prj_dict, wb_path, dat, vba)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'wb_load(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def wb_tbl_attributes(mpy_trace, prj_dict, wb_path, tbl):

    """ This function retrieves all attributes of an MS Excel table. To achieve
        it, the function openpyxl module will be called. If you are fine with
        only the most basic paramters of an MS Excel table, use wb_tbl_inquiry
        instead.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        wb_path - Path to the MS Excel workbook
        tbl - Name of the table to be analyzed
    :return - dictionary
        check - The function ended with no errors
        wb_obj - The workbook object which was loaded
        tbl_attr - List of the table's attributes
    """

    try:
        import sys, mpy_xl
        return mpy_xl.wb_tbl_attributes(mpy_trace, prj_dict, wb_path, tbl)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'wb_tbl_attributes(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def wb_tbl_inquiry(mpy_trace, prj_dict, wb_path):

    """ This function inquires all tables of a worksheet. The result is a
        dictionary containing a number of datatypes.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
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
        import sys, mpy_xl
        return mpy_xl.wb_tbl_inquiry(mpy_trace, prj_dict, wb_path)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'wb_tbl_inquiry(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def tk_progbar_indeterminate(mpy_trace, prj_dict, GUI_dict):

    """ This function invokes a window with an indeterminate progress bar
        and status messages.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
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
        import sys, mpy_ui_tk
        return mpy_ui_tk.tk_progbar_indeterminate(mpy_trace, prj_dict, GUI_dict)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'tk_progbar_indeterminate(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def find_replace_saveas(mpy_trace, prj_dict, search_obj, replace_tpl, save_as, overwrite):

    """ This function finds and replaces strings in a readable object
        line by line. This may be text or csv files, but even strings
        would be converted so they are read line by line. This function
        does not repeat, but it's easy to iterate it. Once every line
        was evaluated and regular expressions got replaced, a file
        will be saved including all changes.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
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
        import sys, mpy_bulk_ops
        return mpy_bulk_ops.find_replace_saveas(mpy_trace, prj_dict, search_obj, replace_tpl, save_as, overwrite)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'find_replace_saveas(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')

def web_request(mpy_trace, prj_dict, URL, req_dict):

    """ This function connects to an URL and delivers the responses requested. Data
        of spreadsheets and other media may be extracted with this method.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
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
        import sys, mpy_wscraper
        return mpy_wscraper.web_request(mpy_trace, prj_dict, URL, req_dict)
#   Error detection
    except Exception as e:
    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        err_m = 'mpy'
        err_o = 'dialog_sel_file(~)'
        mpy_trace = tracing(err_m, err_o, mpy_trace)

        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        log(mpy_trace, prj_dict, log_message, 'error')