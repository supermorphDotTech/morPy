"""
Author:     Bastian Neuwirth
Date:       28.06.2021
Version:    0.1
Descr.:     This module holds all functions used for initialization of the
            morPy framework.
"""

def init_cred():

    """ This function initializes the operation credentials and tracing.
    :param
        -
    :return - dictionary
        mpy_trace - operation credentials and tracing
    """

    #   Initialize operation credentials and tracing
    mpy_trace = { \
        'module' : '__main__' , \
        'operation' : '' , \
        'tracing' : '__main__' , \
        'process_id' : 0 , \
        'thread_id' : 0 , \
        'task_id' : 0 , \
        'log_enable' : False , \
        'interrupt_enable' : False
    }

    return mpy_trace

def init(mpy_trace):

    import mpy_fct, mpy_param, mpy_msg, mpy_mt
    import gc

    """ This function initializes the project dictionary and yields project
        specific information to be handed down through called functions. Have
        in mind that the exec()-method used here to access the localized
        dictionary (language of the messages) is solely used for initialization.
        Usually the exec()-method has to be avoided and is not necessary in
        other parts of this framework.
    :param
        mpy_trace - operation credentials and tracing
    :return - dictionary
        init_lib - Dictionary that holds all initialized information
    """

#   ############################################
#   START Single-threaded initialization
#   ############################################

#   Create the initial framework dictionary
    init_lib = {}

#   Retrieve the starting time of the program
    temp_datetime = mpy_fct.datetime_now(mpy_trace)

#   Update the initialize dictionary with the parameters dictionary
    param_dict = {'temp_datetime' : temp_datetime["datetimestamp"]}
    init_lib.update(mpy_param.parameters(param_dict))

#   Evaluate log_enable
    if init_lib["mpy_log_db_enable"] == False and init_lib["mpy_log_txt_enable"] == False:
        init_lib["mpy_log_enable"] = False

#   Pass down the log enabling parameter
    mpy_trace["log_enable"] = init_lib["mpy_log_enable"]

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_init'
    operation = 'init(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Initialize the morPy-specific localization
    exec(f'import {init_lib["localization"]}')
    exec(f'init_lib.update({init_lib["localization"]}.localization_mpy())')

#   Store the start time and timestamps in the dictionary
    init_lib["init_datetime_value"] = temp_datetime["datetime_value"]
    init_lib["init_date"] = temp_datetime["date"]
    init_lib["init_datestamp"] = temp_datetime["datestamp"]
    init_lib["init_time"] = temp_datetime["time"]
    init_lib["init_timestamp"] = temp_datetime["timestamp"]
    init_lib["init_datetimestamp"] = temp_datetime["datetimestamp"]
    init_lib["init_loggingstamp"] = temp_datetime["loggingstamp"]

#   Retrieve system information
    temp_sysinfo = mpy_fct.sysinfo(mpy_trace)

#   Update init_lib with system information
    init_lib["system"] = temp_sysinfo["system"]
    init_lib["system_release"] = temp_sysinfo["system_release"]
    init_lib["system_version"] = temp_sysinfo["system_version"]
    init_lib["system_arch"] = temp_sysinfo["system_arch"]
    init_lib["processor"] = temp_sysinfo["processor"]
    init_lib["threads"] = temp_sysinfo["threads"]
    init_lib["username"] = temp_sysinfo["username"]
    init_lib["homedir"] = temp_sysinfo["homedir"]
    init_lib["hostname"] = temp_sysinfo["hostname"]
    init_lib["res_height"] = temp_sysinfo["res_height"]
    init_lib["res_width"] = temp_sysinfo["res_width"]

#   Test for elevated privileges
    mpy_fct.privileges_handler(mpy_trace, init_lib)

#   Prepare log levels
    init_lib["events_total"] = 0
    init_lib["events_DEBUG"] = 0
    init_lib["events_INFO"] = 0
    init_lib["events_WARNING"] = 0
    init_lib["events_DENIED"] = 0
    init_lib["events_ERROR"] = 0
    init_lib["events_CRITICAL"] = 0
    init_lib["events_UNDEFINED"] = 0
    init_lib["events_INIT"] = 0
    init_lib["events_EXIT"] = 0

#   Initialize the priority queue and Multithreading
#   Logging may start after this
    mpy_mt.mt_init(mpy_trace, init_lib)

#   Create the first log including the project header
    if init_lib["mpy_log_txt_header_enable"] and \
        mpy_trace["log_enable"] and \
        init_lib["mpy_log_txt_enable"]:

        mpy_log_header(mpy_trace, init_lib)

#   Print mpy_reference.txt to console with all initialized Variables
    if init_lib["mpy_print_init_vars"]:
        print(mpy_fct.prj_dict_to_string(init_lib))

#   Create mpy_reference.txt with all initialized Variables
    mpy_ref(mpy_trace, init_lib)

#   Initialize the project-specific localization
    exec(f'loc_prj = {init_lib["localization"]}.localization_prj()')
    loc_prj_loaded = init_lib["init_loc_prj_loaded"]
    mpy_msg.log(mpy_trace, init_lib, loc_prj_loaded, 'init')

