# MorPyDict Development

## Your Task

Analyse the code provided below and figure out where the RecursionError originates from. The error only ever occurs in multiprocessing mode. If I stick to a single process, regardless of initializing `app_dict` as a standard dict or UltraDict, the error does not appear. I suspect a logical flaw of mine in either `lib.init`, `lib.mp` or both. The root cause may stem from something else, however.

## The Error / Console Messages

```
CRITICAL - 2025-04-02_122854
	Line 516 in module 'lib.mp'
	RecursionError: maximum recursion depth exceeded
```

## Your Methodology

Analyze the Python code provided below. You are supposed to walk through the code chronologically as it would be executed.

All of this is to identify the root cause of the problem described above. Start with `__main__.py` and follow the code line by line to identify it. 

You may study this [SuperFastPython Guide](https://superfastpython.com/multiprocessing-in-python/) to get inspiration.

## __main__.py

```Python
r"""
Author: Bastian Neuwirth, https://www.supermorph.tech/
Date: 28.08.2024
Version: 1.0.0c

TODO IN PROGRESS
- Unit tests
    > common.py | common_test.py

TODO improve error handling to be specific, rather than excessive/graceful

TODO Finish multiprocessing with shared memory
    > consider subprocess library
    > make app_dict flat under the hood, if GIL

TODO Threading orchestrator: 1 for logs, 1 for dequeue, 1 for app_dict
TODO Interrupt and exit overhaul
    - provide function to check for interrupt/exit
    - interrupt when logging: move from mp to the log decorator
    - exit option to log decorator
    - Provide an exit if CRITICAL and dump app_dict and priority queue, offer to pick up on it next restart

TODO define dependencies in one of the supported manifest file types, like package.json or Gemfile.
    > This will enable GitHub to show a dependency graph

TODO make use of the "with" statement
    > Optimize own classes to be supported by with (i.e. __exit__() methods)

TODO class/instantiate logging and sqlite3
TODO class/instantiate file operations

TODO use pyinstaller to generate standalone application
    > specify application icon
    pyinstaller --icon=bulb.ico myscript.py
"""

from lib.exceptions import MorPyException

import sys

init_check: bool = False

def initialize_morpy():
    r"""
    Initialize the morPy framework.
    """

    init_check: bool = False

    try:
        from lib import init
        morpy_trace: dict = init.init_cred()
        app_dict, orchestrator = init.init(morpy_trace)

        if app_dict and orchestrator:
            init_check: bool = True
        return morpy_trace, app_dict, orchestrator, init_check

    except Exception as e:
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

def main(morpy_trace, app_dict, orchestrator):
    r"""
    Run morPy.
    """
    orchestrator._run(morpy_trace, app_dict)

def finalize_morpy(morpy_trace, app_dict):
    r"""
    Finalize morPy components.
    """

    import lib.exit as exit
    exit._exit(morpy_trace, app_dict)

    # Quit the program
    sys.exit()

if __name__ == '__main__':
    try:
        morpy_trace, app_dict, orchestrator, init_check = initialize_morpy()
        main(morpy_trace, app_dict, orchestrator)
    except Exception as e:
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")
    finally:
        try:
            finalize_morpy(morpy_trace, app_dict)
        except Exception as e:
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")
```

## lib.common.py

```Python
r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Module of generally useful functions.
"""

import lib.fct as morpy_fct
import lib.mp as mp
from lib.decorators import metrics, log

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
    This class delivers a priority queue solution. Any task may be enqueued.
    When dequeuing, the highest priority task (lowest number) is pulled
    first. In case there is more than one, the oldest is pulled.

    :param morpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param name: Name or description of the instance

    :methods:
        .enqueue(morpy_trace: dict, app_dict: dict, priority: int=100, task: tuple=None, autocorrect: bool=True,
            is_process: bool=True)
            Adds a task to the priority queue.

            :param priority: Integer representing task priority (lower is higher priority)
            :param task: Tuple of a callable, *args and **kwargs (func, *args, **kwargs)
            :param autocorrect: If False, priority can be smaller than zero. Priority
                smaller zero is reserved for the morPy Core.
            :param is_process: If True, task is run in a new process (not by morPy orchestrator)

        .pull(morpy_trace: dict, app_dict: dict)
            Removes and returns the highest priority task from the priority queue.

            :return: dict
                priority: Integer representing task priority (lower is higher priority)
                counter: Number of the task when enqueued
                task_id : Continuously incremented task ID (counter).
                task_sys_id : ID of the task determined by Python core
                task: The pulled task list
                task_callable: The pulled task callable
                is_process: If True, task is run in a new process (not by morPy orchestrator)

    :example:
        from functools import partial
        # Create queue instance
        queue = morPy.PriorityQueue(morpy_trace, app_dict, name="example_queue")
        # Add a task to the queue
        queue.enqueue(morpy_trace, app_dict, priority=25, task=partial(task, morpy_trace, app_dict))
        # Fetch a task and run it
        task = queue.pull(morpy_trace, app_dict)['task']
        task()
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, name: str=None) -> None:
        r"""
        In order to get metrics for __init__(), call helper method _init() for
        the @metrics decorator to work. It relies on the returned
        {'morpy_trace' : morpy_trace}, which __init__() can not do (needs to be None).

        :param: See ._init() for details

        :return: self

        :example:
            queue = PriorityQueue(morpy_trace, app_dict, name="example_queue")
        """

        module: str = 'lib.common'
        operation: str = 'PriorityQueue.__init__(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        try:
            # Use _init() for initialization to apply @metrics
            self._init(morpy_trace, app_dict, name)

        except Exception as e:
            from lib.exceptions import MorPyException

            err_msg = f'{app_dict["loc"]["morpy"]["PriorityQueue_name"]}: {self.name}'
            raise MorPyException(
                morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical",
                message=err_msg
            )

    @metrics
    def _init(self, morpy_trace: dict, app_dict: dict, name: str) -> dict:
        r"""
        Helper method for initialization to ensure @metrics decorator functionality.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param name: Name or description of the instance

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module: str = 'lib.common'
        operation: str = 'PriorityQueue._init(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            self.name = name if name else 'queue'
            self.heap = []
            self.counter = 0 # Task counter. Starts at 0, increments by 1
            self.task_lookup = set() # Set for quick task existence check

            # Priority queue initialized.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_init_done"]}\n'
                    f'{app_dict["loc"]["morpy"]["PriorityQueue_name"]}: {self.name}')

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException

            err_msg = f'{app_dict["loc"]["morpy"]["PriorityQueue_name"]}: {self.name}'
            raise MorPyException(
                morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical",
                message=err_msg
            )

        return {
            'morpy_trace': morpy_trace,
            'check': check
        }

    @metrics
    def enqueue(self, morpy_trace: dict, app_dict: dict, priority: int=100, task: tuple=None) -> dict:
        r"""
        Adds a task to the priority queue.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param priority: Integer representing task priority (lower is higher priority)
        :param task: Tuple of a callable, *args and **kwargs (func, *args, **kwargs)

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates if the task was enqueued successfully

        :example:
            from functools import partial
            queue = PriorityQueue(morpy_trace, app_dict, name="example_queue")
            task = partial(my_func, morpy_trace, app_dict)
            queue.enqueue(morpy_trace, app_dict, priority=25, task=task)
        """

        module: str = 'lib.common'
        operation: str = 'PriorityQueue.enqueue(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            if task:
                # Pushing task to priority queue.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_enqueue_start"]} {self.name}\n'
                        f'{app_dict["loc"]["morpy"]["PriorityQueue_enqueue_priority"]}: {priority}')

                # Increment task counter
                self.counter += 1

                task_sys_id = id(task)

                # Check, if ID already in queue
                if task_sys_id in self.task_lookup:
                    # Task is already enqueued. Referencing in queue.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_enqueue_task_duplicate"]}\n'
                            f'Task system ID: {task_sys_id}')
                else:
                    self.task_lookup.add(task_sys_id)

                # Push task to queue
                task_qed = (priority, self.counter, task_sys_id, task)
                heappush(self.heap, task_qed)

                check: bool = True
            else:
                # Task can not be None. Skipping enqueue.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_enqueue_none"]}')

        except Exception as e:
            from lib.exceptions import MorPyException

            err_msg = (
                f'{app_dict["loc"]["morpy"]["PriorityQueue_name"]}: {self.name}\n'
                f'{app_dict["loc"]["morpy"]["PriorityQueue_enqueue_priority"]}: {priority}'
            )
            raise MorPyException(
                morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical",
                message=err_msg
            )

        return {
            'morpy_trace': morpy_trace,
            'check': check
        }

    @metrics
    def pull(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Removes and returns the highest priority task from the priority queue.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates if the task was pulled successfully
            priority: Integer representing task priority (lower is higher priority)
            counter: Number of the task when enqueued
            task_id : Continuously incremented task ID (counter).
            task_sys_id : ID of the task determined by Python core
            task: The pulled task list
            task_callable: The pulled task callable

        :example:
            from functools import partial
            queue = PriorityQueue(morpy_trace, app_dict, name="example_queue")
            task = queue.pull(morpy_trace, app_dict)['task']
            task()
        """

        module: str = 'lib.common'
        operation: str = 'PriorityQueue.pull(~)'
        morpy_trace_pull = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        priority = None
        counter = None
        task_sys_id = None
        task = None

        try:
            # Global interrupt - wait for error handling
            while app_dict["morpy"].get("interrupt", False):
                pass

            if len(self.heap) > 0:
                task_dqed = heappop(self.heap)
                priority, counter, task_sys_id, task = task_dqed

                # Pulling task from NAME priority: INT counter: INT
                log(morpy_trace_pull, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_pull_start"]} {self.name}.\n'
                        f'{app_dict["loc"]["morpy"]["PriorityQueue_pull_priority"]}: {priority}\n'
                        f'{app_dict["loc"]["morpy"]["PriorityQueue_pull_cnt"]}: {counter}',
                        verbose = True)

                check: bool = True

            else:
                # Can not pull from an empty priority queue. Skipped...
                log(morpy_trace_pull, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["PriorityQueue_pull_void"]}')

        except Exception as e:
            from lib.exceptions import MorPyException

            err_msg = f'{app_dict["loc"]["morpy"]["PriorityQueue_name"]}: {self.name}'
            raise MorPyException(
                morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error",
                message=err_msg
            )

        return {
            'morpy_trace': morpy_trace_pull,
            'check': check,
            'priority' : priority,
            'counter' : counter,
            'task_id' : morpy_trace["task_id"],
            'task_sys_id' : task_sys_id,
            'task': list(task)
        }

class ProgressTracker:
    r"""
    This class instantiates a progress counter. If ticks, total or counter
    are floats, progress of 100 % may not be displayed.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param description: Describe, what is being processed (i.e. file path or calculation)
    :param total: Mandatory - The total count for completion
    :param ticks: Mandatory - Percentage of total to log the progress. I.e. at ticks=10.7 at every
        10.7% progress exceeded the exact progress will be logged.
    :param float_progress: For efficient progress tracking, by default the progress is not tracked with
        floats. If True, the amount of ticks at which to update progress may be a lot more expensive.
        Defaults to False.
    :param verbose: If True, progress is only logged in verbose mode except for the 100% mark. Defaults to False.

    .update(morpy_trace: dict, app_dict: dict, current: float=None)
        Method to update current progress and log progress if tick is passed.

        :return: dict
            prog_rel: Relative progress, float between 0 and 1
            message: Message generated. None, if no tick was hit.

    :example:
        from morPy import ProgressTracker
        progress = ProgressTracker(morpy_trace, app_dict, description='App Progress', total=total_count, ticks=10)["prog_rel"]
        progress.update(morpy_trace, app_dict, current=current_count)
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, description: str=None, total: float=None, ticks: float=None,
                 float_progress: bool=False, verbose: bool=False) -> None:
        r"""
        In order to get metrics for __init__(), call helper method _init() for
        the @metrics decorator to work. It relies on the returned
        {'morpy_trace' : morpy_trace}, which __init__() can not do (needs to be None).

        :param: See ._init() for details

        :return:
            -

        :example:
            progress = ProgressTracker(morpy_trace, app_dict, description='App Progress', total=100, ticks=10)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.common'
        operation: str = 'ProgressTracker.__init__(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        try:
            # Use self._init() for initialization
            self._init(morpy_trace, app_dict, description=description, total=total, ticks=ticks,
                       float_progress=float_progress, verbose=verbose)

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    @metrics
    def _init(self, morpy_trace: dict, app_dict: dict, description: str=None, total: float=None, ticks: float=None,
              float_progress: bool=False, verbose: bool=False) -> dict:
        r"""
        Helper method for initialization to ensure @metrics decorator usage.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param description: Describe, what is being processed (i.e. file path or calculation)
        :param total: Mandatory - The total count for completion
        :param ticks: Mandatory - Percentage of total to log the progress. I.e. at ticks=10.7 at every
            10.7% progress exceeded the exact progress will be logged. If None or greater 100, will default to 10.
        :param float_progress: For efficient progress tracking, by default the progress is not tracked with
            floats. If True, the amount of ticks at which to update progress may be a lot more expensive.
            Defaults to False.
        :param verbose: If True, progress is only logged in verbose mode except for the 100% mark. Defaults to False.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._init(morpy_trace, app_dict, description=description, total=total, ticks=ticks)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.common'
        operation: str = 'ProgressTracker._init(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
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
            if not verbose or verbose and app_dict["conf"]["msg_verbose"]:
                self.verbose_check = True
            else:
                self.verbose_check = False

            # Determine absolute progress ticks
            self._init_ticks(morpy_trace, app_dict)

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            }

    @metrics
    def _init_ticks(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        This method determines the ticks, at which to log the progress.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._init_ticks(morpy_trace, app_dict)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.common'
        operation: str = 'ProgressTracker._init_ticks(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
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

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            }

    @metrics
    def update(self, morpy_trace: dict, app_dict: dict, current: float=None) -> dict:
        r"""
        Method to update current progress and log progress if tick is passed.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors
            prog_rel: Relative progress, float between 0 and 1
            prog_abs: Absolute progress, float between 0.00 and 100.00
            message: Message generated. None, if no tick was hit.

        :example:
            import morPy

            tot_cnt = 100
            tks = 12.5
            progress = morPy.ProgressTracker(morpy_trace, app_dict, description='App Progress', total=total_count, ticks=tks)

            curr_cnt = 37
            progress.update(morpy_trace, app_dict, current=curr_cnt)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.common'
        operation: str = 'ProgressTracker.update(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        prog_rel = None
        prog_abs_short = None
        message = None

        try:
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
                    log(morpy_trace, app_dict, "warning",
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
                    if self.verbose_check or self.done:
                        # Processing DESCRIPTION
                        log(morpy_trace, app_dict, "info",
                        lambda: f'{app_dict["loc"]["morpy"]["ProgressTracker_proc"]}: {self.description}\n'
                                f'{prog_abs_short}% ({self.update_counter} of {self.total})')

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            'prog_rel' : prog_rel,
            'prog_abs' : prog_abs_short,
            'message' : message
            }

@metrics
def decode_to_plain_text(morpy_trace: dict, app_dict: dict, src_input, encoding: str='') -> dict:
    r"""
    This function decodes different types of data and returns
    a plain text to work with in python. The return result behaves
    like using the open(file, 'r') method.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param src_input: Any kind of data to be decoded. Binary expected.
    :param encoding: String that defines encoding. Leave empty to auto-detect.

    :return: dict
        check: Indicates whether the function executed successfully (True/False).
        morpy_trace: Operation credentials and tracing.
        result: Decoded result. Buffered object that may be used with the readlines() method.
        encoding: String containing the encoding of src_input.
        lines: Number of lines in the file.

    :example:
        src_file = "C:\my_file.enc"
        src_input = open(src_file, 'rb')
        encoding: str = 'utf-16-le'
        retval = decode_to_plain_text(morpy_trace, app_dict, src_input, encoding)
    """

    module: str = 'lib.common'
    operation: str = 'decode_to_plain_text(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    result = None
    decode = False
    lines = 0

    try:
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
                log(morpy_trace, app_dict, "warning",
                lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                        f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                        f'{app_dict["loc"]["morpy"]["decode_to_plain_text_msg"]}: {e}')

        # Validate provided encoding
        else:
            try:
                encoding_val = chardet.detect(src_copy)["encoding"]
                decode = True

            # Not encoded if an exception is raised
            except:
                # Validation of encoding failed.
                raise RuntimeError(f'{app_dict["loc"]["morpy"]["decode_to_plain_text_val_fail"]}')

        # Decode the content
        if decode:
            result = io.StringIO(src_copy.decode(encoding))

            # Decoded from ### to plain text.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["decode_to_plain_text_from"]} {encoding}) '
                    f'{app_dict["loc"]["morpy"]["decode_to_plain_text_to"]}\n'
                    f'encoding: {encoding}')

            check: bool = True

        # Handle unsupported or non-encoded input
        else:
            result = io.StringIO(src_copy.decode('utf-8', errors='ignore'))

            # The Input is not decoded or not supported. No action taken.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["decode_to_plain_text_not"]}\n'
                f'encoding: {encoding}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return {
        'morpy_trace': morpy_trace,
        'check' : check,
        'result': result,
        'encoding': encoding,
        'lines': lines,
    }

@metrics
def fso_copy_file(morpy_trace: dict, app_dict: dict, source: str, dest: str, overwrite: bool=False) -> dict:
    r"""
    Copies a single file from the source to the destination. Includes a file
    check to ensure the operation's validity.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param source: Complete path to the source file, including the file extension.
    :param dest: Complete path to the destination file, including the file extension.
    :param overwrite: Boolean indicating if the destination file may be overwritten. Defaults to False.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        source: Path to the source file as a path object.
        dest: Path to the destination file as a path object.

    :example:
        result = fso_copy_file(morpy_trace, app_dict, "path/to/source.txt", "path/to/destination.txt", True)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'fso_copy_file(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
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
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["fso_copy_file_copy_ovwr"]}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_source"]}: {source}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_dest"]}: {dest}\n'
                        f'dest_exist: {dest_exist}\n'
                        f'ovwr_perm: {overwrite}')

            # Evaluate the existence of the destination and overwrite permission
            if dest_exist and not overwrite:

                shutil.copyfile(source, dest)

                # A file was not copied because it already exists and no overwrite permission was given.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["fso_copy_file_copy_not_ovwr"]}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_source"]}: {source}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_dest"]}: {dest}\n'
                        f'dest_exist: {dest_exist}\n'
                        f'ovwr_perm: {overwrite}')

            if dest_exist:

                shutil.copyfile(source, dest)

                # A file has been copied.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["fso_copy_file_copy"]}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_source"]}: {source}\n'
                        f'{app_dict["loc"]["morpy"]["fso_copy_file_dest"]}: {dest}')

            check: bool = True

        else:
            # A file could not be copied, because it does not exist.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_copy_file_not_exist"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_copy_file_source"]}: {source}\n'
                    f'{app_dict["loc"]["morpy"]["fso_copy_file_dest"]}: {dest}\n'
                    f'source_exist: {source_exist}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'source' : source,
        'dest' : dest
        }

@metrics
def fso_create_dir(morpy_trace: dict, app_dict: dict, mk_dir: str) -> dict:
    r"""
    Creates a directory and its parent directories recursively.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param mk_dir: Path to the directory or directory tree to be created.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        result = fso_create_dir(morpy_trace, app_dict, "path/to/new_directory")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'fso_create_dir(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # Check the directory
        dir_eval = morpy_fct.pathtool(mk_dir)
        dir_exist = dir_eval["dir_exists"]
        mk_dir = dir_eval["out_path"]

        if dir_exist:
            # The directory already exists.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_create_dir_not_created"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_create_dir_directory"]}: {mk_dir}\n'
                    f'{app_dict["loc"]["morpy"]["fso_create_dir_direxist"]}: {dir_exist}')

        else:
            os.makedirs(mk_dir)

            # The directory has been created.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_create_dir_created"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_create_dir_directory"]}: {mk_dir}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check
        }

@metrics
def fso_delete_dir(morpy_trace: dict, app_dict: dict, del_dir: str) -> dict:
    r"""
    Deletes an entire directory, including its contents. A directory check
    is performed before deletion.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param del_dir: Path to the directory to be deleted.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        result = fso_delete_dir(morpy_trace, app_dict, "path/to/directory_to_delete")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'fso_delete_dir(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # Check the directory
        dir_eval = morpy_fct.pathtool(del_dir)
        dir_exist = dir_eval["dir_exists"]
        del_dir = dir_eval["out_path"]

        if dir_exist:

            shutil.rmtree(del_dir)

            # The directory has been deleted.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_delete_dir_deleted"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_create_dir_directory"]}: {del_dir}')

        else:
            # The directory does not exist.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_delete_dir_notexist"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_create_dir_directory"]}: {del_dir}\n'
                    f'{app_dict["loc"]["morpy"]["fso_delete_dir_direxist"]}: {dir_exist}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check
        }

@metrics
def fso_delete_file(morpy_trace: dict, app_dict: dict, del_file: str) -> dict:
    r"""
    Deletes a file. Will check path before deletion.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param del_file: Path to the file to be deleted.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        result = fso_delete_file(morpy_trace, app_dict, "path/to/file_to_delete.txt")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'fso_delete_file(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # Check the directory
        file_eval = morpy_fct.pathtool(del_file)
        file_exist = file_eval["file_exists"]
        del_file = file_eval["out_path"]

        if file_exist:

            os.remove(del_file)

            # The file has been deleted.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_delete_file_deleted"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_delete_file_file"]}: {del_file}')

        else:
            # The file does not exist.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_delete_file_notexist"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_delete_file_file"]}: {del_file}\n'
                    f'{app_dict["loc"]["morpy"]["fso_delete_file_exist"]}: {file_exist}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check
        }

@metrics
def fso_walk(morpy_trace: dict, app_dict: dict, path: str, depth: int=1) -> dict:
    r"""
    Returns the contents of a directory.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param path: Path to the directory to be analyzed.
    :param depth: Limits the depth of the analysis. Defaults to 1. Examples:
                  -1: No limit.
                   0: Path only.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
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
        result = fso_walk(morpy_trace, app_dict, "path/to/directory", -1)["walk_dict"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'fso_delete_file(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    walk_dict: dict = {}
    cnt_roots: int = 0

    try:
        # Check the directory
        if morpy_fct.pathtool(path)["dir_exists"]:
            for root, dirs, files in os.walk(path):
                # Exit if depth is reached
                if cnt_roots > depth:
                    break

                walk_dict.update({f'root{cnt_roots}' : {'root' : root, 'dirs' : dirs, 'files' : files}})
                cnt_roots += 1

            # Directory analyzed.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_walk_path_done"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_walk_path_dir"]}: {path}')

        else:
            # The directory does not exist.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["fso_walk_path_notexist"]}\n'
                    f'{app_dict["loc"]["morpy"]["fso_walk_path_dir"]}: {path}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'walk_dict' : walk_dict
        }

@metrics
def regex_findall(morpy_trace: dict, app_dict: dict, search_obj: object, pattern: str) -> dict:
    r"""
    Searches for a regular expression in a given object and returns a list of found expressions.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        result: List of expressions found in the input, or None if nothing was found.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = regex_findall(morpy_trace, app_dict, string, pattern)["result"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'regex_findall(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check =False
    search_obj: str = f'{search_obj}'
    pattern: str = f'{pattern}'
    result = None

    # Searching for regular expressions.
    log(morpy_trace, app_dict, "debug",
    lambda: f'{app_dict["loc"]["morpy"]["regex_findall_init"]}\n'
            f'{app_dict["loc"]["morpy"]["regex_findall_pattern"]}: {pattern}\n'
            f'search_obj: {search_obj}')

    try:
        # Search for the pattern
        result_matches = re.findall(pattern, search_obj)
        result = result_matches if result_matches else None

        # Search completed.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_findall_compl"]}\n'
                f'{app_dict["loc"]["morpy"]["regex_findall_result"]}: {result}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'result' : result
        }

@metrics
def regex_find1st(morpy_trace: dict, app_dict: dict, search_obj: object, pattern: str) -> dict:
    r"""
    Searches for a regular expression in a given object and returns the first match.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        result: The first match found in the input, or None if nothing was found.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = regex_find1st(morpy_trace, app_dict, string, pattern)["result"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'regex_find1st(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    search_string: str = f'{search_obj}'
    pattern: str = f'{pattern}'
    result = None

    try:
        # Searching for regular expressions.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_find1st_init"]}\n'
                f'{app_dict["loc"]["morpy"]["regex_find1st_pattern"]}: {pattern}\n'
                f'search_obj: {search_string}')

        if search_string is not None:

            result_match = re.search(pattern, search_string)
            result = result_match.group() if result_match else None

            # Search completed.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["regex_find1st_compl"]}\n'
                    f'{app_dict["loc"]["morpy"]["regex_find1st_result"]}: {result}')

            check: bool = True

        else:
            result = [search_obj]

            # String is NoneType. No Regex executed.
            log(morpy_trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["morpy"]["regex_find1st_none"]}\n'
                    f'{app_dict["loc"]["morpy"]["regex_find1st_result"]}: {result}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'result' : result
        }

@metrics
def regex_split(morpy_trace: dict, app_dict: dict, search_obj: object, delimiter: str) -> dict:
    r"""
    Splits an object into a list using a given delimiter.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to be split (converted to a string).
    :param delimiter: The character or string used to split `search_obj` into a list.
                      Special characters may require a preceding backslash (e.g., '\\.'
                      to use '.' as a delimiter).

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        result: The list of parts split from the input.

    :example:
        string = "apple.orange.banana"
        split = r"\\."
        result = regex_split(morpy_trace, app_dict, string, split)["result"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'regex_split(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    search_string: str = f'{search_obj}'
    delimiter: str = f'{delimiter}'
    result = None

    try:
        # Splitting a string by a given delimiter.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_split_init"]}\n'
                f'{app_dict["loc"]["morpy"]["regex_split_delimiter"]}: {delimiter}\n'
                f'search_obj: {search_string}')

        if search_string is not None:

            result = re.split(delimiter, search_string)

            # String has been split.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["regex_split_compl"]}\n'
                    f'{app_dict["loc"]["morpy"]["regex_split_result"]}: {result}')

            check: bool = True

        else:
            result = [search_obj]

            # String is NoneType. No Split executed.
            log(morpy_trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["morpy"]["regex_split_none"]}\n'
                    f'{app_dict["loc"]["morpy"]["regex_split_result"]}: {result}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'result' : result
        }

@metrics
def regex_replace(morpy_trace: dict, app_dict: dict, search_obj: object, search_for: str, replace_by: str) -> dict:
    r"""
    Substitutes characters or strings in an input object based on a regular expression.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object in which to search and replace (converted to a string).
    :param search_for: The regular expression pattern to search for.
    :param replace_by: The character or string to substitute in place of the matches.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        result: The modified string with substitutions applied.

    :example:
        string = "apple.orange.banana"
        search_for = r"\\."
        replace_by = r"-"
        result = regex_replace(morpy_trace, app_dict, string, search_for, replace_by)["result"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'regex_replace(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    search_obj: str = f'{search_obj}'
    search_for: str = f'{search_for}'
    replace_by: str = f'{replace_by}'
    result = None

    try:
        # Changing a string by given parameters.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_replace_init"]}\n'
                f'search_for: {search_for}\n'
                f'replace_by: {replace_by}\n'
                f'search_obj: {search_obj}')

        result = re.sub(search_for, replace_by, search_obj)

        # String substituted.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_replace_compl"]}\n'
                f'{app_dict["loc"]["morpy"]["regex_replace_result"]}: {result}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'result' : result
        }

@metrics
def regex_remove_special(morpy_trace: dict, app_dict: dict, inp_string: str, spec_lst: list) -> dict:
    r"""
    Removes or replaces special characters in a given string. The `spec_lst` parameter
    specifies which characters to replace and their replacements. If no replacement is
    specified, a standard list is used to remove special characters without substitution.

    This function can also perform multiple `regex_replace` actions on the same string,
    as any valid regular expression can be used in the `spec_lst`.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param inp_string: The string to be altered.
    :param spec_lst: A list of 2-tuples defining the special characters to replace and
                     their replacements. Example:
                     [(special1, replacement1), ...]. Use `[('', '')]` to invoke the
                     standard replacement list.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        result: The modified string with special characters replaced or removed.

    :example:
        result = regex_remove_special(
            morpy_trace, app_dict, "Hello!@#$%^&*()", [("@", "AT"), ("!", "")]
        )
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'regex_remove_special(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    load_std: bool = False
    inp_string: str = f'{inp_string}'
    result = None

    try:
        # Define the standard special character removal list. The special characters will
        # later be converted to a raw string with repr(). You may use this list as a
        # guideline of how to define special and replacement characters.
        spec_lst_std =  [
                        (r' ',r''),
                        (r'¤',r''),
                        (r'¶',r''),
                        (r'§',r''),
                        (r'!',r''),
                        (r'\"',r''),
                        (r'#',r''),
                        (r'\$',r''),
                        (r'%',r''),
                        (r'&',r''),
                        (r'\'',r''),
                        (r'\(r',r''),
                        (r'\)',r''),
                        (r'\*',r''),
                        (r'\+',r''),
                        (r',r',r''),
                        (r'-',r''),
                        (r'\.',r''),
                        (r'/',r''),
                        (r':',r''),
                        (r';',r''),
                        (r'=',r''),
                        (r'>',r''),
                        (r'<',r''),
                        (r'\?',r''),
                        (r'@',r''),
                        (r'\[',r''),
                        (r'\]',r''),
                        (r'\\\\',r''),
                        (r'\^',r''),
                        (r'_',r''),
                        (r'`',r''),
                        (r'´',r''),
                        (r'{',r''),
                        (r'}',r''),
                        (r'\|',r''),
                        (r'~',r'')
                        ]

        # Evaluate the length of spec_lst
        lst_len = len(spec_lst)

        # Invoke the standard set of specials to be removed
        if spec_lst[0] == ('','') and lst_len < 2:

            spec_lst = spec_lst_std
            load_std = True

        # Removing special characters of a string and replacing them.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_remove_special_init"]}\n'
                f'inp_string: {inp_string}\n'
                f'spec_lst: {spec_lst}\n'
                f'load_std: {load_std}')

        # Initialize the resulting string
        result = inp_string

        # Loop through the tuples list and remove/replace characters of the
        # input string
        for tpl in spec_lst:

            # Perform search/replace
            result = re.sub(f'{tpl[0]}', f'{tpl[1]}', result)

        # String substituted.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["regex_remove_special_compl"]}\n'
                f'inp_string: {inp_string}\n'
                f'{app_dict["loc"]["morpy"]["regex_remove_special_result"]}: {result}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'result' : result
        }

@metrics
def textfile_write(morpy_trace: dict, app_dict: dict, filepath: str, content: str) -> dict:
    r"""
    Appends content to a text file, creating the file if it does not already exist.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param filepath: Path to the text file, including its name and file extension.
    :param content: The content to be written to the file, converted to a string if necessary.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        result = textfile_write(morpy_trace, app_dict, "path/to/file.txt", "This is some text.")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'textfile_write(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    content: str = f'{content}'
    filepath = os.path.abspath(filepath)

    try:
        # Append to a textfile
        if os.path.isfile(filepath):

            with open(filepath, 'a') as ap:
                ap.write(f'\n{content}')

            # Textfile has been appended to.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["textfile_write_appended"]}\n'
                    f'{app_dict["loc"]["morpy"]["textfile_write_content"]}: {content}')

        # Create and write a textfile
        else:
            with open(filepath, 'w') as wr:
                wr.write(content)

            # Textfile has been created.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["textfile_write_created"]}\n'
                    f'{app_dict["loc"]["morpy"]["textfile_write_content"]}: {content}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        }

@metrics
def testprint(morpy_trace: dict, app_dict: dict, message: str) -> dict:
    r"""
    Prints any value provided. This function is intended for debugging purposes.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param message: The value to be printed, converted to a string if necessary.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check - The function ended with no errors

    :example:
        testprint(morpy_trace, app_dict, "This is a test value.")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'testprint(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        value: str = f'{message}'
        intype: str = f'{type(message)}'

        print(f'<TEST> value: {value}\n'
              f'<TEST> type: {intype}\n')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        }

@metrics
def qrcode_generator_wifi(morpy_trace: dict, app_dict: dict, ssid: str = None, password: str = None,
                          file_path: str = None, file_name: str = None, overwrite: bool = True) -> dict:
    r"""
    Create a QR-code for a Wifi network. Files will be overwritten by default.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param ssid: Name of the Wifi network.
    :param password: WPA2 password of the network. Consider handing the password via prompt instead
        of in code for better security.
    :param file_path: Path where the qr-code generated will be saved. If None, save in '.\data'.
    :param file_name: Name of the file without file extension (always PNG). Default to '.\qrcode.png'.
    :param overwrite: If False, will not overwrite existing files. Defaults to True.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        from morPy import qrcode_generator_wifi
        qrcode_generator_wifi(morpy_trace, app_dict,
            ssid="ExampleNET",
            password="3x4mp13pwd"
        )
    """

    import os
    import qrcode

    # morPy credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'qrcode_generator_wifi(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    generate: bool = True

    try:
        # Check given filepath and eventually default to .\data
        if file_path:
            check_file_path: bool = morpy_fct.pathtool(file_path)["dir_exists"]
            file_path = file_path if check_file_path else app_dict["conf"]["data_path"]
        else:
            file_path = app_dict["conf"]["data_path"]

        # Default file name if needed
        file_name = f'{file_name}.png' if file_name else "qrcode.png"

        # Construct full path
        full_path = os.path.join(file_path, file_name)

        # Check, if file exists and delete existing, if necessary.
        file_exists: bool = morpy_fct.pathtool(file_path)["file_exists"]
        if file_exists:
            if overwrite:
                fso_delete_file(morpy_trace, app_dict, full_path)
            else:
                generate = False

        # Generate and save the QR code
        if generate:
            wifi_config = f'WIFI:S:{ssid};T:WPA;P:{password};;'
            img = qrcode.make(wifi_config)
            img.save(full_path)

        # QR code generated and saved.
        log(morpy_trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["morpy"]["qrcode_generator_wifi_done"]}\n'
                f'{ssid=}\n{full_path=}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        }

