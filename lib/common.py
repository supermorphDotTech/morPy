r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Module of generally useful functions.
"""

import lib.fct as morpy_fct
import morPy
from lib.mp import interrupt, stop_while_interrupt
from morPy import log
from lib.decorators import morpy_wrap

import sys
import chardet
import io
import shutil
import os
import os.path
import re
from heapq import heappush, heappop


class PriorityQueue:
    r"""
    Provides a priority‑based task queue where lower numeric values indicate
    higher priority. Enqueued tasks are also timestamped with an incrementing
    counter to preserve insertion order for tasks sharing the same priority.
    """


    @morpy_wrap
    def __init__(self, trace: dict, app_dict: dict, name: str) -> None:
        r"""
        Sets up the priority queue with tracing, the global configuration, and an
        optional name. It initializes internal counters and data structures needed
        for task storage and lookup.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param name: Name or description of the instance
        """

        self.name = name if name else 'queue'
        self.heap = []
        self.counter = 0 # Task counter. Starts at 0, increments by 1
        self.task_lookup = set() # Set for quick task existence check

        # Priority queue initialized.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_init_done"]}\n'
                    f'{app_dict["loc"]["morpy"]["PriorityQueue_name"]}: {self.name}')


    @morpy_wrap
    def enqueue(self, trace: dict, app_dict: dict, priority: int=100, task: tuple=None) -> None:
        r"""
        Adds a task to the priority queue under a specified integer priority (lower means
        higher priority). The task must be supplied as a callable packaged with its arguments
        (for example, as a tuple or partial). If the task is already present (as determined by
        its system‐ID), a debug message indicates duplication; otherwise, it is inserted with
        an associated counter.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param priority: Integer representing task priority (lower is higher priority)
        :param task: Tuple of a callable, *args and **kwargs (func, *args, **kwargs)

        :example:
            from functools import partial
            queue = PriorityQueue(trace, app_dict, name="example_queue")
            task = partial(my_func, trace, app_dict)
            queue.enqueue(trace, app_dict, priority=25, task=task)
        """

        if task:
            # Pushing task to priority queue.
            log(trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_enqueue_start"]} {self.name}\n'
                        f'{app_dict["loc"]["morpy"]["PriorityQueue_enqueue_priority"]}: {priority}')

            # Increment task counter
            self.counter += 1

            task_sys_id = id(task)

            # Check, if ID already in queue
            if task_sys_id in self.task_lookup:
                # Task is already enqueued. Referencing in queue.
                log(trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_enqueue_task_duplicate"]}\n'
                            f'Task system ID: {task_sys_id}')
            else:
                self.task_lookup.add(task_sys_id)

            # Push task to queue
            task_qed = (priority, self.counter, task_sys_id, task)
            heappush(self.heap, task_qed)
        else:
            # Task can not be None. Skipping enqueue.
            log(trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_enqueue_none"]}')


    @morpy_wrap
    def pull(self, trace: dict, app_dict: dict) -> dict:
        r"""
        Removes the highest‑priority task from the queue and returns a dictionary
        with the task’s priority, counter value, system‑assigned task ID, and the
        task components as a list. If the queue is empty, a debug message is logged.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            priority: Integer representing task priority (lower is higher priority)
            counter: Number of the task when enqueued
            task_sys_id : ID of the task determined by Python core
            task: The pulled task list
            task_callable: The pulled task callable

        :example:
            from functools import partial
            queue = PriorityQueue(trace, app_dict, name="example_queue")
            task = queue.pull(trace, app_dict)['task']
            task()  # Assuming, the object stored is a callable
        """

        priority = None
        counter = None
        task_sys_id = None
        task = None

        # Global interrupt - wait for error handling
        stop_while_interrupt(trace, app_dict)

        if len(self.heap) > 0:
            task_pulled = heappop(self.heap)
            priority, counter, task_sys_id, task = task_pulled

            # Pulling task from NAME priority: INT counter: INT
            log(trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_pull_start"]} {self.name}.\n'
                        f'{app_dict["loc"]["morpy"]["PriorityQueue_pull_priority"]}: {priority}\n'
                        f'{app_dict["loc"]["morpy"]["PriorityQueue_pull_cnt"]}: {counter}',
                        verbose = True)

        else:
            # Can not pull from an empty priority queue. Skipped...
            log(trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_pull_void"]}')

        return {
            'priority' : priority,
            'counter' : counter,
            'task_sys_id' : task_sys_id,
            'task': list(task)
        }


class ProgressTracker:
    r"""
    Maintains a numerical counter to track progress during long‑running operations. It logs progress
    updates at specified tick percentages and supports both floating‑point and integer counting for
    efficiency.
    """


    @morpy_wrap
    def __init__(self, trace: dict, app_dict: dict, description: str=None, total: float=None, ticks: float=None,
              float_progress: bool=False, verbose: bool=False) -> None:
        r"""
        Initializes the progress tracker with a descriptive label, a total count needed for completion,
        and a tick value (in percent) that determines when to log progress updates. An option is
        available to use floating‑point progress and to enable verbose logging.

        :param trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param description: Describe, what is being processed (i.e. file path or calculation)
        :param total: Mandatory - The total count for completion
        :param ticks: Mandatory - Percentage of total to log the progress. I.e. at ticks=10.7 at every
            10.7% progress exceeded the exact progress will be logged. If None or greater 100, will default to 10.
        :param float_progress: For efficient progress tracking, by default the progress is not tracked with
            floats. If True, the amount of ticks at which to update progress may be a lot more expensive.
            Defaults to False.
        :param verbose: If True, progress is only logged in verbose mode except for the 100% mark. Defaults to False.

        :example:
            prog_tracker = morPy.ProgressTracker(trace, app_dict, description=description, total=total, ticks=ticks)
        """

        # Missing total count. Can not track progress if point of completion is unknown.
        if not total: raise ValueError(f'{app_dict["loc"]["morpy"]["ProgressTracker_miss_total"]}')

        # Evaluate ticks
        if not ticks or ticks > 100:
            self.ticks = 10
        else:
            self.ticks = ticks

        self.total = total
        self.ticks_lst = []

        # self.ticks_rel = self.ticks / 100
        # Determine relative progress ticks
        if float_progress:
            self.ticks_rel = self.ticks / 100
        else:
            # If progress is tracked with integers and ticks smaller than they can possibly be, correct
            # the relative ticks for inexpensive tracking.
            ticks_rel_full = self.ticks / 100
            ticks_rel_reduced = 1 / self.total
            self.ticks_rel = ticks_rel_reduced if ticks_rel_reduced > ticks_rel_full else ticks_rel_full

        self.description = f'{description}' if description else ''
        self.update_counter = 0
        self.stop_updates = False
        self.done = False

        # Evaluate verbose mode
        with morPy.conditional_lock(app_dict["morpy"]["conf"]):
            if verbose and app_dict["morpy"]["conf"]["msg_verbose"]:
                self.verbose = True
            else:
                self.verbose = False

        # Determine absolute progress ticks
        self._init_ticks(trace, app_dict)


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def _init_ticks(self, trace: dict, app_dict: dict) -> None:
        r"""
        This method determines the ticks, at which to log the progress.

        :param trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :example:
            self._init_ticks(trace, app_dict)
        """

        # Convert total to integer and determine the factor
        factor: int = 1
        total_fac = self.total
        if isinstance(total_fac, float):
            while not total_fac.is_integer():
                total_fac *= 10
                factor *= 10
        self.total_fac = int(total_fac)
        self.factor = factor

        # Determine the absolute ticks
        abs_tick: int = 0
        cnt_ticks: int = 0
        ticks_lst = [self.total_fac]
        while abs_tick < self.total_fac:
            cnt_ticks += 1
            abs_tick = self.total_fac * self.ticks_rel * cnt_ticks
            if (abs_tick not in ticks_lst) and (abs_tick < self.total_fac):
                ticks_lst.append(int(abs_tick))
        ticks_lst.sort()
        self.ticks_lst = ticks_lst


    @morpy_wrap
    def update(self, trace: dict, app_dict: dict, current: float=None) -> dict:
        r"""
        Updates the current progress count (either incrementally or to a given value) and
        logs progress if a tick threshold is reached.

        :param trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.

        :return: dict
            prog_rel: Relative progress, float between 0 and 1
            prog_abs: Absolute progress, float between 0.00 and 100.00
            message: Message generated. None, if no tick was hit.

        :example:
            import morPy

            tot_cnt = 100
            tks = 12.5
            prog_tracker = morPy.ProgressTracker(trace, app_dict, description='App Progress', total=total_count, ticks=tks)

            curr_cnt = 37
            prog_tracker.update(trace, app_dict, current=curr_cnt)
        """

        prog_rel = None
        prog_abs_short = None
        message = None

        if not self.done:
            # Evaluate current progress absolute count
            if not current:
                self.update_counter += 1
                current = self.update_counter
            elif current > self.update_counter:
                self.update_counter = current

            if current > self.total:
                self.stop_updates = True

                # Current progress exceeded total. Progress updates stopped.
                log(trace, app_dict, "warning",
                    lambda: f'{app_dict["loc"]["morpy"]["ProgressTracker_upd_stopped"]}: {current} > {self.total}')

            # Factor the current value
            current_fac = self.update_counter * self.factor

            # Loop through the absolute ticks, delete them and return the highest tick matched or exceeded
            log_tick = False
            for tick in self.ticks_lst:
                if current_fac >= tick:
                    self.ticks_lst.pop(0)
                    log_tick = True
                else:
                    pass

            if log_tick:
                prog_rel = current_fac / self.total_fac
                prog_abs_short = round(prog_rel * 100, 2)

                # Evaluate, if 100% reached
                self.done = True if prog_rel >= 1 else False

                # Check for verbose logging
                if self.verbose or self.done:
                    # Processing DESCRIPTION
                    log(trace, app_dict, "info",
                        lambda: f'{app_dict["loc"]["morpy"]["ProgressTracker_proc"]}: {self.description}\n'
                                f'{prog_abs_short}% ({self.update_counter} of {self.total})')

        return{
            'prog_rel' : prog_rel,
            'prog_abs' : prog_abs_short,
            'message' : message
            }


@morpy_wrap
def decode_to_plain_text(trace: dict, app_dict: dict, src_input, encoding: str='') -> dict:
    r"""
    Decodes binary data into a plain text (string) buffer using a specified encoding, or
    auto‑detects the encoding if none is provided. Returns a dictionary including the decoded
    result (as a StringIO object), the encoding used, and the number of lines in the text.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param src_input: Any kind of data to be decoded. Binary expected.
    :param encoding: String that defines encoding. Leave empty to auto-detect.

    :return: dict
        result: Decoded result. Buffered object that may be used with the readlines() method.
        encoding: String containing the encoding of src_input.
        lines: Number of lines in the file.

    :example:
        src_file = "C:\my_file.enc"
        src_input = open(src_file, 'rb')
        encoding: str = 'utf-16-le'
        retval = decode_to_plain_text(trace, app_dict, src_input, encoding)
    """

    decode = False

    # Copy all contents
    src_copy = src_input.read()
    lines = src_copy.count(b'\n') + 1

    # Auto-detect encoding if not provided
    if not encoding:
        try:
            encoding = chardet.detect(src_copy)["encoding"]
            decode = True

    #   Warning if src_copy is of wrong format or not encoded.
        except Exception as e:
            log(trace, app_dict, "warning",
                lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno}'
                        f'{app_dict["loc"]["morpy"]["err_module"]} {trace["module"]}\n'
                        f'{app_dict["loc"]["morpy"]["decode_to_plain_text_msg"]}: {e}')

    # Validate provided encoding
    else:
        try:
            encoding = chardet.detect(src_copy)["encoding"]
            decode = True

        # Not encoded if an exception is raised
        except:
            # Validation of encoding failed.
            raise RuntimeError(f'{app_dict["loc"]["morpy"]["decode_to_plain_text_val_fail"]}')

    # Decode the content
    if decode:
        result = io.StringIO(src_copy.decode(encoding))

        # Decoded from ### to plain text.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["decode_to_plain_text_from"]} {encoding}) '
                    f'{app_dict["loc"]["morpy"]["decode_to_plain_text_to"]}\n'
                    f'encoding: {encoding}')

    # Handle unsupported or non-encoded input
    else:
        result = io.StringIO(src_copy.decode('utf-8', errors='ignore'))

        # The Input is not decoded or not supported. No action taken.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["decode_to_plain_text_not"]}\n'
                    f'encoding: {encoding}')

    return {
        'result': result,
        'encoding': encoding,
        'lines': lines,
    }


@morpy_wrap
def fso_copy_file(trace: dict, app_dict: dict, source: str, dest: str, overwrite: bool=False) -> None:
    r"""
    Copies a file from a complete source path to a complete destination path. Before copying,
    it verifies that the source exists and whether the destination should be overwritten based
    on the ‘overwrite’ flag; logs the action accordingly.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param source: Complete path to the source file, including the file extension.
    :param dest: Complete path to the destination file, including the file extension.
    :param overwrite: Boolean indicating if the destination file may be overwritten. Defaults to False.

    :example:
        morPy.fso_copy_file(trace, app_dict, "path/to/source.txt", "path/to/destination.txt", True)
    """

    # Check the source file
    source_eval = morpy_fct.pathtool(source)
    source_exist = source_eval["file_exists"]
    source = source_eval["out_path"]

    # Check the destination file
    dest_eval = morpy_fct.pathtool(dest)
    dest_exist = dest_eval["file_exists"]
    dest = dest_eval["out_path"]

    # Evaluate the existence of the source
    if source_exist:

        # Evaluate the existence of the destination and overwrite permission
        if dest_exist and overwrite:

            shutil.copyfile(source, dest)

            # A file has been copied and the original was overwritten.
            log(trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["fso_copy_file_copy_overwrite"]}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_source"]}: {source}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_dest"]}: {dest}\n'
                        f'dest_exist: {dest_exist}\n'
                        f'overwrite_perm: {overwrite}')

        # Evaluate the existence of the destination and overwrite permission
        if dest_exist and not overwrite:

            shutil.copyfile(source, dest)

            # A file was not copied because it already exists and no overwrite permission was given.
            log(trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["fso_copy_file_copy_not_overwrite"]}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_source"]}: {source}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_dest"]}: {dest}\n'
                        f'dest_exist: {dest_exist}\n'
                        f'overwrite_perm: {overwrite}')

        if dest_exist:

            shutil.copyfile(source, dest)

            # A file has been copied.
            log(trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["fso_copy_file_copy"]}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_source"]}: {source}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_dest"]}: {dest}')

    else:
        # A file could not be copied, because it does not exist.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_copy_file_not_exist"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_copy_file_source"]}: {source}\n'
                    f'{app_dict["loc"]["morpy"]["fso_copy_file_dest"]}: {dest}\n'
                    f'source_exist: {source_exist}')


@morpy_wrap
def fso_create_dir(trace: dict, app_dict: dict, mk_dir: str) -> None:
    r"""
    Creates a directory (and all necessary parent directories) at the specified path.
    If the directory already exists, a debug message is logged and no action is taken.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param mk_dir: Path to the directory or directory tree to be created.

    :example:
        morPy.fso_create_dir(trace, app_dict, "path/to/new_directory")
    """

    # Check the directory
    dir_eval = morpy_fct.pathtool(mk_dir)
    dir_exist = dir_eval["dir_exists"]
    mk_dir = dir_eval["out_path"]

    if dir_exist:
        # The directory already exists.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_create_dir_not_created"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_create_dir_directory"]}: {mk_dir}\n'
                    f'{app_dict["loc"]["morpy"]["fso_create_dir_dir_exist"]}: {dir_exist}')

    else:
        os.makedirs(mk_dir)

        # The directory has been created.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_create_dir_created"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_create_dir_directory"]}: {mk_dir}')


@morpy_wrap
def fso_delete_dir(trace: dict, app_dict: dict, del_dir: str) -> None:
    r"""
    Recursively deletes an entire directory and its contents after checking that the
    specified directory exists. Logs the deletion outcome.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param del_dir: Path to the directory to be deleted.

    :example:
        morPy.fso_delete_dir(trace, app_dict, "path/to/directory_to_delete")
    """

    # Check the directory
    dir_eval = morpy_fct.pathtool(del_dir)
    dir_exist = dir_eval["dir_exists"]
    del_dir = dir_eval["out_path"]

    if dir_exist:

        shutil.rmtree(del_dir)

        # The directory has been deleted.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_delete_dir_deleted"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_create_dir_directory"]}: {del_dir}')

    else:
        # The directory does not exist.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_delete_dir_not_exist"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_create_dir_directory"]}: {del_dir}\n'
                    f'{app_dict["loc"]["morpy"]["fso_delete_dir_dir_exist"]}: {dir_exist}')


@morpy_wrap
def fso_delete_file(trace: dict, app_dict: dict, del_file: str) -> None:
    r"""
    Deletes a single file after verifying that the file exists at the specified path.
    Logs the operation, or if the file does not exist, logs a warning.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param del_file: Path to the file to be deleted.

    :example:
        morPy.fso_delete_file(trace, app_dict, "path/to/file_to_delete.txt")
    """

    # Check the directory
    file_eval = morpy_fct.pathtool(del_file)
    file_exist = file_eval["file_exists"]
    del_file = file_eval["out_path"]

    if file_exist:

        os.remove(del_file)

        # The file has been deleted.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_delete_file_deleted"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_delete_file_file"]}: {del_file}')

    else:
        # The file does not exist.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_delete_file_not_exist"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_delete_file_file"]}: {del_file}\n'
                    f'{app_dict["loc"]["morpy"]["fso_delete_file_exist"]}: {file_exist}')


@morpy_wrap
def fso_walk(trace: dict, app_dict: dict, path: str, depth: int=1) -> dict:
    r"""
    Recursively lists the contents of the specified directory up to a given depth. Returns a
    dictionary mapping each discovered root (labeled sequentially) to its path, a list of
    sub‑directories, and a list of files.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param path: Path to the directory to be analyzed.
    :param depth: Limits the depth of the analysis. Defaults to 1. Examples:
                  -1: No limit.
                   0: Path only.

    :return: dict
        walk_dict: Dictionary of root directories and their contents. Example:
                   {
                       'root0': {
                           'root': root,
                           'dirs': [dir list],
                           'files': [file list]
                       },
                       'root1': {
                           'root': root,
                           'dirs': [dir list],
                           'files': [file list]
                       },
                       [...],
                   }

    :example:
        result = morPy.fso_walk(trace, app_dict, "path/to/directory", -1)["walk_dict"]
    """

    walk_dict: dict = {}
    cnt_roots: int = 0

    # Check the directory
    if morpy_fct.pathtool(path)["dir_exists"]:
        for root, dirs, files in os.walk(path):
            # Exit if depth is reached
            if cnt_roots > depth:
                break

            walk_dict.update({f'root{cnt_roots}' : {'root' : root, 'dirs' : dirs, 'files' : files}})
            cnt_roots += 1

        # Directory analyzed.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_walk_path_done"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_walk_path_dir"]}: {path}')

    else:
        # The directory does not exist.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_walk_path_not_exist"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_walk_path_dir"]}: {path}')

    return{
        'walk_dict' : walk_dict
        }


@morpy_wrap
def regex_findall(trace: dict, app_dict: dict, search_obj: object, pattern: str) -> dict:
    r"""
    Searches the input (converted to a string) for all occurrences of a given regular expression
    pattern and returns a list of all matching substrings, or None if no matches are found.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        result: List of expressions found in the input, or None if nothing was found.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = morPy.regex_findall(trace, app_dict, string, pattern)["result"]
    """

    search_obj: str = f'{search_obj}'
    pattern: str = f'{pattern}'
    result = None

    # Searching for regular expressions.
    log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_findall_init"]}\n'
                f'{app_dict["loc"]["morpy"]["regex_findall_pattern"]}: {pattern}\n'
                f'search_obj: {search_obj}')

    # Search for the pattern
    result_matches = re.findall(pattern, search_obj)
    result = result_matches if result_matches else None

    # Search completed.
    log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_findall_complete"]}\n'
                f'{app_dict["loc"]["morpy"]["regex_findall_result"]}: {result}')

    return{
        'result' : result
        }


@morpy_wrap
def regex_find1st(trace: dict, app_dict: dict, search_obj: object, pattern: str) -> dict:
    r"""
    Searches the input string for the first occurrence of a specified regular expression pattern
    and returns that match, or None if there is no match.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        result: The first match found in the input, or None if nothing was found.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = morPy.regex_find1st(trace, app_dict, string, pattern)["result"]
    """

    search_string: str = f'{search_obj}'
    pattern: str = f'{pattern}'
    result = None

    # Searching for regular expressions.
    log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_find1st_init"]}\n'
                f'{app_dict["loc"]["morpy"]["regex_find1st_pattern"]}: {pattern}\n'
                f'search_obj: {search_string}')

    if search_string is not None:

        result_match = re.search(pattern, search_string)
        result = result_match.group() if result_match else None

        # Search completed.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["regex_find1st_complete"]}\n'
                    f'{app_dict["loc"]["morpy"]["regex_find1st_result"]}: {result}')

    else:
        result = [search_obj]

        # String is NoneType. No Regex executed.
        log(trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["morpy"]["regex_find1st_none"]}\n'
                    f'{app_dict["loc"]["morpy"]["regex_find1st_result"]}: {result}')

    return{
        'result' : result
        }


@morpy_wrap
def regex_split(trace: dict, app_dict: dict, search_obj: object, delimiter: str) -> dict:
    r"""
    Splits the input (converted to a string) into a list of substrings using the specified
    delimiter. Delimiters that are special characters in regex should be escaped appropriately.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to be split (converted to a string).
    :param delimiter: The character or string used to split `search_obj` into a list.
                      Special characters may require a preceding backslash (e.g., '\\.'
                      to use '.' as a delimiter).

    :return: dict
        result: The list of parts split from the input.

    :example:
        string = "apple.orange.banana"
        split = r"\\."
        result = morPy.regex_split(trace, app_dict, string, split)["result"]
    """

    search_string: str = f'{search_obj}'
    delimiter: str = f'{delimiter}'
    result = None

    # Splitting a string by a given delimiter.
    log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_split_init"]}\n'
                f'{app_dict["loc"]["morpy"]["regex_split_delimiter"]}: {delimiter}\n'
                f'search_obj: {search_string}')

    if search_string is not None:

        result = re.split(delimiter, search_string)

        # String has been split.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["regex_split_complete"]}\n'
                    f'{app_dict["loc"]["morpy"]["regex_split_result"]}: {result}')

    else:
        result = [search_obj]

        # String is NoneType. No Split executed.
        log(trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["morpy"]["regex_split_none"]}\n'
                    f'{app_dict["loc"]["morpy"]["regex_split_result"]}: {result}')

    return{
        'result' : result
        }


@morpy_wrap
def regex_replace(trace: dict, app_dict: dict, search_obj: object, search_for: str, replace_by: str) -> dict:
    r"""
    Replaces every occurrence of a regular expression pattern in the input string with a
    provided replacement string, returning the modified string.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object in which to search and replace (converted to a string).
    :param search_for: The regular expression pattern to search for.
    :param replace_by: The character or string to substitute in place of the matches.

    :return: dict
        result: The modified string with substitutions applied.

    :example:
        string = "apple.orange.banana"
        search_for = r"\\."
        replace_by = r"-"
        result = morPy.regex_replace(trace, app_dict, string, search_for, replace_by)["result"]
    """

    search_obj: str = f'{search_obj}'
    search_for: str = f'{search_for}'
    replace_by: str = f'{replace_by}'
    result = None

    # Changing a string by given parameters.
    log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_replace_init"]}\n'
                f'search_for: {search_for}\n'
                f'replace_by: {replace_by}\n'
                f'search_obj: {search_obj}')

    result = re.sub(search_for, replace_by, search_obj)

    # String substituted.
    log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_replace_complete"]}\n'
                f'{app_dict["loc"]["morpy"]["regex_replace_result"]}: {result}')

    return{
        'result' : result
        }


@morpy_wrap
def regex_remove_special(trace: dict, app_dict: dict, inp_string: str, spec_lst: list) -> dict:
    r"""
    Processes the input string to remove or replace special characters according to a list of
    (special, replacement) tuples. If a default list is requested (by specifying an empty tuple),
    a standard set of common special characters is used.

    This function can also perform multiple `regex_replace` actions on the same string,
    as any valid regular expression can be used in the `spec_lst`.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param inp_string: The string to be altered.
    :param spec_lst: A list of 2-tuples defining the special characters to replace and
                     their replacements. Example:
                     [(special1, replacement1), ...]. Use `[('', '')]` to invoke the
                     standard replacement list.

    :return: dict
        result: The modified string with special characters replaced or removed.

    :example:
        my_string: str          = "Hello!@#$%^&*()"
        specials_filter: list   = [("@", "AT"), ("!", "")]
        result = morPy.regex_remove_special(trace, app_dict, my_string, specials_filter)
    """

    inp_string: str = f'{inp_string}'

    # Define the standard special character removal list. The special characters will
    # later be converted to a raw string with repr(). You may use this list as a
    # guideline of how to define special and replacement characters.
    spec_lst_std = [
        (r' ',r''), (r'¤',r''), (r'¶',r''), (r'§',r''), (r'!',r''), (r'\"',r''), (r'#',r''), (r'\$',r''), (r'%',r''),
        (r'&',r''), (r'\'',r''), (r'\(r',r''), (r'\)',r''), (r'\*',r''), (r'\+',r''), (r',r',r''), (r'-',r''),
        (r'\.',r''), (r'/',r''), (r':',r''), (r';',r''), (r'=',r''), (r'>',r''), (r'<',r''), (r'\?',r''), (r'@',r''),
        (r'\[',r''), (r'\]',r''), (r'\\\\',r''), (r'\^',r''), (r'_',r''), (r'`',r''), (r'´',r''), (r'{',r''),
        (r'}',r''), (r'\|',r''), (r'~',r'')
    ]

    # Evaluate the length of spec_lst
    lst_len = len(spec_lst)

    # If specials were not specified, default to full collection.
    if spec_lst[0] == ('','') and lst_len < 2:
        spec_lst = spec_lst_std

    # Removing special characters of a string and replacing them.
    log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_remove_special_init"]}\n'
                f'inp_string: {inp_string}\n'
                f'spec_lst: {spec_lst}')

    # Loop through the tuples list and remove/replace characters of the
    # input string
    for tpl in spec_lst:
        # Perform search/replace
        inp_string = re.sub(f'{tpl[0]}', f'{tpl[1]}', inp_string)

    # String substituted.
    log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_remove_special_complete"]}\n'
                f'inp_string: {inp_string}\n'
                f'{app_dict["loc"]["morpy"]["regex_remove_special_result"]}: {inp_string}')

    return{
        'result' : inp_string
        }


@morpy_wrap
def textfile_write(trace: dict, app_dict: dict, filepath: str, content: str) -> None:
    r"""
    Appends text content to a specified file. If the file does not exist, it is created.
    The content is converted to a string as needed.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param filepath: Path to the text file, including its name and file extension.
    :param content: The content to be written to the file, converted to a string if necessary.

    :example:
        morPy.textfile_write(trace, app_dict, "path/to/file.txt", "This is some text.")
    """

    content: str = f'{content}'
    filepath = os.path.abspath(filepath)

    # Append to a textfile
    if os.path.isfile(filepath):
        with open(filepath, 'a') as ap:
            ap.write(f'\n{content}')

        # Textfile has been appended to.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["textfile_write_appended"]}\n'
                    f'{app_dict["loc"]["morpy"]["textfile_write_content"]}: {content}')

    # Create and write a textfile
    else:
        with open(filepath, 'w') as wr:
            wr.write(content)

        # Textfile has been created.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["textfile_write_created"]}\n'
                    f'{app_dict["loc"]["morpy"]["textfile_write_content"]}: {content}')


@morpy_wrap
def qrcode_generator_wifi(trace: dict, app_dict: dict, ssid: str = None, password: str = None,
                          file_path: str = None, file_name: str = None, overwrite: bool = True) -> None:
    r"""
    Generates a QR code that encodes Wi‑Fi network credentials (SSID and WPA2 password) to allow easy
    network connection via scanning. The QR code is saved as a PNG file in a specified directory
    (defaulting to ‘./data’), and by default will overwrite any existing file with the same name.
    (It is recommended not to hardcode passwords in source code.)

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param ssid: Name of the Wi-Fi network.
    :param password: WPA2 password of the network. Consider handing the password via prompt instead
        of in code for better security.
    :param file_path: Path where the qr-code generated will be saved. If None, save in '.\data'.
    :param file_name: Name of the file without file extension (always PNG). Default to '.\qrcode.png'.
    :param overwrite: If False, will not overwrite existing files. Defaults to True.

    :example:
        # Never save a password in the source code!
        morPy.qrcode_generator_wifi(trace, app_dict,
            ssid="ExampleNET",
            password="3x4mp13pwd"
        )
    """

    import os
    import qrcode

    generate: bool = True

    # Check given filepath and eventually default to .\data
    check_file_path: bool = morpy_fct.pathtool(file_path)["dir_exists"]
    with morPy.conditional_lock(app_dict["morpy"]["conf"]):
        file_path = file_path if check_file_path else app_dict["morpy"]["conf"]["data_path"]

    # Default file name if needed
    file_name = f'{file_name}.png' if file_name else "qrcode.png"

    # Construct full path
    full_path = os.path.join(file_path, file_name)

    # Check, if file exists and delete existing, if necessary.
    file_exists: bool = morpy_fct.pathtool(file_path)["file_exists"]
    if file_exists:
        if overwrite:
            fso_delete_file(trace, app_dict, full_path)
        else:
            generate = False

    # Generate and save the QR code
    if generate:
        wifi_config = f'WIFI:S:{ssid};T:WPA;P:{password};;'
        img = qrcode.make(wifi_config)
        img.save(full_path)

    # QR code generated and saved.
    log(trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["morpy"]["qrcode_generator_wifi_done"]}\n'
                f'{ssid=}\n{full_path=}')


@morpy_wrap
def wait_for_input(trace: dict, app_dict: dict, message: str) -> dict:
    r"""
    Pauses execution until the user provides input at a command‑line prompt. The supplied message
    is displayed, and the user input (always returned as a string) is captured.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param message: The text to be displayed as a prompt before user input.

    :return: dict
        usr_input: The input provided by the user.

    :example:
        prompt = "Please enter your name: "
        result = morPy.wait_for_input(trace, app_dict, prompt)["usr_input"]
    """

    # Set global interrupt
    interrupt(trace, app_dict)

    # user input
    usr_input = input(f'{message}\n')

    # A user input was made.
    log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["wait_for_input_complete"]}\n'
                f'{app_dict["loc"]["morpy"]["wait_for_input_message"]}: {message}\n'
                f'{app_dict["loc"]["morpy"]["wait_for_input_usr_inp"]}: {usr_input}')

    return{
        'usr_input' : usr_input
        }


@morpy_wrap
def wait_for_select(trace: dict, app_dict: dict, message: str, collection: tuple=None) -> dict:
    r"""
    Prompts the user for input that must match one of the elements in a provided tuple. If the
    entered input is invalid, the prompt is repeated (or the process is aborted) until a valid
    option is selected.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param message: The text to be displayed as a prompt before user input.
    :param collection: Tuple, that holds all valid user input options. If None,
        evaluation will be skipped.

    :return: dict
        usr_input: The input provided by the user.

    :example:
        msg_text = "Select 1. this or 2. that"
        collection = (1, 2)
        result = morPy.wait_for_select(trace, app_dict, msg_text, collection)["usr_input"]
    """

    # Set global interrupt
    interrupt(trace, app_dict)

    # user input
    usr_input = input(f'{message}\n')

    if collection:
        # Make collection 'str'
        collection = tuple(map(str, collection))

        while usr_input not in collection:
            # Invalid selection. Repeat?
            rep = (
                f'{app_dict["loc"]["morpy"]["wait_for_select_selection_invalid"]}\n'
                f'[{app_dict["loc"]["morpy"]["wait_for_select_yes_selector"]}] '
                f'{app_dict["loc"]["morpy"]["wait_for_select_yes"]} | '
                f'[{app_dict["loc"]["morpy"]["wait_for_select_quit_selector"]}] '
                f'{app_dict["loc"]["morpy"]["wait_for_select_quit"]}'
            )
            usr_response = input(f'{rep}\n')

            if usr_response == "y":
                usr_input = input(f'{message}\n')
            elif usr_response == "q":
                with morPy.conditional_lock(app_dict["morpy"]["orchestrator"]):
                    app_dict["morpy"]["orchestrator"]["terminate"] = True
                    break
            else:
                pass

    # A user input was made.
    log(trace, app_dict, "debug",
    lambda: f'{app_dict["loc"]["morpy"]["wait_for_select_complete"]}\n'
            f'{app_dict["loc"]["morpy"]["wait_for_select_message"]}: {message}\n'
            f'{app_dict["loc"]["morpy"]["wait_for_select_usr_inp"]}: {usr_input}')

    return{
        'usr_input' : usr_input
        }