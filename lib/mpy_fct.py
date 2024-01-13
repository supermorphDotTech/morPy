"""
Author:     Bastian Neuwirth
Date:       29.06.2021
Version:    0.1
Descr.:     This module yields the most basic functions of the morPy fork. These
            functions are optimised for initilization, so they do not support
            logging. Although not intended, these modules may be used freely
            since they are fully compatible with morPy.
"""

def privileges_handler(mpy_trace, prj_dict):

    """ This function tests the privileges of __main__ and restarts with
        a request for admin rights if it was set in the parameters.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
    :return
        -

    #TODO
    Finish the module and fix all bugs
    """

    import mpy_msg
    import sys, ctypes, enum, gc

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_fct'
    operation = 'privileges_handler(~)'
    mpy_trace = tracing(module, operation, mpy_trace)

    try:

    #   Specification of how to open an elevated program
        class el_spec(enum.IntEnum):

            HIDE = 0
            MAXIMIZE = 3
            MINIMIZE = 6
            RESTORE = 9
            SHOW = 5
            SHOWDEFAULT = 10
            SHOWMAXIMIZED = 3
            SHOWMINIMIZED = 2
            SHOWMINNOACTIVE = 7
            SHOWNA = 8
            SHOWNOACTIVATE = 4
            SHOWNORMAL = 1

    #   Specification of how to interpret errors from ctypes
        class el_error(enum.IntEnum):

            ZERO = 0
            FILE_NOT_FOUND = 2
            PATH_NOT_FOUND = 3
            BAD_FORMAT = 11
            ACCESS_DENIED = 5
            ASSOC_INCOMPLETE = 27
            DDE_BUSY = 30
            DDE_FAIL = 29
            DDE_TIMEOUT = 28
            DLL_NOT_FOUND = 32
            NO_ASSOC = 31
            OOM = 8
            SHARE = 26

    #   Test if elevated privileges are required
        if  prj_dict["mpy_priv_required"]:

        #   Routine for MS Windows
            if prj_dict["system"].upper == 'WINDOWS':
                if ctypes.windll.shell32.IsUserAnAdmin():
                #   Program started with elevated Privileges.
                    msg = prj_dict["mpy_priv_handler_eval"]
                else:
                    hinstance = ctypes.windll.shell32.ShellExecuteW(
                        None, 'runas', sys.executable, sys.argv[0], None, el_spec.SHOWNORMAL
                    )
                    if hinstance <= 32:
                        raise RuntimeError(el_error(hinstance))

        #   Routine for Linux
            elif prj_dict["system"].upper == 'LINUX':
                i = 0

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

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

    from datetime import datetime

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_fct'
    # operation = 'datetime_now(~)'
    # mpy_trace = tracing(module, operation, mpy_trace)

#   Retrieve the actual time value
    datetime_value  = datetime.now()

#   Year
    std_year = datetime_value.year

#   Month
    std_month = f'{datetime_value.month}'
    if datetime_value.month <= 9:
        std_month = f'0{std_month}'
        
#   Day
    std_day = f'{datetime_value.day}'
    if datetime_value.day <= 9:
        std_day = f'0{std_day}'

    date = f'{std_day}.{std_month}.{std_year}'
    datestamp = f'{std_year}-{std_month}-{std_day}'

#   Hour
    std_hour = f'{datetime_value.hour}'
    if datetime_value.hour <= 9:
        std_hour = f'0{std_hour}'

#   Minute
    std_minute = f'{datetime_value.minute}'
    if datetime_value.minute <= 9:
        std_minute = f'0{std_minute}'

#   Second
    std_second = f'{datetime_value.second}'
    if datetime_value.second <= 9:
        std_second = f'0{std_second}'

    time = f'{std_hour}:{std_minute}:{std_second}'
    timestamp = f'{std_hour}{std_minute}{std_second}'

    datetimestamp = f'{datestamp}_{timestamp}'

    loggingstamp = f'{std_year}{std_month}{std_day}_{timestamp}'

    return{
        'datetime_value' : datetime_value , \
        'date' : date , \
        'datestamp' : datestamp , \
        'time' : time , \
        'timestamp' : timestamp , \
        'datetimestamp' : datetimestamp , \
        'loggingstamp' : loggingstamp
    }