@metrics
def wait_for_input(morpy_trace: dict, app_dict: dict, message: str) -> dict:
    r"""
    Pauses program execution until a user provides input. The input is then
    returned to the calling module. Take note, that the returned user input
    will always be a string.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param message: The text to be displayed as a prompt before user input.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check - The function ended with no errors
        usr_input: The input provided by the user.

    :example:
        result = wait_for_input(morpy_trace, app_dict, "Please enter your name: ")["usr_input"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'wait_for_input(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    usr_input = None

    try:
        # Set global interrupt
        mp.interrupt(morpy_trace, app_dict)

        # user input
        usr_input = input(f'{message}\n')

        # A user input was made.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["wait_for_input_compl"]}\n'
                f'{app_dict["loc"]["morpy"]["wait_for_input_message"]}: {message}\n'
                f'{app_dict["loc"]["morpy"]["wait_for_input_usr_inp"]}: {usr_input}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'usr_input' : usr_input
        }

@metrics
def wait_for_select(morpy_trace: dict, app_dict: dict, message: str, collection: tuple=None) -> dict:
    r"""
    Pauses program execution until a user provides input. The input needs to
    be part of a tuple, otherwise it is repeated or aborted. Take note, that the
    returned user input will always be a string.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param message: The text to be displayed as a prompt before user input.
    :param collection: Tuple, that holds all valid user input options. If None,
        evaluation will be skipped.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check - The function ended with no errors
        usr_input: The input provided by the user.

    :example:
        msg_text = "Select 1. this or 2. that"
        collection = (1, 2)
        result = wait_for_select(morpy_trace, app_dict, msg_text, collection)["usr_input"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.common'
    operation: str = 'wait_for_select(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    usr_input = None

    try:
        # Set global interrupt
        mp.interrupt(morpy_trace, app_dict)

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
                    app_dict["morpy"]["orchestrator"]["terminate"] = True
                    break
                else:
                    pass

        # A user input was made.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["wait_for_select_compl"]}\n'
                f'{app_dict["loc"]["morpy"]["wait_for_select_message"]}: {message}\n'
                f'{app_dict["loc"]["morpy"]["wait_for_select_usr_inp"]}: {usr_input}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'usr_input' : usr_input
        }
```

## lib.conf.py

```Python
r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields all basic parameters of the morPy fork. The
            parameters are meant to be tempered with.

TODO provide as json
"""

def settings(start_time=None):
    r"""
    This function defines the parameters morPy will be run with. These
    parameters are meant to be tinkered with and added on to. Have in mind,
    that the return dictionary eventually needs to be altered. The
    morPy framework is preconfigured to support the change of these parameters
    during runtime, although that may be done within app_dict directly, rather
    than initializing the parameters again. There are exceptions though, which
    are pointed out with ">REINITIALIZE<", as an indicator, that the JSON file
    containing all parameters needs to be updated before a change can have an
    effect. To do so, simply execute param_to_json(~) after altering the
    parameters in app_dict like so:
        app_dict["conf"]['my_param'] = 'my_value'
        param_to_json(morpy_trace, app_dict)

    :param start_time: Datetime stamp of runtime start. Defaults to None.

    :return: dict
        > See through the function for detailed descriptions of every morPy setting.
    """

    import pathlib, os

    r"""
>>> LOCALIZATION <<<
    """

    # Choose the language of the app (See ...\loc\ for available dictionaries).
    # Called by: init.init(~)
    language: str = 'en_US'

    r"""
>>> PRIVILEGES <<<
    """

    # Defines, whether elevated privileges are required.
    # Called by: init.init(~)
    mpy_priv_required: bool = False

    r"""
>>> LOGGING & DEBUGGING <<<
    Log Levels: init, debug, info, warning, denied, error, critical, exit, undefined
    """

    # Enable logging. If log_db_enable and log_txt_enable both are set false,
    # then log_enable will be overwritten to be False in init.init(~). Log messages
    # may still be printed to console.
    # Called by: init.init(~)
    log_enable: bool = True

    # Store the initialized system parameters relevant to a developer in a text file.
    # This is for checking initialized app_dict prior to app execution.
    # Called by: init.mpy_ref(~)
    ref_create: bool = False

    # Enable logging to database.
    # Called by: msg.log(~)
    log_db_enable: bool = True

    # Enable logging to a textfile.
    # Called by: msg.log(~)
    log_txt_enable: bool = False

    # Enable the prepared header for the logging textfile.
    # Called by: init.init(~)
    log_txt_header_enable = log_txt_enable

    # Enable printouts of logs to console. This option works, even if log_enable is false.
    # Called by: throughout msg operations
    msg_print: bool = True

    # Activate verbose logging/printing. This means, that the full log message will contain technical
    # data helpful for tracing and context. This option comes with additional storage requirement
    # for logging. If logging to db is activated, there is no need for this option, as all
    # relevant data is stored in the db. When logging to textfile, verbose messages are the only way
    # to get a detailed context of a log message.
    msg_verbose: bool = False

    # Print the initialized app dictionary to console.
    # Called by: init.init(~)
    print_init_vars: bool = False

    # List object to exclude certain log levels from being logged to DB or text file.
    # These log levels may still be printed to console.
    # Called by: throughout msg operations
    # Default: ["debug"]
    log_lvl_nolog: list = ["debug"]

    # List object to exclude certain log levels from being printed to ui or console.
    # These log levels may still be logged to DB or text file.
    # Called by: msg.msg_print(~)
    # Default: ["debug"]
    log_lvl_noprint: list = ["debug", "warning"]

    # List object to have certain log levels raise an interrupt. This will also freeze
    # running threads and processes and eventually abort the program (depending on
    # further implementation of UI). An interrupt is only raised, if msg_print
    # or log_enable is true. If an item is part of this list, it will override being
    # part of the list log_lvl_nolog.
    # Called by: msg.msg_print(~)
    # Default: ["denied","error","critical"]
    log_lvl_interrupts: list = ["denied","error","critical"]

    r"""
>>> METRICS <<<
    """

    # Turn on metrics for the code executed.
    # Data collected: function name, trace, runtime, start time, end time, process ID, task ID
    # >REINITIALIZE<
    metrics_enable: bool = False

    # Perform metrics gathering in performance mode.
    # Data collected: function name, trace, runtime
    # >REINITIALIZE<
    metrics_perfmode: bool = False

    r"""
>>> MEMORY <<<
    TODO implement memory management with UltraDict
    
    These settings only take in effect in Multiprocessed/-threaded apps.
    With this setting memory can be claimed at initialization to prevent later memory
    buffer enhancements. In case of performance issues, memory may be increased.
    """

    # Select the way, how the available RAM is determined. If absolute, an integer
    # value will reflect the Megabytes of maximum memory.
    # Default: False or None
    memory_count_absolute: bool = False

    # Absolute amount of RAM to be utilized. This value will by default not exceed
    # the memory available on the system. If None, all RAM can be utilized.
    # Default: None
    # >REINITIALIZE<
    memory_absolute: int = None

    # Set the relative maximum amount of RAM to be utilized, where 1 resembles 100%
    # utilization and 0 resembles 0% utilization. If None, all RAM can be utilized.
    # Default: None or 1.0
    # >REINITIALIZE<
    memory_relative: float = None

    # Set the Minimum amount of memory in MB, that app_dict has to have reserved.
    # Default: None or 200
    # >REINITIALIZE<
    memory_min_MB: int = None

    r"""
>>> MULTI-PROCESSING <<<
    """

    # Select the way, how the available CPUs are determined. If absolute, an integer
    # value will reflect the maximum number of logical cores to utilize in parallel.
    # Default: False or None
    processes_count_absolute: bool = False

    # Absolute amount of processes to run parallel. This value will by default not exceed
    # the logical cores available on the system. If None, all CPUs can be utilized.
    # Default: None
    processes_absolute: int = 1

    # Set the relative maximum amount of processes to be utilized, where 1 resembles 100%
    # utilization and 0 resembles 0% utilization. If None, all CPUs can be utilized.
    # Default: None or 1.0
    processes_relative: float = 0.92

    # If the relative determination of maximum processes is used, it is necessary
    # to set how the maximum thread count should be rounded in case process_relative
    # does not reflect an integer cpu count. Allowed is "round" (default), "floor" or
    # "ceil".
    processes_relative_math: str = "floor"

    r"""
>>> MULTITHREADING <<<
    """

    # Select how the maximum threads will be determined. If true, you must set
    # an integer value greater than 1 for mt_max_threads_cnt_abs. Ultimately,
    # if the relative determination is chosen, an absolute maximum thread count
    # will be determined during initialization and mt_max_threads will
    # always be addressed after initialization.
    mt_max_threads_set_abs: bool = True

    # Set the absolute maximum amount of threads which shall be utilized. This needs
    # mt_max_threads_set_abs = True in order to have any effect. Have in mind, that
    # your app still needs to utilize these threads by keeping enough tasks in
    # the priority queue.
    mt_max_threads_cnt_abs: int = 1

    # Set the relative maximum amount of threads which shall be utilized, where
    # 1 resembles 100% utilization and 0 resembles 0% utilization. This needs
    # mt_max_threads_set_abs = False in order to have any effect. Have in mind, that
    # your app still needs to utilize these threads by keeping enough tasks in
    # the priority queue.
    mt_max_threads_cnt_rel: float = 1.0

    # If the relative determination of maximum threads is enabled, it is necessary
    # to set whether the maximum thread count should be rounded up or down, since
    # not in every case the result will be an integer value.
    mt_max_threads_rel_floor: bool = False

    r"""
>>> PATHS <<<
    """

    # Path to the app folder
    main_path = pathlib.Path(__file__).parent.parent.resolve()

    # Path to the logfile folder
    log_path = pathlib.Path(os.path.join(f'{main_path}', 'log'))
    # Create the path, if not existing.
    os.makedirs(log_path, exist_ok=True)

    # Path to the logging database.
    log_db_path = pathlib.Path(os.path.join(f'{log_path}', 'log.db'))

    # Path to the logging textfile.
    log_txt_path = os.path.join(f'{log_path}', f'{start_time}.log')

    # Path to the data folder
    data_path = pathlib.Path(os.path.join(f'{main_path}', 'data'))
    # Create the path, if not existing.
    os.makedirs(data_path, exist_ok=True)

    # Path to the main database of the app
    main_db_path = pathlib.Path(os.path.join(f'{main_path}', 'db', 'main.db'))

    # Path to the developed app
    app_path = pathlib.Path(os.path.join(f'{main_path}', 'app'))
    # Create the path, if not existing.
    os.makedirs(app_path, exist_ok=True)

    # Set the app icon (must be .ico)
    app_icon = pathlib.Path(os.path.join(f'{main_path}', 'res', 'icons', 'smph.ico'))

    # Set a GUI banner
    app_banner = pathlib.Path(os.path.join(f'{main_path}', 'res', 'banners', 'supermorph.png'))

    return{
        'language' : language,
        'localization' : f'loc.morPy_{language}',
        'priv_required' : mpy_priv_required,
        'log_enable' : log_enable,
        'ref_create' : ref_create,
        'log_db_enable' : log_db_enable,
        'log_txt_enable' : log_txt_enable,
        'log_txt_header_enable' : log_txt_header_enable,
        'msg_print' : msg_print,
        'msg_verbose' : msg_verbose,
        'print_init_vars' : print_init_vars,
        'log_lvl_nolog' : log_lvl_nolog,
        'log_lvl_noprint' : log_lvl_noprint,
        'log_lvl_interrupts' : log_lvl_interrupts,
        'metrics_enable' : metrics_enable,
        'metrics_perfmode' : metrics_perfmode,
        'memory_count_absolute' : memory_count_absolute,
        'memory_absolute' : memory_absolute,
        'memory_relative' : memory_relative,
        'memory_min_MB' : memory_min_MB,
        'processes_count_absolute' : processes_count_absolute,
        'processes_absolute' : processes_absolute,
        'processes_relative' : processes_relative,
        'processes_relative_math' : processes_relative_math,
        'mt_max_threads_set_abs' : mt_max_threads_set_abs,
        'mt_max_threads_cnt_abs' : mt_max_threads_cnt_abs,
        'mt_max_threads_cnt_rel' : mt_max_threads_cnt_rel,
        'mt_max_threads_rel_floor' : mt_max_threads_rel_floor,
        'main_path' : main_path,
        'log_path' : log_path,
        'log_db_path' : log_db_path,
        'log_txt_path' : log_txt_path,
        'data_path' : data_path,
        'main_db_path' : main_db_path,
        'app_path' : app_path,
        'app_icon' : app_icon,
        'app_banner' : app_banner,
    }
```

## lib.decorators.py

```Python
r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module yields all decorators to be used with the morPy framework.
"""

import time

from functools import wraps

def log(morpy_trace: dict, app_dict: dict, log_level: str, message: callable, verbose: bool=False):
    r"""
    Wrapper for conditional logging based on log level. To benefit from
    this logic, it is necessary to construct "message" in the lambda shown
    in the example, whereas <message> refers to a localized string like

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_level: Severity: debug/info/warning/error/critical/denied
    :param message: A callable (e.g., lambda or function) that returns the log message.
    :param verbose: If True, message is only logged in verbose mode.

    :example:
        from lib.decorators import log
        log(morpy_trace, app_dict, "info",
        lambda: "Hello world!")

    TODO move this to morPy, it's not a decorator
    """

    import lib.msg as msg

    # Skip logging, if message is verbose and verbose is disabled
    if verbose and not app_dict["conf"].get("msg_verbose", False):
        return
    else:
        log_level = log_level.lower()

        if message and app_dict["global"]["morpy"]["logs_generate"].get(log_level, False):
            msg.log(morpy_trace, app_dict, log_level, message(), verbose)

def log_no_q(morpy_trace: dict, app_dict: dict, log_level: str, message: callable, verbose: bool=False):
    r"""
    Wrapper for conditional logging based on log level. This decorator does not enqueue
    logs and is intended for use by morPy orchestrator only.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_level: Severity: debug/info/warning/error/critical/denied
    :param message: A callable (e.g., lambda or function) that returns the log message.
    :param verbose: If True, message is only logged in verbose mode.

    :example:
        from lib.decorators import log_no_q
        log_no_q(morpy_trace, app_dict, level,
        lambda: <message>)

    TODO remove this decorator as lib.msg.log() takes care of "no queue"
    """

    import lib.msg as msg

    # Skip logging, if message is verbose and verbose is disabled
    if verbose and not app_dict["conf"].get("msg_verbose", False):
        return
    else:
        log_level = log_level.lower()

        if message and app_dict["global"]["morpy"]["logs_generate"].get(log_level, False):
            msg.log(morpy_trace, app_dict, log_level, message(), verbose)

def metrics(func):
    r"""
    Decorator used for metrics and performance analytics. in morPy this
    is the outermost decorator.

    :param func: Function to be decorated

    :return retval: Return value of the wrapped function

    :example:
        from lib.decorators import metrics
        @metrics
        my_function_call(morpy_trace, app_dict, *args, **kwargs)
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        perf_mode = None
        enable_metrics = False
        morpy_trace: dict = None
        len_args = len(args)

        # Skip metrics, if arguments morpy_trace or app_dict are missing
        if len_args < 2:
            raise IndexError("Missing arguments morpy_trace and/or app_dict!")
        else:
            # Assume the first arg might be `self` if not a dict
            offset = 0
            if len_args > 0 and not isinstance(args[0], dict):
                # Probably a bound method; skip `self`
                offset = 1

            # Attempt to extract morpy_trace & app_dict from positional args
            try:
                morpy_trace: dict = args[offset]
                app_dict = args[offset + 1]

                # Now we decide if metrics are enabled
                # (only if we found both morpy_trace and app_dict)
                if isinstance(morpy_trace, dict) and isinstance(app_dict, dict):
                    enable_metrics = app_dict.get("lib.conf", {}).get("metrics_enable", False)
                    perf_mode = app_dict.get("lib.conf", {}).get("metrics_perfmode", False)

            except (IndexError, TypeError):
                # If we still don't have them, leave them as None
                pass
            except KeyError:
                raise IndexError("Positional arguments morpy_trace and/or app_dict are missing or at wrong position!")

            if enable_metrics:
                start_time = time.perf_counter()
                retval = func(*args, **kwargs)
                end_time = time.perf_counter()
                run_time = end_time - start_time

                # Performance Mode vs. Full Mode
                if perf_mode:
                    metrics_perf(morpy_trace, run_time)
                else:
                    metrics_full(morpy_trace, run_time)
            else:
                retval = func(*args, **kwargs)

        return retval

    return wrapper

def metrics_perf(morpy_trace, run_time):
    r"""
    This helper function makes use of the data collected by it calling
    function metrics(~) and provides logging and formatting of the data.
    It performs all action in performance mode, which limits the data
    collected to function name, trace and runtime.

    :param morpy_trace: operation credentials and tracing
    :param run_time: Total run time of the wrapped function.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module: str = 'decorators'
    # operation: str = 'metrics_perf(~)'
    # morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

def metrics_full(morpy_trace, run_time):
    r"""
    This helper function makes use of the data collected by it calling
    function metrics(~) and provides logging and formatting of the data.
    It performs all action in performance mode, which limits the data
    collected to function name, trace and runtime.

    :param morpy_trace: operation credentials and tracing
    :param run_time: Total run time of the wrapped function.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module: str = 'decorators'
    # operation: str = 'metrics_full(~)'
    # morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

```

## lib.fct.py

```Python
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

        # Define the priority order for level-1 subdictionaries
        app_dict_order = ["conf", "sys", "run", "global", "proc", "loc"]

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

def tracing(module, operation, morpy_trace, clone=True, process_id=None) -> dict:
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
    morpy_trace_passdown["tracing"] = f'{morpy_trace["tracing"]} > {module}.{operation}'

    return morpy_trace_passdown

```

## lib.init.py

```Python
r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module holds all functions used for initialization of the
            morPy framework.
"""

import lib.fct as morpy_fct
import lib.conf as conf
from lib.common import textfile_write
from lib.decorators import metrics, log, log_no_q
from lib.mp import MorPyOrchestrator, process_q_init

import importlib
import sys
import os
import os.path

def init_cred() -> dict:
    r"""
    This function initializes the operation credentials and tracing.

    :param:
        -

    :return: dict
        morpy_trace - operation credentials and tracing
    """

    # Initialize operation credentials and tracing.
    # Each operation/function/object will fill the dictionary with data
    # by executing morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)
    # as a first step before execution.
    morpy_trace: dict = {
        'module' : '__main__',
        'operation' : '',
        'tracing' : '__main__',
        'process_id' : int(0),
        'thread_id' : int(0),
        'task_id' : int(0),
        'log_enable' : False,
        'interrupt_enable' : False,
    }

    return morpy_trace

