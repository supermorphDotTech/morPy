"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module holds all functions used for initialization of the
            morPy framework.
"""

import mpy_fct
import mpy_conf
import mpy_msg
import mpy_mt

import sys
import logging

def init_cred():

    """ This function initializes the operation credentials and tracing.
    :param
        -
    :return - dictionary
        mpy_trace - operation credentials and tracing
    """

    # Initialize operation credentials and tracing.
    # Each operation/function/object will fill the dictionary with data
    # by executing mpy_trace = mpy.tracing(module, operation, mpy_trace)
    # as a first step before execution.
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
    
    try:

        # ############################################
        # START Single-threaded initialization
        # ############################################
    
        # Create the initial framework dictionary
        init_lib = {}
        # Localization
        init_lib["loc"] = {}
        init_lib["loc"]["mpy"] = {}
        init_lib["loc"]["mpy_dbg"] = {}
        init_lib["loc"]["prj"] = {}
        # Configuration
        init_lib["conf"] = {}
        # System Info
        init_lib["sys"] = {}
        # Runtime Info
        init_lib['run'] = {}
    
        # Retrieve the starting time of the program
        temp_datetime = mpy_fct.datetime_now(mpy_trace)
    
        # Update the initialize dictionary with the parameters dictionary.
        # Add more values as needed for mpy_param.parameters(~)
        param_dict = {'temp_datetime' : temp_datetime["datetimestamp"]}
        init_lib["conf"].update(mpy_conf.parameters(param_dict))
    
        # Evaluate log_enable
        if not init_lib["conf"]["mpy_log_db_enable"] and not init_lib["conf"]["mpy_log_txt_enable"]:
            init_lib["conf"]["mpy_log_enable"] = False
    
        # Pass down the log enabling parameter
        mpy_trace["log_enable"] = init_lib["conf"]["mpy_log_enable"]
    
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_init'
        operation = 'init(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)
        
        # Import the morPy core functions localization into init_lib.
        exec(f'import {init_lib["conf"]["localization"]}')
        exec(f'init_lib["loc"]["mpy"].update({init_lib["conf"]["localization"]}.loc_mpy())')
    
        # Store the start time and timestamps in the dictionary
        init_lib["run"]["init_datetime_value"] = temp_datetime["datetime_value"]
        init_lib["run"]["init_date"] = temp_datetime["date"]
        init_lib["run"]["init_datestamp"] = temp_datetime["datestamp"]
        init_lib["run"]["init_time"] = temp_datetime["time"]
        init_lib["run"]["init_timestamp"] = temp_datetime["timestamp"]
        init_lib["run"]["init_datetimestamp"] = temp_datetime["datetimestamp"]
        init_lib["run"]["init_loggingstamp"] = temp_datetime["loggingstamp"]
    
        # Retrieve system information
        temp_sysinfo = mpy_fct.sysinfo(mpy_trace)
    
        # Update init_lib with system information
        init_lib["sys"]["os"] = temp_sysinfo["os"]
        init_lib["sys"]["os_release"] = temp_sysinfo["os_release"]
        init_lib["sys"]["os_version"] = temp_sysinfo["os_version"]
        init_lib["sys"]["os_arch"] = temp_sysinfo["os_arch"]
        init_lib["sys"]["processor"] = temp_sysinfo["processor"]
        init_lib["sys"]["threads"] = temp_sysinfo["threads"]
        init_lib["sys"]["username"] = temp_sysinfo["username"]
        init_lib["sys"]["homedir"] = temp_sysinfo["homedir"]
        init_lib["sys"]["hostname"] = temp_sysinfo["hostname"]
        init_lib["sys"]["resolution_height"] = temp_sysinfo["resolution_height"]
        init_lib["sys"]["resolution_width"] = temp_sysinfo["resolution_width"]
    
        # Test for elevated privileges
        mpy_fct.privileges_handler(mpy_trace, init_lib)
    
        # Prepare log levels
        init_lib["run"]["events_total"] = 0
        init_lib["run"]["events_DEBUG"] = 0
        init_lib["run"]["events_INFO"] = 0
        init_lib["run"]["events_WARNING"] = 0
        init_lib["run"]["events_DENIED"] = 0
        init_lib["run"]["events_ERROR"] = 0
        init_lib["run"]["events_CRITICAL"] = 0
        init_lib["run"]["events_UNDEFINED"] = 0
        init_lib["run"]["events_INIT"] = 0
        init_lib["run"]["events_EXIT"] = 0
    
        # Initialize the priority queue and Multithreading
        # Logging may start after this
        mpy_mt.mt_init(mpy_trace, init_lib)
    
        # Create the first log including the project header
        if (init_lib["conf"]["mpy_log_txt_header_enable"] and
            mpy_trace["log_enable"] and
            init_lib["conf"]["mpy_log_txt_enable"]):
    
            mpy_log_header(mpy_trace, init_lib)
    
        # Print mpy_reference.txt to console with all initialized Variables
        if init_lib["conf"]["mpy_print_init_vars"]:
            print(mpy_fct.prj_dict_to_string(init_lib))
    
        # Create mpy_reference.txt with all initialized Variables
        mpy_ref(mpy_trace, init_lib)
    
        # Initialize the project-specific localization
        exec(f'loc_prj = {init_lib["conf"]["localization"]}.loc_prj()')
        loc_prj_loaded = init_lib["loc"]["mpy"]["init_loc_prj_loaded"]
        mpy_msg.log(mpy_trace, init_lib, loc_prj_loaded, 'init')
    
        # Update init_lib with language specific strings (project specific)
        # from loc_??.loc_dict_prj(~)
        exec('init_lib["loc"]["prj"].update(loc_prj)')
        init_loc_finished = init_lib["loc"]["mpy"]["init_loc_finished"]
        mpy_msg.log(mpy_trace, init_lib, init_loc_finished, 'init')
    
        # Initialize the global interrupt flag
        init_lib["mpy_interrupt"] = False
    
        # ############################################
        # END Single-threaded initialization
        # START Multi-threaded initialization
        # ############################################
    
        # PLACEHOLDER
    
        # ############################################
        # END Multi-threaded initialization
        # ############################################
    
        # Calculate the runtime of the initialization routine
        temp_duration = mpy_fct.runtime(mpy_trace, init_lib["run"]["init_datetime_value"])
    
        # Record the duration of the initialization
        init_lib["init_rnt_delta"] = temp_duration["rnt_delta"]
    
        init_message = (f'{init_lib["loc"]["mpy"]["init_finished"]}\n'
                       f'{init_lib["loc"]["mpy"]["init_duration"]}: {init_lib["init_rnt_delta"]}')
        mpy_msg.log(mpy_trace, init_lib, init_message, 'init')
    
        # Exit initialization
        return init_lib
    
    except Exception as e:
        mpy_fct.handle_exception_init(e)
        raise

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

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_init'
    operation = 'mpy_log_header(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    # Create the project header
    content = (f'== {init_lib["loc"]["mpy"]["mpy_log_header_start"]}{3*" =="}\n\t'
               f'{init_lib["loc"]["mpy"]["mpy_log_header_author"]}: Bastian Neuwirth\n\t'
               f'{init_lib["loc"]["mpy"]["mpy_log_header_project"]}: {init_lib["prj_path"]}\n\t'
               f'{init_lib["loc"]["mpy"]["mpy_log_header_timestamp"]}: {init_lib["run"]["init_datetimestamp"]}\n\t'
               f'{init_lib["loc"]["mpy"]["mpy_log_header_user"]}: {init_lib["sys"]["username"]}\n\t'
               f'{init_lib["loc"]["mpy"]["mpy_log_header_system"]}: {init_lib["sys"]["os"]} {init_lib["sys"]["os_release"]}\n\t'
               f'{init_lib["loc"]["mpy"]["mpy_log_header_version"]}: {init_lib["sys"]["os_version"]}\n\t'
               f'{init_lib["loc"]["mpy"]["mpy_log_header_architecture"]}: {init_lib["sys"]["os_arch"]}\n\t'
               f'{init_lib["loc"]["mpy"]["mpy_log_header_threads"]}: {init_lib["sys"]["threads"]}\n'
               f'== {init_lib["loc"]["mpy"]["mpy_log_header_begin"]}{3*" =="}\n'
               )

    # Write to the logfile
    filepath = init_lib.get('log_txt_path')
    mpy_fct.txt_wr(mpy_trace, init_lib, filepath, content)

    # Garbage collection
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

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_init'
    operation = 'mpy_ref(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)
    pnt = False

    try:
        # Create a copy of the initialized project dictionary in a textfile.
        if init_lib["conf"]["mpy_ref_create"]:

            mpy_ref_path = os.path.join(f'{init_lib["conf"]["prj_path"]}', 'mpy_reference.txt')
            mpy_reference = open(mpy_ref_path,'w')

            # mpy_reference description
            mpy_reference.write(f'{init_lib["loc"]["mpy"]["mpy_ref_descr"]}\n\n')
            
            # -- Set Parameters --
            mpy_reference.write(f'-- {init_lib["loc"]["mpy"]["mpy_ref_glob_param"]} --\n')

            for key, value in init_lib.items():

                # Write the actual keys and parameters
                mpy_reference.write(f'{key} : {value}\n')

                # Exit the loop after the last relevant key
                if f'{key}' == 'main_db_path': break

            # -- Initialized System and Project Parameters --
            mpy_reference.write(f'\n-- {init_lib["loc"]["mpy"]["mpy_ref_sys_param"]} --\n')

            for key, value in init_lib.items():

                # Go through the dictionary until the first useful key is found
                # and print key-value pairs from there on.
                if f'{key}' == 'init_datetime_value': pnt = True


                # Write the actual keys and parameters from a certain position.
                if pnt == True: mpy_reference.write(f'{key} : {value}\n')

                # Exit the loop after the last relevant key.
                if f'{key}' == 'res_width': break

            # Create a log
            # The initialization reference was written to a textfile.
            log_message = (f'{init_lib["loc"]["mpy"]["mpy_ref_created"]}\n'
                          f'{init_lib["loc"]["mpy"]["mpy_ref_path"]}: {mpy_ref_path}')

            # Close the file
            mpy_reference.close()

        else:
            # Create a log
            # The project dictionary was created.
            log_message = init_lib["loc"]["mpy"]["mpy_ref_noref"]

        mpy_msg.log(mpy_trace, init_lib, log_message, 'init')

    # Error detection
    except Exception as e:
        log_message = (f'{init_lib["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{init_lib["loc"]["mpy"]["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, init_lib, log_message, 'error')