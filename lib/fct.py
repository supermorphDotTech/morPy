r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields the most basic functions of the morPy fork. These
            functions are optimised for initilization, so they do not support
            logging. Although not intended, these modules may be used freely
            since they are fully compatible with morPy.
"""

from lib.decorators import log

import sys
import psutil
import logging

def privileges_handler(morPy_trace, app_dict):

    r""" This function tests the privileges of __main__ and restarts with
        a request for admin rights if it was set in the parameters.
    :param
        morPy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
    :return
        -

    TODO Finish the module and fix all bugs
    """

    import lib.msg
    import sys, ctypes, enum, gc

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'fct'
    operation = 'privileges_handler(~)'
    morPy_trace = tracing(module, operation, morPy_trace)

    # Preparing parameters
    check = False

    try:

        # Specification of how to open an elevated program
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

        # Specification of how to interpret errors from ctypes
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

        # Test if elevated privileges are required
        if  app_dict["conf"]["priv_required"]:

            # Routine for MS Windows
            if app_dict["sys"]["os"].upper == 'WINDOWS':
                if ctypes.windll.shell32.IsUserAnAdmin():
                    # Program started with elevated Privileges.
                    msg = app_dict["priv_handler_eval"]
                else:
                    hinstance = ctypes.windll.shell32.ShellExecuteW(
                        None, 'runas', sys.executable, sys.argv[0], None, el_spec.SHOWNORMAL
                    )
                    if hinstance <= 32:
                        raise RuntimeError(el_error(hinstance))

            # Routine for Linux
            elif app_dict["sys"]["os"].upper == 'LINUX':
                i = 0

        check = True

    # Error detection
    except Exception as e:
        log(morPy_trace, app_dict, "critical",
            lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'morPy_trace' : morPy_trace,
            'check' : check
            }

def datetime_now(morPy_trace):

    r""" This function reads the current date and time and returns formatted
        stamps.
    :param
        morPy_trace - operation credentials and tracing
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

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module = 'fct'
    # operation = 'datetime_now(~)'
    # morPy_trace = tracing(module, operation, morPy_trace)

    # Retrieve the actual time value
    datetime_value  = datetime.now()

    # Year
    std_year = datetime_value.year

    # Month
    std_month = f'{datetime_value.month}'
    if datetime_value.month <= 9:
        std_month = f'0{std_month}'

    # Day
    std_day = f'{datetime_value.day}'
    if datetime_value.day <= 9:
        std_day = f'0{std_day}'

    date = f'{std_day}.{std_month}.{std_year}'
    datestamp = f'{std_year}-{std_month}-{std_day}'

    # Hour
    std_hour = f'{datetime_value.hour}'
    if datetime_value.hour <= 9:
        std_hour = f'0{std_hour}'

    # Minute
    std_minute = f'{datetime_value.minute}'
    if datetime_value.minute <= 9:
        std_minute = f'0{std_minute}'

    # Second
    std_second = f'{datetime_value.second}'
    if datetime_value.second <= 9:
        std_second = f'0{std_second}'

    time = f'{std_hour}:{std_minute}:{std_second}'
    timestamp = f'{std_hour}{std_minute}{std_second}'

    datetimestamp = f'{datestamp}_{timestamp}'

    loggingstamp = f'{std_year}{std_month}{std_day}_{timestamp}'

    return{
        'datetime_value' : datetime_value ,
        'date' : date ,
        'datestamp' : datestamp ,
        'time' : time ,
        'timestamp' : timestamp ,
        'datetimestamp' : datetimestamp ,
        'loggingstamp' : loggingstamp
    }

def runtime(morPy_trace, in_ref_time):

    r""" This function calculates the actual runtime and returns it.
    :param
        morPy_trace - operation credentials and tracing
        in_ref_time - Value of the reference time to calculate the actual runtime
    :return - dictionary
        rnt_delta - Value of the actual runtime.
    """

    from datetime import datetime

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module = 'fct'
    # operation = 'runtime(~)'
    # morPy_trace = tracing(module, operation, morPy_trace)

    rnt_delta = datetime.now() - in_ref_time

    return{
        'rnt_delta' : rnt_delta
    }