def init(morpy_trace) -> (dict, MorPyOrchestrator):
    r"""
    This function initializes the app dictionary and yields app
    specific information to be handed down through called functions.

    :param morpy_trace: operation credentials and tracing

    :return app_dict: morPy global dictionary containing app configurations
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'init(~)'
    morpy_trace_init = morpy_fct.tracing(module, operation, morpy_trace)

    try:
        # ############################################
        # START Single-threaded initialization
        # ############################################

        # Build the app_dict
        init_dict = build_app_dict(morpy_trace_init, create=True)

        init_dict["morpy"].update({"tasks_created" : morpy_trace_init["task_id"]})
        init_dict["morpy"].update({"proc_available" : set()})
        init_dict["morpy"].update({"proc_busy" : {morpy_trace_init["process_id"],}})
        init_dict["morpy"]["proc_joined"] = True
        init_dict["morpy"].update({"proc_master" : morpy_trace['process_id']})

        # Initialize the global interrupt flag and exit flag
        init_dict["morpy"]["interrupt"] = False
        init_dict["morpy"]["exit"] = False

        # Set an initialization complete flag
        init_dict["run"]["init_complete"] = False

        # Retrieve the starting time of the program
        init_datetime = morpy_fct.datetime_now()

        # Store the start time and timestamps in the dictionary
        for time_key in init_datetime:
            init_dict["run"][f'init_{time_key}'] = init_datetime[f'{time_key}']

        # Update the initialize dictionary with the parameters dictionary
        init_dict["conf"].update(conf.settings(start_time=init_dict["run"]["init_datetimestamp"]))

        # Evaluate log_enable
        if not init_dict["conf"]["log_db_enable"] and not init_dict["conf"]["log_txt_enable"]:
            init_dict["conf"]["log_enable"] = False

        # Pass down the log enabling parameter
        morpy_trace["log_enable"] = init_dict["conf"]["log_enable"]
        morpy_trace_init["log_enable"] = init_dict["conf"]["log_enable"]

        # Import the morPy core functions localization into init_dict.
        morpy_loc = importlib.import_module(init_dict["conf"]["localization"])
        init_dict["loc"]["morpy"].update(getattr(morpy_loc, 'loc_morpy')())

        # Build nested dictionary for log generation
        log_levels = ("init", "debug", "info", "warning", "denied", "error", "critical", "exit")
        for log_level in log_levels:
            if (
                (init_dict["conf"]["log_enable"] and
                 not (log_level in init_dict["conf"]["log_lvl_nolog"])
                 ) or (
                init_dict["conf"]["msg_print"] and
                 not (log_level in init_dict["conf"]["log_lvl_noprint"]))
            ):
                init_dict["global"]["morpy"]["logs_generate"].update({log_level : True})
            else:
                init_dict["global"]["morpy"]["logs_generate"].update({log_level : False})

        # Retrieve system information
        sysinfo = morpy_fct.sysinfo()

        # Update init_dict with system information
        for sys_key in sysinfo:
            init_dict["sys"][sys_key] = sysinfo[sys_key]

        # Test for elevated privileges
        # TODO make an elevation handler

        # Prepare log levels
        init_dict["run"]["events_total"] = 0
        init_dict["run"]["events_DEBUG"] = 0
        init_dict["run"]["events_INFO"] = 0
        init_dict["run"]["events_WARNING"] = 0
        init_dict["run"]["events_DENIED"] = 0
        init_dict["run"]["events_ERROR"] = 0
        init_dict["run"]["events_CRITICAL"] = 0
        init_dict["run"]["events_UNDEFINED"] = 0
        init_dict["run"]["events_INIT"] = 0
        init_dict["run"]["events_EXIT"] = 0

        # Create first log in txt-file including the app header
        if (init_dict["conf"]["log_txt_header_enable"] and
            morpy_trace_init["log_enable"] and
            init_dict["conf"]["log_txt_enable"]
        ):
            morpy_log_header(morpy_trace_init, init_dict)

        # Initialize the morPy debug-specific localization
        init_dict["loc"]["morpy_dgb"].update(getattr(morpy_loc, 'loc_morpy_dbg')())
        log_no_q(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_dbg_loaded"]}')

        # Initialize the app-specific localization
        app_loc = importlib.import_module(f'loc.app_{init_dict["conf"]["language"]}')
        init_dict["loc"]["app"].update(getattr(app_loc, 'loc_app')())
        init_dict["loc"]["app_dbg"].update(getattr(app_loc, 'loc_app_dbg')())
        log_no_q(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_app_loaded"]}')

        # Localization initialized.
        log_no_q(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_loc_finished"]}\n'
                f'{init_dict["loc"]["morpy"]["init_loc_lang"]}: {init_dict["conf"]["language"]}')

        # Load init_dict as a string
        if init_dict["conf"]["print_init_vars"] or init_dict["conf"]["ref_create"]:
            init_dict_str = morpy_fct.app_dict_to_string(init_dict)
        else:
            init_dict_str = ""

        # Print init_dict to console
        if init_dict["conf"]["print_init_vars"]:
            print(init_dict_str)

        # Initialize the morPy orchestrator
        orchestrator = MorPyOrchestrator(morpy_trace_init, init_dict)

        # ############################################
        # END Single-threaded initialization
        # START Multi-threaded initialization
        # ############################################

        # task = morPy.testprint(morpy_trace_init, "Message")
        # mp.run_parallel(mpy_task, app_dict, task)

        # ############################################
        # END Multi-threaded initialization
        # ############################################

        # Calculate the runtime of the initialization routine
        init_duration = morpy_fct.runtime(init_dict["run"]["init_datetime_value"])

        # Record the duration of the initialization
        init_dict["run"]["init_rnt_delta"] = init_duration["rnt_delta"]

        log_no_q(morpy_trace_init, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["init_finished"]}\n'
            f'{init_dict["loc"]["morpy"]["init_duration"]}: {init_dict["run"]["init_rnt_delta"]}')

        # Write app_dict to file: initialized_app_dict.txt
        if init_dict["conf"]["ref_create"]:
            morpy_ref(morpy_trace_init, init_dict, init_dict_str)

        # Exit initialization
        retval = init_dict, orchestrator
        return retval

    except Exception as e:
        morpy_fct.handle_exception_init(e)
        raise

def build_app_dict(morpy_trace: dict, create: bool=False) -> dict:
    r"""
    This function builds the app_dict in accordance to multiprocessing and whether GIL
    is included in the Python environment.

    :param morpy_trace: operation credentials and tracing
    :param create: If True, a (nested) dictionary is created. Otherwise, purely
        references to the UltraDict.

    :return init_dict: morPy global dictionary containing app configurations

    :example:
        init_dict = build_app_dict(morpy_trace, create=True)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'build_app_dict(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    # Check for GIL and decide for an app_dict structure.
    gil = has_gil(morpy_trace)
    init_dict = None
    init_mem = 1_000_000 # TODO get memory from config
    min_mem = 1_000

    try:
        # FIXME
        # if gil:
        if True:
            from lib.mp import shared_dict

            def mem_evaluation(mem, min_mem) -> int:
                mem = mem if mem > min_mem else min_mem
                return mem

            mem = mem_evaluation(init_mem, min_mem)
            init_dict = shared_dict(
                name="app_dict",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["conf"] = shared_dict(
                name="app_dict[conf]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 10, min_mem)
            init_dict["morpy"] = shared_dict(
                name="app_dict[morpy]",
                create=create,
                size=mem,
                recurse=True
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["morpy"]["orchestrator"] = shared_dict(
                name="app_dict[morpy][orchestrator]",
                create=create,
                size=mem,
                recurse=True
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["morpy"]["proc_refs"] = shared_dict(
                name="app_dict[morpy][proc_refs]",
                create=create,
                size=mem,
                recurse=True
            )

            mem = mem_evaluation(init_mem // 10, min_mem)
            init_dict["sys"] = shared_dict(
                name="app_dict[sys]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 10, min_mem)
            init_dict["run"] = shared_dict(
                name="app_dict[run]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem, min_mem)
            init_dict["global"] = shared_dict(
                name="app_dict[global]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["global"]["morpy"] = shared_dict(
                name="app_dict[global][morPy]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 10, min_mem)
            init_dict["global"]["app"] = shared_dict(
                name="app_dict[global][app]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["proc"] = shared_dict(
                name="app_dict[proc]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["proc"]["morpy"] = shared_dict(
                name="app_dict[proc][morPy]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["proc"]["app"] = shared_dict(
                name="app_dict[proc][app]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 1_000, min_mem)
            init_dict["loc"] = shared_dict(
                name="app_dict[loc]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem, min_mem)
            init_dict["loc"]["morpy"] = shared_dict(
                name="app_dict[loc][morPy]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["loc"]["morpy_dgb"] = shared_dict(
                name="app_dict[loc][mpy_dbg]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem, min_mem)
            init_dict["loc"]["app"] = shared_dict(
                name="app_dict[loc][app]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 100, min_mem)
            init_dict["loc"]["app_dbg"] = shared_dict(
                name="app_dict[loc][app_dbg]",
                create=create,
                size=mem
            )

            mem = mem_evaluation(init_mem // 1_000, min_mem)
            init_dict["global"]["morpy"]["logs_generate"] = shared_dict(
                name="app_dict[global][morPy][logs_generate]",
                create=create,
                size=mem
            )

        # Without GIL, allow for true nesting
        else:
            init_dict = {}

            init_dict["conf"] = {}
            init_dict["morpy"] = {}
            init_dict["morpy"]["orchestrator"] = {}
            init_dict["morpy"]["proc_refs"] = {}
            init_dict["sys"] = {}
            init_dict["run"] = {}
            init_dict["global"] = {}
            init_dict["global"]["morpy"] = {}
            init_dict["global"]["app"] = {}
            init_dict["proc"] = {}
            init_dict["proc"]["morpy"] = {}
            init_dict["proc"]["app"] = {}
            init_dict["loc"] = {}
            init_dict["loc"]["morpy"] = {}
            init_dict["loc"]["morpy_dgb"] = {}
            init_dict["loc"]["app"] = {}
            init_dict["loc"]["app_dbg"] = {}
            init_dict["global"]["morpy"]["logs_generate"] = {}

        return init_dict

    # Error detection
    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

def morpy_log_header(morpy_trace: dict, init_dict: dict) -> None:
    r"""
    This function writes the header for the logfile including app specific
    information.

    :param morpy_trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)

    :return:
        -

    :example:
        morpy_log_header(morpy_trace, init_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'log_header(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    # Create the app header
    content = (
        f'== {init_dict["loc"]["morpy"]["log_header_start"]}{3*" =="}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_author"]}: Bastian Neuwirth\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_app"]}: {init_dict["conf"]["main_path"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_timestamp"]}: {init_dict["run"]["init_datetimestamp"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_user"]}: {init_dict["sys"]["username"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_system"]}: {init_dict["sys"]["os"]} {init_dict["sys"]["os_release"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_version"]}: {init_dict["sys"]["os_version"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_architecture"]}: {init_dict["sys"]["os_arch"]}\n\t'
        f'{init_dict["loc"]["morpy"]["log_header_threads"]}: {init_dict["sys"]["threads"]}\n'
        f'== {init_dict["loc"]["morpy"]["log_header_begin"]}{3*" =="}\n'
    )

    # Write to the logfile
    filepath = init_dict["conf"]["log_txt_path"]
    textfile_write(morpy_trace, init_dict, filepath, content)

    # Clean up
    del morpy_trace

def morpy_ref(morpy_trace: dict, init_dict: dict, init_dict_str: str) -> None:
    r"""
    This function documents the initialized dictionary (reference). It is stored
    in the same path as __main__.py and serves development purposes.

    :param morpy_trace: operation credentials and tracing
    :param init_dict: Dictionary holding all initialized data (init of app_dict)
    :param init_dict_str: String of the init_dict

    :return:
        -

    :example:
        morpy_ref(morpy_trace, init_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.init'
    operation: str = 'ref(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    try:
        morpy_ref_path = os.path.join(f'{init_dict["conf"]["main_path"]}', 'initialized_app_dict.txt')
        init_dict_txt = open(morpy_ref_path,'w')

        # Write init_dict to file
        init_dict_txt.write(f'{init_dict["loc"]["morpy"]["ref_descr"]}\n\n')
        init_dict_txt.write(init_dict_str)

        # Close the file
        init_dict_txt.close()

        # The init_dict was written to textfile.
        log_no_q(morpy_trace, init_dict, "init",
        lambda: f'{init_dict["loc"]["morpy"]["ref_created"]}\n'
                f'{init_dict["loc"]["morpy"]["ref_path"]}: {morpy_ref_path}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, None, e, sys.exc_info()[-1].tb_lineno, "error")

def has_gil(morpy_trace: dict) -> bool | None:
    r"""
    Return True if we detect a standard GIL-based Python runtime on a 'typical' operating system.
    Return False if we suspect a 'no-gil' or 'free-threading' build on Linux/macOS/Windows, or if
    we detect certain alternative Pythons. This is *heuristic* and not a guaranteed official check.

    :param morpy_trace: operation credentials and tracing information

    :return gil_detected: If True, Python environment has GIL implemented. Process forking not supported.

    :example:
        gil = has_gil(morpy_trace)
    """

    # module: str = 'lib.init'
    # operation: str = 'has_gil(~)'
    # morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    try:
        if sys.version_info >= (3, 13):
            status = sys._is_gil_enabled()
            if status:
                return True
            else:
                return False
        else:
            return True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, None, e, sys.exc_info()[-1].tb_lineno, "error")

```

## lib.mp.py

```Python
r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Multiprocessing functionality for morPy.

TODO provide a general purpose lock
    > Find a way to lock file objects and dirs
"""
import copy

import lib.fct as morpy_fct
from lib.decorators import metrics, log, log_no_q

import sys
import time
from UltraDict import UltraDict
from multiprocessing import Process
from functools import partial
from heapq import heappush, heappop

class MorPyOrchestrator:
    r"""
    TODO implement memory management
    Class of morPy orchestrators.
    """

    def __init__(self, morpy_trace: dict, app_dict: dict) -> None:
        r"""
        In order to get metrics for __init__(), call helper method _init() for
        the @metrics decorator to work. It relies on the returned
        {'morpy_trace' : morpy_trace}, which __init__() can not do (needs to be None).

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        # Setup morPy tracing
        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator.__init__(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        try:
            # Initialize with self._init() for metrics decorator support
            self._init(morpy_trace, app_dict)

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    @metrics
    def _init(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Initialization helper method for parallel processing setup.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._init(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Set app termination flag
            app_dict["morpy"]["orchestrator"]["terminate"] = False

            # Determine processes and memory to use
            self._init_processes(morpy_trace, app_dict)
            self._init_memory(morpy_trace, app_dict)

            # Initialize the process queue shared dictionary.
            self.process_q = process_q_init(morpy_trace, app_dict, create=True)["process_q_dict"]

            # Set up fist tasks
            self._init_app_dict(morpy_trace, app_dict)
            self._init_run(morpy_trace, app_dict)

            # MorPyOrchestrator initialized.
            log_no_q(morpy_trace, app_dict, "init",
            lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_done"]}')

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

    @metrics
    def _init_processes(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Get the maximum amount of processes to handle and prepare app_dict.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        TODO make compatible with forking/free-threading
        TODO when made compatible, take care of self._run(), init.init() and ProcessQueue._init()
        """

        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._init_processes(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Set up multiprocessing
            system_logical_cpus = int(app_dict["sys"]["logical_cpus"])
            self.processes_min = 1
            processes_count_absolute = app_dict["conf"]["processes_count_absolute"]
            processes_absolute = app_dict["conf"]["processes_absolute"]
            processes_relative = app_dict["conf"]["processes_relative"]
            processes_relative_math = app_dict["conf"]["processes_relative_math"]

            # Guard for configured values in conf.py
            if isinstance(processes_count_absolute, bool) or processes_count_absolute is None:
                processes_count_absolute = processes_count_absolute or False
            else:
                # Value is not a boolean. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_not_bool"]}\n'
                    f'{processes_count_absolute=}'
                )

            # Guard for configured values in conf.py
            if isinstance(processes_absolute, int) or processes_absolute is None:
                processes_absolute = processes_absolute or system_logical_cpus
            else:
                # Value is not an integer. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_not_int"]}\n'
                    f'{processes_absolute=}'
                )

            # Guard for configured values in conf.py
            if isinstance(processes_relative, float) or processes_relative is None:
                processes_relative = processes_relative or 1.0
            else:
                # Value is not a float. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_not_float"]}\n'
                    f'{processes_relative=}'
                )

            # Guard for configured values in conf.py
            if isinstance(processes_relative_math, str) or processes_relative_math is None:
                processes_relative_math = processes_relative_math or "round"
                if processes_relative_math not in ("round", "floor", "ceil"):
                    # Rounding corrected.
                    log_no_q(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_processes_rel_math_corr"]}\n'
                            f'{processes_relative_math} > round')

                    processes_relative_math = "round"
            else:
                # Value is not a string. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_not_str"]}\n'
                    f'{processes_relative_math=}'
                )

            # Determine maximum parallel processes
            if processes_count_absolute:
                if processes_absolute <= self.processes_min:
                    self.processes_max = self.processes_min
                elif processes_absolute >= system_logical_cpus:
                    self.processes_max = system_logical_cpus
                else:
                    self.processes_max = processes_absolute
            else:
                if processes_relative <= 0.0:
                    self.processes_max = self.processes_min
                elif processes_relative >= 1.0:
                    self.processes_max = system_logical_cpus
                else:
                    if processes_relative_math == "round":
                        self.processes_max = round(processes_relative * system_logical_cpus)
                    elif processes_relative_math == "floor":
                        self.processes_max = int(processes_relative * system_logical_cpus)
                    elif processes_relative_math == "ceil":
                        relative_result = processes_relative * system_logical_cpus
                        self.processes_max = int(relative_result) if relative_result == int(relative_result) else relative_result + 1
                    else:
                        # Wrong rounding parameter. Fallback to 'round' for determining maximum amount of parallel processes.
                        log_no_q(morpy_trace, app_dict, "warning",
                        lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_err_rounding_val"]}\n{processes_relative_math=}')
                        self.processes_max = round(processes_relative * system_logical_cpus)

            self._mp = True if self.processes_max > 1 else False

            # Store in app_dict
            app_dict["morpy"]["orchestrator"]["processes_max"] = self.processes_max
            app_dict["morpy"]["orchestrator"]["mp"] = self._mp

            # Maximum amount of parallel processes determined
            log_no_q(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_cpus_determined"]}\n'
                    f'Maximum parallel processes for runtime: {self.processes_max}')

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

    @metrics
    def _init_memory(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Set the maximum amount of memory to be utilized.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._init_memory(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            sys_memory_bytes = int(app_dict["sys"]["sys_memory_bytes"])
            self.memory_min = app_dict["conf"]["memory_min_MB"]
            memory_count_absolute = app_dict["conf"]["memory_count_absolute"]
            memory_absolute = app_dict["conf"]["memory_absolute"]
            memory_relative = app_dict["conf"]["memory_relative"]

            # Guard for configured values in conf.py
            if isinstance(self.memory_min, int) or self.memory_min is None:
                # Change unit from MB to Byte
                self.memory_min = self.memory_min*1024*1024 if self.memory_min else 200*1024*1024
            else:
                # Value is not an integer. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_not_int"]}\n'
                    f'{self.memory_min=}'
                )

            # Guard for configured values in conf.py
            if isinstance(memory_count_absolute, bool) or memory_count_absolute is None:
                memory_count_absolute = memory_count_absolute or False
            else:
                # Value is not a boolean. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_not_bool"]}\n'
                    f'{memory_count_absolute=}'
                )

            # Guard for configured values in conf.py
            if isinstance(memory_absolute, int) or memory_absolute is None:
                # Change unit from MB to Byte
                memory_absolute = memory_absolute*1024*1024 if memory_absolute else sys_memory_bytes
            else:
                # Value is not an integer. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_not_int"]}\n'
                    f'{memory_absolute=}'
                )

            # Guard for configured values in conf.py
            if isinstance(memory_relative, float) or memory_relative is None:
                memory_relative = memory_relative or 1.0
            else:
                # Value is not a float. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_not_float"]}\n'
                    f'{memory_relative=}'
                )

            # Evaluate calculation methods and maximum parallel processes
            if memory_count_absolute:
                if memory_absolute <= self.memory_min:
                    self.memory_max = self.memory_min
                elif memory_absolute >= sys_memory_bytes:
                    self.memory_max = sys_memory_bytes
                else:
                    self.memory_max = memory_absolute
            else:
                if memory_relative <= 0.0:
                    self.memory_max = self.memory_min
                elif memory_relative >= 1.0:
                    self.memory_max = sys_memory_bytes
                else:
                    relative_result = memory_relative * sys_memory_bytes
                    self.memory_max = int(relative_result)

            # Store in app_dict
            app_dict["morpy"]["orchestrator"]["memory_max"] = self.memory_max

            # Maximum memory set.
            log_no_q(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_memory_set"]}\n'
                f'Maximum memory for runtime: {self.memory_max // 1024} KB / {self.memory_max // 1024**2} MB')

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

    @metrics
    def _init_app_dict(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Prepare nested dictionaries and store data in app_dict.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._init_app_dict(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Initialize the total task counter
            # TODO clean up, currently '[morpy][tasks_created]' is used
            app_dict["morpy"]["orchestrator"]["task_counter"] = 0

            # Get global process sets for membership testing
            processes_available = app_dict["morpy"]["proc_available"]
            processes_busy = app_dict["morpy"]["proc_busy"]

            p = 0
            while p < self.processes_max:
                # Check for process IDs reserved during early initialization of morPy
                if p in processes_busy:
                    pass
                elif p in processes_available:
                    pass
                else:
                    # Append to available processes
                    processes_available = app_dict["morpy"]["proc_available"]
                    processes_available.add(p)
                    app_dict["morpy"]["proc_available"] = processes_available # reassign to trigger synchronization

                p += 1

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

    @metrics
    def _init_run(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Setup attributes for orchestrator._run().

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._init_run(~)'
        morpy_trace_init_run = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Set attributes for _run
            self.ref_module: str = module
            self.ref_operation: str = operation
            self.morpy_trace: dict = morpy_trace

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

        return {
            'morpy_trace': morpy_trace_init_run,
            'check': check,
        }

    @metrics
    def _app_run(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Sequential app init, run and exit routine.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._app_run(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            from app.init import app_init
            from app.run import app_run
            from app.exit import app_exit

            # App starting.
            log_no_q(morpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_app_run_start"]}')

            # Initialize and run the app
            morpy_trace["tracing"] = ""
            app_init_return = app_init(morpy_trace, app_dict)["app_init_return"]
            app_run_return = app_run(morpy_trace, app_dict, app_init_return)["app_run_return"]

            # Exit the app and signal morPy to exit
            app_exit(morpy_trace, app_dict, app_run_return)

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

    @metrics
    def _run(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Routine of the morPy orchestrator. Cyclic program.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._run(~)'
        # TODO Find out, why morpy_trace["process_id"] is overwritten in app trace
        # The enforced deepcopy morpy_fct.tracing() is a workaround.
        morpy_trace_app = morpy_fct.tracing(module, operation, morpy_trace)
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        self_ref = app_dict["morpy"]["orchestrator"]

        try:
            # TODO provide case for 2-core mode
            #   > 1 core for orchestrator and 1 core for app, so no additional spawns
            #   > Can be mitigated by making waiting processes participate in taking tasks
            # TODO Add logging thread

            # Start the app
            app_task = [self._app_run, morpy_trace_app, app_dict]
            process_enqueue(morpy_trace, app_dict, priority=-20, task=app_task, autocorrect=False, force=self._mp)

            if self._mp:
                while not self_ref["terminate"]:
                    self._main_loop(morpy_trace, app_dict)

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

        finally:
            return {
                'morpy_trace': morpy_trace,
                'check': check,
            }

    @metrics
    def _main_loop(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Function

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates if the task was pulled successfully

        :example:
            self._main_loop(morpy_trace, app_dict)
        """

        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._main_loop(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        self_ref = app_dict["morpy"]["orchestrator"]

        try:
            while (not self_ref["terminate"]) or (len(self.process_q["heap"]) > 0):
                # Check process queue for tasks
                if len(self.process_q["heap"]) > 0:
                    task_pull = process_pull(morpy_trace, app_dict)
                    task = task_pull["task"]
                    priority = task_pull["priority"]
                    is_process = task_pull["is_process"]
                    func = task[0]
                    args = task[1:]
                    # Run a new parallel process
                    if is_process:
                        app_dict["morpy"]["proc_joined"] = False
                        run_parallel(morpy_trace, app_dict, task=task, priority=priority)
                        self_ref["terminate"] = False
                    # Run an orchestrator task internally
                    else:
                        retval = func(*args)

                        # Introduce wait time, if waiting for processes
                        if priority == -20:
                            time.sleep(0.02)  # 0.02 seconds = 20 milliseconds
                else:
                    # Sleep if heap is empty
                    time.sleep(0.05)  # 0.05 seconds = 50 milliseconds

                # Initiate program exit
                # TODO make use of program exit with critical exceptions
                # TODO dev a process kill app to end spawned processes and empty memory
                if app_dict["morpy"]["exit"]:
                    self_ref["terminate"] = True

                # Evaluate if spawned processes need to end. As long as the app is running in
                # a different process, the orchestrator will not terminate. Also, a critical exception
                # may end the app.
                if len(app_dict["morpy"]["proc_busy"]) == 0:
                    self_ref["terminate"] = True

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

        finally:
            return {
                'morpy_trace': morpy_trace,
                'check': check,
            }

@metrics
def process_q_init(morpy_trace: dict, app_dict: dict, create: bool = False) -> dict:
    r"""
    Initialize the morPy process queue in a separated non-nested shared dictionary.

    :param morpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param create: If True, creates new shared dictionary for the proces queue. Else if
        False, attaches to shared dictionary.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether initialization completed without errors
        process_q_dict: Shared dictionary for the process queue
    """

    module: str = 'lib.mp'
    operation: str = 'process_q_init(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    name: str = "morPy::process_q"
    process_q_dict: dict = None

    try:
        # TODO get size from lib.init to support memory management
        process_q_dict = shared_dict(
            name=name,
            create=create,
            size=100_000
        )

        if create:
            process_q_dict["heap"] = []
            process_q_dict["counter"] = 0
            process_q_dict["task_lookup"] = set()
    
            # Priority queue initialized.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["process_q_init_done"]}\n'
                    f'{app_dict["loc"]["morpy"]["process_q_name"]}: "{name}"')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException

        err_msg = f'{app_dict["loc"]["morpy"]["process_q_name"]}: "{name}"'
        raise MorPyException(
            morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical",
            message=err_msg
        )

    return {
        'morpy_trace': morpy_trace,
        'check': check,
        'process_q_dict': process_q_dict
    }

@metrics
def process_enqueue(morpy_trace: dict, app_dict: dict, priority: int=100, task: tuple=None, autocorrect: bool=True,
            is_process: bool=True, force: bool = False) -> dict:
    r"""
    Adds a task to the morPy process queue.

    :param morpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param priority: Integer representing task priority (lower is higher priority)
    :param task: Tuple of a callable, *args and **kwargs (func, *args, **kwargs)
    :param autocorrect: If False, priority can be smaller than zero. Priority
        smaller zero is reserved for the morPy Core.
    :param is_process: If True, task is run in a new process (not by morPy orchestrator)
    :param force: If True, enforces queueing instead of direct execution. Used by morPy
        orchestrator to spawn the first app process.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was enqueued successfully

    :example:
        from lib.mp import process_enqueue
        from functools import partial
        task = partial(my_func, morpy_trace, app_dict)
        process_enqueue(morpy_trace, app_dict, priority=25, task=task)
    """

    module: str = 'lib.mp'
    operation: str = 'process_enqueue(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # Attach to process queue shared dictionary.
        process_q = process_q_init(morpy_trace, app_dict)["process_q_dict"]
        name: str = process_q.name

        if task:
            # Omit queuing, if in single core mode
            if not (morpy_trace["process_id"] == app_dict["morpy"]["proc_master"]) or force:

                # Check and autocorrect process priority
                if priority < 0 and autocorrect:
                    # Invalid argument given to process queue. Autocorrected.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["process_enqueue_prio_corr"]}\n'
                            f'{app_dict["loc"]["morpy"]["process_enqueue_priority"]}: {priority} to 0')
                    priority = 0

                # Pushing task to priority queue.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["process_enqueue_start"]} {name}\n'
                        f'{app_dict["loc"]["morpy"]["process_enqueue_priority"]}: {priority}')

                next_task_id = app_dict["morpy"]["tasks_created"] + 1
                task_sys_id = id(task)

                # Check, if ID already in queue
                if task_sys_id in process_q["task_lookup"]:
                    # Task is already enqueued. Referencing in queue.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["process_enqueue_task_duplicate"]}\n'
                            f'Task system ID: {task_sys_id}')

                # Push task to queue
                task_qed = (priority, next_task_id, task_sys_id, task, is_process)

                heap = process_q["heap"]
                heappush(heap, task_qed)
                process_q["heap"] = heap # reassign to trigger synchronization

                task_lookup = process_q["task_lookup"]
                task_lookup.add(task_sys_id)
                process_q["task_lookup"] = task_lookup # reassign to trigger synchronization

                # Updating global tasks created last in case an error occurs
                process_q["counter"] += 1
                app_dict["morpy"]["tasks_created"] += 1
                morpy_trace["task_id"] = app_dict["morpy"]["tasks_created"]

            # If run by morPy orchestrator or in single core mode, execute without queueing.
            else:
                func = task[0]
                args = task[1:]
                retval = func(*args)

            check: bool = True
        else:
            # Task can not be None. Skipping enqueue.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["process_enqueue_none"]}')

    except Exception as e:
        from lib.exceptions import MorPyException

        try:
            name: str = process_q.name
        except:
            name: str = "???"

        err_msg = (
            f'{app_dict["loc"]["morpy"]["ProcessQueue_name"]}: {name}\n'
            f'{app_dict["loc"]["morpy"]["process_enqueue_priority"]}: {priority}'
        )
        raise MorPyException(
            morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical",
            message=err_msg
        )

    return {
        'morpy_trace': morpy_trace,
        'check': check
    }

@metrics
def process_pull(self, morpy_trace: dict, app_dict: dict) -> dict:
    r"""
    Removes and returns the highest priority task from the process queue.

    :param morpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was pulled successfully
        priority: Integer representing task priority (lower is higher priority)
        counter: Number of the task when enqueued
        task_id : Continuously incremented task ID (counter).
        task_sys_id : ID of the task determined by Python core
        task: The pulled task list
        task_callable: The pulled task callable
        is_process: If True, task is run in a new process (not by morPy orchestrator)

    :example:
        from lib.mp import process_pull
        from functools import partial
        task = process_pull(morpy_trace, app_dict)['task']
        task()
    """

    module: str = 'lib.mp'
    operation: str = 'process_pull(~)'
    morpy_trace_pull = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    priority = None
    counter = None
    task_sys_id = None
    task = None
    is_process = None

    try:
        # Attach to process queue shared dictionary.
        process_q = process_q_init(morpy_trace, app_dict)["process_q_dict"]
        name: str = process_q.name

        # Global interrupt - wait for error handling
        while app_dict["morpy"].get("interrupt", False):
            pass

        if len(process_q["heap"]) > 0:
            heap = process_q["heap"]
            task_dqed = heappop(heap)
            process_q["heap"] = heap # reassign to trigger synchronization

            priority, counter, task_sys_id, task, is_process = task_dqed

            task_lookup = process_q["task_lookup"]
            task_lookup.remove(task_sys_id)
            process_q["task_lookup"] = task_lookup # reassign to trigger synchronization

            # Pulling task from NAME priority: INT counter: INT
            log(morpy_trace_pull, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["process_pull_start"]} {name}.\n'
                    f'{app_dict["loc"]["morpy"]["process_pull_priority"]}: {priority}\n'
                    f'{app_dict["loc"]["morpy"]["process_pull_cnt"]}: {counter}',
                    verbose = True)

            check: bool = True

        else:
            # Can not pull from an empty priority queue. Skipped...
            log(morpy_trace_pull, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["process_pull_void"]}')

    except Exception as e:
        from lib.exceptions import MorPyException

        try:
            name: str = process_q.name
        except:
            name: str = "???"

        err_msg = f'{app_dict["loc"]["morpy"]["ProcessQueue_name"]}: {name}'
        raise MorPyException(
            morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error",
            message=err_msg
        )

    return {
        'morpy_trace': morpy_trace_pull,
        'check': check,
        'priority' : priority,
        'counter' : counter,
        'task_id' : morpy_trace["task_id"],
        'task_sys_id' : task_sys_id,
        'task': list(task),
        'is_process': is_process
    }

@metrics
def run_parallel(morpy_trace: dict, app_dict: dict, task: list=None, priority=None, task_sys_id=None) -> dict:
    r"""
    This function is takes a task from the morPy priority queue, reserves a process ID, modifies the
    morpy_trace of the task and ultimately starts the parallel process.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param task: The pulled task list
    :param priority: Integer representing task priority (lower is higher priority)
    :param task_sys_id: System ID only for internal use. Handled by
        @process_control, not used in function call.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was pulled successfully

    :example:
        # The priority, counter, task_sys_id and task arguments are passed directly to the
        # process_control decorator and are delivered by common.ProcessQueue.dequeue().

        pulled = app_dict["proc"]["morpy"]["queue"].dequeue(morpy_trace, app_dict)
        priority = pulled["priority"]
        counter = pulled["counter"]
        task_sys_id = pulled["task_sys_id"]
        task = pulled["task"]
        run_parallel(morpy_trace, app_dict, task=task, priority=priority)
    """

    import lib.fct as morpy_fct

    module: str = 'lib.mp'
    operation: str = 'run_parallel(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    id_check: bool = False
    id_search: int = 0
    process_id: int = -1
    id_err_avl: bool = False
    id_err_busy: bool = False

    try:
        if isinstance(task, tuple):
            task = list(task)
            # The 'task' provided is a tuple. Autocorrected to list.
            log_no_q(morpy_trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["morpy"]["run_parallel_task_corr"]}\n{task=}')

        # Starting process control with arguments:
        log_no_q(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["run_parallel_start_w_arg"]}:\n'
                f'morpy_trace: {morpy_trace}\n'
                f'priority: {priority}\n'
                f'task_sys_id: {task_sys_id}')

        # Fetch the maximum processes to be utilized by morPy
        processes_max = app_dict["morpy"]["orchestrator"]["processes_max"]

        if callable(task[0]):
            # Search for available process IDs and stop searching after 2x maximum processes
            while (not id_check) and (id_search <= 2 * processes_max):

                id_search += 1

                # Searching for available process ID.
                log_no_q(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["run_parallel_search_p_id"]}:\n'
                        f'id_check: {id_check}\n'
                        f'id_search: {id_search}')

                # Fetch sets for membership testing
                processes_available = app_dict["morpy"]["proc_available"]
                processes_busy = app_dict["morpy"]["proc_busy"]

                process_id = min(processes_available)

                # Membership testing / avoid conflicts during process ID fetch
                if process_id in processes_available:
                    # Pop process ID from available list
                    processes_available.remove(process_id)
                    app_dict["morpy"]["proc_available"] = processes_available
                else:
                    # Process ID conflict. Possible concurrent process creation. Process creation skipped.
                    id_err_avl = True

                # Membership testing / adding process to busy
                if process_id in processes_busy:
                    # Process ID conflict. ID# seemed available, is busy. Process creation skipped.
                    id_err_busy = True
                else:
                    # Add process ID to busy list
                    processes_busy.add(process_id)
                    app_dict["morpy"]["proc_busy"] = processes_busy

                # Processes available / processes busy
                log_no_q(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["run_parallel_proc_avl"]}:'
                        f'{app_dict["morpy"]["proc_available"]}\n'
                        f'{app_dict["loc"]["morpy"]["run_parallel_proc_busy"]}:'
                        f'{app_dict["morpy"]["proc_busy"]}')

                # Process ID conflict. A process may have terminated dirty. Process creation skipped.
                if id_err_busy or id_err_avl:
                    id_check = False
                else:
                    id_check = True

                # Process ID determined.
                log_no_q(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["run_parallel_search_iter_end"]}:\n'
                        f'id_check: {id_check}\n'
                        f'id_search: {id_search}')

            # Execute the task
            if process_id >= 0 and id_check:

                # Parallel process starting.
                log_no_q(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["run_parallel_start"]}: {process_id}')

                # Increment the total task count
                app_dict["morpy"]["orchestrator"]["task_counter"] += 1

                # Tracing update and ID assignment for the new process
                task[1].update({"process_id" : process_id})
                task[1].update({"thread_id" : 0})
                task[1].update({"task_id" : app_dict["morpy"]["orchestrator"]["task_counter"]})
                task[1].update({"tracing" : ""})

                # Remove app_dict from the task to prevent unnecessary pickling
                task[2] = {}

                # Run the task
                if task is not None:
                    # Check for remnants of old process, prevent collisions due to shelving
                    watcher(morpy_trace, app_dict, task, single_check=True)

                    p = Process(target=partial(spawn, task))
                    p.start()

                    # Create references to the process
                    proc_refs = app_dict["morpy"]["proc_refs"]
                    proc_refs.update({f'{process_id}': p.name})
                    app_dict["morpy"]["proc_refs"] = proc_refs # reassign to trigger synchronization

                    # Enqueue a process watcher
                    process_watcher = (watcher, morpy_trace, app_dict, task)
                    process_enqueue(
                        morpy_trace, app_dict, priority=priority, task=process_watcher,
                        autocorrect=False, is_process=False
                    )

            else:
                # Enqueue the task again to prevent data loss
                if task_sys_id in app_dict["proc"]["morpy"]["queue"].task_lookup:
                    # Task could not be enqueued again. Task ID still in queue. Data loss possible.
                    raise RuntimeError(
                        f'{app_dict["loc"]["morpy"]["run_parallel_requeue_err"]}\n'
                        f'{app_dict["loc"]["morpy"]["run_parallel_task_sys_id"]}: {task}\n'
                        f'{app_dict["loc"]["morpy"]["run_parallel_task"]}: {task_sys_id}')
                else:
                    app_dict["proc"]["morpy"]["queue"].enqueue(
                        morpy_trace, app_dict, priority=priority,
                        task=partial(task, morpy_trace, app_dict)
                    )

                # Could not get process ID. Task was enqueued again. Issues encountered:
                # [CONDITIONAL] Process ID conflict. Possible concurrent process creation. Process creation skipped.
                # [CONDITIONAL] Process ID conflict. ID# seemed available, is busy. Process creation skipped.
                message = f'{app_dict["loc"]["morpy"]["run_parallel_id_abort"]}'

                if id_err_avl or id_err_busy:
                    message = f'{message}\n{app_dict["loc"]["morpy"]["run_parallel_issues"]}'
                    if id_err_avl:
                        message = f'{message}\n{app_dict["loc"]["morpy"]["run_parallel_id_err_avl"]}'
                    elif id_err_busy:
                        message = f'{message}\n{app_dict["loc"]["morpy"]["run_parallel_id_err_busy"]}'
                    raise RuntimeError(message)

            # Parallel process created.
            log_no_q(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["run_parallel_exit"]}: {process_id}')

        else:
            # Task provided is not callable.
            raise ValueError(f'{app_dict["loc"]["morpy"]["run_parallel_call_err"]}\n{task[0]}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    finally:
        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

def spawn(task: list) -> dict:
    r"""
    This function registers a task in app_dict and executes it.

    :param task: Task represented by a list

    :return: dict
        morpy_trace: operation credentials and tracing information
        check: Indicates if the task was pulled successfully
        process_partial: Process to be spawned, packed with partial

    :example:
        pulled = app_dict["proc"]["morpy"]["queue"].dequeue(morpy_trace, app_dict)
        task = pulled["task"]
        p = Process(target=spawn, args=task,)
        p.start()
    """

    from lib.init import build_app_dict

    morpy_trace: dict = None
    app_dict: dict = None

    try:
        # Extract morpy_trace and app_dict (which must be provided by the parent).
        morpy_trace = task[1]
        app_dict = build_app_dict(morpy_trace)

        # Assign referenced app_dict to task (process) and run it
        task[2] = app_dict
        func, *args = task
        result = func(*args)

        # Remove own process reference
        proc_refs = app_dict["morpy"]["proc_refs"]
        proc_refs.pop(morpy_trace['process_id'], None)
        app_dict["morpy"]["proc_refs"] = proc_refs # reassign to trigger synchronization

        proc_busy = app_dict["morpy"]["proc_busy"]
        proc_busy.remove(morpy_trace['process_id'])
        app_dict["morpy"]["proc_busy"] = proc_busy # reassign to trigger synchronization

    except Exception as e:
        # Remove own process reference
        try:
            proc_refs = app_dict["morpy"]["proc_refs"]
            proc_refs.pop(morpy_trace['process_id'], None)
            app_dict["morpy"]["proc_refs"] = proc_refs # reassign to trigger synchronization

            proc_busy = app_dict["morpy"]["proc_busy"]
            proc_busy.remove(morpy_trace['process_id'])
            app_dict["morpy"]["proc_busy"] = proc_busy  # reassign to trigger synchronization
        except:
            pass

        from lib.exceptions import MorPyException
        morpy_trace["module"] = 'lib.mp'
        morpy_trace["operation"] = 'spawn(~)'
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

@metrics
def watcher(morpy_trace: dict, app_dict: dict, task: list, single_check: bool=False) -> dict:
    r"""
    Watcher function that monitors a running process based on the provided task reference. It verifies
    if the process is still active and, if so, re-enqueues itself for continued monitoring unless
    single_check is set to True. Once the process is detected to be inactive, it cleans up references
    to free the process ID and related resources, in case process was killed.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param task: Task represented by a tuple
    :param single_check: If True, watcher() will not be enqueued again.

    :example 1:
        process_watcher = (watcher, morpy_trace, app_dict, task)
        process_enqueue(
            morpy_trace, app_dict, priority=priority, task=process_watcher, autocorrect=False, is_process=False
        )

    :example 2:
        watcher(morpy_trace, app_dict, task, single_check=True)
    """

    import lib.fct as morpy_fct
    import copy
    from multiprocessing import active_children

    morpy_trace_in = copy.deepcopy(morpy_trace)
    module: str = 'lib.mp'
    operation: str = 'watcher(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    priority: int = -20
    is_active: bool = False

    try:
        active = active_children()
        task_morpy_trace: dict = task[1]
        process_id = task_morpy_trace["process_id"]

        # Check, if process is still active
        if f'{process_id}' in app_dict["morpy"]["proc_refs"].keys():
            p_name = app_dict["morpy"]["proc_refs"][f'{process_id}']

            for p in active:
                if p.name == p_name:
                    is_active = True
                    break

            # If process is still alive enqueue watcher again
            if is_active:
                # Process Watcher: Process still alive.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["watcher_is_alive"]}:\n'
                        f'{app_dict["morpy"]["proc_refs"]}',
                        verbose=True)

                if not single_check:
                    task = (watcher, morpy_trace_in, app_dict, task)
                    process_enqueue(
                        morpy_trace, app_dict, priority=priority, task=task, autocorrect=False, is_process=False
                    )

            # Clean up process references, if process is not running.
            else:
                # Process Watcher: Process ended, cleaning up.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["watcher_end"]}:\n'
                        f'{app_dict["morpy"]["proc_refs"]}',
                        verbose=True)

                # Cleanup app_dict
                proc_available = app_dict["morpy"]["proc_available"]
                if process_id not in proc_available:
                    proc_available.add(process_id)
                    app_dict["morpy"]["proc_available"] = proc_available # reassign to trigger synchronization

                proc_busy = app_dict["morpy"]["proc_busy"]
                if process_id in proc_busy:
                    proc_busy.remove(process_id)
                    app_dict["morpy"]["proc_busy"] = proc_busy # reassign to trigger synchronization

                proc_refs = app_dict["morpy"]["proc_refs"]
                proc_refs.pop(f'{process_id}', None)
                app_dict["morpy"]["proc_refs"] = proc_refs

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    finally:
        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

@metrics
def join_all_by_master(morpy_trace: dict, app_dict: dict, child_pid: int | str = None) -> dict:
    r"""
    Task for the orchestrator to join all morPy registered processes.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param child_pid: Process ID of the child process calling the function. Required filter out
        the child process, that is waiting for joining all.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was pulled successfully

    :example:
        task = (join_all_by_master, morpy_trace, app_dict, child_pid)
        process_enqueue(
            morpy_trace, app_dict, priority=0, task=task, autocorrect=False, is_process=False
    """

    module: str = 'lib.mp'
    operation: str = 'join_all_by_master(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # Make a copy of the process references to avoid race conditions.
        proc_refs: dict = copy.deepcopy(app_dict["morpy"]["proc_refs"])

        # Remove child and master process references from pool
        proc_refs.pop(str(child_pid), None)
        proc_refs.pop(str(morpy_trace["process_id"]), None)  # Should not be in the pool

        if len(proc_refs.keys()) > 0:
            # Waiting for processes to finish before transitioning app phase.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["join_all_by_master_start"]}:\n'
                    f'{app_dict["morpy"]["proc_refs"]}')

            from multiprocessing import active_children

            # Loop until all known process references have been joined.
            for p_id, p_name in proc_refs.items():
                for proc in active_children():
                    if proc.name == p_name:
                        proc.join()

                proc_refs.pop(p_id, None)

        # Signal all processes joined
        app_dict["morpy"]["proc_joined"] = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    finally:
        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

@metrics
def join_all_from_child(morpy_trace: dict, app_dict: dict, child_pid: int | str = None) -> dict:
    r"""
    Join all processes orchestrated by morPy. This can not be used, to arbitrarily join processes.
    It is tailored to be used at the end of app.init, app.run and app.exit! The function is to
    join all processes of one of the steps (init - run - exit) before transitioning into the next.

    Cleanup of process references is performed by enqueued watcher() functions.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param child_pid: Process ID of the child process calling the function. Required filter out
        the child process, that is waiting for joining all.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was pulled successfully

    :example:
        join_all_from_child(morpy_trace, app_dict)
    """

    import time

    module: str = 'lib.mp'
    operation: str = 'join_all_from_child(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # Check, if join is necessary
        if not app_dict["morpy"]["proc_joined"]:
            # Waiting for processes to finish.
            log(morpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["morpy"]["join_all_from_child_start"]}')

            # Create join-task for morPy orchestrator
            task = (join_all_by_master, morpy_trace, app_dict, child_pid)
            process_enqueue(
                morpy_trace, app_dict, priority=-1, task=task, autocorrect=False, is_process=False
            )

        # Wait for processes to join
        while not app_dict["morpy"]["proc_joined"]:
            time.sleep(0.05)    # 0.05 seconds = 50 milliseconds

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    finally:
        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

@metrics
def interrupt(morpy_trace: dict, app_dict: dict) -> dict:
    r"""
    This function sets a global interrupt flag. Processes and threads
    will halt once they pass (the most recurring) morPy functions.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was pulled successfully

    :example:
        interrupt(morpy_trace, app_dict)


    TODO finish this function
    """

    module: str = 'lib.mp'
    operation: str = 'interrupt(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # TODO check for program exit as an exit point
        #   > app_dict["global"]["morpy"]["exit"]
        pass

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    finally:
        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

def shared_dict(name: str = None, create: bool = False, shared_lock: bool = True, size: int = 100_000,
              auto_unlink: bool = False, recurse: bool = False) -> UltraDict:

    # TODO docstring
    shared_dict = UltraDict(
        name=name,
        create=create,
        shared_lock=shared_lock,
        buffer_size=size,
        full_dump_size=size,
        auto_unlink=auto_unlink,
        recurse=recurse
    )

    return shared_dict

```

## lib.msg.py

```Python
r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers functions to debug, warn and log any operations
            executed within the morPy framework. At the same time it processes
            all kinds of messaging, whether it be via console or ui.

TODO make logging a class
    > Needed to efficiently share the lock on the db
"""

import lib.fct as morpy_fct
from lib.mp import process_enqueue
from lib.common import textfile_write
from lib.decorators import metrics

import sys
import time

@metrics
def log(morpy_trace: dict, app_dict: dict, level: str, message: callable, verbose: bool) -> None:
    r"""
    This function writes an event to a specified file and/or prints it out
    according to it's severity (level).

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param level: Severity: debug/info/warning/error/critical/denied
    :param message: A callable (e.g., lambda or function) that returns the log message.
    :param verbose: If True, message is only logged in verbose mode.

    :return
        -

    :example:
        log(morpy_trace, app_dict, level, message)

    TODO Implement a mechanism to keep logfile size in check
        > Preferably auto delete logs based on "no errors occurred" per process, task, thread and __main__
    """

    morpy_trace_eval: dict = None

    try:
        # Wait for an interrupt to end
        while app_dict["morpy"]["interrupt"] == True:
            time.sleep(0.05)

        # Event handling (counting and formatting)
        log_event_dict = log_event_handler(app_dict, message, level)
        level_dict = log_event_dict["level_dict"]

        # The log level will be evaluated as long as logging or prints to console are enabled. The
        # morpy_trace may be manipulated.
        if app_dict["conf"]["msg_print"] or app_dict["conf"]["log_enable"]:
            morpy_trace_eval = log_eval(morpy_trace, app_dict, log_event_dict["level"], level_dict)

        # Retrieve a log specific datetimestamp
        time_lst = morpy_fct.datetime_now()
        datetimestamp = time_lst["datetimestamp"]
        datetime_value = time_lst["datetime_value"]

        # Prepare a passthrough dictionary for logging operations
        log_dict = {
            'level' : log_event_dict["level"],
            'verbose' : verbose,
            'datetimestamp' : datetimestamp,
            'datetime_value' : datetime_value,
            'module' : morpy_trace_eval["module"],
            'operation' : morpy_trace_eval["operation"],
            'tracing' : morpy_trace_eval["tracing"],
            'process_id' : morpy_trace_eval["process_id"],
            'thread_id' : morpy_trace_eval["thread_id"],
            'task_id' : morpy_trace_eval["task_id"],
            'message' : message,
            'log_msg_complete' : None,
            'log_enable' : morpy_trace_eval["log_enable"] ,
            'pnt_enable' : morpy_trace_eval["pnt_enable"] ,
            'interrupt_enable' : morpy_trace_eval["interrupt_enable"]
        }

        # Build the complete log message
        msg = log_msg_builder(app_dict, log_dict)
        log_dict["log_msg_complete"] = msg

        # Buffer logging parameters
        logging = app_dict["conf"]["log_enable"] and log_dict["log_enable"]
        write_log_txt = logging and app_dict["conf"]["log_txt_enable"]
        write_log_db = logging and app_dict["conf"]["log_db_enable"]
        print_log = app_dict["conf"]["msg_print"]

        if morpy_trace["process_id"] == app_dict["morpy"]["proc_master"]:
            # Go on with logging directly if calling process is orchestrator.
            log_task(morpy_trace, app_dict, log_dict, write_log_txt, write_log_db, print_log)
        else:
            # Enqueue the orchestrator task
            task = (log_task, morpy_trace, app_dict, log_dict, write_log_txt, write_log_db, print_log)
            process_enqueue(
                morpy_trace, app_dict, priority=-100, task=task, autocorrect=False, is_process=False
            )
            # Generate print required for GUIs in the regarding child process.
            if print_log:
                msg_print(morpy_trace, app_dict, log_dict)

        # Clean up
        del log_dict
        del morpy_trace

    except:
        # Severe morPy logging error.
        raise RuntimeError(f'{app_dict["loc"]["morpy"]["log_crit_fail"]}')

def log_task(morpy_trace: dict, app_dict: dict, log_dict: dict, write_log_txt: bool, write_log_db: bool,
             print_log: bool) -> None:
    r"""
    Task that finally writes the logs. May be handed to orchestrator via priority queue.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations
    :param write_log_txt: If True, log is written to textfile.
    :param write_log_db: If True, log is written to database.
    :param print_log: If True, logs are printed to console.

    :return:
        -

    :example:
        log_task(morpy_trace, app_dict, log_dict, write_log_txt, write_log_db, print_log)
    """

    if write_log_txt:
        # Write to text file - Fallback if SQLite functionality is broken
        log_txt(log_dict, app_dict, log_dict)

    if write_log_db:
        # Write to logging database
        log_db(log_dict, app_dict, log_dict)

    if print_log:
        # Print the events according to their log level
        msg_print(morpy_trace, app_dict, log_dict)

def log_eval(morpy_trace: dict, app_dict: dict, level: str, level_dict: dict) -> dict:
    r"""
    This function evaluates the log level and makes manipulation of morpy_trace
    possible for passdown only. That means, for the purpose of logging, certain
    parameters (keys) may be altered in check with mpy_param.py or other parts
    of the code to hide, extend, enable or what else is needed for a log.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param level: uppercase formatted level
    :param level_dict: Dictionary defining all possible log levels of the morPy framework

    :return morpy_trace_eval: Evaluated and/or manipulated morpy_trace
    """

    import copy

    # Deepcopy morpy_trace to manipulate it "passdown only"
    morpy_trace_eval = copy.deepcopy(morpy_trace)

    # Set defaults
    log_enable = True
    pnt_enable = True
    morpy_trace_eval["pnt_enable"] = True

    # Check, if logging is enabled globally.
    if app_dict["conf"]["log_enable"]:

        # Evaluate the log level, if it is excluded from logging.
        for lvl_nolog in app_dict["conf"]["log_lvl_nolog"]:

            if level == lvl_nolog:
                morpy_trace_eval["log_enable"] = False
                log_enable = False
                break

    else: log_enable = False

    # Check, if printing is enabled globally.
    if app_dict["conf"]["msg_print"]:

        # Evaluate the log level, if it is excluded from printing.
        for lvl_noprint in app_dict["conf"]["log_lvl_noprint"]:

            if level == lvl_noprint:
                morpy_trace_eval["pnt_enable"] = False
                pnt_enable = False
                break

    else: pnt_enable = False

    # Evaluate the log level, if it will raise an interrupt.
    for lvl_intpt in app_dict["conf"]["log_lvl_interrupts"]:

        if level == lvl_intpt:
            morpy_trace_eval["interrupt_enable"] = True
            break

    # Count occurrences per log level. Count only if relevant regarding app parameters.
    # (see mpy_param.py to alter behaviour)
    if log_enable or pnt_enable:

        app_dict["run"]["events_total"] += 1
        app_dict["run"][f'events_{level.upper()}'] += 1

    return morpy_trace_eval

def log_event_handler(app_dict: dict, message: str, level: str) -> dict:
    r"""
    This function handles the log levels by formatting and counting events.

    :param app_dict: morPy global dictionary
    :param message: The message to be logged
    :param level: Defines the log level as handed by the calling function

    :return: dict
        level - uppercase formatted level
        level_dict - Dictionary defining all possible log levels of the morPy framework
    """

    # standardizing the log level to uppercase
    level = f'{level.lower()}'

    # Log level definition. Dictionary serves the purpose of avoiding a loop over a list.
    level_dict = {
        'init' : 'init',
        'debug' : 'debug',
        'info' : 'info',
        'warning' : 'warning',
        'denied' : 'denied',
        'error' : 'error',
        'critical' : 'critical',
        'exit' : 'exit',
        'undefined' : 'undefined'
    }

    # Set logging level UNDEFINED if not part of level definition
    try: level = level_dict[level]
    except: level = 'undefined'

    return {
            'level' : level,
            'level_dict' : level_dict
            }

def log_interrupt(morpy_trace: dict, app_dict: dict) -> None:
    r"""
    This function handles the interrupt routine of morPy.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary

    :return
        -

    TODO Change the way an interrupt is displayed. Only the interrupt-raising
        process should request an input, other processes should just wait!
    """

    import lib.fct as morpy_fct

    morpy_trace: dict = morpy_fct.tracing(morpy_trace["module"], morpy_trace["operation"], morpy_trace)
    morpy_trace["log_enable"] = False

    # Set the global interrupt flag
    app_dict["morpy"]["interrupt"] = True

    # INTERRUPT <<< Press Enter to continue...
    msg_text = app_dict["loc"]["morpy"]["msg_print_intrpt"]
    log_wait_for_input(morpy_trace, app_dict, msg_text)

    # Reset the global interrupt flag
    app_dict["morpy"]["interrupt"] = False

def log_msg_builder(app_dict: dict, log_dict: dict) -> str:
    r"""
    This function formats a complete log message ready to print.

    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations

    :return msg: hand back the standardized and complete log message
    """

    # Apply standard formats
    message = log_dict["message"]

    # Format the message
    msg_indented = ''

    # Indentation
    for line in message.splitlines():
        line_indented = f'\t{line}'

        # Check, if msg_indented is an empty string
        if msg_indented:
            msg_indented = f'{msg_indented}\n{line_indented}'
        else:
            msg_indented = line_indented

    # Build the log message
    if app_dict["conf"]["msg_verbose"]:
        msg = (f'{log_dict["level"].upper()} - {log_dict["datetimestamp"]}\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_trace"]}: {log_dict["tracing"]}\n\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_process_id"]}: {log_dict["process_id"]}\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_thread_id"]}: {log_dict["thread_id"]}\n\t'
              f'{app_dict["loc"]["morpy"]["log_msg_builder_task_id"]}: {log_dict["task_id"]}\n\n'
              f'{msg_indented}\n')
    else:
        msg = f'{log_dict["level"].upper()} - {log_dict["datetimestamp"]}\n{msg_indented}\n'

    return msg

def msg_print(morpy_trace: dict, app_dict: dict, log_dict: dict) -> None:
    r"""
    This function prints logs on screen according to their log level. For
    further debugging an interrupt can be enabled for the according log
    levels.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations

    :return:
        -
    """

    # print messages according to their log level
    pnt = True

    for lvl_pnt in app_dict["conf"]["log_lvl_noprint"]:

        if log_dict["level"] == lvl_pnt:
            pnt = False
            break

    if pnt:
        print(log_dict["log_msg_complete"])
        # Enforce immediate output
        sys.stdout.flush()

    # Raise an interrupt if certain log levels are met
    if log_dict["interrupt_enable"]:
        log_interrupt(morpy_trace, app_dict)

def log_txt(morpy_trace: dict, app_dict: dict, log_dict: dict) -> None:
    r"""
    This function writes the logs into the defined textfile.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations

    :return:
        -
    """

    import lib.fct as morpy_fct

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'msg'
    operation: str = 'log_db(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
    morpy_trace["log_enable"] = False

    # Write to text file - Fallback if SQLite functionality is broken
    filepath = app_dict["conf"]["log_txt_path"]
    textfile_write(morpy_trace, app_dict, filepath, log_dict["log_msg_complete"])

def log_db(morpy_trace: dict, app_dict: dict, log_dict: dict) -> None:
    r"""
    This function writes the logs into the defined logging database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_dict: Passthrough dictionary for logging operations

    :return:
        -
    """

    import lib.fct as morpy_fct

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'msg'
    operation: str = 'log_db(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
    morpy_trace["log_enable"] = False

    # Define the table to be adressed.
    db_path = app_dict["conf"]["log_db_path"]
    table_name = f'log_{app_dict["run"]["init_loggingstamp"]}'

    check: bool = log_db_table_check(morpy_trace, app_dict, db_path, table_name)

    # Define the columns for logging and their data types.
    columns = ["level","process_id","thread_id","task_id","datetimestamp","module","operation","tracing","message"]
    col_types = ["CHAR(20)","BIGINT","BIGINT","BIGINT","DATETIME","TEXT","TEXT","TEXT","TEXT"]

    # Check, if the actual logging table already exists.
    if not check:

        # Create table for logging during runtime.
        log_db_table_create(morpy_trace, app_dict, db_path, table_name)

        # Add columns to the new log table.
        log_db_table_add_column(morpy_trace, app_dict, db_path, table_name, columns, col_types)

    # Insert the actual log into the logging database table.
    log_db_row_insert(morpy_trace, app_dict, db_path, table_name, columns, log_dict)

def log_db_connect(morpy_trace: dict, app_dict: dict, db_path: str) -> object | None:
    r"""
    This function connects to a SQLite database. The database will be
    created if it does not exist already.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered

    :return:
        conn - Connection object or None
    """

    import lib.fct as morpy_fct
    import sys, sqlite3

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'msg'
    operation: str = 'log_db_connect(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
    morpy_trace["log_enable"] = False

    try:
        conn = sqlite3.connect(db_path)

        return conn

    except Exception as e:
        from lib.exceptions import MorPyException
        msg = (
            f'{type(e).__name__}: {e}\n'
            f'{app_dict["loc"]["morpy"]["log_db_connect_excpt"]}\n'
            f'db_path: {db_path}'
        )
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error", message=msg)

def log_db_disconnect(morpy_trace: dict, app_dict: dict, db_path: str) -> None:
    r"""
    This function disconnects a SQLite database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered

    :return:
        -
    """

    import lib.fct as morpy_fct
    import sys, sqlite3

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'msg'
    operation: str = 'log_db_disconnect(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
    morpy_trace["log_enable"] = False

    conn = None
    try:
        conn = sqlite3.connect(db_path)

    except Exception as e:
        from lib.exceptions import MorPyException
        msg = (
            f'{type(e).__name__}: {e}\n'
            f'{app_dict["loc"]["morpy"]["log_db_disconnect_excpt"]}\n'
            f'db_path: {db_path}'
        )
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error", message=msg)

    finally:
        if conn:
            conn.close()

def log_db_table_create(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str) -> None:
    r"""
    This function creates a table inside a SQLite database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered
    :param table_name: Name of the database table to be created

    :return:
        -
    """

    import lib.fct as morpy_fct
    import sys

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'msg'
    operation: str = 'log_db_table_create(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
    morpy_trace["log_enable"] = False

    # Apply standard formats
    table_name = f'{table_name}'

    # Define the execution statement
    exec_statement = \
        f'CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY)'

    # Execution
    try:
        # Connect the database
        conn = log_db_connect(morpy_trace, app_dict, db_path)

        # Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

        # Create the actual table
        conn.execute(exec_statement)

        # Commit changes to the database
        conn.commit()

        # Disconnect from the database
        log_db_disconnect(morpy_trace, app_dict, db_path)

    except Exception as e:
        from lib.exceptions import MorPyException
        msg = (
            f'{type(e).__name__}: {e}\n'
            f'{app_dict["loc"]["morpy"]["log_db_table_create_excpt"]}\n'
            f'{app_dict["loc"]["morpy"]["log_db_table_create_stmt"]}: {exec_statement}'
        )
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error", message=msg)

def log_db_table_check(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str) -> bool | None:
    r"""
    This function checks on the existence of a table inside a given SQLite
    database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be addressed or altered
    :param table_name: Name of the database table to be created

    :return check: If TRUE, the table was found
    """

    import lib.fct as morpy_fct
    import sys

    module: str = 'msg'
    operation: str = 'log_db_table_check(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    morpy_trace["log_enable"] = False
    table_name = f'{table_name}'
    check: bool = False

    # Define the execution statement
    exec_statement = (f'SELECT count(name) FROM sqlite_master WHERE type=\'table\' AND name=\'{table_name}\'')

    try:
        # Connect the database
        conn = log_db_connect(morpy_trace, app_dict, db_path)

        # Activate WAL mode to acces the database
        conn.execute('pragma journal_mode=wal;')

        c = conn.cursor()

        # Check for the existence of a table
        c.execute(exec_statement)

        # Check the count of found tables
        if c.fetchone()[0] == 1:
            check: bool = True

        # Close the cursor
        c.close()

        # Disconnect from the database
        log_db_disconnect(morpy_trace, app_dict, db_path)

        return check

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

def log_db_table_add_column(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str, columns: list,
                            col_types: list) -> bool | None:
    r"""
    This function inserts a column into a table inside a given SQLite
    database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be adressed or altered
    :param table_name: Name of the database table to be created
    :param columns: List of the columns to be added
    :param col_types: List of datatypes for the columns as specified for SQLite

    :return check: If TRUE, the function was successful
    """

    import lib.fct as morpy_fct
    import sys

    module: str = 'msg'
    operation: str = 'log_db_table_add_column(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    morpy_trace["log_enable"] = False
    table_name = f'{table_name}'

    try:
        # Check the existence of the table
        check: bool = log_db_table_check(morpy_trace, app_dict, db_path, table_name)

        if check:

            # Connect the database
            conn = log_db_connect(morpy_trace, app_dict, db_path)

            # Activate WAL mode to acces the database
            conn.execute('pragma journal_mode=wal;')

            i = 0

            for col in columns:
                # Define the execution statement
                exec_statement = f'ALTER TABLE {table_name} ADD COLUMN {columns[i]} {col_types[i]}'

                # Execution
                try:
                    # Insert a new row and write to cell(s)
                    conn.execute(exec_statement)

                    # Commit changes to the database and close the cursor
                    conn.commit()

                # Error detection
                except Exception as e:
                    # The log table could not be edited.
                    raise RuntimeError(
                        f'{app_dict["loc"]["morpy"]["log_db_table_add_column_excpt"]}\n'
                        f'{app_dict["loc"]["morpy"]["log_db_table_add_column_stmt"]}: {exec_statement}'
                    )

                i += 1

            # Disconnect from the database
            log_db_disconnect(morpy_trace, app_dict, db_path)

        else:
            # The log table could not be found. Logging not possible.
            message = app_dict["log_db_table_add_column_failed"]
            log(morpy_trace, app_dict, message, 'critical')

        return check

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

def log_db_row_insert(morpy_trace: dict, app_dict: dict, db_path: str, table_name: str, columns: list,
                      log_dict: dict) -> dict[str, int | bool | None] | None:
    r"""
    This function inserts a row into a table inside a given SQLite
    database.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param db_path: Path to the db to be adressed or altered
    :param table_name: Name of the database table to be created
    :param columns: List of the columns to be added
    :param log_dict: Passthrough dictionary for logging operations

    :return: dict
        check - If TRUE, the function was successful
        row_id - ID of the row inserted
    """

    import lib.fct as morpy_fct
    import sys

    module: str = 'msg'
    operation: str = 'log_db_row_insert(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    morpy_trace["log_enable"] = False
    table_name = f'{table_name}'
    row_id = 0

    try:
        # Define the execution statement
        exec_statement = f'INSERT INTO {table_name} (\'level\',\'process_id\',\'thread_id\',\'task_id\',\'datetimestamp\',\'module\',\'operation\',\'tracing\',\'message\') VALUES (?,?,?,?,?,?,?,?,?)'

        # Check the existence of the table
        check: bool = log_db_table_check(morpy_trace, app_dict, db_path, table_name)

        if check:

            # Connect the database
            conn = log_db_connect(morpy_trace, app_dict, db_path)

            # Activate WAL mode to acces the database
            conn.execute('pragma journal_mode=wal;')

            # Execution
            try:
                c = conn.cursor()

                # Insert a new row and write to cell(s)
                c.execute(exec_statement, (
                          log_dict["level"].upper(),
                          log_dict["process_id"],
                          log_dict["thread_id"],
                          log_dict["task_id"],
                          log_dict["datetime_value"],
                          log_dict["module"],
                          log_dict["operation"],
                          log_dict["tracing"],
                          log_dict["message"]),
                          )

                # Check for the last ID
                row_id = int(c.lastrowid)

                # Commit changes to the database and close the cursor
                conn.commit()
                c.close()

            # Error detection
            except Exception as e:
                # The log entry could not be created.
                raise RuntimeError(
                    f'{app_dict["loc"]["morpy"]["log_db_row_insert_excpt"]}\n'
                    f'{app_dict["loc"]["morpy"]["log_db_row_insert_stmt"]}: {exec_statement}'
                )

            # Disconnect from the database
            log_db_disconnect(morpy_trace, app_dict, db_path)

        else:
            # The log table could not be found. Logging not possible.
            message = app_dict["log_db_row_insert_failed"]
            log(morpy_trace, app_dict, message, 'critical')

        return{
            'check' : check ,
            'row_id' : row_id
            }

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

def log_wait_for_input(morpy_trace: dict, app_dict: dict, msg_text: str) -> str | None:
    r"""
    This function makes the program wait until a user input was made.
    The user input can be returned to the calling module.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param msg_text: The text to be displayed before user input

    :return usr_input: Returns the input of the user
    """

    import lib.fct as morpy_fct
    import sys

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'msg'
    operation: str = 'log_wait_for_input(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    try:
        usr_input = input(f'{msg_text}\n')

        return usr_input

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")
```

## lib.ui_tk.py

```Python
r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module provides UI-building functions using the Tkinter.
"""

import lib.fct as morpy_fct
import lib.common as common
from lib.decorators import metrics, log

import sys
import threading, queue
import ctypes
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import TclError
from PIL import Image, ImageTk

class FileDirSelectTk:
    r"""
    A tkinter GUI for file and directory selection. Each row represents a file or directory selection.
    Optionally displays a top row of icons (display only).
    selection rows.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: morPy global dictionary containing app configurations.
    :param rows_data: Dictionary defining the selection rows.
        Expected structure:
            {
                "selection_name" : {
                    "is_dir" : True | False,  # True for directory selection, False for file selection.
                    "file_types" : (('PDF','*.pdf'), ('Textfile','*.txt'), ('All Files','*.*')),  # For file dialogs.
                    "image_path" : "path/to/image.png",  # Optional custom image.
                    "image_size" : (width, height),  # Optional; defaults to (48, 48) if not provided.
                    "default_path" : "prefilled/default/path"  # Optional prefill for the input.
                },
                ...
            }
    :param title: Title of the tkinter window. Defaults to morPy localization if not provided.
    :param icon_data: (Optional) Dictionary containing configuration for top row icons. Defaults to None.
        Expected structure:
        {
            "icon_name" : {
                "position" : 1,         # placement, order (lowest first)
                "img_path" : "path/to/image.png",     # image file path
                "icon_size" : (width, height),        # (optional) size for the icon
            },
            ...
        }

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether initialization completed without errors
        selections: Dictionary with selections made, keyed with the row name. Example:
            {"selection_name" : value}

    :example:
        import morPy

        icon_data = {
            "company_logo1" : {
                "position" : 1,                       # placement, order (lowest first)
                "img_path" : "path/to/image.png",     # image file path
            }
        }

        selection_config = {
            "file_select" : {
                "is_dir" : False,
                "file_types" : (('Textfile','*.txt'), ('All Files','*.*')),
                "default_path" : "prefilled/default/path"
            },
            "dir_select" : {
                "is_dir" : True,
                "default_path" : "prefilled/default/path"
            }
        }

        gui = morPy.FileDirSelectTk(morpy_trace, app_dict, rows_data, title="Select...")
        results = gui.run(morpy_trace, app_dict)["selections"]
        file = results["file_selected"]
        dir = results["dir_selected"]
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, rows_data: dict, title: str = None,
                 icon_data: dict = None):
        r"""
        Initializes the GUI for grid of image tiles.

        In order to get metrics for __init__(), call helper method _init()
        for the @metrics decorator to work. It relies on the returned
        {'morpy_trace' : morpy_trace}, which __init__() can not do (needs to be None).

        :param: See ._init() for details

        :return: self
        """

        module: str = 'ui_tk'
        operation: str = 'FileDirSelectTk.__init__(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        try:
            self._init(morpy_trace, app_dict, rows_data, title=title, icon_data=icon_data)

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    @metrics
    def _init(self, morpy_trace: dict, app_dict: dict, rows_data: dict, title: str = None,
                 icon_data: dict = None):
        r"""
        A tkinter GUI for file and directory selection. Each row represents a file or directory selection.
        Optionally displays a top row of icons (display only).
        selection rows.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: morPy global dictionary containing app configurations.
        :param rows_data: Dictionary defining the selection rows.
            Expected structure:
                {
                    "selection_name" : {
                        "is_dir" : True | False,  # True for directory selection, False for file selection.
                        "file_types" : (('PDF','*.pdf'), ('Textfile','*.txt'), ('All Files','*.*')),  # For file dialogs.
                        "image_path" : "path/to/image.png",  # Optional custom image.
                        "image_size" : (width, height),  # Optional; defaults to (48, 48) if not provided.
                        "default_path" : "prefilled/default/path"  # Optional prefill for the input.
                    },
                    ...
                }
        :param title: Title of the tkinter window. Defaults to morPy localization if not provided.
        :param icon_data: (Optional) Dictionary containing configuration for top row icons. Defaults to None.
            Expected structure:
            {
                "icon_name" : {
                    "position" : 1,         # placement, order (lowest first)
                    "img_path" : "path/to/image.png",     # image file path
                    "icon_size" : (width, height),        # (optional) size for the icon
                },
                ...
            }

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
            selections: Dictionary with selections made, keyed with the row name. Example:
                {"selection_name" : value}

        :example:
            import morPy

            icon_data = {
                "company_logo1" : {
                    "position" : 1,                       # placement, order (lowest first)
                    "img_path" : "path/to/image.png",     # image file path
                }
            }

            selection_config = {
                "file_select" : {
                    "is_dir" : False,
                    "file_types" : (('Textfile','*.txt'), ('All Files','*.*')),
                    "default_path" : "prefilled/default/path"
                },
                "dir_select" : {
                    "is_dir" : True,
                    "default_path" : "prefilled/default/path"
                }
            }

            gui = morPy.FileDirSelectTk(morpy_trace, app_dict, rows_data, title="Select...")
            results = gui.run(morpy_trace, app_dict)["selections"]
            file = results["file_selected"]
            dir = results["dir_selected"]
        """

        module: str = 'ui_tk'
        operation: str = 'FileDirSelectTk._init(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Try to make the process DPI-aware
            # TODO port into os-class instead of hardcoding and make sure that each spawn will run this.
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass

            self.rows_data = rows_data
            self.title = title if title else app_dict["loc"]["morpy"]["FileDirSelectTk_title"]

            if icon_data:
                self.icon_data = icon_data
            else:
                self.icon_data = {
                "app_banner" : {
                    "position" : 1,
                    "img_path" : app_dict["conf"]["app_banner"],
                    "icon_size" : (214, 48)
                }
            }

            # Set default icon size
            icon_dim = int(app_dict["sys"]["resolution_height"] // 64)
            self.default_icon_size = (icon_dim, icon_dim)

            # Set default entry width
            entry_dim = int(app_dict["sys"]["resolution_height"] // 24)
            self.default_entry_width = entry_dim

            # Set default link size
            link_dim = int(app_dict["sys"]["resolution_height"] // 48)
            self.default_link_size = (link_dim, link_dim)

            self.selections = {}  # Will hold the final user inputs keyed by row name.

            # Dictionary to hold references to PhotoImage objects.
            self._photos = {}
            self.app_dict = app_dict

            # Create the main tkinter window.
            self.root = tk.Tk()
            self.root.iconbitmap(app_dict["conf"]["app_icon"])
            self.root.title(self.title)
            # Allow the window to be resizable.
            self.root.resizable(True, True)

            # Build the UI.
            self._setup_ui(morpy_trace, app_dict)

            # Calculate coordinates for the window to be centered.
            x = (int(app_dict["sys"]["resolution_width"]) // 2) - (self.frame_width // 2)
            y = (int(app_dict["sys"]["resolution_height"]) * 2 // 5) - (self.frame_height // 2)
            self.root.geometry(f'{self.frame_width}x{self.frame_height}+{x}+{y}')

            # Bind the _on_close() method to closing the window
            self.root.protocol("WM_DELETE_WINDOW", lambda: self._on_close(morpy_trace, app_dict))

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        finally:
            return {
                "morpy_trace" : morpy_trace,
                "check" : check
            }

    def _setup_ui(self, morpy_trace: dict, app_dict: dict):
        r"""
        Constructs the grid layout with the provided configuration.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module: str = 'ui_tk'
        operation: str = 'FileDirSelectTk._setup_ui(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Optional top icon row.
            if self.icon_data:
                icon_frame = tk.Frame(self.root)
                icon_frame.pack(fill='x', anchor='e', padx=20, pady=(20, 10))
                if hasattr(Image, "Resampling"):
                    resample_filter = Image.Resampling.LANCZOS
                else:
                    resample_filter = Image.ANTIALIAS

                for icon_name, config in sorted(self.icon_data.items(),
                                                key=lambda item: item[1].get("position", 0)):
                    img_path = morpy_fct.pathtool(config.get("img_path"))["out_path"]
                    icon_size = config.get("icon_size", self.default_icon_size)

                    try:
                        img = Image.open(img_path)
                    except Exception as e:
                        raise RuntimeError(
                            f'{app_dict["loc"]["morpy"]["FileDirSelectTk_img_fail"]}\n'
                            f'Icon {icon_name}: {img_path}'
                        )

                    img = img.resize(icon_size, resample_filter)
                    photo = ImageTk.PhotoImage(img)
                    self._photos[icon_name] = photo
                    lbl = tk.Label(icon_frame, image=photo)
                    lbl.pack(side=tk.RIGHT, padx=5)

            # Create a frame to contain all selection rows.
            rows_container = tk.Frame(self.root)
            rows_container.pack(fill='both', expand=True, padx=20, pady=20)

            # For each selection row, create a container frame.
            self.row_widgets = {}  # To store per-row widgets.
            for row_name, config in self.rows_data.items():
                # Container for a single row (including its optional description).
                row_container = tk.Frame(rows_container)
                row_container.pack(fill='x', pady=10)

                # If a description is provided in the config, create a descriptive headline.
                if config.get("description"):
                    desc_label = tk.Label(row_container, text=config["description"], font=("Arial", 8))
                    desc_label.pack(anchor='w', pady=(0, 5))

                # Create a frame for the input widgets (entry and button) in this row.
                row_frame = tk.Frame(row_container)
                row_frame.pack(fill='x')

                # Entry widget.
                entry = tk.Entry(row_frame, width=self.default_entry_width)
                default_path = ''  # or config.get("default_path", "")
                entry.insert(0, default_path)
                entry.pack(side=tk.LEFT, fill='x', expand=True, padx=(0, 10))
                self.row_widgets[row_name] = {"entry": entry}

                # Determine which image to display.
                custom_img = config.get("image_path")
                image_size = config.get("image_size", self.default_link_size)

                # If no custom image is provided, use a default icon.
                if not custom_img:
                    if config.get("is_dir", False):
                        custom_img = morpy_fct.pathtool(f'{app_dict["conf"]["main_path"]}\\res\\icons\\dir_open.png')["out_path"]
                    else:
                        custom_img = morpy_fct.pathtool(f'{app_dict["conf"]["main_path"]}\\res\\icons\\file_open.png')["out_path"]

                # Load the image.
                try:
                    img_path = morpy_fct.pathtool(custom_img)["out_path"]
                    img = Image.open(img_path)
                except Exception as e:
                    # Failed to load image.
                    raise RuntimeError(
                        f'{app_dict["loc"]["morpy"]["FileDirSelectTk_img_fail"]}\n'
                        f'{app_dict["loc"]["morpy"]["FileDirSelectTk_row_name"]}: {row_name}\n'
                        f'{app_dict["loc"]["morpy"]["FileDirSelectTk_img"]}: {custom_img}'
                    )

                if image_size:
                    img = img.resize(image_size, resample_filter if "resample_filter" in locals() else Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                self._photos[row_name] = photo  # Keep a reference.

                # Button to trigger the selection dialog.
                btn = tk.Button(row_frame, image=photo,
                                command=lambda rn=row_name, cfg=config: self._on_select(morpy_trace, app_dict, rn, cfg))
                btn.pack(side=tk.RIGHT)
                self.row_widgets[row_name]["button"] = btn

            # At the bottom, add a confirmation button.
            confirm_btn = ttk.Button(self.root, text=f'{app_dict["loc"]["morpy"]["FileDirSelectTk_confirm"]}',
                                     command=lambda: self._on_confirm(morpy_trace, app_dict))
            confirm_btn.pack(pady=(10, 20))

            # Update frame dimensions.
            self.root.update_idletasks()  # Process pending geometry updates
            self.frame_width = self.root.winfo_width()
            self.frame_height = self.root.winfo_height()

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        finally:
            return {
                "morpy_trace": morpy_trace,
                "check": check
            }

    def _on_select(self, morpy_trace: dict, app_dict: dict, row_name: str, config: dict):
        r"""
        Callback for a selection row button. Opens a file or directory dialog based on the "is_dir" flag.
        Updates the corresponding Entry widget with the chosen path.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module: str = 'ui_tk'
        operation: str = 'FileDirSelectTk._on_select(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = True

        try:
            if config.get("is_dir", False):
                # Directory selection.
                description = config.get("description", app_dict["loc"]["morpy"]["dialog_sel_dir_select"])
                init_dir = config.get("default_path", app_dict["conf"]["data_path"])

                path = dialog_sel_dir(morpy_trace, app_dict, init_dir=init_dir, title=description)["dir_path"]

            else:
                # File selection.
                file_types = config.get("file_types", (("All Files", "*.*"),))
                description = config.get("description", app_dict["loc"]["morpy"]["dialog_sel_file_select"])
                init_dir = config.get("default_path", app_dict["conf"]["data_path"])

                path = dialog_sel_file(morpy_trace, app_dict, init_dir=init_dir, file_types=file_types,
                                       title=description)["file_path"]

            if path:
                # Update the entry.
                self.row_widgets[row_name]["entry"].delete(0, tk.END)
                self.row_widgets[row_name]["entry"].insert(0, path)

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        finally:
            return {
                "morpy_trace": morpy_trace,
                "check": check
            }

    def _on_confirm(self, morpy_trace: dict, app_dict: dict):
        r"""
        Callback for the confirm button. Reads all the entries and stores them in self.selections.
        Then, quits the main loop.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module: str = 'ui_tk'
        operation: str = 'FileDirSelectTk._on_confirm(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            for row_name, widgets in self.row_widgets.items():
                self.selections[row_name] = widgets["entry"].get()
            self.root.quit()

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        finally:
            return {
                "morpy_trace": morpy_trace,
                "check": check
            }

    @metrics
    def _on_close(self, morpy_trace: dict, app_dict: dict):
        r"""
        Close or abort the GUI.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._on_close(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'FileDirSelectTk._on_close(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            self.root.quit()

            # Initiate program exit
            app_dict["morpy"]["exit"] = True

            # Release the global interrupts
            app_dict["morpy"]["interrupt"] = False

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    def run(self, morpy_trace: dict, app_dict: dict):
        r"""
        Launches the GUI and waits for the user to complete the selection.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
            selections: A dictionary of user inputs keyed by row name.
        """

        module: str = 'ui_tk'
        operation: str = 'FileDirSelectTk.run(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            self.root.mainloop()
            # After mainloop, destroy the window.
            self.root.destroy()

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        finally:
            return {
                "morpy_trace": morpy_trace,
                "check": check,
                "selections": self.selections
            }

class GridChoiceTk:
    r"""
    A tkinter GUI displaying a dynamic grid of image tiles. Each tile shows an image
    with a text label below it. Clicking a tile returns its associated value.

    :param morpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param tile_data: Dictionary containing configuration for each tile.
        The expected structure is:
        {
            "tile_name" : {
                "row_column" : (row, column),         # grid placement
                "img_path" : "path/to/image.png",     # image file path
                "text" : "Descriptive text",          # label under the image
                "return_value" : some_value,          # value returned when clicked
                "tile_size" : (width, height),        # (optional) size for the image tile
            },
            ...
        }
    :param title: Title of the tkinter window. Defaults to morPy localization.
    :param default_tile_size: Default (width, height) if a tile does not specify its own size. Defaults to
                              a fraction of main monitor height.
    :param icon_data: (Optional) Dictionary containing configuration for top row icons. Defaults to None.
        Expected structure:
        {
            "icon_name" : {
                "position" : 1,         # placement, order (lowest first)
                "img_path" : "path/to/image.png",     # image file path
                "icon_size" : (width, height),        # (optional) size for the icon
            },
            ...
        }

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether initialization completed without errors

    :example:
        import morPy

        icon_data = {
            "company_logo1" : {
                "position" : 1,                       # placement, order (lowest first)
                "img_path" : "path/to/image.png",     # image file path
            }
        }

        tile_data = {
            "start" : {
                "row_column" : (row, column),
                "img_path" : "path/to/image.png",
                "text" : "Start the App",
                "return_value" : 1,
            },
            ...
        }
        gui = morPy.GridChoiceTk(morpy_trace, app_dict, tile_data,
            title="Start Menu",
            default_tile_size=(128, 128),
            icon_data=icon_data
        )
        result = gui.run(morpy_trace, app_dict)["choice"]
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, tile_data: dict, title: str=None,
                 default_tile_size: tuple=None, icon_data: dict=None):
        r"""
        Initializes the GUI for grid of image tiles.

        In order to get metrics for __init__(), call helper method _init()
        for the @metrics decorator to work. It relies on the returned
        {'morpy_trace' : morpy_trace}, which __init__() can not do (needs to be None).

        :param: See ._init() for details

        :return: self
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk.__init__(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        try:
            self._init(morpy_trace, app_dict, tile_data, title=title, default_tile_size=default_tile_size,
                       icon_data=icon_data)

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    @metrics
    def _init(self, morpy_trace: dict, app_dict: dict, tile_data: dict, title: str=None,
              default_tile_size: tuple=None, icon_data: dict=None):
        r"""
        A tkinter GUI displaying a dynamic grid of image tiles. Each tile shows an image
        with a text label below it. Clicking a tile returns its associated value.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param tile_data: Dictionary containing configuration for each tile.
            The expected structure is:
            {
                "tile_name" : {
                    "row_column" : (row, column),         # grid placement
                    "img_path" : "path/to/image.png",     # image file path
                    "text" : "Descriptive text",          # label under the image
                    "return_value" : some_value,          # value returned when clicked
                    "tile_size" : (width, height),        # (optional) size for the image tile
                },
                ...
            }
        :param title: Title of the tkinter window. Defaults to morPy localization.
        :param default_tile_size: Default (width, height) if a tile does not specify its own size. Defaults to
                                  a fraction of main monitor height.
        :param icon_data: (Optional) Dictionary containing configuration for top row icons. Defaults to None.
            Expected structure:
            {
                "icon_name" : {
                    "position" : 1,         # placement, order (lowest first)
                    "img_path" : "path/to/image.png",     # image file path
                    "icon_size" : (width, height),        # (optional) size for the icon
                },
                ...
            }

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            import morPy

            icon_data = {
                "company_logo1" : {
                    "position" : 1,                       # placement, order (lowest first)
                    "img_path" : "path/to/image.png",     # image file path
                }
            }

            tile_data = {
                "start" : {
                    "row_column" : (row, column),
                    "img_path" : "path/to/image.png",
                    "text" : "Start the App",
                    "return_value" : 1,
                },
                ...
            }
            gui = morPy.GridChoiceTk(morpy_trace, app_dict, tile_data,
                title="Start Menu",
                default_tile_size=(128, 128),
                icon_data=icon_data
            )
            result = gui.run(morpy_trace, app_dict)["choice"]
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk.__init__(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Try to make the process DPI-aware
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass

            self.tile_data = tile_data
            self.title = title if title else app_dict["loc"]["morpy"]["GridChoiceTk_title"]

            # Set default tile size
            tile_dim = int(app_dict["sys"]["resolution_height"] // 8)
            self.default_tile_size = (tile_dim, tile_dim)

            if icon_data:
                self.icon_data = icon_data
            else:
                self.icon_data = {
                "app_banner" : {
                    "position" : 1,
                    "img_path" : app_dict["conf"]["app_banner"],
                    "icon_size" : (214, 48)
                }
            }

            # Set default icon size
            icon_dim = int(app_dict["sys"]["resolution_height"] // 64)
            self.default_icon_size = (icon_dim, icon_dim)

            self.choice = None
            self.frame_width = 0
            self.frame_height = 0

            # Create the main tkinter window.
            self.root = tk.Tk()
            self.root.iconbitmap(app_dict["conf"]["app_icon"])
            self.root.title(self.title)

            # A dictionary to keep references to PhotoImage objects. Prevents garbage collection of images.
            self._photos = {}

            self._setup_ui(morpy_trace, app_dict)

            # Calculate coordinates for the window to be centered.
            x = (int(app_dict["sys"]["resolution_width"]) // 2) - (self.frame_width // 2)
            y = (int(app_dict["sys"]["resolution_height"]) * 2 // 5) - (self.frame_height // 2)
            self.root.geometry(f'{self.frame_width}x{self.frame_height}+{x}+{y}')

            # Bind the _on_close() method to closing the window
            self.root.protocol("WM_DELETE_WINDOW", lambda: self._on_close(morpy_trace, app_dict))

            # Fix the frame size, since it's contents do not resize.
            self.root.resizable(False, False)

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        finally:
            return {
                "morpy_trace" : morpy_trace,
                "check" : check,
            }

    def _setup_ui(self, morpy_trace: dict, app_dict: dict):
        r"""
        Constructs the grid layout with the provided tile data.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._setup_ui(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # If icon_data is provided, create a top row for icons.
            if self.icon_data:
                # Create a frame for the icons (placed at the top of the window).
                icon_frame = tk.Frame(self.root)
                icon_frame.pack(fill='x', anchor='e', padx=20, pady=(20, 10))  # extra top padding if desired

                # Determine the resampling filter (same as for tiles).
                if hasattr(Image, "Resampling"):
                    resample_filter = Image.Resampling.LANCZOS
                else:
                    resample_filter = Image.ANTIALIAS

                # Process icons in sorted order (using the "position" value).
                for icon_name, config in sorted(self.icon_data.items(),
                                                  key=lambda item: item[1].get("position", 0)):
                    img_path = morpy_fct.pathtool(config.get("img_path"))["out_path"]
                    # If an icon size is provided, use it; else, use a reasonable default (e.g. same as tile size)
                    icon_size = config.get("icon_size", self.default_icon_size)
                    try:
                        img = Image.open(img_path)
                    except Exception as e:
                        raise RuntimeError(
                            f'{app_dict["loc"]["morpy"]["GridChoiceTk_img_fail"]}\n'
                            f'{app_dict["loc"]["morpy"]["GridChoiceTk_path"]}: {img_path}\n'
                            f'{app_dict["loc"]["morpy"]["GridChoiceTk_tile"]}: {icon_name}'
                        )
                    if icon_size:
                        img = img.resize(icon_size, resample_filter)
                    photo = ImageTk.PhotoImage(img)
                    self._photos[icon_name] = photo  # Prevent garbage collection

                    # Create a label to display the icon.
                    lbl = tk.Label(icon_frame, image=photo)
                    lbl.pack(side=tk.RIGHT, padx=5)

            # Create the container for the grid of tiles.
            container = tk.Frame(self.root)
            container.pack(padx=10, pady=10)

            for tile_name, config in self.tile_data.items():
                row, column = config.get("row_column", (0, 0))
                img_path = morpy_fct.pathtool(config.get("img_path"))["out_path"]
                text = config.get("text", "")
                return_value = config.get("return_value")
                tile_size = config.get("tile_size", self.default_tile_size)

                # Create a frame for this tile.
                tile_frame = tk.Frame(container)
                tile_frame.grid(row=row, column=column, padx=10, pady=10)

                # Determine the appropriate resampling filter.
                if hasattr(Image, "Resampling"):
                    resample_filter = Image.Resampling.LANCZOS
                else:
                    resample_filter = Image.ANTIALIAS

                # Load and resize the image.
                try:
                    img = Image.open(img_path)
                except Exception as e:
                    # Failed to load image.
                    raise RuntimeError(
                        f'{app_dict["loc"]["morpy"]["GridChoiceTk_img_fail"]}\n'
                        f'{app_dict["loc"]["morpy"]["GridChoiceTk_path"]}: {img_path}\n'
                        f'{app_dict["loc"]["morpy"]["GridChoiceTk_tile"]}: {tile_name}'
                    )

                img = img.resize(tile_size, resample_filter)
                photo = ImageTk.PhotoImage(img)
                self._photos[tile_name] = photo  # Save a reference to avoid garbage collection.

                # Create a button with the image.
                btn = tk.Button(tile_frame, image=photo,
                                command=lambda val=return_value: self._on_select(morpy_trace, app_dict, val))
                btn.pack()

                # Create a label below the image.
                lbl = tk.Label(tile_frame, text=text, font=("Arial", 8, "bold"))
                lbl.pack(pady=(5, 0))

                # Update frame dimensions.
                self.root.update_idletasks()  # Process pending geometry updates
                self.frame_width = self.root.winfo_width()
                self.frame_height = self.root.winfo_height()

                check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        finally:
            return {
                "morpy_trace" : morpy_trace,
                "check" : check,
            }

    def _on_select(self, morpy_trace: dict, app_dict: dict, value):
        r"""
        Callback when a tile is clicked. Sets the selected value and quits the mainloop.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param value: Selected value relating to the clicked tile.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._on_select(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            self.choice = value
            self.root.quit()

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        finally:
            return {
                "morpy_trace" : morpy_trace,
                "check" : check,
            }

    @metrics
    def _on_close(self, morpy_trace: dict, app_dict: dict):
        r"""
        Close or abort the GUI.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._on_close(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'GridChoiceTk._on_close(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            self.root.quit()

            # Initiate program exit
            app_dict["morpy"]["exit"] = True

            # Release the global interrupts
            app_dict["morpy"]["interrupt"] = False

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    def run(self, morpy_trace: dict, app_dict: dict):
        r"""
        Launches the GUI and waits for the user to make a selection.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
            choice: The value associated with the selected tile.

        :example:
            import morPy

            tile_data = {
                "start" : {
                    "row_column" : (row, column),
                    "img_path" : "path/to/image.png",
                    "text" : "Start the App",
                    "return_value" : 1,
                },
                ...
            }
            gui = morPy.GridChoiceTk(morpy_trace, app_dict, tile_data,
                title="Start Menu",
                default_tile_size=(128, 128),
            )
            result = gui.run(morpy_trace, app_dict)["choice"]
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk.run(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            self.root.mainloop()
            self.root.destroy()

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        finally:
            return {
                "morpy_trace" : morpy_trace,
                "check" : check,
                "choice" : self.choice
            }

class ProgressTrackerTk:
    r"""
    A progress tracking GUI using tkinter to visualize the progress of a background task. The GUI can
    be adjusted with the arguments during construction.

    :param morpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param frame_title: Window frame title as shown in the title bar.
        :param frame_width: Frame width in pixels.
                            Defaults to 1/3rd of main monitor width.
    :param frame_height: Frame height in pixels.
                         Defaults to a value depending on which widgets are displayed.
    :param headline_total: Descriptive name for the overall progress.
                           Defaults to morPy localization.
    :param headline_font_size: Font size for both, overall and stage descriptive names.
                               Defaults to 10.
    :param detail_description_on: If True, a widget for the detail messages will be drawn to GUI.
                                  Defaults to False.
    :param description_font_size: Font size for description/status.
                                  Defaults to 8.
    :param font: Font to be used in the GUI, except for the title bar and console widget.
                 Defaults to "Arial".
    :param stages: Sum of stages until complete. Will not show progress bar for overall progress if equal to 1.
                   Defaults to 1.
    :param console: If True, will reroute console output to GUI.
                    Defaults to False.
    :param auto_close: If True, window automatically closes at 100%. If False, user must click "Close".
                       Defaults to False.
    :param work: A callable (e.g. functools.partial()). Will run in a new thread.

    :methods:
        .run(morpy_trace: dict, app_dict: dict)
            Start the GUI main loop.

        .begin_stage(self, morpy_trace: dict, app_dict: dict, stage_limit: (int, float) = 1, headline_stage: str = None,
                    detail_description: str=None)
            Start a new stage of progress. Will set the stage prior to 100%, if
            not already the case.

            :param stage_limit: This is the maximum value of the stage progress. Set it to 0 to turn off the stage progress.
                                It represents the maximum value the stage progress will reach until 100%, which is
                                determined by which value you choose to increment the progress with (defaults to 1 per
                                increment). A value of 10 for example amounts to 10% per increment.
                                Defaults to 1.
            :param headline_stage: Descriptive name for the actual stage.
                                   Defaults to morPy localization.
            :param detail_description: Description or status. Will
                                       not be shown if None at construction.
                                       Defaults to None.
            :param ticks: [optional] Percentage of total to log the progress. I.e. at ticks=10.7 at every
                          10.7% progress exceeded the exact progress will be logged. Defaults to 0.01.

        .update_progress(morpy_trace: dict, app_dict: dict, current: float = None, stage_limit: int = None)
            Update stage progress & overall progress. If overall hits 100% and auto_close=True, close window. Else,
            switch button text to "Close" and stop console redirection. Enqueues a UI request for the
            main thread to process. Safe to call from any thread.

            :param current: Current progress count. If None, each call of this method will add +1
                to the progress count. Defaults to None.

        .update_text(morpy_trace: dict, app_dict: dict, headline_total: str = None, headline_stage: str = None,
                    detail_description: str = None)
            Update the headline texts or description at runtime. Enqueues a UI request for the
            main thread to process. Safe to call from any thread.

            :param headline_total: If not None, sets the overall progress headline text.
            :param headline_stage: If not None, sets the stage progress headline text.
            :param detail_description: If not None, sets the description text beneath the stage headline.

        .end_stage(self, morpy_trace: dict, app_dict: dict)
            End the current stage by setting it to 100%.

    :example:
        from functools import partial
        import time

        # Define a function or method to be progress tracked. It will be executed in a new thread, because
        # tkinter needs to run in main thread. The argument "gui" will be referenced automatically by the
        # GUI, no explicit assignment is needed.
        def my_func(morpy_trace, app_dict, gui=None):
            outer_loop_count = 2 # Amount stages, i.e. folders to walk
            inner_loop_count = 10 # Increments in the stage, i.e. files modified

            if gui:
                gui.update_text(morpy_trace, app_dict, headline_total=f'My Demo')

            # Loop to demo amount of stages
            for i in range(outer_loop_count):
                # Begin a stage
                headline = "Currently querying"
                description = "Starting stage..."
                progress.begin_stage(morpy_trace, app_dict, stage_limit=inner_loop_count, headline_stage=headline,
                                     detail_description=description)

                # Update Headline for overall progress
                if gui:
                    gui.update_text(morpy_trace, app_dict, headline_stage=f'Stage {i}')

                time.sleep(.5) # Wait time, so progress can be viewed (mocking execution time)

                # Loop to demo stage progression
                for j in range(1, inner_loop_count + 1):
                    time.sleep(.2) # Wait time, so progress can be viewed (mocking execution time)

                    # Update progress and text for actual stage
                    if gui:
                        gui.update_text(morpy_trace, app_dict, detail_description=f'This describes progress no. {j} of the stage.')
                        gui.update_progress(morpy_trace, app_dict)

        if name == "__main__":
            # Run function with GUI. For full customization during construction see the
            # ProgressTrackerTk.__init__() description.

            # Define a callable to be progress tracked
            work = partial(my_func, morpy_trace, app_dict)

            # Construct the GUI
            gui = morPy.ProgressTrackerTk(morpy_trace, app_dict,
                frame_title="My Demo Progress GUI",
                stages=2,
                detail_description_on=True,
                work=work)

            # Start GUI in main thread and run "work" in separate thread
            gui.run(morpy_trace, app_dict)
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, frame_title: str=None, frame_width: int=None,
              frame_height: int=None, headline_total: str=None, headline_font_size: int=10,
              detail_description_on: bool=False, description_font_size: int=8, font: str="Arial",
              stages: int=1, console: bool=False, auto_close: bool=False, work=None):
        r"""
        Initializes the GUI with progress tracking.

        In order to get metrics for __init__(), call helper method _init()
        for the @metrics decorator to work. It relies on the returned
        {'morpy_trace' : morpy_trace}, which __init__() can not do (needs to be None).

        :param: See ._init() for details

        :return: self
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk.__init__(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        try:
            self._init(morpy_trace, app_dict, frame_title=frame_title, frame_width=frame_width,
                       frame_height=frame_height, headline_total=headline_total, headline_font_size=headline_font_size,
                       detail_description_on=detail_description_on, description_font_size=description_font_size,
                       font=font, stages=stages, console=console, auto_close=auto_close, work=work)

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    @metrics
    def _init(self, morpy_trace: dict, app_dict: dict, frame_title: str=None, frame_width: int=None,
              frame_height: int=None, headline_total: str=None, headline_font_size: int=10,
              detail_description_on: bool=False, description_font_size: int=8, font: str="Arial",
              stages: int=1, console: bool=False, auto_close: bool=False, work=None):
        r"""
        Initializes the GUI with progress tracking.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param frame_title: Window frame title as shown in the title bar.
        :param frame_width: Frame width in pixels.
                            Defaults to 1/3rd of main monitor width.
        :param frame_height: Frame height in pixels.
                             Defaults to a value depending on which widgets are displayed.
        :param headline_total: Descriptive name for the overall progress.
                               Defaults to morPy localization.
        :param headline_font_size: Font size for both, overall and stage descriptive names.
                                   Defaults to 10.
        :param detail_description_on: If True, a widget for the detail messages will be drawn to GUI.
                                      Defaults to False.
        :param description_font_size: Font size for description/status.
                                      Defaults to 8.
        :param font: Font to be used in the GUI, except for the title bar and console widget.
                     Defaults to "Arial".
        :param stages: Sum of stages until complete. Will not show progress bar for overall progress if equal to 1.
                       Defaults to 1.
        :param ticks: [optional] Percentage of total to log the progress. I.e. at ticks=10.7 at every
                      10.7% progress exceeded the exact progress will be logged. Defaults to 0.01.
        :param console: If True, will reroute console output to GUI.
                        Defaults to False.
        :param auto_close: If True, window automatically closes at 100%. If False, user must click "Close".
                           Defaults to False.
        :param work: A callable (e.g. functools.partial()). Will run in a new thread.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            gui = morPy.ProgressTrackerTk(morpy_trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Generic Progress stage",
                stages=outer_loop_count,
                stage_limit=inner_loop_count,
                work=work)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._init(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        self.frame_height_sizing = False
        self.height_factor_headlines = 0
        self.height_factor_description = 0

        try:
            # Try to make the process DPI-aware
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass

            self.console_on = console
            self.auto_close = auto_close
            self.done = False  # Will be True once overall progress is 100%
            self.main_loop_interval = 50 # ms, how often we do the main loop

            # Default texts
            self.frame_title = (app_dict["loc"]["morpy"]["ProgressTrackerTk_prog"]
                                if not frame_title else frame_title)
            self.frame_width = frame_width
            self.headline_total_nocol = (f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_overall"]}'
                             if not headline_total else f'{headline_total}')
            self.detail_description_on = detail_description_on
            self.headline_font_size = headline_font_size
            self.description_font_size = description_font_size
            self.font = font
            self.button_text_abort = f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_abort"]}'
            self.button_text_close = f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_close"]}'

            self.ui_calls = queue.Queue()  # Queue for collecting UI update requests from background thread

            # Progress tracking
            self.stages = stages

            self.stages_finished = 0
            self.overall_progress_abs = 0

            # Set frame width
            if not frame_width:
                sys_width = int(app_dict["sys"]["resolution_width"])
                self.frame_width = sys_width // 3
            else:
                self.frame_width = frame_width

            # Calculate factors for frame height
            sys_height = int(app_dict["sys"]["resolution_height"])
            height_factor = sys_height * .03125 # Height of main monitor * 32dpi // 1024px
            if not frame_height:
                self.frame_height = 0
                self.frame_height_sizing = True
                self.height_factor_headlines = round(height_factor * self.headline_font_size / 10)
                self.height_factor_description = round(height_factor * self.description_font_size / 10)
            else:
                self.frame_height = frame_height
                self.frame_height_sizing = False

            # Overall progress bar
            if self.stages > 1:
                self.overall_progress_on = True

                # Set fraction of overall progress per stage
                self.fraction_per_stage  = 100.0 / self.stages

                # Add height for overall progress bar
                if self.frame_height_sizing:
                    self.frame_height += self.height_factor_headlines

                # Construct the overall progress tracker
                self.overall_progress_tracker = common.ProgressTracker(
                    morpy_trace, app_dict, description=self.headline_total_nocol, total=self.stages, ticks=.01,
                    verbose=True
                )

                # Finalize overall headline
                self.headline_total = f'{self.headline_total_nocol}:'
            else:
                self.overall_progress_on = False

            # Add height for stage progress bar
            if self.frame_height_sizing:
                self.frame_height += self.height_factor_headlines

            # Detail description
            if self.detail_description_on:
                # Add height for description of latest update
                if self.frame_height_sizing:
                    self.frame_height += self.height_factor_description

            # For capturing prints
            self.console_queue = None  # Always define, even if console_on=False
            if self.console_on:
                self.console_queue = queue.Queue()

                # Add frame height for console
                if self.frame_height_sizing:
                    self.frame_height += app_dict["sys"]["resolution_height"] // 2

            # Calculate coordinates for the window to be centered.
            x = (int(app_dict["sys"]["resolution_width"]) // 2) - (self.frame_width // 2)
            y = (int(app_dict["sys"]["resolution_height"]) * 2 // 5) - (self.frame_height // 2)

            # Tk window
            self.root = tk.Tk()
            self.root.iconbitmap(app_dict["conf"]["app_icon"])
            self.root.title(self.frame_title)
            self.root.geometry(f'{self.frame_width}x{self.frame_height}+{x}+{y}')

            # Bind the _on_close() method to closing the window
            self.root.protocol("WM_DELETE_WINDOW", lambda: self._on_close(morpy_trace, app_dict))

            self._create_widgets(morpy_trace, app_dict)

            # The background work to run (if any)
            self.work_callable = work
            if self.work_callable is not None:
                self._start_work_thread(morpy_trace, app_dict)

            self.init_passed = check = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        finally:
            return {
                "morpy_trace" : morpy_trace,
                "check" : check,
            }

    @metrics
    def _create_widgets(self, morpy_trace: dict, app_dict: dict):
        r"""
        Build and place all widgets in a grid layout.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._create_widgets(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._create_widgets(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        self.overall_progress_text = None
        self.stage_progress_text = None

        try:
            # Check, if running in main thread (if you have that function)
            check_main_thread(app_dict)

            # Grid config - columns
            self.root.columnconfigure(0, weight=1)
            self.root.columnconfigure(1, weight=0)
            self.root.columnconfigure(2, weight=0)

            # Overall Progress
            if self.overall_progress_on:
                # Grid config
                self.root.rowconfigure(0, weight=0)

                # Overall headline (ttk.Label)
                self.total_headline_label = ttk.Label(
                    self.root,
                    text=self.headline_total,
                    font=(self.font, self.headline_font_size)
                )
                self.total_headline_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

                # Overall percentage (ttk.Label)
                self.overall_label_var = tk.StringVar(value="0.00%")
                self.overall_label = ttk.Label(self.root, textvariable=self.overall_label_var)
                self.overall_label.grid(row=0, column=1, padx=0, pady=(10, 0), sticky="nsw")

                # Overall progress bar (ttk.Progressbar)
                self.overall_progress = ttk.Progressbar(
                    self.root,
                    orient=tk.HORIZONTAL,
                    length=int(self.frame_width * 0.6),
                    mode="determinate"
                )
                self.overall_progress.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="nsew")
            else:
                self.total_headline_label = None
                self.overall_progress = None
                self.overall_label_var = None
                self.overall_label = None

            # Stage Progress
            self.root.rowconfigure(1, weight=0)

            # Stage headline (ttk.Label)
            self.stage_headline_label = ttk.Label(
                self.root,
                text="",
                font=(self.font, self.headline_font_size)
            )
            self.stage_headline_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsw")

            # Stage percentage (ttk.Label)
            self.stage_label_var = tk.StringVar(value="0.00%")
            self.stage_label = ttk.Label(self.root, textvariable=self.stage_label_var)
            self.stage_label.grid(row=1, column=1, padx=0, pady=(10, 0), sticky="nsew")

            # Stage progress bar (ttk.Progressbar)
            self.stage_progress = ttk.Progressbar(
                self.root,
                orient=tk.HORIZONTAL,
                length=int(self.frame_width * 0.6),
                mode="determinate"
            )
            self.stage_progress.grid(row=1, column=2, padx=10, pady=(10, 0), sticky="nsew")

            # Detail description at progress update
            if self.detail_description_on:
                self.root.rowconfigure(2, weight=0)
                # Still a ttk.Label
                self.stage_description_label = ttk.Label(
                    self.root,
                    text="",
                    font=(self.font, self.description_font_size)
                )
                self.stage_description_label.grid(row=2, column=0, columnspan=3, padx=10, pady=(5, 5), sticky="nsw")

            # Console widget (tk.Text has no direct TTK equivalent)
            if self.console_on:
                self.root.rowconfigure(3, weight=1)
                self.console_output = tk.Text(self.root, height=10, wrap="word")
                self.console_output.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
                self.console_output.configure(bg="black", fg="white")

                # Create a vertical Scrollbar
                self.console_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.console_output.yview)
                self.console_scrollbar.grid(row=3, column=3, sticky="ns", padx=(0, 10), pady=5)
                self.console_output["yscrollcommand"] = self.console_scrollbar.set
            else:
                self.console_output = None

            # Grid config - Bottom row
            self.root.rowconfigure(4, weight=0)

            # Close/Abort button (ttk.Button)
            self.button_text = tk.StringVar(value=self.button_text_abort)
            self.close_button = ttk.Button(
                self.root,
                textvariable=self.button_text,
                command=lambda: self._on_close(morpy_trace, app_dict)
            )
            self.close_button.grid(row=4, column=2, columnspan=1, padx=10, pady=(0, 10), sticky="nse")

            # Enforce an update on the GUI
            self._enforce_update()

            # Redirect output to console
            if self.console_on:
                self._redirect_console(morpy_trace, app_dict)

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    def _enforce_update(self):
        r"""
        Enforce an update of the GUI. If not leveraged after GUI update, might not display.

        :example:
            # Enforce an update on the GUI
            self._enforce_update()
        """

        # Guard this method against callbacks after closing
        if self.root.winfo_exists():
            self.root.update_idletasks()
            self.root.update()

    @metrics
    def _redirect_console(self, morpy_trace: dict, app_dict: dict):
        r"""
        Redirect sys.stdout/sys.stderr to self.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._redirect_console(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._redirect_console(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            sys.stdout = self
            sys.stderr = self

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace": morpy_trace,
            "check": check,
        }

    def write(self, message: str):
        r"""
        Captured print statements go into a queue.

        :param message: Message to be printed to console

        TODO fix writes to console. Somehow not arriving at GUI.
        """

        if self.console_queue is not None:
            self.console_queue.put(message)

    def flush(self):
        r"""
        Required for stdout redirection.
        """
        pass

    @metrics
    def _stop_console_redirection(self, morpy_trace: dict, app_dict: dict):
        r"""
        Stop capturing print statements in the GUI console.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._stop_console_redirection(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._stop_console_redirection(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace": morpy_trace,
            "check": check,
        }

    @metrics
    def _main_loop(self, morpy_trace, app_dict):
        r"""
        Main repeating loop for GUI refreshes. Read console queue to update text widget (unless we are done &
        auto_close=False). Update the progress bars (unless done), then schedule itself again.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._main_loop(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._main_loop(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Immediately exit if done/closing.
            if self.done or not self.root.winfo_exists():
                return

            # Process console output if needed
            if self.console_on and not self.done:
                self._update_console(morpy_trace, app_dict)

            # Process any pending UI updates from the background thread
            while not self.ui_calls.empty():
                call_type, kwargs = self.ui_calls.get_nowait()

                if call_type == "update_text":
                    self._real_update_text(morpy_trace, app_dict, **kwargs)
                elif call_type == "update_progress":
                    self._real_update_progress(morpy_trace, app_dict, **kwargs)
                elif call_type == "begin_stage":
                    self._real_begin_stage(morpy_trace, app_dict, **kwargs)

            # Only schedule the next loop if still alive
            if not self.done and self.root.winfo_exists():
                self.root.after(self.main_loop_interval, lambda: self._main_loop(morpy_trace, app_dict))

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace": morpy_trace,
            "check": check,
        }

    @metrics
    def _update_console(self, morpy_trace: dict, app_dict: dict):
        r"""
        One-time call to read from the queue and add text to the widget.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._update_console(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._update_console(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Check, if running in main thread
            check_main_thread(app_dict)

            while not self.console_queue.empty():
                msg = self.console_queue.get_nowait()
                if self.console_output is not None:
                    self.console_output.insert(tk.END, msg)
                    self.console_output.see(tk.END)

                # Enforce an update on the GUI
                self._enforce_update()

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def begin_stage(self, morpy_trace: dict, app_dict: dict, stage_limit: (int, float) = 1, headline_stage: str = None,
                    detail_description: str=None, ticks: float=.01):
        r"""
        Start a new stage of progress. Will set the stage prior to 100%, if
        not already the case.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param stage_limit: This is the maximum value of the stage progress. Set it to 0 to turn off the stage progress.
                            It represents the maximum value the stage progress will reach until 100%, which is
                            determined by which value you choose to increment the progress with (defaults to 1 per
                            increment). A value of 10 for example amounts to 10% per increment.
                            Defaults to 1.
        :param headline_stage: Descriptive name for the actual stage.
                               Defaults to morPy localization.
        :param detail_description: Description or status. Will
                                   not be shown if None at construction.
                                   Defaults to None.
        :param ticks: [optional] Percentage of total to log the progress. I.e. at ticks=10.7 at every
                      10.7% progress exceeded the exact progress will be logged. Defaults to 0.01.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            # Set up the next stage
            headline = "Currently querying"
            description = "Starting stage..."
            progress.begin_stage(morpy_trace, app_dict, stage_limit=10, headline_stage=headline,
            detail_description=description)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk.begin_stage(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Prevent updates after the GUI is closed.
            if not self.done:

                call_kwargs = {
                    "stage_limit" : stage_limit,
                    "detail_description" : detail_description,
                    "ticks" : ticks
                }
                self.ui_calls.put(("begin_stage", call_kwargs))

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def _real_begin_stage(self, morpy_trace: dict, app_dict: dict, stage_limit: (int, float) = 1, headline_stage: str = None,
                    detail_description: str=None, ticks: float=.01):
        r"""
        Start a new stage of progress. Will set the stage prior to 100%, if
        not already the case.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param stage_limit: This is the maximum value of the stage progress. Set it to 0 to turn off the stage progress.
                            It represents the maximum value the stage progress will reach until 100%, which is
                            determined by which value you choose to increment the progress with (defaults to 1 per
                            increment). A value of 10 for example amounts to 10% per increment.
                            Defaults to 1.
        :param headline_stage: Descriptive name for the actual stage.
                               Defaults to morPy localization.
        :param detail_description: Description or status. Will
                                   not be shown if None at construction.
                                   Defaults to None.
        :param ticks: [optional] Percentage of total to log the progress. I.e. at ticks=10.7 at every
                      10.7% progress exceeded the exact progress will be logged. Defaults to 0.01.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            # Set up the next stage
            headline = "Currently querying"
            description = "Starting stage..."
            progress.begin_stage(morpy_trace, app_dict, stage_limit=10, headline_stage=headline,
            detail_description=description)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk.begin_stage(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Prevent updates after the GUI is closed.
            if not self.done:
                # Try resetting progress
                if hasattr(self, "stage_progress_tracker"):
                    self._real_update_progress(morpy_trace, app_dict, current=0)

                # Stage headline
                self.headline_stage_nocol = (f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_curr"]}'
                                 if not headline_stage else f'{headline_stage}')
                # Finalize stage headline
                self.headline_stage = f'{self.headline_stage_nocol}:'

                self.detail_description = detail_description
                self.stage_limit = stage_limit

                # Construct the stage progress tracker
                self.stage_progress_tracker = common.ProgressTracker(
                    morpy_trace, app_dict, description=self.headline_stage_nocol, total=self.stage_limit,
                    ticks=ticks, verbose=True
                )

                # Send text updates to the queue
                call_kwargs = {
                    "headline_stage" : self.headline_stage_nocol,
                    "detail_description" : self.detail_description,
                }
                self.ui_calls.put(("update_text", call_kwargs))

                # Enforce an update on the GUI
                self._enforce_update()

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def end_stage(self, morpy_trace: dict, app_dict: dict):
        r"""
        End the current stage by setting it to 100%.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self.end_stage(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk.end_stage(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            self.update_progress(morpy_trace, app_dict, current=self.stage_limit)

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def update_progress(self, morpy_trace: dict, app_dict: dict, current: float = None):
        r"""
        Update stage progress & overall progress. If overall hits 100% and auto_close=True, close window. Else,
        switch button text to "Close" and stop console redirection. Enqueues a UI request for the
        main thread to process. Safe to call from any thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            progress = morPy.ProgressTrackerTk(morpy_trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Starting stage 1",
                stages=2,
                stage_limit=10,
                work=work)

            progress.run(morpy_trace, app_dict)

            curr_cnt = 5.67
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(morpy_trace, app_dict, current=curr_cnt, detail_description=msg)

            # stage 1 is at 100%
            curr_cnt = 10
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(morpy_trace, app_dict, current=curr_cnt, detail_description=msg)

            # Setup stage 2
            progress.update_text(morpy_trace, app_dict,
                headline_stage="Starting stage 2",
                detail_description="Now copying data...",
            )
            progress.update_progress(morpy_trace, app_dict, current=0, stage_limit=15)

            # stage 2 is at 100%
            curr_cnt = 15
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(morpy_trace, app_dict, current=curr_cnt, detail_description=msg)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk.update_progress(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Prevent updates after the GUI is closed.
            if not self.done:

                call_kwargs = {
                    "current" : current,
                }
                self.ui_calls.put(("update_progress", call_kwargs))

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    def _real_update_progress(self, morpy_trace: dict, app_dict: dict, current: float = None):
        """
        Update stage progress & overall progress. If overall hits 100% and auto_close=True, close window. Else,
        switch button text to "Close" and stop console redirection. Enqueues a UI request for the
        main thread to process. Safe to call from any thread. Actually updates Tk widgets. Must be called only
        from the main thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._real_update_progress(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        reset_stage_progress = False

        try:
            # Check, if running in main thread
            check_main_thread(app_dict)

            # If we're already done, just clamp visually
            if self.done:
                if self.overall_progress_on and self.overall_progress is not None:
                    self.overall_progress["value"] = 100.0
                    self.overall_label_var.set("100.00%")

                    # Enforce an update on the GUI
                    self._enforce_update()
            else:
                # 1) stage progress
                self.stage_info = self.stage_progress_tracker.update(morpy_trace, app_dict, current=current)
                self.stage_abs = self.stage_info["prog_abs"]  # Absolute float value representing 0..100%

                if self.stage_progress is not None and self.stage_abs:
                    self.stage_progress["value"] = self.stage_abs
                if self.stage_label_var is not None and self.stage_abs:
                    self.stage_label_var.set(f"{self.stage_abs:.2f}%")

                # If stage hits 100%, increment the stage count, reset stage bar
                if (self.stage_abs is not None) and self.stage_abs >= 100.0:
                    if self.overall_progress_on:
                        reset_stage_progress = True
                        self.stages_finished += 1
                    else:
                        self.stages_finished += 1
                        # If all stages are finished, mark as done
                        self.done = True
                        if self.auto_close:
                            self._stop_console_redirection(morpy_trace, app_dict)
                            self._on_close(morpy_trace, app_dict)
                        else:
                            self.button_text.set(self.button_text_close)
                            self._enforce_update()
                            self._stop_console_redirection(morpy_trace, app_dict)

                # Enforce an update on the GUI
                self._enforce_update()

                # 2) Overall fraction
                if self.overall_progress_on:
                    # Add fraction of stage to overall progress
                    overall_progress = self.stages_finished * self.fraction_per_stage
                    if (self.stage_abs is not None) and self.stage_abs < 100.0:
                        overall_progress += (self.stage_abs / 100.0) * self.fraction_per_stage

                    # Update the GUI elements for overall progress
                    self.overall_progress["value"] = overall_progress
                    self.overall_label_var.set(f"{overall_progress:.2f}%")

                    # If overall progress reaches 100%, handle completion
                    if overall_progress >= 100.0:
                        # If all stages are finished, mark as done
                        self.done = True
                        if self.auto_close:
                            self._stop_console_redirection(morpy_trace, app_dict)
                            self._on_close(morpy_trace, app_dict)
                        else:
                            self.button_text.set(self.button_text_close)
                            self._stop_console_redirection(morpy_trace, app_dict)

                        # All done for ##
                        log(morpy_trace, app_dict, "info",
                        lambda: f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_done"]} "{self.frame_title}".')

                    # Enforce an update on the GUI
                    self._enforce_update()

                # 3) Reset stage progress last to avoid lag in between update of stage and overall progress.
                if reset_stage_progress:
                    if self.stages_finished < self.stages:
                        if self.stage_progress is not None:
                            self.stage_progress["value"] = 0.0
                        if self.stage_label_var is not None:
                            self.stage_label_var.set("0.00%")
                    else:
                        # If all stages are finished, mark as done
                        self.done = True

                    # Enforce an update on the GUI
                    self._enforce_update()

            # Decrement self.unfinished_tasks
            self.ui_calls.task_done()

            # Enforce an update on the GUI
            self._enforce_update()

            check: bool = True

        # Handle errors from GUI after aborting
        except TclError as tcl_e:
            # GUI ended ungracefully.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_exit_dirty"]}\n'
                    f'{type(tcl_e).__name__}: {tcl_e}')

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def update_text(self, morpy_trace: dict, app_dict: dict, headline_total: str = None, headline_stage: str = None,
                    detail_description: str = None):
        r"""
        Update the headline texts or description at runtime. Enqueues a UI request for the
        main thread to process. Safe to call from any thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param headline_total: If not None, sets the overall progress headline text.
        :param headline_stage: If not None, sets the stage progress headline text.
        :param detail_description: If not None, sets the description text beneath the stage headline.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether text update completed without errors

        :example:
            gui.update_text(morpy_trace, app_dict,
                headline_total="Processing Outer Loop 3",
                headline_stage="Processing File 5",
                detail_description="Now copying data...",
            )
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk.update_text(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Prevent updates after the GUI is closed.
            if not self.done:

                # Send text updates to the queue
                call_kwargs = {
                    "headline_total" : headline_total,
                    "headline_stage" : headline_stage,
                    "detail_description" : detail_description,
                }
                self.ui_calls.put(("update_text", call_kwargs))

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace": morpy_trace,
            "check": check,
        }

    @metrics
    def _real_update_text(self, morpy_trace: dict, app_dict: dict, headline_total: str = None,
                          headline_stage: str = None, detail_description: str = None):
        r"""
        Update the headline texts or description at runtime. Actually updates Tk widgets.
        Must be called only from the main thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param headline_total: If not None, sets the overall progress headline text.
        :param headline_stage: If not None, sets the stage progress headline text.
        :param detail_description: If not None, sets the description text beneath the stage headline.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether text update completed without errors

        :example:
            gui.update_text(morpy_trace, app_dict,
                headline_total="Processing Outer Loop 3",
                headline_stage="Processing File 5",
                detail_description="Now copying data...",
            )
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._real_update_text(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Avoid updates after "abort"
            if not self.done:
                # Check, if running in main thread
                check_main_thread(app_dict)

                # Update overall headline
                if headline_total is not None and self.overall_progress_on:
                    # Retain the final colon to stay consistent with constructor
                    self.headline_total_nocol = headline_total
                    self.headline_total = self.headline_total_nocol + ":"
                    if hasattr(self, "overall_progress_tracker"):
                        self.overall_progress_tracker.description = self.headline_total_nocol
                    if self.total_headline_label is not None:
                        self.total_headline_label.config(text=self.headline_total)

                    # Enforce an update on the GUI
                    self._enforce_update()

                # Update stage headline
                if headline_stage is not None:
                    # Retain the final colon to stay consistent with constructor
                    self.headline_stage_nocol = headline_stage
                    self.headline_stage = self.headline_stage_nocol + ":"
                    if hasattr(self, "stage_progress_tracker"):
                        self.stage_progress_tracker.description = self.headline_stage_nocol
                    if self.stage_headline_label is not None:
                        self.stage_headline_label.config(text=self.headline_stage)

                    # Enforce an update on the GUI
                    self._enforce_update()

                # Update description
                if detail_description is not None:
                    self.detail_description = detail_description
                    # If the label didn't exist but was called, we don't create it on the fly.
                    # We only update if the widget is already present:
                    if self.stage_description_label is not None:
                        self.stage_description_label.config(text=self.detail_description)

                    # Enforce an update on the GUI
                    self._enforce_update()

            check: bool = True

        # Handle errors from GUI after aborting
        except TclError as tcl_e:
            # GUI ended ungracefully.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_exit_dirty"]}\n'
                    f'{type(tcl_e).__name__}: {tcl_e}')

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {"morpy_trace": morpy_trace, "check": check}

    @metrics
    def run(self, morpy_trace: dict, app_dict: dict):
        r"""
        Start the GUI main loop and run the Tk mainloop on the main thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            progress = morPy.ProgressTrackerTk(morpy_trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Generic Progress stage",
                stages=1,
                stage_limit=10,
                work=work)

            progress.run(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk.run(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Start our custom loop
            self._main_loop(morpy_trace, app_dict)
            self.root.mainloop()

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def _start_work_thread(self, morpy_trace: dict, app_dict: dict):
        r"""
        TODO implement morPy threading and use it here
            > right now interrupt/abort does not work as desired: background threads shall be terminated immediately.

        Launch the user-supplied function in a background thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._start_work_thread(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._start_work_thread(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        def _thread_wrapper():
            try:
                # Automatically pass gui=self to the work_callable
                self.work_callable(gui=self)
            except Exception as e:
                # Exception in the worker thread.
                log(morpy_trace, app_dict, "error",
                lambda: f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_start_work_thread_err"]}\n'
                        f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno} '
                        f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                        f'{type(e).__name__}: {e}')

        try:
            self.worker_thread = threading.Thread(target=_thread_wrapper, daemon=True)
            self.worker_thread.start()

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def _on_close(self, morpy_trace: dict, app_dict: dict):
        r"""
        Close or abort the GUI.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._on_close(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk._on_close(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # In case of aborting progress quit the program.
            if not self.done:

                # Set done to omit pulling from GUI queue after close
                self.done = True

                # Initiate global exit
                app_dict["morpy"]["exit"] = True

                # Release the global interrupts to proceed with exit
                app_dict["morpy"]["interrupt"] = False


            # Clear any pending UI update calls.
            while not self.ui_calls.empty():
                try:
                    self.ui_calls.get_nowait()
                except Exception:
                    break

            # Clear any pending console messages.
            if self.console_queue is not None:
                while not self.console_queue.empty():
                    try:
                        self.console_queue.get_nowait()
                    except Exception:
                        break

            # Restore original console if not already done
            self._stop_console_redirection(morpy_trace, app_dict)
            self.root.quit()
            self.root.destroy()

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def get_console_output(self, morpy_trace: dict, app_dict: dict):
        r"""
        Retrieve the current text from the console widget.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self.get_console_output(morpy_trace, app_dict)
        """

        module: str = 'ui_tk'
        operation: str = 'ProgressTrackerTk.get_console_output(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        console_text = ""

        try:
            if self.console_output is not None:
                console_text = self.console_output.get("1.0", tk.END).strip()

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
            "console_output" : console_text,
        }

def check_main_thread(app_dict: dict):
    r"""
    Check, if GUI runs in main thread and raise error if so. Otherwise,
    instabilities are introduced with tkinter.

    :param app_dict: morPy global dictionary containing app configurations

    :return:
        -

    :example:
        check_main_thread(app_dict)
    """

    # UI must run in main thread. Currently in ###
    if threading.current_thread() is not threading.main_thread():
        raise RuntimeError(
            f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_check_main"]}: {threading.current_thread()}'
        )

@metrics
def dialog_sel_file(morpy_trace: dict, app_dict: dict, init_dir: str=None, file_types: tuple=None, title: str=None) -> dict:

    r"""
    This function opens a dialog for the user to select a file.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param file_types: This tuple of 2-tuples specifies, which filetypes will be
        selectable in the dialog box.
    :param title: Title of the open file dialog

    :return: dict
        morpy_trace: operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        file_path: Path of the selected file
        file_selected: True, if file was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        file_types = (('PDF','*.pdf'),('Textfile','*.txt'),('All Files','*.*'))
        title = 'Select a file...'
        file_path = morPy.dialog_sel_file(morpy_trace, app_dict, init_dir=init_dir,
                        file_types=file_types, title=title)["file_path"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'ui_tk'
    operation: str = 'dialog_sel_file(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    file_path = None
    file_selected = False

    try:
        if not init_dir:
            init_dir = app_dict["conf"]["main_path"]
        if not file_types:
            file_types = (f'{app_dict["loc"]["morpy"]["dialog_sel_file_all_files"]}', '*.*')
        if not title:
            title = f'{app_dict["loc"]["morpy"]["dialog_sel_file_select"]}'

        # Invoke the Tkinter root window and withdraw it to force the
        # dialog to be opened in the foreground
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.iconbitmap(app_dict["conf"]["app_icon"])

        # Open the actual dialog in the foreground and store the chosen folder
        file_path = filedialog.askopenfilename(
            parent = root,
            title = f'{title}',
            initialdir = init_dir,
            filetypes = file_types,
        )

        if not file_path:
            # No file was chosen by the user.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_file_nosel"]}\n'
                    f'{app_dict["loc"]["morpy"]["dialog_sel_file_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_file_cancel"]}')

        else:
            file_selected = True
            # A file was chosen by the user.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_file_asel"]}\n'
                    f'{app_dict["loc"]["morpy"]["dialog_sel_file_path"]}: {file_path}\n'
                    f'{app_dict["loc"]["morpy"]["dialog_sel_file_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_file_open"]}')

            # Create a path object
            morpy_fct.pathtool(file_path)

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'file_path' : file_path,
        'file_selected' : file_selected,
        }

@metrics
def dialog_sel_dir(morpy_trace: dict, app_dict: dict, init_dir: str=None, title: str=None) -> dict:

    r"""
    This function opens a dialog for the user to select a directory.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param title: Title of the open directory dialog

    :return: dict
        morpy_trace: operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        dir_path: Path of the selected directory
        dir_selected: True, if directory was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        title = 'Select a directory...'
        dir_path = morPy.dialog_sel_dir(morpy_trace, app_dict, init_dir=init_dir, title=title)["dir_path"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'ui_tk'
    operation: str = 'dialog_sel_dir(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    dir_path = None
    dir_selected = False

    try:
        if not init_dir:
            init_dir = app_dict["conf"]["main_path"]
        if not title:
            title = f'{app_dict["loc"]["morpy"]["dialog_sel_dir_select"]}'

        # Invoke the Tkinter root window and withdraw it to force the
        # dialog to be opened in the foreground
        root = tk.Tk()
        root.withdraw()
        root.iconbitmap(app_dict["conf"]["app_icon"])

        # Open the actual dialog in the foreground and store the chosen folder
        root.dir_name = filedialog.askdirectory(
            parent = root,
            title = f'{title}',
            initialdir = init_dir,
        )
        dir_path = root.dir_name

        if not dir_path:
            # No directory was chosen by the user.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_dir_nosel"]}\n'
                f'{app_dict["loc"]["morpy"]["dialog_sel_dir_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_dir_cancel"]}')
        else:
            dir_selected = True
            # A directory was chosen by the user.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_dir_asel"]}\n'
                    f'{app_dict["loc"]["morpy"]["dialog_sel_dir_path"]}: {dir_path}\n'
                    f'{app_dict["loc"]["morpy"]["dialog_sel_dir_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_dir_open"]}')

            # Create a path object
            morpy_fct.pathtool(dir_path)

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'dir_path' : dir_path,
        'dir_selected' : dir_selected,
        }

```

## lib.xl.py

```
r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers Microsoft Excel specific routines.

NOTES on OpenPyXL:
OpenPyXL does currently not read all possible items in an Excel file so
images and charts will be lost from existing files if they are opened
and saved with the same name.
NB you must use the English name for a function and function arguments
must be separated by commas and not other punctuation such as semicolons.
"""

import lib.fct as morpy_fct
import lib.common as common
from lib.decorators import metrics, log

import sys
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Protection
import openpyxl.utils.cell

class XlWorkbook:
    r"""
    This class constructs an API to an Excel workbook and delivers methods
    to read from and write to the workbook. It uses OpenPyXL and all those
    methods can be used on self.wb_obj if a more versatile API is required.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param workbook: Path of the workbook
    :param create: If True and file does not yet exist, will create the workbook.
    :param data_only: If True, cells with formulae are represented by their calculated values.
                Closing and reopening the workbook is required for this to change.
    :param keep_vba: If True, preserves any Visual Basic elements in the workbook. Only has an effect
                on workbooks supporting vba (i.e. xlsm-files). These elements remain immutable. Closing
                and reopening the workbook is required to change behaviour.

    :methods:
        .save_workbook(morpy_trace: dict, app_dict: dict, close_workbook: bool=False)

            Saves the changes to the MS Excel workbook.
            :param close_workbook: If True, closes the workbook.

            :return: dict
                wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                    reference to an instance.

        .close_workbook(morpy_trace: dict, app_dict: dict)

            Closes the MS Excel workbook.
            :return: dict
                wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                    reference to an instance.

        .activate_worksheet(morpy_trace: dict, app_dict: dict, worksheet: str)

            Activates a specified worksheet in the workbook. If the sheet is not found,
            an error is logged.
            :param worksheet: The name of the worksheet to activate.

        .read_cells(self, morpy_trace: dict, app_dict: dict, cell_range: list=None,
                   cell_styles: bool=False, worksheet: str=None)

            Reads the cells of MS Excel workbooks. Overlapping ranges will get auto-formatted
            to ensure every cell is addressed only once.
            :param cell_range: The cell or range of cells to read from. Accepted formats:
                - not case-sensitive
                - Single cell: ["A1"]
                - Range of cells: ["A1:ZZ1000"]
                - Ranges of cells: ["A1:ZZ1000", "c2:fl342"]
            :param cell_styles: If True, cell styles will be retrieved. If False, get value only.
            :param worksheet: Name of the worksheet, where the cell is located. If None, the
                active sheet is addressed.

            :return: dict
                cl_dict: Dictionary of cell content dictionaries containing values and styles of cells. Following is
                        an example of a single complete cell write:
                    cl_dict = {
                        "A1" : {
                            "value" : "Data in Cell",
                            "comment" : {
                                "text" : "This is a comment",
                                "author" : "Mr. Author Man",
                            },
                            "format" : "General",           # Options: General|Number|Currency|Accounting|Date|Time|Percentage
                                                            # > Fraction|Scientific|Text|custom strings
                            "font" : {
                                "name" : "Calibri",
                                "bold" : True,
                                "italic" : True,
                                "vertical align" : None,    # Options: None|superscript|subscript
                                "underline" : None,         # Options: None|single|double|singleAccounting|doubleAccounting
                                "strike" : False,
                                "size" : 14,
                                "color" : "D1760C",
                            },
                            "background" : {
                                "fill type" : None,         # Options: None|solid|darkGrid|darkTrellis|lightDown|lightGray
                                                            # > lightGrid|lightHorizontal|lightTrellis|lightUp
                                                            # > lightVertical|mediumGray
                                "start color" : "307591",
                                "end color" : "67CCCC",
                            },
                            "border" : {
                                "edge" : "outline",         # Options: left|right|top|bottom|diagonal|outline
                                                            # > vertical|horizontal
                                "style" : None,             # Options: None|dashDot|dashDotDot|dashed|dotted|double|hair|medium
                                                            # > medium|mediumDashDot|mediumDashDotDot|mediumDashed|slantDashDot
                                                            # > thick|thin
                                "color" : "2A7F7F",
                                "diagonal direction" : 0,   # Options: 0 (no diagonal) | 1 (downwards) | 2 (upwards)
                            },
                            "alignment" : {
                                "horizontal" : "general",   # Options: general|left|center|right|fill|justify|centerContinuous
                                                            # > distributed
                                "vertical" : "center",      # Options: top|center|bottom|justify|distributed
                                "text rotation" : 0,
                                "wrap text" : False,
                                "shrink to fit" : False,
                                "indent" : 0,
                            },
                            "protection" : {
                                "locked" : False,
                                "hidden" : False,
                            },
                        },
                        "A2" : { ... }
                    }

            :example:
                wb_path = "C:\my.xlsx"
                wb = morPy.XlWorkbook(morpy_trace, app_dict, wb_path)
                cl_dict = wb.read_cells(morpy_trace, app_dict, "Sheet1", ["A1", "B2:C3"])["cl_dict"]
                print(f'{cl_dict}')

        .write_ranges(self, morpy_trace: dict, app_dict: dict, worksheet: str=None, cell_range: list=None,
                     cell_writes: list=None, fill_range: bool=False, style_default: bool=False,
                     save_workbook: bool=True, close_workbook: bool=False)

            Writes data into cells of an Excel workbook.
            :param worksheet: Name of the worksheet, where the cell is located. If None, the
                active sheet is addressed.
            :param cell_range: The cell or range of cells to write. Accepted formats:
                - not case-sensitive
                - Single cell: ["A1"]
                - Range of cells: ["A1:ZZ1000"]
                - Ranges of cells: ["A1:ZZ1000", "c2:fl342"]
            :param cell_writes: WARNING this data structure is not equal to 'cl_dict' of .read_cells()
                List of cell content dictionaries to be written consecutively. If the list is shorter
                than the amount of cells in the range, it will stop writing to cells and finish the operation. The
                dictionaries do not need to contain all possible keys, only assign the cell attributes/values needed.
                See example for a display of usage. Following is an example of a single complete cell write:
                    cl_list = [
                        {"value" : "Data in Cell",
                        "comment" : {
                            "text" : "This is a comment",
                            "author" : "Mr. Author Man",
                        },
                        "format" : "General",           # Options: General|Number|Currency|Accounting|Date|Time|Percentage
                                                        # > Fraction|Scientific|Text|custom strings
                        "font" : {
                            "name" : "Calibri",
                            "bold" : True,
                            "italic" : True,
                            "vertical align" : None,    # Options: None|superscript|subscript
                            "underline" : None,         # Options: None|single|double|singleAccounting|doubleAccounting
                            "strike" : False,
                            "size" : 14,
                            "color" : "D1760C",
                        },
                        "background" : {
                            "fill type" : None,         # Options: None|solid|darkGrid|darkTrellis|lightDown|lightGray
                                                        # > lightGrid|lightHorizontal|lightTrellis|lightUp
                                                        # > lightVertical|mediumGray
                            "start color" : "307591",   # This must exist in order for background to work
                            "end color" : "67CCCC",     # This must exist in order for background to work
                        },
                        "border" : {
                            "edge" : "outline",         # Options: left|right|top|bottom|diagonal|outline
                                                        # > vertical|horizontal
                            "style" : None,             # Options: None|dashDot|dashDotDot|dashed|dotted|double|hair|medium
                                                        # > medium|mediumDashDot|mediumDashDotDot|mediumDashed|slantDashDot
                                                        # > thick|thin
                            "color" : "2A7F7F",
                            "diagonal direction" : 0,   # Options: 0 (no diagonal) | 1 (downwards) | 2 (upwards)
                        },
                        "alignment" : {
                            "horizontal" : "general",   # Options: general|left|center|right|fill|justify|centerContinuous
                                                        # > distributed
                            "vertical" : "center",      # Options: top|center|bottom|justify|distributed
                            "text rotation" : 0,
                            "wrap text" : False,
                            "shrink to fit" : False,
                            "indent" : 0,
                        },
                        "protection" : {
                            "locked" : False,
                            "hidden" : False,
                        },
                    },
                    { ... }]
            :param fill_range: If True and if the cell_writes list is shorter than the amount
                of cells in the range, it will continue writing the values from beginning until the end
                of the range.
            :param style_default: If True, styles/attributes of cells will be reset to default. If False,
                the styles/attributes of the original cell will be preserved.
            :param save_workbook: If True, saves the workbook after the changes.
            :param close_workbook: If True, closes the workbook.

            :return: dict
                wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                    reference to an instance.

            :example:
                w_sh = "Sheet1"
                cl_rng = ["A1:A10"]
                cell_writes = []
                cell_writes.append(
                    {"value": "Example"}
                )
                cell_writes.append({
                    "value" : r"=1+2",
                    "font" : {
                        "color" : "D1760C",
                        },
                })
                wb = wb.write_cells(morpy_trace, app_dict, worksheet=w_sh, cell_range=cl_rng, cell_writes=cl_list
                                    save_workbook=True, close_workbook=True)["wb_obj"]

    :example:
        # Construct a workbook instance
        wb_path = "C:\my.xlsx"
        wb = XlWorkbook(morpy_trace, app_dict, wb_path)

        # Activate a certain worksheet
        worksheet1 = "Sheet1"
        wb.activate_worksheet(morpy_trace, app_dict, worksheet1)

        # Read cells in range
        range1 = ["A1", "B2:C3"]
        worksheet2 = "Sheet2"
        cl_dict = wb.read_cells(morpy_trace, app_dict, worksheet=worksheet2, cell_range=range1)["cl_dict"]

        # Write to cells in a range and apply styles. Fill range in alternating pattern (fill_range=True).
        cell_writes = []
        cell_writes.append({"value": "Example"})
        cell_writes.append({"value" : r"=1+2", "font" : {"color" : "D1760C",}})
        wb = wb.write_cells(morpy_trace, app_dict, worksheet=worksheet1, cell_range=range1, cell_writes=cell_writes
                            save_workbook=False, close_workbook=False, fill_range=True)["wb_obj"]

        # Save the workbook.
        wb = wb.save_workbook(morpy_trace, app_dict, close=False)["wb_obj"]

        # Close the workbook. Write "None" to the reference "wb".
        wb = wb.close_workbook(morpy_trace, app_dict)["wb_obj"]
    """

    __slots__ = (
        "wb_obj",
        "wb_path",
        "wb_sheets",
        "active_sheet",
        "active_sheet_title",
        "tables_ranges",
        "tables_sheets",
        "file_ext",
        "files_vbs",
    )

    def __init__(self, morpy_trace: dict, app_dict: dict, workbook: str, create: bool=False,
              data_only: bool=False, keep_vba: bool=True) -> None:
        r"""
        In order to get metrics for __init__(), call helper method _init() for
        the @metrics decorator to work. It relies on the returned
        {'morpy_trace' : morpy_trace}, which __init__() can not do (needs to be None).

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param workbook: Path of the workbook
        :param create: If True and file does not yet exist, will create the workbook.
        :param data_only: If True, cells with formulae are represented by their calculated values.
                    Closing and reopening the workbook is required for this to change.
        :param keep_vba: If True, preserves any Visual Basic elements in the workbook. Only has an effect
                    on workbooks supporting vba (i.e. xlsm-files). These elements remain immutable. Closing
                    and reopening the workbook is required to change behaviour.

        :return:
            -

        :example:
            wb_path = "C:\projects\my.xlsx"
            wb = XlWorkbook(morpy_trace, app_dict, wb_path)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.xl'
        operation: str = 'XlWorkbook.__init__(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        try:
            # Use self._init() for initialization
            check: bool = self._init(morpy_trace, app_dict, workbook, create)["check"]

            if not check:
                # Instance construction aborted.
                raise RuntimeError(f'{app_dict["loc"]["morpy"]["XlWorkbook_inst_abort"]}')

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    @metrics
    def _init(self, morpy_trace: dict, app_dict: dict, workbook: str, create: bool=False,
              data_only: bool=False, keep_vba: bool=True) -> dict:
        r"""
        Helper method for initialization to ensure @metrics decorator usage.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param workbook: Path of the workbook
        :param create: If True and file does not yet exist, will create the workbook. If file exists, will
                    open the existing file.
        :param data_only: If True, cells with formulae are represented by their calculated values.
                    Closing and reopening the workbook is required for this to change.
        :param keep_vba: If True, preserves any Visual Basic elements in the workbook. Only has an effect
                    on workbooks supporting vba (i.e. xlsm-files). These elements remain immutable. Closing
                    and reopening the workbook is required to change behaviour.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._init(morpy_trace, app_dict)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.xl'
        operation: str = 'XlWorkbook._init(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            self.wb_path = morpy_fct.pathtool(workbook)["out_path"]

            # Opening MS Excel workbook.
            log(morpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["morpy"]["XlWorkbook_construct"]}\n'
                    f'{app_dict["loc"]["morpy"]["XlWorkbook_wb"]}: {self.wb_path}')

            self.wb_sheets = []
            self.active_sheet = None
            self.active_sheet_title = ""
            self.tables_ranges = {}
            self.tables_sheets = {}

            # Get the file extension in lowercase
            self.file_ext = morpy_fct.pathtool(self.wb_path)["file_ext"].lower()

            # Set vba supporting file extensions
            self.files_vbs = {".xlsm", ".xltm"}

            path_eval = morpy_fct.pathtool(self.wb_path)
            file_exists = path_eval["file_exists"]

            if not file_exists:
                if create:
                    self._create_workbook(morpy_trace, app_dict)
                else:
                    # File does not exist and was not created.
                    raise LookupError(
                        f'{app_dict["loc"]["morpy"]["XlWorkbook_not_create"]}\n'
                        f'{app_dict["loc"]["morpy"]["XlWorkbook_create"]}: {create}'
                    )

            # Re-evaluate file creation
            path_eval = morpy_fct.pathtool(self.wb_path)
            is_file = path_eval["is_file"]
            if not is_file:
                # The path to the workbook is invalid.
                raise LookupError(
                    f'{app_dict["loc"]["morpy"]["XlWorkbook_path_invalid"]}\n'
                    f'{app_dict["loc"]["morpy"]["XlWorkbook_path"]}: {self.wb_path}'
                )

            # Evaluate, if file type supports vba
            if keep_vba and self.file_ext not in self.files_vbs:
                keep_vba = False

            # Open the workbook
            self.wb_obj = load_workbook(self.wb_path, data_only=data_only, keep_vba=keep_vba)

            # Update workbook metadata
            self._update_meta(morpy_trace, app_dict)

            # MS Excel workbook instantiated.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["XlWorkbook_inst"]}'
                    f'{app_dict["loc"]["morpy"]["XlWorkbook_wb"]}: {self.wb_path}')

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            }

    @metrics
    def _create_workbook(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Creates a new, empty Excel workbook at the specified path.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).

        :example:
            self._create_workbook(morpy_trace, app_dict)
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.xl'
        operation: str = 'XlWorkbook._create_workbook(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            wb = Workbook()
            wb.save(filename=f'{self.wb_path}')

            # MS Excel workbook created.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["create_workbook_done"]}\n'
                    f'xl_path: {self.wb_path}')

            check: bool = True

        # Error detection
        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            'morpy_trace': morpy_trace,
            'check': check
        }

    @metrics
    def _update_meta(self, morpy_trace: dict, app_dict: dict, minimal: bool=False) -> dict:
        r"""
        Update which metadata of the workbook. This could be which sheet is active
        and which sheets there are.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param minimal: If True, updates only the attributes that could change
            without actually writing to the cell (i.e. active_sheet).

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).

        :example:
            self._update_sheets(morpy_trace, app_dict)
            print(f'{self.active_sheet_title}')
            print(f'{self.wb_sheets}')
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.xl'
        operation: str = 'XlWorkbook._update_meta(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        table_range = None
        table_sheet = None
        table_list = None

        try:
            # Retrieve the name of the active sheet
            self.active_sheet = self.wb_obj.active
            self.active_sheet_title = self.wb_obj.active.title

            if not minimal:
                # Retrieve all sheet names of the workbook
                self.wb_sheets = self.wb_obj.sheetnames

                # Retrieve the tables dictionary and create a dictionary with the table
                # being the key and the sheet of the workbook being the object
                for sheet in self.wb_sheets:
                    # Get all tables of the sheet including the range (List)
                    table_data = self.wb_obj[sheet].tables.items()

                    # Build the dictionaries
                    for tpl in table_data:
                        table = tpl[0]
                        table_range = tpl[1]

                        # Create a list of tables
                        if not table_list:
                            table_list = [table]
                        else:
                            table_list.append(table)

                        # Create a dictionary of tables and ranges
                        table_range = {table: table_range} if not isinstance(table_range, dict) else table_range.update({table: table_range})

                        # Create a dictionary of tables and sheets
                        table_sheet = {table: sheet} if not isinstance(table_sheet, dict) else table_sheet.update({table: sheet})

                # Store table ranges table sheets
                self.tables_ranges = table_range if table_range else {}
                self.tables_sheets = table_sheet if table_sheet else {}

            check: bool = True

        # Error detection
        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            'morpy_trace': morpy_trace,
            'check': check
        }

    @metrics
    def _cell_ref_autoformat(self, morpy_trace: dict, app_dict: dict, cell_range: list) -> dict:
        r"""
        Converts a list of cells and cell ranges to a dictionary. Overlapping cell
        ranges/cells will be auto-formatted to a single reference.
    
        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param cell_range: The cell or range of cells to read from. Accepted formats:
            - Single cell: ["A1"]
            - Range of cells: ["A1:ZZ1000", "C3", ...] (not case-sensitive).
    
        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).
            cl_dict: Dictionary where cells are keys with empty arguments:
                     {'cell1': '', 'cell2': '', ...}
    
        :example:
            cl_range = ["A1", "B2:C3"]
            cl_dict = self._cell_ref_autoformat(morpy_trace, app_dict, cell_range = cl_range)["cl_dict"]
        """
    
        # Define operation credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.xl'
        operation: str = 'XlWorkbook._cell_ref_autoformat(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
    
        check: bool = False
        cl_valid = False
        cl_dict = {}
    
        try:
    
            # Loop through every list item
            for cl in cell_range:

                # Harmonize cell letters
                cl = cl.upper()
    
                # Evaluate the type. If a list with 0 or more than 2 items was found, the cell
                # list is invalid. For 1 item it is a single cell and for 2 items it is a range.
                pattern = '[a-zA-Z]?[a-zA-Z]{1}[0-9]+'
                type_cl = common.regex_findall(morpy_trace, app_dict, cl, pattern)["result"]
                type_cl_len = len(type_cl)
    
                # The item is a cell
                if type_cl_len == 1:
                    # Add the cell to the dictionary
                    cl_dict.update({type_cl[0] : ''})
    
                    # A single cell was added to the dictionary.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["cell_ref_autoformat_1cell"]}\n'
                            f'{app_dict["loc"]["morpy"]["cell_ref_autoformat_cl"]}: {type_cl[0]}')

                    cl_valid = True
    
                # The item is a range
                elif type_cl_len == 2:
                    # Convert the range to a list
                    # 1) Extract columns
                    pattern = '[a-zA-Z]?[a-zA-Z]{1}'
                    range_col1 = common.regex_findall(morpy_trace, app_dict, type_cl[0], pattern)["result"]
                    pattern = '[a-zA-Z]?[a-zA-Z]{1}'
                    range_col2 = common.regex_findall(morpy_trace, app_dict, type_cl[1], pattern)["result"]
    
                    # Compare columns by string length
                    if len(range_col1) <= len(range_col2):
                        col_from = range_col1
                        col_to = range_col2
                    else:
                        col_from = range_col2
                        col_to = range_col1
    
                    # Extract and enumerate components of columns to loop through them.
                    if len(col_from[0]) == 2:
                        pattern = '[A-Z]{1}'
                        col_from = common.regex_findall(morpy_trace, app_dict, col_from, pattern)["result"]
    
                        # Build the sum of columns from A to col_from for further comparison.
                        # 64 refers to the Unicode value of capital A minus 1.
                        col_from_sum = abs((int(ord(col_from[0])) - 64) * 26 + (int(ord(col_from[1])) - 64))
                    else:
                        col_from_sum = int(ord(col_from[0])) - 64
    
                    # Extract and enumerate components of columns to loop through them.
                    if len(col_to[0]) == 2:
                        pattern = '[A-Z]{1}'
                        col_to = common.regex_findall(morpy_trace, app_dict, col_to, pattern)["result"]
    
                        # Build the sum of columns from A to col_to for further comparison.
                        # 64 refers to the Unicode value of capital A minus 1.
                        col_to_sum = abs((int(ord(col_to[0])) - 64) * 26 + (int(ord(col_to[1])) - 64))
                    else:
                        col_to_sum = int(ord(col_to[0])) - 64
    
                    # Temporarily store col_from and col_to for eventual reordering
                    tmp_col_from = col_from
                    tmp_col_from_sum = col_from_sum
                    tmp_col_to = col_to
                    tmp_col_to_sum = col_to_sum
    
                    # Compare columns by the enumerated values and exchange them if necessary
                    if col_from_sum > col_to_sum:
                        col_from = tmp_col_to
                        col_from_sum = tmp_col_to_sum
                        col_to = tmp_col_from
                        col_to_sum = tmp_col_from_sum
    
                    # 2) Extract rows
                    pattern = '[0-9]+'
                    range_row1 = common.regex_findall(morpy_trace, app_dict, type_cl[0], pattern)["result"]
                    pattern = '[0-9]+'
                    range_row2 = common.regex_findall(morpy_trace, app_dict, type_cl[1], pattern)["result"]
    
                    # Make rows integers
                    range_row1 = int(range_row1[0])
                    range_row2 = int(range_row2[0])
    
                    # Compare rows to which is higher and set start and end of rows for the range
                    if range_row1 <= range_row2:
                        row_from = range_row1
                        row_to = range_row2
                    else:
                        row_to = range_row1
                        row_from = range_row2
    
                    # Loop through all cells and add them to the dictionary
                    # 1) Loop through columns
                    col_counter = col_from_sum
    
                    while col_counter <= col_to_sum:
                        # Start from the first requested row
                        row_counter = row_from
    
                        # 2) Loop through rows
                        while row_counter <= row_to:
                            # Rebuild the cell
                            clmn = openpyxl.utils.cell.get_column_letter(col_counter)
                            cll = f'{clmn}{row_counter}'
    
                            # Add the cell to the dictionary
                            cl_dict.update({cll : ''})
    
                            # Iterate
                            row_counter += 1
    
                        # Iterate
                        col_counter += 1
    
                    # A range of cells was added to the dictionary.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["cell_ref_autoformat_done"]}\n'
                            f'{app_dict["loc"]["morpy"]["cell_ref_autoformat_rng"]}: '
                            f'({openpyxl.utils.cell.get_column_letter(col_from_sum)}:{row_from}) - '
                            f'({openpyxl.utils.cell.get_column_letter(col_to_sum)}:{row_to})')

                    cl_valid = True

                # The item is not a valid cell
                else:
                    cl_valid = False
    
                    # The cell value is invalid. Autoformatting aborted.
                    log(morpy_trace, app_dict, "warning",
                    lambda: f'{app_dict["loc"]["morpy"]["cell_ref_autoformat_invalid"]}\n'
                            f'{app_dict["loc"]["morpy"]["cell_ref_autoformat_cls"]}: {cell_range}\n'
                            f'check: {check}')
    
            # Evaluate the validity of the dictionary
            if cl_valid:
                check: bool = True
    
        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")
    
        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            'cl_dict' : cl_dict
            }

    @metrics
    def save_workbook(self, morpy_trace: dict, app_dict: dict, close_workbook: bool=False) -> dict:
        r"""
        Saves the changes to the MS Excel workbook.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param close_workbook: If True, closes the workbook.

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).
            wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                reference to an instance.

        :example:
            wb_path = "C:\my.xlsx"
            wb = XlWorkbook(morpy_trace, app_dict, wb_path)

            # Save and close the workbook. Write "None" to the reference "wb".
            wb = wb.save_workbook(morpy_trace, app_dict, close=True)["wb_obj"]
            print(f'{wb}')
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.xl'
        operation: str = 'XlWorkbook.save_workbook(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        wb_obj_return = self

        try:
            # Save the workbook
            self.wb_obj.save(filename=self.wb_path)

            if close_workbook:
                # Close the workbook
                wb_obj_return = self.close_workbook(morpy_trace, app_dict)["wb_obj"]

            check: bool = True

        # Error detection
        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            'morpy_trace' : morpy_trace,
            'check' : check,
            'wb_obj' : wb_obj_return,
        }

    @metrics
    def close_workbook(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Closes the MS Excel workbook.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).
            wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                reference to an instance.

        :example:
            wb_path = "C:\my.xlsx"
            wb = XlWorkbook(morpy_trace, app_dict, wb_path)

            # Close the workbook. Write "None" to the reference "wb".
            wb = wb.close_workbook(morpy_trace, app_dict)["wb_obj"]
            print(f'{wb}')
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.xl'
        operation: str = 'XlWorkbook.close_workbook(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Close the workbook
            wb_path = self.wb_path
            self.wb_obj.close()

            # The workbook object was closed.
            log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["close_workbook_done"]}\n'
                        f'{app_dict["loc"]["morpy"]["close_workbook_path"]}: {wb_path}')

            check: bool = True

        # Error detection
        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            'morpy_trace' : morpy_trace,
            'check' : check,
            'wb_obj' : None,
        }

    @metrics
    def activate_worksheet(self, morpy_trace: dict, app_dict: dict, worksheet: str) -> dict:
        r"""
        Activates a specified worksheet in the workbook. If the sheet is not found,
        an error is logged.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param worksheet: The name of the worksheet to activate.

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).

        :example:
            wb_path = "C:\my.xlsx"
            wb = XlWorkbook(morpy_trace, app_dict, wb_path)
            w_sht = "Sheet1"
            wb.activate_worksheet(morpy_trace, app_dict, w_sht)
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.xl'
        operation: str = 'XlWorkbook.activate_worksheet(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Check if the requested sheet exists in the workbook
            if worksheet in self.wb_sheets:
                # Check for the active sheet
                self._update_meta(morpy_trace, app_dict, minimal=True)

                if not worksheet == self.active_sheet_title:
                    # Set the requested sheet as active
                    self.wb_obj.active = self.wb_obj[worksheet]
                    # Store active sheet in meta data
                    self._update_meta(morpy_trace, app_dict, minimal=True)

                    # The worksheet was successfully activated.
                    log(morpy_trace, app_dict, "debug",
                        lambda: f'{app_dict["loc"]["morpy"]["activate_worksheet_done"]}\n'
                                f'{app_dict["loc"]["morpy"]["activate_worksheet_sht"]}: {worksheet}')

                check: bool = True
            else:
                # The requested sheet was not found.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["activate_worksheet_nfnd"]}\n'
                    f'{app_dict["loc"]["morpy"]["activate_worksheet_file"]}: {self.wb_path}\n'
                    f'{app_dict["loc"]["morpy"]["activate_worksheet_req_sht"]}: {worksheet}'
                )

        # Error detection
        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            'morpy_trace': morpy_trace,
            'check': check
        }

    @metrics
    def read_cells(self, morpy_trace: dict, app_dict: dict, cell_range: list=None,
                   cell_styles: bool=False, worksheet: str=None, gui=None) -> dict:
        r"""
        Reads the cells of MS Excel workbooks. Overlapping ranges will get auto-formatted
        to ensure every cell is addressed only once.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param cell_range: The cell or range of cells to read from. If cell range is None, will read all cells
            inside the matrix of max_row and max_column (also empty ones). formats:
            - not case-sensitive
            - Single cell: ["A1"]
            - Range of cells: ["A1:ZZ1000"]
            - Ranges of cells: ["A1:ZZ1000", "c2:fl342"]
        :param cell_styles: If True, cell styles will be retrieved. If False, get value only.
        :param worksheet: Name of the worksheet, where the cell is located. If None, the
            active sheet is addressed.
        :param gui: User Interface reference. Automatically referenced by morPy.ProgressTrackerTk()

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).
            cl_dict: Dictionary of cell content dictionaries containing values and styles of cells. Following is
                    an example of a single complete cell write:
                cl_dict = {
                    "A1" : {
                        "value" : "Data in Cell",
                        "comment" : {
                            "text" : "This is a comment",
                            "author" : "Mr. Author Man",
                        },
                        "format" : "General",           # Options: General|Number|Currency|Accounting|Date|Time|Percentage
                                                        # > Fraction|Scientific|Text|custom strings
                        "font" : {
                            "name" : "Calibri",
                            "bold" : True,
                            "italic" : True,
                            "vertical align" : None,    # Options: None|superscript|subscript
                            "underline" : None,         # Options: None|single|double|singleAccounting|doubleAccounting
                            "strike" : False,
                            "size" : 14,
                            "color" : "D1760C",
                        },
                        "background" : {
                            "fill type" : None,         # Options: None|solid|darkGrid|darkTrellis|lightDown|lightGray
                                                        # > lightGrid|lightHorizontal|lightTrellis|lightUp
                                                        # > lightVertical|mediumGray
                            "start color" : "307591",
                            "end color" : "67CCCC",
                        },
                        "border" : {
                            "edge" : "outline",         # Options: left|right|top|bottom|diagonal|outline
                                                        # > vertical|horizontal
                            "style" : None,             # Options: None|dashDot|dashDotDot|dashed|dotted|double|hair|medium
                                                        # > medium|mediumDashDot|mediumDashDotDot|mediumDashed|slantDashDot
                                                        # > thick|thin
                            "color" : "2A7F7F",
                            "diagonal direction" : 0,   # Options: 0 (no diagonal) | 1 (downwards) | 2 (upwards)
                        },
                        "alignment" : {
                            "horizontal" : "general",   # Options: general|left|center|right|fill|justify|centerContinuous
                                                        # > distributed
                            "vertical" : "center",      # Options: top|center|bottom|justify|distributed
                            "text rotation" : 0,
                            "wrap text" : False,
                            "shrink to fit" : False,
                            "indent" : 0,
                        },
                        "protection" : {
                            "locked" : False,
                            "hidden" : False,
                        },
                    },
                    "A2" : { ... }
                }

        :example:
            wb_path = "C:\my.xlsx"
            wb = morPy.XlWorkbook(morpy_trace, app_dict, wb_path)
            cl_dict = wb.read_cells(morpy_trace, app_dict, worksheet="Sheet1", cell_range=["A1", "B2:C3"])["cl_dict"]
            print(f'{cl_dict}')
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.xl'
        operation: str = 'XlWorkbook.read_cells(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        cl_dict = {}

        try:
            # Update metadata of the workbook instance
            self._update_meta(morpy_trace, app_dict)

            # Check if sheet is already active
            if self.active_sheet_title == worksheet:
                worksheet_obj = self.active_sheet

            # Set the requested sheet active
            else:
                # Check if sheet exists
                if worksheet in self.wb_sheets:
                    self.activate_worksheet(morpy_trace, app_dict, worksheet)
                    worksheet_obj = self.active_sheet

                elif not worksheet:
                    worksheet_obj = self.active_sheet
                    worksheet = self.active_sheet_title

                # The requested sheet was not found
                else:
                    # Could not find the requested worksheet.
                    raise ValueError(
                        f'{app_dict["loc"]["morpy"]["read_cells_nfnd"]}\n'
                        f'{app_dict["loc"]["morpy"]["read_cells_file"]}: {self.wb_path}\n'
                        f'{app_dict["loc"]["morpy"]["read_cells_sht"]}: {worksheet}\n'
                        f'{app_dict["loc"]["morpy"]["read_cells_av_shts"]}: {self.wb_sheets}'
                    )

            if not cell_range:
                cell_range = [
                    f'{openpyxl.utils.cell.get_column_letter(self.active_sheet.min_column)}{self.active_sheet.min_row}:'
                    f'{openpyxl.utils.cell.get_column_letter(self.active_sheet.max_column)}{self.active_sheet.max_row}'
                ]

            # Autoformat cell reference(s)
            cl_dict = self._cell_ref_autoformat(morpy_trace, app_dict, cell_range)["cl_dict"]

            # Loop through all the cells and read them
            for cl in cl_dict:
                cell_obj = worksheet_obj[cl]

                if cell_styles:
                    cl_dict[cl] =  {
                        "value": cell_obj.value,
                        "comment": {
                            "text": cell_obj.comment.text if cell_obj.comment else None,
                            "author": cell_obj.comment.author if cell_obj.comment else None,
                        },
                        "format": cell_obj.number_format,
                        "font": {
                            "name": cell_obj.font.name,
                            "bold": cell_obj.font.bold,
                            "italic": cell_obj.font.italic,
                            "vertical align": cell_obj.font.vertAlign,
                            "underline": cell_obj.font.underline,
                            "strike": cell_obj.font.strike,
                            "size": cell_obj.font.sz,
                            "color": cell_obj.font.color.rgb if cell_obj.font.color else None,
                        },
                        "background": {
                            "fill type": cell_obj.fill.fill_type,
                            "start color": cell_obj.fill.start_color.rgb if cell_obj.fill.start_color else None,
                            "end color": cell_obj.fill.end_color.rgb if cell_obj.fill.end_color else None,
                        },
                        "border": {
                            "top": {
                                "style": cell_obj.border.top.style if cell_obj.border.top else None,
                                "color": cell_obj.border.top.color.rgb if cell_obj.border.top.color else None,
                            },
                            "bottom": {
                                "style": cell_obj.border.bottom.style if cell_obj.border.bottom else None,
                                "color": cell_obj.border.bottom.color.rgb if cell_obj.border.bottom.color else None,
                            },
                            "left": {
                                "style": cell_obj.border.left.style if cell_obj.border.left else None,
                                "color": cell_obj.border.left.color.rgb if cell_obj.border.left.color else None,
                            },
                            "right": {
                                "style": cell_obj.border.right.style if cell_obj.border.right else None,
                                "color": cell_obj.border.right.color.rgb if cell_obj.border.right.color else None,
                            },
                        },
                        "alignment": {
                            "horizontal": cell_obj.alignment.horizontal,
                            "vertical": cell_obj.alignment.vertical,
                            "text rotation": cell_obj.alignment.textRotation,
                            "wrap text": cell_obj.alignment.wrapText,
                            "shrink to fit": cell_obj.alignment.shrinkToFit,
                            "indent": cell_obj.alignment.indent,
                        },
                        "protection": {
                            "locked": cell_obj.protection.locked,
                            "hidden": cell_obj.protection.hidden,
                        },
                    }
                else:
                    cl_dict[cl] =  {
                        "value": cell_obj.value,
                    }

            # The worksheet was read from.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["read_cells_read"]}\n'
                f'{app_dict["loc"]["morpy"]["read_cells_file"]}: {self.wb_path}\n'
                f'{app_dict["loc"]["morpy"]["read_cells_sht"]}: {worksheet}\n'
                f'{app_dict["loc"]["morpy"]["read_cells_cls"]}: {cell_range}')

            check: bool = True

        # Error detection
        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            'cl_dict' : cl_dict
            }

    @metrics
    def write_ranges(self, morpy_trace: dict, app_dict: dict, worksheet: str=None, cell_range: list=None,
                     cell_writes: list=None, fill_range: bool=False, style_default: bool=False,
                     save_workbook: bool=True, close_workbook: bool=False) -> dict:
        r"""
        Writes data into cells of an Excel workbook. OpenPyXL documentation:
        https://openpyxl.readthedocs.io/en/stable/api/openpyxl.cell.cell.html#openpyxl.cell.cell.Cell
        https://openpyxl.readthedocs.io/en/3.1.3/styles.html

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param worksheet: Name of the worksheet, where the cell is located. If None, the
            active sheet is addressed.
        :param cell_range: The cell or range of cells to write. Accepted formats:
            - not case-sensitive
            - Single cell: ["A1"]
            - Range of cells: ["A1:ZZ1000"]
            - Ranges of cells: ["A1:ZZ1000", "c2:fl342"]
        :param cell_writes: List of cell content dictionaries to be written consecutively. If the list is shorter
            than the amount of cells in the range, it will stop writing to cells and finish the operation. The
            dictionaries do not need to contain all possible keys, only assign the cell attributes/values needed.
            See example for a display of usage. Following is an example of a single complete cell write:
                cl_list = [
                    {"value" : "Data in Cell",
                    "comment" : {
                        "text" : "This is a comment",
                        "author" : "Mr. Author Man",
                    },
                    "format" : "General",           # Options: General|Number|Currency|Accounting|Date|Time|Percentage
                                                    # > Fraction|Scientific|Text|custom strings
                    "font" : {
                        "name" : "Calibri",
                        "bold" : True,
                        "italic" : True,
                        "vertical align" : None,    # Options: None|superscript|subscript
                        "underline" : None,         # Options: None|single|double|singleAccounting|doubleAccounting
                        "strike" : False,
                        "size" : 14,
                        "color" : "D1760C",
                    },
                    "background" : {
                        "fill type" : None,         # Options: None|solid|darkGrid|darkTrellis|lightDown|lightGray
                                                    # > lightGrid|lightHorizontal|lightTrellis|lightUp
                                                    # > lightVertical|mediumGray
                        "start color" : "307591",
                        "end color" : "67CCCC",
                    },
                    "border" : {
                        "edge" : "outline",         # Options: left|right|top|bottom|diagonal|outline
                                                    # > vertical|horizontal
                        "style" : None,             # Options: None|dashDot|dashDotDot|dashed|dotted|double|hair|medium
                                                    # > medium|mediumDashDot|mediumDashDotDot|mediumDashed|slantDashDot
                                                    # > thick|thin
                        "color" : "2A7F7F",
                        "diagonal direction" : 0,   # Options: 0 (no diagonal) | 1 (downwards) | 2 (upwards)
                    },
                    "alignment" : {
                        "horizontal" : "general",   # Options: general|left|center|right|fill|justify|centerContinuous
                                                    # > distributed
                        "vertical" : "center",      # Options: top|center|bottom|justify|distributed
                        "text rotation" : 0,
                        "wrap text" : False,
                        "shrink to fit" : False,
                        "indent" : 0,
                    },
                    "protection" : {
                        "locked" : False,
                        "hidden" : False,
                    },
                },
                { ... }]
        :param fill_range: If True and if the cell_writes list is shorter than the amount
            of cells in the range, it will continue writing the values from beginning until the end
            of the range.
        :param style_default: If True, styles/attributes of cells will be reset to default. If False,
            the styles/attributes of the original cell will be preserved.
        :param save_workbook: If True, saves the workbook after the changes.
        :param close_workbook: If True, closes the workbook.

        :return: dict
            check: Indicates whether the function executed successfully (True/False).
            morpy_trace: Operation credentials and tracing.
            wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                reference to an instance.

        :example:
            w_sh = "Sheet1"
            cl_rng = ["A1:A10"]
            cell_writes = []
            cell_writes.append(
                {"value": "Example"}
            )
            cell_writes.append({
                "value" : r"=1+2",
                "font" : {
                    "color" : "D1760C",
                    },
            })
            wb = wb.write_cells(morpy_trace, app_dict, worksheet=w_sh, cell_range=cl_rng, cell_writes=cell_writes
                                save_workbook=True, close_workbook=True)["wb_obj"]
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.xl'
        operation: str = 'write_ranges(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        wb_obj_return = self

        try:
            if not worksheet:
                self._update_meta(morpy_trace, app_dict, minimal=True)
                worksheet_obj = self.active_sheet
                sht_check: bool = True
            else:
                sht_check: bool = self.activate_worksheet(morpy_trace, app_dict, worksheet)["check"]
                worksheet_obj = self.active_sheet
                
            if cell_range and sht_check:
                cl_dict = self._cell_ref_autoformat(morpy_trace, app_dict, cell_range=cell_range)["cl_dict"]
                cell_keys = list(cl_dict.keys())
                write_count = len(cell_writes)

                for i, cell_key in enumerate(cell_keys):
                    cell_obj = worksheet_obj[cell_key]
                    write_data = cell_writes[i % write_count] if fill_range else cell_writes[i] if i < write_count else None

                    # Finish cell writes conditionally
                    if not write_data:
                        break

                    # Reset styles if requested
                    if style_default:
                        cell_obj.style = 'Normal'

                    # Get cell styles to be merged with cell_writes
                    cell_data = self.read_cells(morpy_trace, app_dict, cell_range=[cell_key],
                                                    worksheet=self.active_sheet_title)

                    if not cell_data["check"]:
                        continue

                    # Merge current styles with the ones provided in write_data

                    current_styles = cell_data["cl_dict"]  # e.g. {"A2": {"value":..., "font":...}}
                    cell_styles = current_styles.get(cell_key, {})  # e.g. {"value":..., "font":...}

                    # Merge in any new style info from write_data
                    for style_key, style_val in write_data.items():
                        if style_key in cell_styles and isinstance(style_val, dict):
                            # Merge with existing dictionary (e.g. "font", "alignment", "border")
                            cell_styles[style_key].update(style_val)
                        else:
                            # Overwrite or add a new key (e.g. "value")
                            cell_styles[style_key] = style_val

                    # Apply to the real cell:
                    if "value" in cell_styles:
                        cell_obj.value = cell_styles["value"]
                    if "comment" in cell_styles and cell_styles["comment"]:
                        from openpyxl.comments import Comment
                        cell_obj.comment = Comment(
                            text=cell_styles["comment"].get("text", ""),
                            author=cell_styles["comment"].get("author", ""),
                        )
                    if "font" in cell_styles:
                        cell_obj.font = Font(**cell_styles["font"])
                    if "background" in cell_styles:
                        cell_obj.fill = PatternFill(
                            fill_type=cell_styles["background"]["fill type"],
                            start_color=cell_styles["background"]["start color"],
                            end_color=cell_styles["background"]["end color"],
                        )
                    if "alignment" in cell_styles:
                        cell_obj.alignment = Alignment(**cell_styles["alignment"])
                    if "protection" in cell_styles:
                        cell_obj.protection = Protection(**cell_styles["protection"])

            elif not cell_range:
                # Missing cell range. Skipped writing to cells.
                raise ValueError(f'{app_dict["loc"]["morpy"]["write_cells_no_range"]}')

            # Cells written to.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["write_cells_done"]}\n'
                    f'{app_dict["loc"]["morpy"]["write_cells_range"]}: {cell_range}')

            if save_workbook:
                wb_obj_return = self.save_workbook(morpy_trace, app_dict, close_workbook=close_workbook)["wb_obj"]

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return {
            'morpy_trace' : morpy_trace,
            'check' : check,
            'wb_obj' : wb_obj_return,
        }

    @metrics
    def get_table_attributes(self, morpy_trace: dict, app_dict: dict, table: str) -> dict:
        r"""
        Retrieves all attributes of an MS Excel table. OpenPyXL documentation:
        https://openpyxl.readthedocs.io/en/stable/api/openpyxl.worksheet.table.html#openpyxl.worksheet.table.Table

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param table: Name of the table to be analyzed.

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).
            table_attr: List of the table's attributes.

        :example:
            wb_path = "C:\my.xlsx"
            wb = morPy.XlWorkbook(morpy_trace, app_dict, wb_path)
            table_attr = wb.get_table_attributes(morpy_trace, app_dict, "Table1")["table_attr"]
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module: str = 'lib.xl'
        operation: str = 'XlWorkbook.get_table_attributes(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        table_attr = None

        try:
            # Update metadata of the workbook instance
            self._update_meta(morpy_trace, app_dict, minimal=True)

            # Inquire the according worksheet of the table
            worksheet = self.tables_sheets[table]

            # Get all values of the table
            table_data = self.wb_obj[worksheet].tables.values()
            table_data = openpyxl_table_data_dict(morpy_trace, app_dict, table_data, table)
            table_attr = table_data["table_attr"]

            # Retrieved all values of an MS Excel table.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["get_table_attributes_retr"]}\n'
                    f'{app_dict["loc"]["morpy"]["get_table_attributes_path"]}: {self.wb_path}\n'
                    f'{app_dict["loc"]["morpy"]["get_table_attributes_sheet"]}: {worksheet}\n'
                    f'{app_dict["loc"]["morpy"]["get_table_attributes_table"]}: {table}')

            check: bool = True

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            'table_attr' : table_attr,
            }

@metrics
def openpyxl_table_data_dict(morpy_trace: dict, app_dict: dict, table_data: object, table: str) -> dict:

    r"""
    Converts the interface of an OpenPyXL data book into a dictionary containing
    all attributes of the specified table. This function is a helper and is
    typically called by `get_all_tables_attributes` to improve on the OpenPyXL
    API.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param table_data: The data book object as generated by OpenPyXL.
    :param table: Name of the table to be analyzed.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        table_attr: List containing all attributes of the OpenPyXL databook.

    :example:
        openpyxl_table_data_dict(morpy_trace, app_dict, databook_obj, "Table1")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module: str = 'lib.xl'
    operation: str = 'table_opyxl_datb_dict(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    table_data = f'{table_data}'
    table_item = ""
    table_attr = []

    try:
        # Search for regular expressions in the data book to extract only the
        # relevant Part.

        # 1. Purge all whitespace characters to make regex easier and more precise
        table_data = common.regex_replace(morpy_trace, app_dict, table_data, r'\s', '')

        # 2. Split the data-book into a list of distinct table attributes
        delimiter = '<openpyxl.worksheet.table.Tableobject>'
        table_data_list = common.regex_split(morpy_trace, app_dict, table_data, delimiter)

        # 3. Iterate through the list in search for the table and delete
        # elements not associated with it
        pattern = f'\'{table}\''

        for table_item in table_data_list:

            result = common.regex_find1st(morpy_trace, app_dict, table_item, pattern)

            if result:
                break

        # 4. Replace the comma at the end of the string, if there is any
        table_item = common.regex_replace(morpy_trace, app_dict, table_item, ',$', '')

        # 5. Add the first delimiter and reinsert some spaces for compatibility
        # with OpenPyXL
        table_item = f'<openpyxl.worksheet.table.Tableobject>{table_item}'
        table_item = common.regex_replace(morpy_trace, app_dict, table_item, 'object>', ' object>')

        # 6. Split the string into different sections
        table_attr = common.regex_split(morpy_trace, app_dict, table_item, ',')

        # Converted an OpenPyXL data-book into a list specific to the attributes of the MS Excel table.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["openpyxl_table_data_dict_conv"]}\n'
                f'{app_dict["loc"]["morpy"]["openpyxl_table_data_dict_tbl"]}: {table}\n'
                f'{app_dict["loc"]["morpy"]["openpyxl_table_data_dict_attr"]}:\n{table_attr}')

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'table_attr' : table_attr
        }
```

## app.init.py

```Python
r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from lib.decorators import metrics, log

import sys

@metrics
def app_init(morpy_trace: dict, app_dict: dict) -> dict:

    r"""
    This function runs the initialization workflow of the app.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_init_return: Return value (dict) of the initialization process, handed to app_run

    :example:
    >>> from app import init as app_init
    >>> init_retval = app_init(morpy_trace, app_dict)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module: str = 'app.init'
    operation: str = 'app_init(~)'
    morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

    # OPTION enable/disable logging
    # ??? morpy_trace["log_enable"] = False

    check: bool = False
    app_init_return = {}

    try:
        # TODO: MY CODE

        check: bool = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{type(e).__name__}: {e}')
    finally:
        # Initialization complete flag
        # Up until this point prints to console are mirrored on splash screen
        app_dict["run"]["init_complete"] = True

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            'app_init_return' : app_init_return
            }
```

## app.run.py

```Python
r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from lib.decorators import metrics, log

import sys

@metrics
def app_run(morpy_trace: dict, app_dict: dict, app_init_return: dict) -> dict:
    r"""
    This function runs the main workflow of the app.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_init_return: Return value (dict) of the initialization process, returned by app_init

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        app_run_return: Return value (dict) of the app process, handed to app_exit

    :example:
    >>> from app import init as app_init
    >>> from app import run as app_run

    >>> init_retval = app_init(morpy_trace, app_dict)
    >>> run_retval = app_run(morpy_trace, app_dict, init_retval)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module: str = 'app.run'
    operation: str = 'app_run(~)'
    morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

    check: bool = False
    app_run_return = {}

    try:
        # Demonstrate how to use lib.ui_tk.ProgressTrackerTk()
        import demo.ProgressTrackerTk as demo_ProgressTrackerTk
        demo_ProgressTrackerTk.run(morpy_trace, app_dict)

        # app_dict["global"]["app"]["test"] = True

        check: bool = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'app_run_return' : app_run_return
        }

@metrics
def new_process(morpy_trace: dict, app_dict: dict, counter: int=0) -> dict:
    r"""
    This function runs the entire app using user input to specify
    the actions performed.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param counter: Processes opened counter

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        new_process(morpy_trace, app_dict, counter)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module: str = 'app.run'
    operation: str = 'new_process(~)'
    morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

    check: bool = False
    p = None

    try:
        # TODO port to it's own demo module
        # log(morpy_trace, app_dict, "info",
        # lambda: "New process starting...")
        #
        # task = (arbitrary_parallel_task, morpy_trace, app_dict)  # Memory reference to app_dict
        # priority = 100
        # morPy.process_q(task=task, priority=priority)
        #
        # task_dqued = app_dict["proc"]["morpy"]["process_q"].dequeue(morpy_trace, app_dict)
        #
        # mp.run_parallel(morpy_trace, app_dict, task=task_dqued["task"], priority=task_dqued["priority"])

        check: bool = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'process' : p
        }
```

## app.exit.py

```Python
r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from lib.mp import join_all_from_child
from lib.decorators import metrics, log

import sys

@metrics
def app_exit(morpy_trace: dict, app_dict: dict, app_run_return: dict) -> dict:
    r"""
    This function runs the exit workflow of the app.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param app_run_return: Return value (dict) of the app, returned by app_run.
        This dictionary is not shared with other processes by default.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        from app import init as app_init
        from app import run as app_run
        from app import exit as app_exit

        # Assuming app_dict is initialized correctly
        init_retval = app_init(morpy_trace, app_dict)
        run_retval = app_run(morpy_trace, app_dict, init_retval)
        app_exit(morpy_trace, app_dict, run_retval)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module: str = 'app.exit'
    operation: str = 'app_exit(~)'
    morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

    # OPTION enable/disable logging
    # ??? morpy_trace["log_enable"] = False

    check: bool = False

    try:
        # TODO: first statement .join()
        # TODO: MY CODE
        check: bool = True

    except Exception as e:
        raise morPy.exception(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    finally:
        # Join all spawned processes before transitioning into the next phase.
        join_all_from_child(morpy_trace, app_dict, child_pid=morpy_trace["process_id"])
        # Signal morPy orchestrator of app termination
        app_dict["morpy"]["exit"] = True

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            }
```

## UltraDict.py (original)

```Python
#
# UltraDict
#
# A sychronized, streaming Python dictionary that uses shared memory as a backend
#
# Copyright [2022] [Ronny Rentner] [ultradict.code@ronny-rentner.de]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__all__ = ['UltraDict']

import multiprocessing, multiprocessing.shared_memory, multiprocessing.synchronize
import collections, os, pickle, sys, time, weakref
import importlib.util, importlib.machinery

try:
    # Needed for the shared locked
    import atomics
except ModuleNotFoundError:
    pass

try:
    import ultraimport
    Exceptions = ultraimport('__dir__/Exceptions.py')
    try:
        log = ultraimport('__dir__/utils/log.py', 'log', package=1)
        log.log_targets = [ sys.stderr ]
    except ultraimport.ResolveImportError:
        import logging as log
except ModuleNotFoundError:
    from . import Exceptions
    try:
        from .utils import log
        log.log_targets = [ sys.stderr ]
    except ModuleNotFoundError:
        import logging as log

def remove_shm_from_resource_tracker():
    """
    Monkey-patch multiprocessing.resource_tracker so SharedMemory won't be tracked
    More details at: https://bugs.python.org/issue38119
    """
    # pylint: disable=protected-access, import-outside-toplevel
    # Ignore linting errors in this bug workaround hack
    from multiprocessing import resource_tracker
    def fix_register(name, rtype):
        if rtype == "shared_memory":
            return None
        return resource_tracker._resource_tracker.register(name, rtype)
    resource_tracker.register = fix_register
    def fix_unregister(name, rtype):
        if rtype == "shared_memory":
            return None
        return resource_tracker._resource_tracker.unregister(name, rtype)
    resource_tracker.unregister = fix_unregister
    if "shared_memory" in resource_tracker._CLEANUP_FUNCS:
        del resource_tracker._CLEANUP_FUNCS["shared_memory"]

#More details at: https://bugs.python.org/issue38119
remove_shm_from_resource_tracker()

class UltraDict(collections.UserDict, dict):

    Exceptions = Exceptions
    log = log

    class RLock(multiprocessing.synchronize.RLock):
        """ Not yet used """
        pass

    class SharedLock():
        """
        Lock stored in shared_memory to provide an additional layer of protection,
        e.g. when using spawned processes.

        Internally uses atomics package of patomics for atomic locking.

        This is needed if you write to the shared memory with independent processes.
        """

        __slots__ = 'parent', 'has_lock',  'ctx', 'lock_atomic', 'lock_remote', \
            'pid', 'pid_bytes', 'pid_remote', 'pid_remote_ctx', 'pid_remote_atomic', \
            'next_acquire_parameters'

        def __init__(self, parent, lock_name, pid_name):
            self.has_lock = 0
            self.next_acquire_parameters = ()

            # `lock_name` contains the name of the attribute that the parent uses
            # to store the memory view on the remote lock, so `self.lock_remote` is
            # referring to a memory view
            self.lock_remote = getattr(parent, lock_name)
            self.pid_remote = getattr(parent, pid_name)

            self.init_pid()

            try:
                self.ctx = atomics.atomicview(buffer=self.lock_remote[0:1], atype=atomics.BYTES)
                self.pid_remote_ctx = atomics.atomicview(buffer=self.pid_remote[0:4], atype=atomics.BYTES)
            except NameError as e:
                self.cleanup()
                raise e
            self.lock_atomic = self.ctx.__enter__()
            self.pid_remote_atomic = self.pid_remote_ctx.__enter__()

            def after_fork():
                if self.has_lock:
                    raise Exception("Release the SharedLock before you fork the process")

                # After forking, we got a new pid
                self.init_pid()

            if sys.platform != 'win32':
                os.register_at_fork(after_in_child=after_fork)

        def init_pid(self):
            self.pid = multiprocessing.current_process().pid
            self.pid_bytes = self.pid.to_bytes(4, 'little')

        def acquire_with_timeout(self, block=True, sleep_time=0.000001, timeout=1.0, steal_after_timeout=False):
            # The block parameter will be ignored
            time_start = None
            blocking_pid = None
            while True:
                try:
                    return self.acquire(block=False, sleep_time=sleep_time)
                except Exceptions.CannotAcquireLock as e:
                    if not time_start:
                        time_start = e.timestamp
                        blocking_pid = e.blocking_pid

                    # We should not be the blocking pid
                    assert blocking_pid != self.pid

                    time_passed = time.monotonic() - time_start

                    if time_passed >= timeout:
                        if steal_after_timeout:
                            # If the blocking pid has changed meanwhile, someone else took or stole the lock
                            if blocking_pid == e.blocking_pid:
                                self.steal_from_dead(from_pid=blocking_pid, release=True)
                            time_start = None
                            blocking_pid = None
                            continue
                        raise Exceptions.CannotAcquireLockTimeout(blocking_pid = e.blocking_pid, timestamp=time_start) from None


        #@profile
        def acquire(self, block=True, sleep_time=0.000001, timeout=None, steal_after_timeout=False):
            # If we already own the lock, just increment our counter
            if self.has_lock:
                self.has_lock += 1
                return True

            if timeout:
                return self.acquire_with_timeout(sleep_time=sleep_time, timeout=timeout, steal_after_timeout=steal_after_timeout)

            while True:
                # We need both, the shared lock to be False and the lock_pid to be 0
                if self.test_and_inc():

                    assert self.has_lock == 0
                    self.has_lock = 1

                    # If nobody had owned the lock, so the remote pid should be zero
                    assert self.pid_remote[0:4] == b'\x00\x00\x00\x00'

                    self.pid_remote[:] = self.pid_bytes
                    return True

                # If set to 0, we practically have a busy wait
                if sleep_time:
                    # On Python < 3.10, this smallest possible time is actually rather big,
                    #  maybe around 10 ms, depending on your CPU.
                    time.sleep(sleep_time)

                if not block:
                    raise Exceptions.CannotAcquireLock(blocking_pid=self.get_remote_pid())

        #@profile
        def test_and_inc(self):
            old = self.lock_atomic.exchange(b'\x01')
            if old != b'\x00':
                # Oops, someone else was faster than us
                return False
            return True

        #@profile
        def test_and_dec(self):
            old = self.lock_atomic.exchange(b'\x00')
            if old != b'\x01':
                raise Exception("Failed to release lock")
            return True

        #@profile
        def release(self, *args):
            #log.debug("Release lock, lock={}", self.has_lock)
            if self.has_lock > 0:
                owner = int.from_bytes(self.pid_remote, 'little')
                if owner != self.pid:
                    raise Exception(f"Our lock for pid {self.pid} was stolen by pid {owner}")
                self.has_lock -= 1
                # Last local lock released, release shared lock
                if not self.has_lock:
                    self.pid_remote[:] = b'\x00\x00\x00\x00'
                    self.test_and_dec()
                #log.debug("Relased lock, lock={} pid_remote={}", self.has_lock, int.from_bytes(self.pid_remote, 'little'))
                return True

            return False

        def reset(self):
            # Risky
            self.lock_remote[:] = b'\x00'
            self.pid_remote[:] = b'\x00\x00\x00\x00'
            self.has_lock = 0

        def reset_acquire_parameters(self):
            self.next_acquire_parameters = ()

        def steal(self, from_pid=0, release=False):
            if self.has_lock:
                raise Exception("Cannot steal the lock because we have already acquired it. Use release() to release the lock.")

            #log.debug(f'Stealing from_pid={from_pid}, remote_pid={self.get_remote_pid()}')

            # It's not locked, so nothing to steal from
            if not self.get_remote_lock():
                return False

            # Someone else has stolen the lock
            if from_pid != self.get_remote_pid():
                return False

            # Stealing the lock means actually just putting our pid into the shared memory overwriting the other pid.
            # This can go wrong if the lock owner is actually still alive and working.
            result = self.pid_remote_atomic.cmpxchg_strong(expected=from_pid.to_bytes(4, 'little'), desired=self.pid_bytes)
            if result.success:
                self.has_lock = 1
                if release:
                    self.release()
            return result.success

        def steal_from_dead(self, from_pid=0, release=False):
            """ Check if from_pid is actually a dead process and if yes, steal the lock from it.
                Optionally, the lock can be directly released after stealing it.
            """

            try:
                import psutil
            except ModuleNotFoundError:
                raise Exceptions.MissingDependency("Install `psutil` Python package to use shared_lock=True") from None
            # No process must exist anymore with the from_pid or it must at least be dead (ie. zombie status)
            try:
                p = psutil.Process(from_pid)
                if p and p.is_running() and p.status() not in [psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD]:
                    raise Exception(f"Trying to steal lock from process that is still alive, something seems really wrong from_pid={from_pid} pid={self.pid} p={p}")
            except psutil.NoSuchProcess:
                # If the process is already gone, we cannot find information about it.
                # It will be safe to steal the lock.
                pass
            except Exception as e:
                raise e

            return self.steal(from_pid=from_pid, release=release)

        def status(self):
            return {
                'has_lock': self.has_lock,
                'lock_remote': int.from_bytes(self.lock_remote, 'little'),
                'pid': self.pid,
                'pid_remote': int.from_bytes(self.pid_remote, 'little'),
            }

        def print_status(self, status=None):
            import pprint
            if not status:
                status = self.status()
            pprint.pprint(status)

        def cleanup(self):
            if hasattr(self, 'ctx'):
                self.ctx.__exit__(None, None, None)
                del self.ctx
            if hasattr(self, 'lock_atomic'):
                del self.lock_atomic
            if hasattr(self, 'pid_remote_ctx'):
                self.pid_remote_ctx.__exit__(None, None, None)
                del self.pid_remote_ctx
            if hasattr(self, 'pid_remote_aotmic'):
                del self.pid_remote_atomic
            del self.lock_remote
            del self.pid_remote
            del self.pid_bytes
            del self.pid

        def get_remote_pid(self):
            return int.from_bytes(self.pid_remote, 'little')

        def get_remote_lock(self):
            return int.from_bytes(self.lock_remote, 'little')

        def __repr__(self):
            return f"{self.__class__.__name__} @{hex(id(self))} lock_remote={int.from_bytes(self.lock_remote, 'little')}, has_lock={self.has_lock}, pid={self.pid}), pid_remote={int.from_bytes(self.pid_remote, 'little')}"

        def __enter__(self):
            self.acquire(*self.next_acquire_parameters)
            self.reset_acquire_parameters()
            return self

        def __exit__(self, type, value, traceback):
            self.release()
            # Make sure exceptions are not ignored
            return False

        def __call__(self, block=True, timeout=None, sleep_time=0.000001, steal_after_timeout=False):
            self.next_acquire_parameters = ( block, timeout, sleep_time, steal_after_timeout )

            return self

    __slots__ = 'name', 'control', 'buffer', 'buffer_size', 'lock', 'shared_lock', \
        'update_stream_position', 'update_stream_position_remote', \
        'full_dump_counter', 'full_dump_memory', 'full_dump_size', \
        'serializer', \
        'lock_pid_remote', \
        'lock_remote', \
        'full_dump_counter_remote', \
        'full_dump_static_size_remote', \
        'shared_lock_remote', \
        'recurse', 'recurse_remote', 'recurse_register', \
        'full_dump_memory_name_remote', \
        'data', 'closed', 'auto_unlink', \
        'finalizer'

    def __init__(self, *args, name=None, create=None, buffer_size=10_000, serializer=pickle, shared_lock=None, full_dump_size=None,
            auto_unlink=None, recurse=None, recurse_register=None, **kwargs):
        # pylint: disable=too-many-branches, too-many-statements

        # On win32, only multiples of 4k are allowed
        if sys.platform == 'win32':
            buffer_size = -(buffer_size // -4096) * 4096
            if full_dump_size:
                full_dump_size = -(full_dump_size // -4096) * 4096

        assert buffer_size < 2**32

        if recurse:
            assert serializer == pickle

        self.data = {}

        # Local position, ie. the last position we have processed from the stream
        self.update_stream_position  = 0

        # Local version counter for the full dumps, ie. if we find a higher version
        # remote, we need to load a full dump
        self.full_dump_counter       = 0

        self.closed = False
        self.auto_unlink = auto_unlink

        # Small 1000 bytes of shared memory where we store the runtime state
        # of our update stream
        self.control = self.get_memory(create=create, name=name, size=1000)
        self.name = self.control.name

        def finalize(weak_self, name):
            #log.debug('Finalize', name)
            resolved_self = weak_self()
            if resolved_self is not None:
                #log.debug('Weakref is intact, closing')
                resolved_self.close(from_finalizer=True)
            #log.debug('Finalized')

        self.finalizer = weakref.finalize(self, finalize, weakref.ref(self), self.name)

        self.init_remotes()

        self.serializer = serializer

        # Actual stream buffer that contains marshalled data of changes to the dict
        self.buffer = self.get_memory(create=create, name=self.name + '_memory', size=buffer_size)
        # TODO: Raise exception if buffer size mismatch
        self.buffer_size = self.buffer.size

        self.full_dump_memory = None

        # Dynamic full dump memory handling
        # Warning: Issues on Windows when the process ends that has created the full dump memory
        self.full_dump_size = None

        if hasattr(self.control, 'created_by_ultra'):

            if auto_unlink is None:
                self.auto_unlink = True

            if recurse:
                self.recurse_remote[0:1] = b'1'

            if shared_lock:
                self.shared_lock_remote[0:1] = b'1'

            # We created the control memory, thus let's check if we need to create the
            # full dump memory as well
            if full_dump_size:
                self.full_dump_size = full_dump_size
                self.full_dump_static_size_remote[:] = full_dump_size.to_bytes(4, 'little')

                self.full_dump_memory = self.get_memory(create=True, name=self.name + '_full', size=full_dump_size)
                self.full_dump_memory_name_remote[:] = self.full_dump_memory.name.encode('utf-8').ljust(255)

        # We just attached to the existing control
        else:
            # TODO: Detect configuration mismatch and raise an exception

            # Check if we have a fixed size full dump memory
            size = int.from_bytes(self.full_dump_static_size_remote, 'little')

            # Check if shared_lock parameter was not set to inconsistent value
            shared_lock_remote = self.shared_lock_remote[0:1] == b'1'
            if shared_lock is None:
                shared_lock = shared_lock_remote
            elif shared_lock != shared_lock_remote:
                raise Exceptions.ParameterMismatch(f"shared_lock={shared_lock} was set but the creator has used shared_lock={shared_lock_remote}")

            # Check if recurse parameter was not set to inconsistent value
            recurse_remote = self.recurse_remote[0:1] == b'1'
            if recurse is None:
                recurse = recurse_remote
            elif recurse != recurse_remote:
                raise Exceptions.ParameterMismatch(f"recure={recurse} was set but the creator has used recurse={recurse_remote}")

            # Got existing size of full dump memory, that must mean it's static size
            # and we should attach to it
            if size > 0:
                self.full_dump_size = size
                self.full_dump_memory = self.get_memory(create=False, name=self.name + '_full')

        # Local lock for all processes and threads created by the same interpreter
        if shared_lock:
            try:
                self.lock = self.SharedLock(self, 'lock_remote', 'lock_pid_remote')
            except NameError:
                #self.cleanup()
                raise Exceptions.MissingDependency("Install `atomics` Python package to use shared_lock=True") from None
        else:
            self.lock = multiprocessing.RLock()

        self.shared_lock = shared_lock

        # Parameters that could be read from remote if we are connecting to an existing UltraDict
        self.recurse = recurse

        # In recurse mode, we must ensure a recurse register
        if self.recurse:
            # Must be either the name of an UltraDict as a string or an UltraDict instance
            if recurse_register is not None:
                if type(recurse_register) == str:
                    self.recurse_register = UltraDict(name=recurse_register)
                elif type(recurse_register) == UltraDict:
                    self.recurse_register = recurse_register
                else:
                    raise Exception("Bad type for recurse_register")

            # If no register was defined, we should create one
            else:
                self.recurse_register = UltraDict(name=f'{self.name}_register',
                    recurse=False, auto_unlink=False, shared_lock=self.shared_lock)
                # The register should not run its own finalizer if we need it later for unlinking our nested children
                if self.auto_unlink:
                    self.recurse_register.finalizer.detach()
                    #log.debug("Created recurse register with name={}", self.recurse_register.name)

        else:
            self.recurse_register = None

        super().__init__(*args, **kwargs)

        # Load all data from shared memory
        self.apply_update()

        if sys.platform == 'win32':
            if not shared_lock:
                log.warning('You are running on win32, potentially without locks. Consider setting shared_lock=True')


        #if auto_unlink:
        #    atexit.register(self.unlink)
        #else:
        #    atexit.register(self.cleanup)

        #log.debug("Initialized", self.name)

    def __del__(self):
        #log.debug("__del__", self.name)
        self.close()
        if hasattr(self, 'recurse') and self.recurse:
            #log.debug("Close recurse register")
            self.recurse_register.close()
            del self.recurse_register


    def init_remotes(self):
        # Memoryviews to the right buffer position in self.control
        self.update_stream_position_remote = self.control.buf[ 0:  4]
        self.lock_pid_remote               = self.control.buf[ 4:  8]
        self.lock_remote                   = self.control.buf[ 8: 10]
        self.full_dump_counter_remote      = self.control.buf[10: 14]
        self.full_dump_static_size_remote  = self.control.buf[14: 18]
        self.shared_lock_remote            = self.control.buf[18: 19]
        self.recurse_remote                = self.control.buf[19: 20]
        self.full_dump_memory_name_remote  = self.control.buf[20:275]

    def del_remotes(self):
        """
        Delete all instance attributes whose name ends with '_remote' from
        the instance for cleanup. This shall ensure there are no
        reference left to shared memory views so proper cleanup can happen.
        """
        remotes = [ r for r in dir(self) if r.endswith('_remote') ]
        for r in remotes:
            if hasattr(self, r):
                delattr(self, r)

    def __reduce__(self):
        from functools import partial
        return (partial(self.__class__, name=self.name, auto_unlink=self.auto_unlink, recurse_register=self.recurse_register), ())

    @staticmethod
    def get_memory(*, create=True, name=None, size=0):
        """
        Attach an existing SharedMemory object with `name`.

        If `create` is True, create the object if it does not exist.
        """
        assert size > 0 or not create
        if name:
            # First try to attach to existing memory
            try:
                memory = multiprocessing.shared_memory.SharedMemory(name=name)
                #log.debug('Attached shared memory: ', memory.name)

                if create:
                    raise Exceptions.AlreadyExists(f"Cannot create memory '{name}' because it already exists")

                return memory
            except FileNotFoundError:
                pass

        # No existing memory found
        if create or create is None:
            memory = multiprocessing.shared_memory.SharedMemory(create=True, size=size, name=name)
            #multiprocessing.resource_tracker.unregister(memory._name, 'shared_memory')
            # Remember that we have created this memory
            memory.created_by_ultra = True
            #log.debug('Created shared memory: ', memory.name)

            return memory

        raise Exceptions.CannotAttachSharedMemory(f"Could not get memory '{name}'")

    #@profile
    def dump(self):
        """ Dump the full dict into shared memory """

        with self.lock:
            old = bytes(self.full_dump_memory_name_remote).decode('utf-8').strip().strip('\x00')

            self.apply_update()

            marshalled = self.serializer.dumps(self.data)
            length = len(marshalled)

            # If we don't have a fixed size, let's create full dump memory dynamically
            # TODO: This causes issues on Windows because the memory is not persistant
            #       Maybe switch to mmaped file?
            if self.full_dump_size and self.full_dump_memory:
                full_dump_memory = self.full_dump_memory
            else:
                # Dynamic full dump memory
                full_dump_memory = self.get_memory(create=True, size=length + 6)

            #log.debug("Full dump memory: ", full_dump_memory)

            if length + 6 > full_dump_memory.size:
                raise Exceptions.FullDumpMemoryFull(f'Full dump memory too small for full dump: needed={length + 6} got={full_dump_memory.size}')

            # Write header, 6 bytes
            # First byte is FF byte
            full_dump_memory.buf[0:1] = b'\xFF'
            # Then comes 4 bytes of length of the body
            full_dump_memory.buf[1:5] = length.to_bytes(4, 'little')
            # Then another FF bytes, end of header
            full_dump_memory.buf[5:6] = b'\xFF'

            # Write body
            full_dump_memory.buf[6:6+length] = marshalled

            # On Windows, if we close it, it cannot be read anymore by anyone else.
            if not self.full_dump_size and sys.platform != 'win32':
                full_dump_memory.close()

            # TODO: There's a slight chance of something going wrong when we first update
            #       the remote memory name and then the counter.

            # Only after we have filled the new full dump memory with the marshalled data,
            # we update the remote name so other users can find it
            if not (self.full_dump_size and self.full_dump_memory):
                self.full_dump_memory_name_remote[:] = full_dump_memory.name.encode('utf-8').ljust(255)

            self.full_dump_counter += 1
            current = int.from_bytes(self.full_dump_counter_remote, 'little')
            # Now also increment the remote counter
            self.full_dump_counter_remote[:] = int(current + 1).to_bytes(4, 'little')

            # Reset the stream position to zero as we have
            # just provided a fresh new full dump
            self.update_stream_position = 0
            self.update_stream_position_remote[:] = b'\x00\x00\x00\x00'

            #log.info("Dumped dict with {} elements to {} bytes, remote_counter={}", len(self), len(marshalled), current+1)

            # If the old full dump memory was dynamically created, delete it
            if old and old != full_dump_memory.name and not self.full_dump_size:
                self.unlink_by_name(old)

            # On Windows, we need to keep a reference to the full dump memory,
            # otherwise it's destoryed
            self.full_dump_memory = full_dump_memory

            return full_dump_memory

    def get_full_dump_memory(self, max_retry=3, retry=0):
        """
        Attach to the full dump memory.

        Retry if necessary for a low number of times. It could happen that the full
        dump memory was removed because a new full dump was created before we had the
        chance to read the old full dump.

        """
        try:
            name = bytes(self.full_dump_memory_name_remote).decode('utf-8').strip().strip('\x00')
            #log.debug("Full dump name={}", name)
            assert len(name) >= 1
            return self.get_memory(create=False, name=name)
        except Exceptions.CannotAttachSharedMemory as e:
            if retry < max_retry:
                return self.get_full_dump_memory(max_retry=max_retry, retry=retry+1)
            elif retry == max_retry:
                # On the last retry, let's use a lock to ensure we can safely import the dump
                with self.lock:
                    return self.get_full_dump_memory(max_retry=max_retry, retry=retry+1)
            else:
                raise e

    #@profile
    def load(self, force=False):
        """
        Opportunistacally load full dumps without any locking.

        There is a rare case where a full dump is replaced with a newer full dump while
        we didn't have the chance to load the old one. In this case, we just retry.
        """
        full_dump_counter = int.from_bytes(self.full_dump_counter_remote, 'little')
        #log.debug("Loading full dump local_counter={} remote_counter={}", self.full_dump_counter, full_dump_counter)
        try:
            if force or (self.full_dump_counter < full_dump_counter):
                if self.full_dump_size and self.full_dump_memory:
                    full_dump_memory = self.full_dump_memory
                else:
                    # Retry if necessary
                    full_dump_memory = self.get_full_dump_memory()

                buf = full_dump_memory.buf
                pos = 0

                # Read header
                # The first byte should be a FF byte to introduce the header
                assert bytes(buf[pos:pos+1]) == b'\xFF'
                pos += 1
                # Then comes 4 bytes of length
                length = int.from_bytes(bytes(buf[pos:pos+4]), 'little')
                assert length > 0, (self.status(), full_dump_memory, bytes(buf[:]).decode('utf-8').strip().strip('\x00'), len(buf))
                pos += 4
                #log.debug("Found update, pos={} length={}", pos, length)
                assert bytes(buf[pos:pos+1]) == b'\xFF'
                pos += 1
                # Unserialize the update data, we expect a tuple of key and value
                self.data = self.serializer.loads(bytes(buf[pos:pos+length]))
                self.full_dump_counter = full_dump_counter
                self.update_stream_position = 0

                if sys.platform != 'win32' and not self.full_dump_memory:
                    full_dump_memory.close()
            else:
                raise Exception("Cannot load full dump, no new data available")
        except AssertionError as e:
            full_dump_delta = int.from_bytes(self.full_dump_counter_remote, 'little') - self.full_dump_counter
            if full_dump_delta > 1:
                # If more than one new full dump was created during the time we were trying to load one full dump
                # it can happen that our full dump has just disappeared
                return self.load(force=True)
            # TODO: Before we reach max recursion depth, try to load the full dump using a lock
            self.print_status()
            raise e

    #@profile
    def append_update(self, key, item, delete=False):
        """ Append dict changes to shared memory stream """

        # If mode is 0, it means delete the key from the dict
        # If mode is 1, it means update the key
        #mode = not delete
        marshalled = self.serializer.dumps((not delete, key, item))
        length = len(marshalled)

        with self.lock:
            start_position = int.from_bytes(self.update_stream_position_remote, 'little')
            # 6 bytes for the header
            end_position = start_position + length + 6
            #log.debug("Update start from={} len={}", start_position, length)
            if end_position > self.buffer_size:
                #log.debug("Buffer is full")

                # todo: is is necessary? apply_update() is also done inside dump()
                self.apply_update()
                if not delete:
                    self.data.__setitem__(key, item)
                self.dump()
                return

            marshalled = b'\xFF' + length.to_bytes(4, 'little') + b'\xFF' + marshalled

            # Write body with the real data
            self.buffer.buf[start_position:end_position] = marshalled

            # Inform others about it
            self.update_stream_position = end_position
            self.update_stream_position_remote[:] = end_position.to_bytes(4, 'little')
            #log.debug("Update end to={} buffer_size={} ", end_position, self.buffer_size)

    #@profile
    def apply_update(self):
        """ Opportunistically apply dict changes from shared memory stream without any locking.  """

        if self.full_dump_counter < int.from_bytes(self.full_dump_counter_remote, 'little'):
            self.load(force=True)

        if self.update_stream_position < int.from_bytes(self.update_stream_position_remote, 'little'):

            # Remember start position in the update stream
            pos = self.update_stream_position
            #log.debug("Apply update: stream position own={} remote={} full_dump_counter={}", pos, int.from_bytes(self.update_stream_position_remote, 'little'), self.full_dump_counter)

            try:
                # Iterate over all updates until the start of the last update
                while pos < int.from_bytes(self.update_stream_position_remote, 'little'):
                    # Read header
                    # The first byte should be a FF byte to introduce the headerfull_dump_counter_remote
                    assert bytes(self.buffer.buf[pos:pos+1]) == b'\xFF'
                    pos += 1
                    # Then comes 4 bytes of length
                    length = int.from_bytes(bytes(self.buffer.buf[pos:pos+4]), 'little')
                    pos += 4
                    #log.debug("Found update, update_stream_position={} length={}", self.update_stream_position, length + 6)
                    assert bytes(self.buffer.buf[pos:pos+1]) == b'\xFF'
                    pos += 1
                    # Unserialize the update data, we expect a tuple of key and value
                    mode, key, value = self.serializer.loads(bytes(self.buffer.buf[pos:pos+length]))
                    # Update or local dict cache (in our parent)
                    if mode:
                        self.data.__setitem__(key, value)
                    else:
                        self.data.__delitem__(key)
                    pos += length
                    # Remember that we have applied the update
                    self.update_stream_position = pos
            except (AssertionError, pickle.UnpicklingError) as e:

                # It can happen that a slow process is not fast enough reading the stream and some
                # other process already got around overwriting the current position. It is possible to
                # recover from this situation if and only if a new, fresh full dump exists that can be loaded.
                if self.full_dump_counter < int.from_bytes(self.full_dump_counter_remote, 'little'):
                    log.warning(f"Full dumps too fast full_dump_counter={self.full_dump_counter} full_dump_counter_remote={int.from_bytes(self.full_dump_counter_remote, 'little')}. Consider increasing buffer_size.")
                    return self.apply_update()

                # As a last resort, let's get a lock. This way we are safe but slow.
                with self.lock:
                    if self.full_dump_counter < int.from_bytes(self.full_dump_counter_remote, 'little'):
                        log.warning(f"Full dumps too fast full_dump_counter={self.full_dump_counter} full_dump_counter_remote={int.from_bytes(self.full_dump_counter_remote, 'little')}. Consider increasing buffer_size.")
                        return self.apply_update()

                raise e

    def update(self, other=None, *args, **kwargs):
        # pylint: disable=arguments-differ, keyword-arg-before-vararg

        # The original signature would be `def update(self, other=None, /, **kwargs)` but
        # this is not possible with Cython. *args will just be ignored.

        if other is not None:
            for k, v in other.items() if isinstance(other, collections.abc.Mapping) else other:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def __delitem__(self, key):
        #log.debug("__delitem__ {}", key)
        with self.lock:
            self.apply_update()

            # Update our local copy
            self.data.__delitem__(key)

            self.append_update(key, b'', delete=True)
            # TODO: Do something if append_update() fails

    def __setitem__(self, key, item):
        #log.debug("__setitem__ {}, {}", key, item)
        with self.lock:
            self.apply_update()

            if self.recurse:

                assert type(self.recurse_register) == UltraDict, "recurse_register must be an UltraDict instance"

                if type(item) == dict:
                    # TODO: Use parent's buffer with a namespace prefix?
                    item = UltraDict(item,
                                     recurse          = True,
                                     recurse_register = self.recurse_register,
                                     auto_unlink      = False,
                                     shared_lock      = self.shared_lock,
                                     buffer_size      = self.buffer_size,
                                     full_dump_size   = self.full_dump_size)

                    if item.name not in self.recurse_register.data:
                        self.recurse_register[item.name] = True

            # Update our local copy
            # It's important for the integrity to do this first
            self.data.__setitem__(key, item)

            # Append the update to the update stream
            self.append_update(key, item)
            # TODO: Do something if append_u int.from_bytes(self.update_stream_position_remote, 'little')pdate() fails

    def __getitem__(self, key):
        #log.debug("__getitem__ {}", key)
        self.apply_update()
        return self.data[key]

    # deprecated in Python 3
    def has_key(self, key):
        self.apply_update()
        return key in self.data

    def __eq__(self, other):
        return self.apply_update() == other.apply_update()

    def __contains__(self, key):
        self.apply_update()
        return key in self.data

    def __len__(self):
        self.apply_update()
        return len(self.data)

    def __iter__(self):
        self.apply_update()
        return iter(self.data)

    def __repr__(self):
        try:
            self.apply_update()
        except Exceptions.AlreadyClosed:
            # If something goes wrong during the update, let's ignore it and still return a representation
            # TODO: Maybe somehow add a stale update warning?
            pass
        return self.data.__repr__()

    def status(self):
        """ Internal debug helper to get the control state variables """
        ret = { attr: getattr(self, attr) for attr in self.__slots__ if hasattr(self, attr) and attr != 'data' }

        ret['update_stream_position_remote'] = int.from_bytes(self.update_stream_position_remote, 'little')
        ret['lock_pid_remote']               = int.from_bytes(self.lock_pid_remote, 'little')
        ret['lock_remote']                   = int.from_bytes(self.lock_remote, 'little')
        ret['shared_lock_remote']            = self.shared_lock_remote[0:1] == b'1'
        ret['recurse_remote']                = self.recurse_remote[0:1] == b'1'
        ret['lock']                          = self.lock
        ret['full_dump_counter_remote']      = int.from_bytes(self.full_dump_counter_remote, 'little')
        ret['full_dump_memory_name_remote']  = bytes(self.full_dump_memory_name_remote).decode('utf-8').strip('\x00').strip()

        return ret

    def print_status(self, status=None, stderr=False):
        """ Internal debug helper to pretty print the control state variables """
        import pprint
        if not status:
            status = self.status()
        pprint.pprint(status, stream=sys.stderr if stderr else sys.stdout)

    def cleanup(self):
        #log.debug('Cleanup')

        #for item in self.data.items():
        #    print(type(item))

        if hasattr(self, 'lock') and hasattr(self.lock, 'cleanup'):
            self.lock.cleanup()

        # If we use RLock(), this closes the file handle
        if hasattr(self, 'lock'):
            del self.lock
        if hasattr(self, 'full_dump_memory'):
            del self.full_dump_memory

        data = self.data
        del self.data

        self.del_remotes()

        #self.control.close()
        #self.buffer.close()

        #if self.full_dump_memory:
        #    self.full_dump_memory.close()

        # No further cleanup on Windows, it will break everything
        #if sys.platform == 'win32':
        #    return

        #Only do cleanup once
        #atexit.unregister(self.cleanup)

        self.apply_update = self.raise_already_closed
        self.append_update = self.raise_already_closed

        return data

    def raise_already_closed(self, *args, **kwargs):
        raise Exceptions.AlreadyClosed('UltraDict already closed, you can only access the `UltraDict.data` buffer!')

    def keys(self):
        self.apply_update()
        return self.data.keys()

    def values(self):
        self.apply_update()
        return self.data.values()

    def unlink(self):
        self.close(unlink=True)

    def close(self, unlink=False, from_finalizer=False):
        #log.debug('Close name={} unlink={} auto_unlink={} creator={}', self.name, unlink, self.auto_unlink, hasattr(self.control, 'created_by_ultra'))

        if self.closed:
            #log.debug('Already closed, doing nothing')
            return
        self.closed = True

        if hasattr(self, 'finalizer'):
            self.finalizer.detach()

        if hasattr(self, 'full_dump_memory_name_remote'):
            full_dump_name = bytes(self.full_dump_memory_name_remote).decode('utf-8').strip().strip('\x00')

        data = self.cleanup()

        # If we are the master creator of the shared memory, we'll delete (unlink) it
        # including the full dump memory; for the full dump memory, we delete it even
        # if we are not the creator
        if unlink or (self.auto_unlink and hasattr(self.control, 'created_by_ultra')):
            #log.debug('Unlink', self.name)
            self.control.unlink()
            self.buffer.unlink()
            if full_dump_name:
                self.unlink_by_name(full_dump_name, ignore_errors=True)

            if getattr(self, 'recurse', False):
                self.unlink_recursed()

        if hasattr(self, 'control'):
            self.control.close()
        if hasattr(self, 'buffer'):
            self.buffer.close()

        return data

    def unlink_recursed(self):
        #log.debug("Unlink recursed id={}", hex(id(self)))
        if not self.recurse or (type(self.recurse_register) != UltraDict):
            raise Exception("Cannot unlink recursed for non-recurse UltraDict")

        ignore_errors = sys.platform == 'win32'
        for name in self.recurse_register.keys():
            #log.debug("Unlink recursed child name={}", name)
            self.unlink_by_name(name=name, ignore_errors=ignore_errors)
            self.unlink_by_name(name=f"{name}_memory", ignore_errors=ignore_errors)

        self.recurse_register.close(unlink=True)


    @staticmethod
    def unlink_by_name(name, ignore_errors=False):
        """
        Can be used to delete left over shared memory blocks after crashes.
        """
        try:
            #log.debug("Unlinking memory '{}'", name)
            memory = UltraDict.get_memory(create=False, name=name)
            memory.unlink()
            memory.close()
            return True
        except Exceptions.CannotAttachSharedMemory as e:
            if not ignore_errors:
                raise e
        return False



# Saved as a reference

#def bytes_to_int(bytes):
#    result = 0
#    for b in bytes:
#        result = result * 256 + int(b)
#    return result
#
#def int_to_bytes(value, length):
#    result = []
#    for i in range(0, length):
#        result.append(value >> (i * 8) & 0xff)
#    result.reverse()
#    return result

#class Mapping(dict):
#
#    def __init__(self, *args, **kwargs):
#        print("__init__", args, kwargs)
#        super().__init__(*args, **kwargs)
#
#    def __setitem__(self, key, item):
#        print("__setitem__", key, item)
#        self.__dict__[key] = item
#
#    def __getitem__(self, key):
#        print("__getitem__", key)
#        return self.__dict__[key]
#
#    def __repr__(self):
#        print("__repr__")
#        return repr(self.__dict__)
#
#    def __len__(self):
#        print("__len__")
#        return len(self.__dict__)
#
#    def __delitem__(self, key):
#        print("__delitem__")
#        del self.__dict__[key]
#
#    def clear(self):
#        print("clear")
#        return self.__dict__.clear()
#
#    def copy(self):
#        print("copy")
#        return self.__dict__.copy()
#
#    def has_key(self, k):
#        print("has_key")
#        return k in self.__dict__
#
#    def update(self, *args, **kwargs):
#        print("update")
#        return self.__dict__.update(*args, **kwargs)
#
#    def keys(self):
#        print("keys")
#        return self.__dict__.keys()
#
#    def values(self):
#        print("values")
#        return self.__dict__.values()
#
#    def items(self):
#        print("items")
#        return self.__dict__.items()
#
#    def pop(self, *args):
#        print("pop")
#        return self.__dict__.pop(*args)
#
#    def __cmp__(self, dict_):
#        print("__cmp__")
#        return self.__cmp__(self.__dict__, dict_)
#
#    def __contains__(self, item):
#        print("__contains__", item)
#        return item in self.__dict__
#
#    def __iter__(self):
#        print("__iter__")
#        return iter(self.__dict__)
#
#    def __unicode__(self):
#        print("__unicode__")
#        return unicode(repr(self.__dict__))
#

```