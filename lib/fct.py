r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields the most basic functions of the morPy fork. These
            functions are designed for the initialization, so they can not support
            logging. Although not intended, these modules may be used freely
            since they are fully compatible with morPy.
"""

import sys
import psutil
import logging
import hashlib

def datetime_now() -> dict:
    r"""
    This function reads the current date and time and returns formatted
    stamps.

    :return: dict
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

def hashify(string: str) -> str:
    """
    Hash the given string using SHA-256 and return the hexadecimal digest.

    :param string: The input string to hash.

    :return str: A SHA-256 hash of the string as a hexadecimal string.
    """
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def runtime(in_ref_time) -> dict:
    r"""
    This function calculates the time delta between now and a reference time.

    :param in_ref_time: Value of the reference time to calculate the actual runtime

    :return: dict
        rnt_delta - Value of the actual runtime.
    """

    from datetime import datetime

    rnt_delta = datetime.now() - in_ref_time

    return{
        'rnt_delta' : rnt_delta
    }

def sysinfo() -> dict:
    r"""
    This function returns various information about the hardware and operating system.

    :return: dict
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

    system = platform.uname().system
    release = platform.uname().release
    version = platform.uname().version
    arch = platform.uname().machine
    processor = platform.uname().processor
    logical_cpus = perfinfo()["cpu_count_log"]
    sys_memory_bytes = psutil.virtual_memory().total

    username = getpass.getuser()
    homedir = os.path.expanduser("~")
    hostname = socket.gethostname()

    # Try to get main monitor info
    try:
        import ctypes
        # Make process DPI aware
        try:
            # For Windows 8.1 or later
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # or use 2 for per-monitor DPI awareness
        except Exception:
            # Fallback for older systems or if the call fails.
            ctypes.windll.user32.SetProcessDPIAware()
        # Get primary monitor resolution using Windows API
        user32 = ctypes.windll.user32
        res_width = user32.GetSystemMetrics(0)
        res_height = user32.GetSystemMetrics(1)
    # Fallback to tkinter, if ctypes is not supported. May not return info of main monitor.
    except Exception:
        # Fallback: use tkinter to get the resolution
        from tkinter import Tk
        root = Tk()
        res_width = root.winfo_screenwidth()
        res_height = root.winfo_screenheight()
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

def pathtool(in_path) -> dict:
    r"""
    This function takes a string and converts it to a path. Additionally,
    it returns path components and checks.

    :param in_path: Path to be converted

    :return: dict
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
        file_path = morPy.pathtool(file_path)["out_path"]
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

def path_join(path_parts, file_extension):
    r"""
    This function joins components of a tuple to a path with auto-detection of a file extension.

    :param path_parts: Tuple of parts to be joined. Exact order is critical. Examples:
                     ('C:', 'This', 'is', 'my', 'path', '.txt') - C:\This\is\my\path.txt
                     ('T:This_Fol', 'der_Will_Be_Split', 'this_Way') - T:\This_Fol\der_Will_Be_Split\this_Way
                     ('Y:', 'myFile.txt') - Y:\myFile.txt
    :param file_extension: String of the file extension (i.e. '.txt'). Leave
                         empty if path is a directory (None or '') or if the tuple already includes the
                         file extension.
    :return path_obj: OS path object of the joined path parts. Is None, if path_parts is not a tuple.
    """

    import pathlib

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

def perfinfo() -> dict:
    r"""
    This function returns hardware stats relevant for performance.

    :return: dict
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

    # Gather boot time
    boot_time = datetime.fromtimestamp(psutil.boot_time())

    # CPU counts
    cpu_count_phys = psutil.cpu_count(logical=False)
    cpu_count_log  = psutil.cpu_count(logical=True)

    # CPU frequencies
    freq_info     = psutil.cpu_freq(percpu=False)
    cpu_freq_max  = freq_info.max
    cpu_freq_min  = freq_info.min
    cpu_freq_comb = freq_info.current

    # CPU percentages:
    # Use a small interval so psutil measures CPU usage instead of returning a cached value.
    cpu_percent_list = psutil.cpu_percent(interval=0.1, percpu=True)
    cpu_perc_indv    = cpu_percent_list
    cpu_perc_comb    = sum(cpu_percent_list) / len(cpu_percent_list) if cpu_percent_list else 0.0

    # Memory info in MB
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

def app_dict_to_string(app_dict, depth: int=0) -> str:
    r"""
    This function creates a string for the entire app_dict. May exceed memory.

    :param app_dict: morPy global dictionary
    :param depth: Tracks the current indentation level for formatting the dictionary structure.
                  Increases with each nested dictionary. Not intended to be used when calling
                  it first.

    :return app_dict_str: morPy global dictionary as a UTF-8 string

    :example:
        app_dict_to_string(app_dict) # Do not specify depth!
    """

    if isinstance(app_dict, dict):

        # Define the priority order for level-1 nested dictionaries
        app_dict_order = ["conf", "sys", "run", "morpy", "loc"]

        lines = []
        indent = 4 * " " * depth  # 4 spaces per depth level

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

def tracing(module, operation, morpy_trace, clone=True, process_id=None, reset: bool=False,
            reset_w_prefix: str=None) -> dict:
    r"""
    This function formats the trace to any given operation. This function is
    necessary to alter the morpy_trace as a pass down rather than pointing to the
    same morpy_trace passed down by the calling operation. If morpy_trace is to be altered
    in any way (i.e. 'log_enable') it needs to be done after calling this function.
    This is why this function is called at the top of any morPy-operation.

    :param module: Name of the module, the operation is defined in (i.e. 'lib.common')
    :param operation: Name of the operation executed (i.e. 'tracing(~)')
    :param morpy_trace: operation credentials and tracing
    :param clone: If true (default), a clone of the trace will be created ensuring the tracing
        within morPy. If false, the parent trace will be altered directly (intended for
        initialization only).
    :param process_id: Adjust the process ID of the trace. Intended to be used by morPy
        orchestrator only.
    :param reset: If True, the trace will be reset/lost.
    :param reset_w_prefix: If reset is True, a custom preset can be set in order to retain
        a customized trace.

    :return morpy_trace_passdown: operation credentials and tracing
    """

    # Deepcopy the morpy_trace dictionary. Any change in either dictionary is not reflected
    # in the other one. This is important to pass down a functions trace effectively.
    if clone:
        import copy
        morpy_trace_passdown = copy.deepcopy(morpy_trace)
    else:
        morpy_trace_passdown = morpy_trace

    if process_id:
        morpy_trace_passdown["process_id"] = process_id

    # Define operation credentials (see init.init_cred() for all dict keys)
    morpy_trace_passdown["module"] = f'{module}'
    morpy_trace_passdown["operation"] = f'{operation}'

    if reset:
        morpy_trace_passdown["tracing"] = \
            f'{reset_w_prefix} > {module}.{operation}' if reset_w_prefix else f'{module}.{operation}'
    else:
        morpy_trace_passdown["tracing"] = f'{morpy_trace["tracing"]} > {module}.{operation}'

    return morpy_trace_passdown
