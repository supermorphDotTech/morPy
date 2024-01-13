"""
Author:     Bastian Neuwirth
Date:       18.09.2023
Version:    0.1
Descr.:     This module includes operations used to massively repeat/automize
            workflows.
"""

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

    import mpy_msg, mpy_fct, mpy_common
    import sys, gc

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_bulk_ops'
    operation = 'find_replace_saveas(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False
    search_obj = f'{search_obj}'

    try:
        
        #   Create a log
        #   Operation start.
        log_message = prj_dict["find_replace_saveas_start"]
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')
        
    #   Check if file exists
        file_exists = mpy_fct.pathtool(mpy_trace, save_as)["file_exists"]
    
    #   If file exists and overwrite is false, skip action.
        if file_exists and not overwrite:
            
            #   Create a log
            #   File already exists. Operation skipped.
            log_message = prj_dict["find_replace_saveas_f_ex_skip"]
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')
        
        else:
            
        #   Delete the target file if it exists and overwrite is true.
            if file_exists:
                
                mpy_common.fso_delete_file(mpy_trace, prj_dict, save_as)
            
        #   Check for tuple and make one if necessary
            if type(replace_tpl) is not tuple:
                
                replace = (replace_tpl)
            
        #   Check for tuple of tuples and raise error if necessary
            if type(replace_tpl(0)) is not tuple:
                
                #   Create a log
                #   Wrong type. Input must be a tuple of tuples.
                log_message = (f'{prj_dict["find_replace_saveas_tpl_err"]}\n'
                              f'type(replace_tpl): {type(replace_tpl)}\n'
                              f'replace_tpl: {replace_tpl}\n'
                              f'type(replace_tpl(0)): {type(replace_tpl(0))}\n'
                              f'replace_tpl(0): {replace_tpl(0)}')
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')
    
            else:
                
            #   Search line by line
                for line in search_obj.readlines():
                    
                #   Loop through all replace tuples.
                    for tpl in replace:
                        
                    #   Replace the actual findings
                        new_line = mpy_common.regex_replace(mpy_trace, prj_dict, line, tpl(0), tpl(1))
                        mpy_common.textfile_write(mpy_trace, prj_dict, save_as, new_line)
                    
                check = True

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

    #   Return a dictionary
        return{
            'check' : check
            }