def runtime(mpy_trace, in_ref_time):

    """ This function calculates the actual runtime and returns it.
    :param
        mpy_trace - operation credentials and tracing
        in_ref_time - Value of the reference time to calculate the actual runtime
    :return - dictionary
        rnt_delta - Value of the actual runtime.
    """

    from datetime import datetime

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_fct'
    # operation = 'runtime(~)'
    # mpy_trace = tracing(module, operation, mpy_trace)

    rnt_delta = datetime.now() - in_ref_time

    return{
        'rnt_delta' : rnt_delta
    }

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

    import platform, getpass, os.path, socket
    from tkinter import Tk

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_fct'
    # operation = 'sysinfo(~)'
    # mpy_trace = tracing(module, operation, mpy_trace)

    system      = platform.uname().system
    release     = platform.uname().release
    version     = platform.uname().version
    arch        = platform.uname().machine
    processor   = platform.uname().processor
    threads     = perfinfo(mpy_trace)["cpu_count_log"]

    username    = getpass.getuser()
    homedir     = os.path.expanduser("~")
    hostname    = socket.gethostname()
    
    root = Tk()
    res_height = root.winfo_screenheight()
    res_width = root.winfo_screenwidth()
    root.destroy()

    return{
        'system' : system, \
        'system_release' : release, \
        'system_version' : version, \
        'system_arch' : arch, \
        'processor' : processor, \
        'threads' : threads, \
        'username' : username,\
        'homedir' : homedir, \
        'hostname' : hostname, \
        'res_height' : res_height, \
        'res_width' : res_width
    }

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

    import pathlib, os.path

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_fct'
    # operation = 'makepath(~)'
    # mpy_trace = tracing(module, operation, mpy_trace)

    out_path    = pathlib.Path(f'{in_path}')

    if os.path.isfile(in_path):
        is_file      = os.path.isfile(out_path)
        file_exists  = os.path.exists(out_path)
        file_name    = os.path.split(out_path)[1]
        file_ext     = os.path.splitext(out_path)
    else:
        is_file      = os.path.isfile(out_path)
        file_exists  = os.path.exists(out_path)
        file_name    = 'VOID'
        file_ext     = 'VOID'

    if os.path.isdir(in_path):
        is_dir       = os.path.isdir(out_path)
        dir_exists   = os.path.exists(out_path)
        dir_name     = os.path.split(out_path)[1]
        parent_dir   = os.path.split(out_path)[0]
    else:
        is_dir       = os.path.isdir(out_path)
        dir_exists   = os.path.exists(out_path)
        dir_name     = 'VOID'
        parent_dir   = 'VOID'

    return{
        'out_path' : out_path, \
        'is_file' : is_file, \
        'file_exists' : file_exists, \
        'file_name' :file_name, \
        'file_ext' :file_ext, \
        'is_dir' : is_dir, \
        'dir_exists' : dir_exists, \
        'dir_name' : dir_name, \
        'parent_dir' : parent_dir
    }

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
        path_obj - OS path object of the joined path parts. Is None, if path_parts is not a tuple.
    """

    import pathlib

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_fct'
    # operation = 'makepath(~)'
    # mpy_trace = tracing(module, operation, mpy_trace)

#   Preparation
    path_str = ''
    cnt = 0
    
#   Autocorrect path_parts to tuple
    if type(path_parts) is str:
        
        path_parts = (path_parts,)

#   Check, if path_parts is a tuple to ensure correct loop
    if type(path_parts) is tuple:
    
    #   Harmonize file extension
        if not file_extension:
            
            file_extension = None
    
    #   Loop through all parts of the path
        for part in path_parts:
    
        #   Check, if count is greater 0.
            if cnt:
                path_str += f'\\{part}'
                cnt += 1
            else:
                path_str = f'{part}'
                cnt += 1
    
    #   Add the file extension
        if file_extension is not None:
            
            path_str += f'{file_extension}'
        
        path_obj = pathlib.Path(path_str)
        
    else:
        
        path_obj = None

    return path_obj

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

    import psutil
    from datetime import datetime

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_fct'
    # operation = 'perfinfo(~)'
    # mpy_trace = tracing(module, operation, mpy_trace)

#TODO: "cpu_perc_indv" only works on Linux
#TODO: "cpu_perc_comb" and "cpu_perc_indv" do not work if interval=None

    boot_time       = datetime.fromtimestamp(psutil.boot_time())

    cpu_count_phys  = psutil.cpu_count(logical=False)
    cpu_count_log   = psutil.cpu_count(logical=True)
    cpu_freq_max    = psutil.cpu_freq(percpu=False).max
    cpu_freq_min    = psutil.cpu_freq(percpu=False).min
    cpu_freq_comb   = psutil.cpu_freq(percpu=False).current
    cpu_perc_comb   = psutil.cpu_percent(interval=None, percpu=False)
    cpu_perc_indv   = psutil.cpu_percent(interval=None, percpu=True)
    mem_total_MB    = psutil.virtual_memory().total / 1024**2
    mem_available_MB= psutil.virtual_memory().available / 1024**2
    mem_used_MB     = psutil.virtual_memory().used / 1024**2
    mem_free_MB     = psutil.virtual_memory().free / 1024**2

    return{
        'boot_time' : boot_time, \
        'cpu_count_phys' : cpu_count_phys, \
        'cpu_count_log' : cpu_count_log, \
        'cpu_freq_max' : cpu_freq_max, \
        'cpu_freq_min' : cpu_freq_min, \
        'cpu_freq_comb' : cpu_freq_comb, \
        'cpu_perc_comb' : cpu_perc_comb, \
        'cpu_perc_indv' : cpu_perc_indv, \
        'mem_total_MB' : mem_total_MB, \
        'mem_available_MB' : mem_available_MB, \
        'mem_used_MB' : mem_used_MB, \
        'mem_free_MB' : mem_free_MB, \
    }

def prj_dict_to_string(prj_dict):

    """ This function creates a string for the entire prj_dict. May exceed emory.
    :param
        prj_dict - morPy global dictionary
    :return
        prj_dict_str - morPy global dictionary as a UTF-8 string
    """

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    # module = 'mpy_fct'
    # operation = 'prj_dict_to_string(~)'
    # mpy_trace = tracing(module, operation, mpy_trace)

    prj_dict_str = ''

    for key, value in prj_dict.items():
        prj_dict_str = f'{prj_dict_str}\n{key} : {value}'
        prj_dict_str.strip()
        
    return prj_dict_str

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

    import copy

#   Deepcopy the mpy_trace dictionary. Any change in either dictionary is not reflected
#   in the other one. This is important to pass down informationen opersation for
#   operation and log for log.
    mpy_trace_passdown = copy.deepcopy(mpy_trace)

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    mpy_trace_passdown["module"] = f'{module}'
    mpy_trace_passdown["operation"] = f'{operation}'
    mpy_trace_passdown["tracing"] = f'{mpy_trace["tracing"]} > {module}.{operation}'

    return mpy_trace_passdown

def txt_wr(mpy_trace, prj_dict, filepath, content):

    import mpy_msg
    import sys, gc, pathlib

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

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_fct'
    operation = 'txt_wr(~)'
    mpy_trace = tracing(module, operation, mpy_trace)

#   Apply standard formats
    content = f'{content}'
    filepath = pathlib.Path(filepath)

#   Write to file
    try:

    #   Append to a textfile
        if filepath.is_file():

            with open(filepath, 'a') as ap:
                ap.write(f'\n{content}')

    #   Create and write a textfile
        else:

            with open(filepath, 'w') as wr:
                wr.write(content)

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()