def sysinfo(morPy_trace):

    r""" This function returns various informations about the hardware and operating system.
    :param
        morPy_trace - operation credentials and tracing
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

    import platform, getpass, os.path, socket
    from tkinter import Tk

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module = 'fct'
    # operation = 'sysinfo(~)'
    # morPy_trace = tracing(module, operation, morPy_trace)

    system = platform.uname().system
    release = platform.uname().release
    version = platform.uname().version
    arch = platform.uname().machine
    processor = platform.uname().processor
    logical_cpus = perfinfo(morPy_trace)["cpu_count_log"]
    sys_memory_bytes = psutil.virtual_memory().total

    username = getpass.getuser()
    homedir = os.path.expanduser("~")
    hostname = socket.gethostname()

    root = Tk()
    res_height = root.winfo_screenheight()
    res_width = root.winfo_screenwidth()
    root.destroy()

    return{
        'os' : system,
        'os_release' : release,
        'os_version' : version,
        'os_arch' : arch,
        'processor' : processor,
        'logical_cpus' : logical_cpus,
        'sys_memory_bytes' : sys_memory_bytes,
        'username' : username,
        'homedir' : homedir,
        'hostname' : hostname,
        'resolution_height' : res_height,
        'resolution_width' : res_width,
    }

def pathtool(morPy_trace: dict, in_path):
    r"""
    This function takes a string and converts it to a path. Additionally,
    it returns path components and checks.

    :param morPy_trace: operation credentials and tracing
    :param in_path: Path to be converted

    :return: dictionary
        out_path - Same as the input, but converted to a path.
        is_file - The path is a file path. File does not need to exist.
        file_exists - The file has been found under the given path.
        file_name - This is the actual file name.
        file_ext - This is the file extension or file type.
        is_dir - The path is a directory. Directory does not need to exist.
        dir_exists - The directory has been found under the given path.
        dir_name - This is the actual directory name.
        parent_dir - Path of the parent directory.

    :example:
        file_path = "C:\my_file.txt"
        file_path = morPy.pathtool(morPy_trace, file_path)["out_path"]
    """

    import pathlib

    p = pathlib.Path(in_path).resolve()

    # Check if path *exists* on disk
    path_exists = p.exists()

    # Heuristic: If path has a suffix (i.e. ".txt"), treat as file.
    # If no suffix, or p ends with a slash, treat as directory.
    has_suffix = bool(p.suffix)  # True if something like ".txt", ".xlsx", etc.

    # Even though p.exists() might be False, we can still treat it as "is_file"
    # if it has an extension. This is purely a custom rule.
    is_file = has_suffix
    is_dir = p.is_dir() if path_exists else (not has_suffix)

    file_name = p.name if is_file else None
    file_ext = p.suffix if is_file else None

    dir_name = p.name if is_dir else None
    parent_dir = str(p.parent)

    return{
        'out_path' : str(p),
        'is_file' : is_file,
        'file_exists' : path_exists and is_file,
        'file_name' :file_name,
        'file_ext' :file_ext,
        'is_dir' : is_dir,
        'dir_exists' : path_exists and is_dir,
        'dir_name' : dir_name,
        'parent_dir' : parent_dir,
    }

def path_join(morPy_trace, path_parts, file_extension):

    r"""
    This function joins components of a tuple to an OS path.

    :param
        morPy_trace - operation credentials and tracing
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

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module = 'fct'
    # operation = 'makepath(~)'
    # morPy_trace = tracing(module, operation, morPy_trace)

    # Preparation
    path_str = ''
    cnt = 0

    # Autocorrect path_parts to tuple
    if type(path_parts) is str:

        path_parts = (path_parts,)

    # Check, if path_parts is a tuple to ensure correct loop
    if type(path_parts) is tuple:

        # Harmonize file extension
        if not file_extension:

            file_extension = None

        # Loop through all parts of the path
        for part in path_parts:

            # Check, if count is greater 0.
            if cnt:
                path_str += f'\\{part}'
                cnt += 1
            else:
                path_str = f'{part}'
                cnt += 1

        # Add the file extension
        if file_extension is not None:

            path_str += f'{file_extension}'

        path_obj = pathlib.Path(path_str)

    else:

        path_obj = None

    return path_obj

def perfinfo(morPy_trace):

    r""" This function returns performance metrics.
    :param
        morPy_trace - operation credentials and tracing
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

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module = 'fct'
    # operation = 'perfinfo(~)'
    # morPy_trace = tracing(module, operation, morPy_trace)

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
        'boot_time' : boot_time,
        'cpu_count_phys' : cpu_count_phys,
        'cpu_count_log' : cpu_count_log,
        'cpu_freq_max' : cpu_freq_max,
        'cpu_freq_min' : cpu_freq_min,
        'cpu_freq_comb' : cpu_freq_comb,
        'cpu_perc_comb' : cpu_perc_comb,
        'cpu_perc_indv' : cpu_perc_indv,
        'mem_total_MB' : mem_total_MB,
        'mem_available_MB' : mem_available_MB,
        'mem_used_MB' : mem_used_MB,
        'mem_free_MB' : mem_free_MB,
    }

def app_dict_to_string(app_dict, depth=0):

    r"""
    This function creates a string for the entire app_dict. May exceed memory.

    :param app_dict: morPy global dictionary

    :return app_dict_str: morPy global dictionary as a UTF-8 string
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module = 'fct'
    # operation = 'app_dict_to_string(~)'
    # morPy_trace = tracing(module, operation, morPy_trace)

    if isinstance(app_dict, dict):

        # Define the priority order for level-1 subdictionaries
        app_dict_order = ["conf", "sys", "run", "global", "proc", "loc"]

        lines = []
        indent = 3 * " " * depth  # 4 spaces per depth level

        for key, value in app_dict.items():
            if isinstance(value, dict):
                    lines.append(f"{indent}{key}:")
                    lines.append(app_dict_to_string(value, depth + 1))  # Recursively handle nested dictionaries
            else:
                value_linebreak = ""
                l = 0
                for line in f"{value}".splitlines():
                    l += 1
                    value_linebreak += line if l==1 else f'\n{indent}{(len(key)+3)*" "}{line}'
                lines.append(f"{indent}{key} : {value_linebreak}")

        return '\n'.join(lines)
    else:
        return None