#   Update init_lib with language specific strings (project specific)
#   from loc_??.loc_dict_prj(~)
    exec('init_lib.update(loc_prj)')
    init_loc_finished = init_lib["init_loc_finished"]
    mpy_msg.log(mpy_trace, init_lib, init_loc_finished, 'init')

#   Initialize the global interrupt flag
    init_lib["mpy_interrupt"] = False

#   ############################################
#   END Single-threaded initialization
#   START Multi-threaded initialization
#   ############################################

    # PLACEHOLDER

#   ############################################
#   END Multi-threaded initialization
#   ############################################

#   Calculate the runtime of the initialization routine
    temp_duration = mpy_fct.runtime(mpy_trace, init_lib["init_datetime_value"])

#   Record the duration of the initialization
    init_lib["init_rnt_delta"] = temp_duration["rnt_delta"]

    init_message = (f'{init_lib["init_finished"]}\n'
                   f'{init_lib["init_duration"]}: {init_lib["init_rnt_delta"]}')
    mpy_msg.log(mpy_trace, init_lib, init_message, 'init')

#   Garbage collection
    gc.collect()

#   Exit initialization
    return init_lib

def mpy_log_header(mpy_trace, init_lib):

    import mpy_fct

    """ This function writes the header for the logfile including project specific
        information.
    :param
        mpy_trace - operation credentials and tracing
        init_lib - Dictionary that holds all initialized information
    :return
        -
    """

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_init'
    operation = 'mpy_log_header(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Create the project header
    content = (f'== {init_lib["mpy_log_header_start"]}{3*" =="}\n\t'
               f'{init_lib["mpy_log_header_author"]}: Bastian Neuwirth\n\t'
               f'{init_lib["mpy_log_header_project"]}: {init_lib["prj_path"]}\n\t'
               f'{init_lib["mpy_log_header_timestamp"]}: {init_lib["init_datetimestamp"]}\n\t'
               f'{init_lib["mpy_log_header_user"]}: {init_lib["username"]}\n\t'
               f'{init_lib["mpy_log_header_system"]}: {init_lib["system"]} {init_lib["system_release"]}\n\t'
               f'{init_lib["mpy_log_header_version"]}: {init_lib["system_version"]}\n\t'
               f'{init_lib["mpy_log_header_architecture"]}: {init_lib["system_arch"]}\n\t'
               f'{init_lib["mpy_log_header_threads"]}: {init_lib["threads"]}\n'
               f'== {init_lib["mpy_log_header_begin"]}{3*" =="}\n'
               )

#   Write to the logfile
    filepath = init_lib.get('log_txt_path')
    mpy_fct.txt_wr(mpy_trace, init_lib, filepath, content)

#   Garbage collection
    del mpy_trace

def mpy_ref(mpy_trace, init_lib):

    import mpy_fct, mpy_msg
    import sys, gc, os

    """ This function documents the initialized dictionary (reference).
    :param
        mpy_trace - operation credentials and tracing
        init_lib - Dictionary that holds all initialized information
    :return
        -
    """

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_init'
    operation = 'mpy_ref(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)
    pnt = False

    try:
    #   Create a copy of the initialized project dictionary in a textfile.
        if init_lib["mpy_ref_create"]:

            mpy_ref_path = os.path.join(f'{init_lib["prj_path"]}', 'mpy_reference.txt')
            mpy_reference = open(mpy_ref_path,'w')

        #   mpy_reference description
            mpy_reference.write(f'{init_lib["mpy_ref_descr"]}\n\n')
            
        #   -- Set Parameters --
            mpy_reference.write(f'-- {init_lib["mpy_ref_glob_param"]} --\n')

            for key, value in init_lib.items():

            #   Write the actual keys and parameters
                mpy_reference.write(f'{key} : {value}\n')

            #   Exit the loop after the last relevant key
                if f'{key}' == 'main_db_path': break

        #   -- Initialized System and Project Parameters --
            mpy_reference.write(f'\n-- {init_lib["mpy_ref_sys_param"]} --\n')

            for key, value in init_lib.items():

            #   Go through the dictionary until the first useful key is found
            #   and print key-value pairs from there on.
                if f'{key}' == 'init_datetime_value': pnt = True


            #   Write the actual keys and parameters from a certain position.
                if pnt == True: mpy_reference.write(f'{key} : {value}\n')

            #   Exit the loop after the last relevant key.
                if f'{key}' == 'res_width': break

        #   Create a log
        #   The initialization reference was written to a textfile.
            log_message = (f'{init_lib["mpy_ref_created"]}\n'
                          f'{init_lib["mpy_ref_path"]}: {mpy_ref_path}')

        #   Close the file
            mpy_reference.close()

        else:
        #   Create a log
        #   The project dictionary was created.
            log_message = init_lib["mpy_ref_noref"]

        mpy_msg.log(mpy_trace, init_lib, log_message, 'init')

#   Error detection
    except Exception as e:
        log_message = (f'{init_lib["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{init_lib["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, init_lib, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()