def tracing(module, operation, morPy_trace, clone=True, process_id=None):

    r"""
    This function formats the trace to any given operation. This function is
    necessary to alter the morPy_trace as a pass down rather than pointing to the
    same morPy_trace passed down by the calling operation. If morPy_trace is to altered
    in any way (i.e. 'log_enable') it needs to be done after calling this function.
    This is why this function is called at the top of any operation.

    :param module: Name of the module, the operation is defined in (i.e. 'common')
    :param operation: Name of the operation executed (i.e. 'tracing(~)')
    :param morPy_trace: operation credentials and tracing
    :param clone: If true (default), a clone of the trace will be created ensuring the tracing
        within morPy. If false, the parent trace will be altered directly (intended for
        initialization only).
    :param process_id: Adjust the process ID of the trace. Intended to be used by morPy
        orchestrator only.

    :return morPy_trace_passdown: operation credentials and tracing
    """

    # Deepcopy the morPy_trace dictionary. Any change in either dictionary is not reflected
    # in the other one. This is important to pass down a functions trace effectively.
    if clone:
        import copy
        morPy_trace_passdown = copy.deepcopy(morPy_trace)
    else:
        morPy_trace_passdown = morPy_trace

    if process_id:
        morPy_trace_passdown["process_id"] = process_id

    # Define operation credentials (see init.init_cred() for all dict keys)
    morPy_trace_passdown["module"] = f'{module}'
    morPy_trace_passdown["operation"] = f'{operation}'
    morPy_trace_passdown["tracing"] = f'{morPy_trace["tracing"]} > {module}.{operation}'

    return morPy_trace_passdown

def txt_wr(morPy_trace, app_dict, filepath, content):

    import lib.msg
    import sys, gc, pathlib

    r""" This function appends to any textfile and creates it, if it does not
        exist yet.
    :param
        morPy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        filepath - Path to the textfile including its name and filetype
        content - Something that will be printed as a string.
    :return
        -
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'fct'
    operation = 'txt_wr(~)'
    morPy_trace = tracing(module, operation, morPy_trace)

    # Preparing parameters
    check = False

    # Apply standard formats
    content = f'{content}'
    filepath = pathlib.Path(filepath)

    # Write to file
    try:

        # Append to a textfile
        if filepath.is_file():

            with open(filepath, 'a') as ap:
                ap.write(f'\n{content}')

        # Create and write a textfile
        else:

            with open(filepath, 'w') as wr:
                wr.write(content)

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    finally:
        # Return a dictionary
        return{
            'morPy_trace' : morPy_trace,
            'check' : check
            }

def handle_exception_main(e, init=False, app_dict=None):
    r"""
    Handle any exception outside the scope of msg.py
    """
    import lib.msg

    if init and app_dict is not None:
        message = (f'{app_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                       f'{app_dict["err_excp"]}: {e}')
        msg.log('__main__', app_dict, message, 'critical')
    elif not init:
        # Fallback logging in case the app dictionary or logging fails
        logging.critical(f'Module: __main__\n'
                         f'Line: {sys.exc_info()[-1].tb_lineno}\n'
                         f'CRITICAL Exception: {e}\n'
                         f'morPy initialization failed!')
    elif init and app_dict is None:
        # Fallback logging in case the app dictionary or logging fails
        logging.critical(f'Module: __main__\n'
                         f'Line: {sys.exc_info()[-1].tb_lineno}\n'
                         f'CRITICAL Exception: {e}\n'
                         f'Missing app_dict - morPy execution failed!')

    # Quit the program
    sys.exit()

def handle_exception_init(e):
    r"""
    Handle any exception outside the scope of msg.py
    """

    # Fallback logging in case the app dictionary or logging fails
    logging.critical(f'Module: init\n'
                     f'Line: {sys.exc_info()[-1].tb_lineno}\n'
                     f'CRITICAL Exception: {e}\n'
                     f'morPy initialization failed!')

    # Quit the program
    sys.exit()

def handle_exception_decorator(e):
    r"""
    Handle any exception outside the scope of msg.py
    """

    # Fallback logging in case the app dictionary or logging fails
    logging.critical(f'Module: decorators\n'
                     f'Line: {sys.exc_info()[-1].tb_lineno}\n'
                     f'CRITICAL Exception: {e}\n'
                     f'Wrapper function error.')

    # Quit the program
    sys.exit()

def handle_exception_mp(e):
    r"""
    Handle any exception outside the scope of msg.py
    """

    # Fallback logging in case the app dictionary or logging fails
    logging.critical(f'Module: mp\n'
                     f'Line: {sys.exc_info()[-1].tb_lineno}\n'
                     f'CRITICAL Exception: {e}\n'
                     f'Multiprocessing decorator error.')

    # Quit the program
    sys.exit()