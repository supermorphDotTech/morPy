r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Module of generally useful functions.
"""

import lib.fct as fct
import lib.mp as mp

from lib.decorators import metrics, log, log_no_q

import sys
import chardet
import io
import shutil
import os
import os.path
import re

from heapq import heappush, heappop

class cl_priority_queue:
    r"""
    This class delivers a priority queue solution. Any task may be enqueued.
    When dequeueing, the highest priority task (lowest number) is dequeued
    first. In case there is more than one, the oldest is dequeued.

    :param morPy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param name: Name or description of the instance

    :methods:
        .enqueue(morPy_trace: dict, app_dict: dict, priority: int=100, task: tuple=None, autocorrect: bool=True,
            is_process: bool=True)
            Adds a task to the priority queue.

            :param priority: Integer representing task priority (lower is higher priority)
            :param task: Tuple of a callable, *args and **kwargs (func, *args, **kwargs)
            :param autocorrect: If False, priority can be smaller than zero. Priority
                smaller zero is reserved for the morPy Core.
            :param is_process: If True, task is run in a new process (not by morPy orchestrator)

        .dequeue(morPy_trace: dict, app_dict: dict)
            Removes and returns the highest priority task from the priority queue.

            :return: dict
                priority: Integer representing task priority (lower is higher priority)
                counter: Number of the task when enqueued
                task_id : Continuously incremented task ID (counter).
                task_sys_id : ID of the task determined by Python core
                task: The dequeued task list
                task_callable: The dequeued task callable
                is_process: If True, task is run in a new process (not by morPy orchestrator)

    :example:
        from functools import partial
        # Create queue instance
        queue = morPy.cl_priority_queue(morPy_trace, app_dict, name="example_queue")
        # Add a task to the queue
        queue.enqueue(morPy_trace, app_dict, priority=25, task=partial(task, morPy_trace, app_dict))
        # Fetch a task and run it
        task = queue.dequeue(morPy_trace, app_dict)['task']
        task()
    """

    def __init__(self, morPy_trace: dict, app_dict: dict, name: str=None, is_manager: bool=False) -> None:
        r"""
        In order to get metrics for __init__(), call helper method _init() for
        the @metrics decorator to work. It relies on the returned
        {'morPy_trace' : morPy_trace}, which __init__() can not do (needs to be None).

        :param morPy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param name: Name or description of the instance
        :param is_manager: If True, priority queue is worked on as a manger. Intended
            for morPy orchestrator only.

        :return: self

        :example:
            queue = cl_priority_queue(morPy_trace, app_dict, name="example_queue")
        """

        module = 'common'
        operation = 'cl_priority_queue.__init__(~)'
        morPy_trace = fct.tracing(module, operation, morPy_trace)

        try:
            self.is_manager = is_manager

            # Use _init() for initialization to apply @metrics
            self._init(morPy_trace, app_dict, name)

        except Exception as e:
            err_msg = (
                lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{type(e).__name__}: {e}\n'
                        f'{app_dict["loc"]["morPy"]["cl_priority_queue_name"]}: {self.name}'
            )
            if self.is_manager:
                log_no_q(morPy_trace, app_dict, "critical", err_msg)
            else:
                log(morPy_trace, app_dict, "critical", err_msg)

    @metrics
    def _init(self, morPy_trace: dict, app_dict: dict, name: str, is_manager: bool=False) -> dict:
        r"""
        Helper method for initialization to ensure @metrics decorator functionality.

        :param morPy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param name: Name of the instance

        :return: dict
            morPy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module = 'common'
        operation = 'cl_priority_queue._init(~)'
        morPy_trace = fct.tracing(module, operation, morPy_trace)

        check = False

        try:
            self.name = name if name else 'queue'
            self.heap = []
            self.counter = 0 # Task counter. Starts at 0, increments by 1
            self.task_lookup = set() # Set for quick task existence check

            # Initialize in single core mode. Orchestrator is initialized afterward.
            # In single-core mode, skip queue.
            self._single_core = True

            # Set up the global task counter (serves also as the task ID)
            app_dict["proc"]["morPy"]["tasks_created"] = 0

            # Priority queue initialized.
            log_msg = (
                lambda: f'{app_dict["loc"]["morPy"]["cl_priority_queue_init_done"]}\n'
                        f'{app_dict["loc"]["morPy"]["cl_priority_queue_name"]}: {self.name}'
            )
            if self.is_manager:
                log_no_q(morPy_trace, app_dict, "debug", log_msg)
            else:
                log(morPy_trace, app_dict, "debug", log_msg)

            check = True

        except Exception as e:
            err_msg = (
                lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{type(e).__name__}: {e}\n'
                        f'{app_dict["loc"]["morPy"]["cl_priority_queue_name"]}: {self.name}'
            )
            if self.is_manager:
                log_no_q(morPy_trace, app_dict, "critical", err_msg)
            else:
                log(morPy_trace, app_dict, "critical", err_msg)

        return {
            'morPy_trace': morPy_trace,
            'check': check
        }

    @metrics
    def _init_mp(self, morPy_trace: dict, app_dict: dict) -> dict:
        r"""
        Helper method for initialization to ensure @metrics decorator functionality. Multiprocessing
        component/activation.

        :param morPy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morPy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module = 'common'
        operation = 'cl_priority_queue._init_mp(~)'
        morPy_trace = fct.tracing(module, operation, morPy_trace)

        check = False

        try:
            # In single-core mode, skip queue
            self._single_core = False if app_dict["proc"]["morPy"]["cl_orchestrator"].processes_max > 1 else True

            check = True

        except Exception as e:
            err_msg = (
                lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{type(e).__name__}: {e}\n'
                        f'{app_dict["loc"]["morPy"]["cl_priority_queue_name"]}: {self.name}'
            )
            if self.is_manager:
                log_no_q(morPy_trace, app_dict, "critical", err_msg)
            else:
                log(morPy_trace, app_dict, "critical", err_msg)

        return {
            'morPy_trace': morPy_trace,
            'check': check
        }

    @metrics
    def enqueue(self, morPy_trace: dict, app_dict: dict, priority: int=100,
                task: tuple=None, autocorrect: bool=True, is_process: bool=True) -> dict:
        r"""
        Adds a task to the priority queue.

        :param morPy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param priority: Integer representing task priority (lower is higher priority)
        :param task: Tuple of a callable, *args and **kwargs (func, *args, **kwargs)
        :param autocorrect: If False, priority can be smaller than zero. Priority
            smaller zero is reserved for the morPy Core.
        :param is_process: If True, task is run in a new process (not by morPy orchestrator)

        :return: dict
            morPy_trace: Operation credentials and tracing
            check: Indicates if the task was enqueued successfully

        :example:
            from functools import partial
            task = partial(my_func, morPy_trace, app_dict)
            queue.enqueue(morPy_trace, app_dict, priority=25, task=task)
        """

        module = 'common'
        operation = 'cl_priority_queue.enqueue(~)'
        morPy_trace = fct.tracing(module, operation, morPy_trace)

        check = False

        try:
            if task:
                # Omit queuing, if single core mode
                if self._single_core:
                    func = task[0]
                    args = task[1:]
                    retval = func(*args)
                else:
                    # Check and autocorrect process priority
                    if priority < 0 and autocorrect:
                        # Invalid argument given to process queue. Autocorrected.
                        log_msg = (
                            lambda: f'{app_dict["loc"]["morPy"]["cl_priority_queue_enqueue_prio_corr"]}\n'
                                    f'{app_dict["loc"]["morPy"]["cl_priority_queue_enqueue_priority"]}: {priority} to 0'
                        )
                        if self.is_manager:
                            log_no_q(morPy_trace, app_dict, "debug", log_msg)
                        else:
                            log(morPy_trace, app_dict, "debug", log_msg)

                        priority = 0

                    # Pushing task to priority queue.
                        log_msg = (
                            lambda: f'{app_dict["loc"]["morPy"]["cl_priority_queue_enqueue_start"]} {self.name}\n'
                                    f'{app_dict["loc"]["morPy"]["cl_priority_queue_enqueue_priority"]}: {priority}'
                        )
                        if self.is_manager:
                            log_no_q(morPy_trace, app_dict, "debug", log_msg)
                        else:
                            log(morPy_trace, app_dict, "debug", log_msg)

                    # Increment task counter
                    self.counter += 1

                    # Check for incremented task ID
                    new_id = app_dict["proc"]["morPy"]["tasks_created"] + 1

                    # Check continuously counted task ID
                    if self.counter == new_id:
                        task_sys_id = id(task)

                        # Check, if ID already in queue
                        if task_sys_id in self.task_lookup:
                            # Task is already enqueued. Referencing in queue.
                            log_msg = (
                                lambda: f'{app_dict["loc"]["morPy"]["cl_priority_queue_enqueue_task_duplicate"]}\n'
                                        f'Task system ID: {task_sys_id}'
                            )
                            if self.is_manager:
                                log_no_q(morPy_trace, app_dict, "debug", log_msg)
                            else:
                                log(morPy_trace, app_dict, "debug", log_msg)

                        # Push task to queue
                        task_qed = (priority, self.counter, task_sys_id, task, is_process)
                        heappush(self.heap, task_qed)
                        self.task_lookup.add(task_sys_id)

                        # Updating global tasks created last in case an error occurs
                        app_dict["proc"]["morPy"]["tasks_created"] += 1
                        morPy_trace["task_id"] = app_dict["proc"]["morPy"]["tasks_created"]

                    else:
                        # Task not enqueued. Task ID mismatch or conflict.
                        raise RuntimeError(f'{app_dict["loc"]["morPy"]["cl_priority_queue_enqueue_id_conflict"]}\nID: {self.counter}<>{morPy_trace["task_id"]}')

                    check = True
            else:
                # Task can not be None. Skipping enqueue.
                log_msg = (
                    lambda: f'{app_dict["loc"]["morPy"]["cl_priority_queue_enqueue_none"]}'
                )
                if self.is_manager:
                    log_no_q(morPy_trace, app_dict, "debug", log_msg)
                else:
                    log(morPy_trace, app_dict, "debug", log_msg)

        except Exception as e:
            err_msg = (
                lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{type(e).__name__}: {e}\n'
                        f'{app_dict["loc"]["morPy"]["cl_priority_queue_name"]}: {self.name}\n'
                        f'{app_dict["loc"]["morPy"]["cl_priority_queue_enqueue_priority"]}: {priority}'
            )
            if self.is_manager:
                log_no_q(morPy_trace, app_dict, "critical", err_msg)
            else:
                log(morPy_trace, app_dict, "critical", err_msg)

        return {
            'morPy_trace': morPy_trace,
            'check': check
        }

    @metrics
    def dequeue(self, morPy_trace: dict, app_dict: dict) -> dict:
        r"""
        Removes and returns the highest priority task from the priority queue.

        :param morPy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morPy_trace: Operation credentials and tracing
            check: Indicates if the task was dequeued successfully
            priority: Integer representing task priority (lower is higher priority)
            counter: Number of the task when enqueued
            task_id : Continuously incremented task ID (counter).
            task_sys_id : ID of the task determined by Python core
            task: The dequeued task list
            task_callable: The dequeued task callable
            is_process: If True, task is run in a new process (not by morPy orchestrator)

        :example:
            from functools import partial
            task = queue.dequeue(morPy_trace, app_dict)['task']
            task()
        """

        module = 'mt'
        operation = 'cl_priority_queue.dequeue(~)'
        morPy_trace_dequeue = fct.tracing(module, operation, morPy_trace)

        check = False
        priority = None
        counter = None
        task_sys_id = None
        task = None
        is_process = None

        try:
            # Global interrupt - wait for error handling
            while app_dict["global"]["morPy"].get("interrupt", False):
                pass

            if len(self.heap) > 0:
                task_dqed = heappop(self.heap)
                priority, counter, task_sys_id, task, is_process = task_dqed

                # Pulling task from NAME priority: INT counter: INT
                # TODO mark verbose
                log_msg = (
                    lambda: f'{app_dict["loc"]["morPy"]["cl_priority_queue_dequeue_start"]} {self.name}.\n'
                            f'{app_dict["loc"]["morPy"]["cl_priority_queue_dequeue_priority"]}: {priority}\n'
                            f'{app_dict["loc"]["morPy"]["cl_priority_queue_dequeue_cnt"]}: {counter}'
                )
                if self.is_manager:
                    log_no_q(morPy_trace_dequeue, app_dict, "debug", log_msg)
                else:
                    log(morPy_trace_dequeue, app_dict, "debug", log_msg)

                check = True

            else:
                # Can not dequeue from an empty priority queue. Skipped...
                log_msg = (
                    lambda: f'{app_dict["loc"]["morPy"]["cl_priority_queue_dequeue_void"]}'
                )
                if self.is_manager:
                    log_no_q(morPy_trace_dequeue, app_dict, "debug", log_msg)
                else:
                    log(morPy_trace_dequeue, app_dict, "debug", log_msg)

        except Exception as e:
            err_msg = (
                lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{type(e).__name__}: {e}\n'
                        f'{app_dict["loc"]["morPy"]["cl_priority_queue_name"]}: {self.name}'
            )
            if self.is_manager:
                log_no_q(morPy_trace_dequeue, app_dict, "critical", err_msg)
            else:
                log(morPy_trace_dequeue, app_dict, "critical", err_msg)

        return {
            'morPy_trace': morPy_trace_dequeue,
            'check': check,
            'priority' : priority,
            'counter' : counter,
            'task_id' : morPy_trace["task_id"],
            'task_sys_id' : task_sys_id,
            'task': list(task),
            'is_process': is_process
        }

    def task_exists(self, task):
        """
        Check if a task already exists in the queue.

        :param task: A callable (function or lambda) representing the task

        :return: bool - True, if task ID is found to already exist in queue

        :example:
            task_exists = self.task_exists(task)
        """

        return id(task) in self.task_lookup

class cl_progress():
    r"""
    This class instantiates a progress counter. If ticks, total or counter
    are floats, progress of 100 % may not be displayed.

    :param morPy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param description: Describe, what is being processed (i.e. file path or calculation)
    :param total: Mandatory - The total count for completion
    :param ticks: Mandatory - Percentage of total to log the progress. I.e. at ticks=10.7 at every
        10.7% progress exceeded the exact progress will be logged.

    .update(morPy_trace: dict, app_dict: dict, current: float=None)
        Method to update current progress and log progress if tick is passed.

        :return: dict
            prog_rel: Relative progress, float between 0 and 1
            message: Message generated. None, if no tick was hit.

    :example:
        progress = cl_progress(morPy_trace, app_dict, description='App Progress', total=total_count, ticks=10)["prog_rel"]
        progress.update(morPy_trace, app_dict, current=current_count)
    """

    def __init__(self, morPy_trace: dict, app_dict: dict, description: str=None, total: float=None, ticks: float=None) -> None:
        r"""
        In order to get metrics for __init__(), call helper method _init() for
        the @metrics decorator to work. It relies on the returned
        {'morPy_trace' : morPy_trace}, which __init__() can not do (needs to be None).

        :param morPy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param description: Describe, what is being processed (i.e. file path or calculation)
        :param total: Mandatory - The total count for completion
        :param ticks: Mandatory - Percentage of total to log the progress. I.e. at ticks=10.7 at every
            10.7% progress exceeded the exact progress will be logged. Independent of the ticks, at
            100.0% an update is always logged.

        :return:
            -

        :example:
            instance = cl_progress(morPy_trace, app_dict, description='App Progress', total=100, ticks=10)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module = 'common'
        operation = 'cl_progress.__init__(~)'
        morPy_trace = fct.tracing(module, operation, morPy_trace)

        try:
            # Use self._init() for initialization
            self._init(morPy_trace, app_dict, description=description, total=total, ticks=ticks)

        except Exception as e:
            log(morPy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

    @metrics
    def _init(self, morPy_trace: dict, app_dict: dict, description: str=None, total: float=None, ticks: float=None) -> dict:
        r"""
        Helper method for initialization to ensure @metrics decorator usage.

        :param morPy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param description: Describe, what is being processed (i.e. file path or calculation)
        :param total: Mandatory - The total count for completion
        :param ticks: Mandatory - Percentage of total to log the progress. I.e. at ticks=10.7 at every
            10.7% progress exceeded the exact progress will be logged. If None or greater 100, will default to 10.

        :return: dict
            morPy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._init(morPy_trace, app_dict, description=description, total=total, ticks=ticks)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module = 'common'
        operation = 'cl_progress._init(~)'
        morPy_trace = fct.tracing(module, operation, morPy_trace)

        check = False

        try:
            # Null guard and evaluation
            # TODO localization
            if not total: raise ValueError('Missing total: {total}')

            # Evaluate ticks
            if not ticks or ticks > 100:
                self.ticks = 10
            else:
                self.ticks = ticks

            self.total = total
            self.ticks_rel = self.ticks / 100
            self.description = f'{description}' if description else ''
            self.update_counter = 0
            self.stop_updates = False

            # Determine absolute progress ticks
            self._init_ticks(morPy_trace, app_dict)

            check = True

        except Exception as e:
            log(morPy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

        return{
            'morPy_trace' : morPy_trace,
            'check' : check,
            }

    @metrics
    def _init_ticks(self, morPy_trace: dict, app_dict: dict) -> dict:
        r"""
        This method determines the ticks, at which to log the progress.

        :param morPy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count

        :return: dict
            morPy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._init_ticks(morPy_trace, app_dict)

        TODO mark progress log as verbose
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module = 'common'
        operation = 'cl_progress._init_ticks(~)'
        morPy_trace = fct.tracing(module, operation, morPy_trace)

        check = False

        try:
            # Convert total to integer and determine the factor
            factor = 1
            total_fac = self.total
            if isinstance(total_fac, float):
                while not total_fac.is_integer():
                    total_fac *= 10
                    factor *= 10
            self.total_fac = int(total_fac)
            self.factor = factor

            # Determine the absolute ticks
            abs_tick = 0
            cnt_ticks = 0
            ticks_lst = [self.total_fac]
            while abs_tick < self.total_fac:
                cnt_ticks += 1
                abs_tick = self.total_fac * self.ticks_rel * cnt_ticks
                if abs_tick not in ticks_lst and abs_tick < self.total_fac:
                    ticks_lst.append(int(abs_tick))
            ticks_lst.sort()
            self.ticks_lst = ticks_lst

            check = True

        except Exception as e:
            log(morPy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

        return{
            'morPy_trace' : morPy_trace,
            'check' : check,
            }

    @metrics
    def update(self, morPy_trace: dict, app_dict: dict, current: float=None) -> dict:
        r"""
        Method to update current progress and log progress if tick is passed.

        :param morPy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.

        :return: dict
            morPy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors
            prog_rel: Relative progress, float between 0 and 1
            prog_abs: Absolute progress, float between 0.00 and 100.00
            message: Message generated. None, if no tick was hit.

        :example:
            tot_cnt = 100
            tks = 12.5
            progress = morPy.cl_progress(morPy_trace, app_dict, description='App Progress', total=total_count, ticks=tks)

            curr_cnt = 37
            progress.update(morPy_trace, app_dict, current=curr_cnt)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module = 'common'
        operation = 'cl_progress.update(~)'
        morPy_trace = fct.tracing(module, operation, morPy_trace)

        check = False
        prog_rel = None
        prog_abs_short = None
        message = None

        try:
            # Evaluate current progress absolute count
            if not current:
                self.update_counter += 1
                current = self.update_counter
            elif current > self.update_counter:
                self.update_counter = current

            if current > self.total:
                self.stop_updates = True

                # Current progress exceeded total. Progress updates stopped.
                log(morPy_trace, app_dict, "warning",
                lambda: f'{app_dict["loc"]["morPy"]["cl_progress_upd_stopped"]}: {current} > {self.total}')

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

                # Processing DESCRIPTION
                log(morPy_trace, app_dict, "info",
                lambda: f'{app_dict["loc"]["morPy"]["cl_progress_proc"]}: {self.description}\n'
                        f'{prog_abs_short}% ({self.update_counter} of {self.total})')

            check = True

        except Exception as e:
            log(morPy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

        return{
            'morPy_trace' : morPy_trace,
            'check' : check,
            'prog_rel' : prog_rel,
            'prog_abs' : prog_abs_short,
            'message' : message
            }

@metrics
def decode_to_plain_text(morPy_trace: dict, app_dict: dict, src_input: str, encoding: str) -> dict:

    r"""
    This function decodes different types of data and returns
    a plain text to work with in python. The return result behaves
    like using the open(file, 'r') method.

    :param morPy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param src_input: Any kind of data to be decoded. Binary expected.
    :param encoding: String that defines encoding. Leave empty to auto detect.

    :return: dict
        result: Decoded result. Buffered object that may be used with the
            readlines() method.
        encoding: String containing the encoding of src_input.
        lines: Number of lines in the file.
        morPy_trace: Operation credentials and tracing

    :example:
        src_input = open(src_file, 'rb')
        encoding = 'utf-16-le'
        retval = decode_to_plain_text(morPy_trace, app_dict, src_input, encoding)
    """

    module = 'common'
    operation = 'decode_to_plain_text(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    result = None
    src_copy = b''
    decode = False
    lines = 0
    if encoding is None: encoding = ''

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
                log(morPy_trace, app_dict, "warning",
                lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{app_dict["loc"]["morPy"]["decode_to_plain_text_msg"]}: {e}')

        # Validate provided encoding
        else:
            try:
                encoding_val = chardet.detect(src_copy)["encoding"]
                decode = True

        #   Not encoded if an exception is raised
            except:
                raise RuntimeError

        # Decode the content
        if decode:
            result = io.StringIO(src_copy.decode(encoding))

            # Decoded from ### to plain text.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["decode_to_plain_text_from"]} {encoding}) '
                    f'{app_dict["loc"]["morPy"]["decode_to_plain_text_to"]}\n'
                    f'encoding: {encoding}')

        # Handle unsupported or non-encoded input
        else:
            result = io.StringIO(src_copy.decode('utf-8', errors='ignore'))

            # The Input is not decoded or not supported. No action taken.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["decode_to_plain_text_not"]}\n'
                f'encoding: {encoding}')

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return {
        'morPy_trace': morPy_trace,
        'result': result,
        'encoding': encoding,
        'lines': lines,
    }

@metrics
def fso_copy_file(morPy_trace: dict, app_dict: dict, source: str, dest: str, ovwr_perm: bool) -> dict:

    r"""
    Copies a single file from the source to the destination. Includes a file
    check to ensure the operation's validity.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param source: Complete path to the source file, including the file extension.
    :param dest: Complete path to the destination file, including the file extension.
    :param ovwr_perm: Boolean indicating if the destination file may be overwritten.

    :return: dict
        check: Indicates whether the function executed successfully (True/False).
        source: Path to the source file as a path object.
        dest: Path to the destination file as a path object.
        morPy_trace: Operation credentials and tracing.

    :example:
        result = fso_copy_file(morPy_trace, app_dict, "path/to/source.txt", "path/to/destination.txt", True)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'fso_copy_file(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False

    try:
        # Check the source file
        source_eval = fct.pathtool(morPy_trace, source)
        source_exist = source_eval["file_exists"]
        source = source_eval["out_path"]

        # Check the destination file
        dest_eval = fct.pathtool(morPy_trace, dest)
        dest_exist = dest_eval["file_exists"]
        dest = dest_eval["out_path"]

        # Evaluate the existence of the source
        if source_exist:

            # Evaluate the existence of the destination and overwrite permission
            if dest_exist and ovwr_perm:

                shutil.copyfile(source, dest)

                # A file has been copied and the original was overwritten.
                log(morPy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morPy"]["fso_copy_file_copy_ovwr"]}\n'
                        f'{app_dict["loc"]["morPy"]["fso_copy_file_source"]}: {source}\n'
                        f'{app_dict["loc"]["morPy"]["fso_copy_file_dest"]}: {dest}\n'
                        f'dest_exist: {dest_exist}\n'
                        f'ovwr_perm: {ovwr_perm}')

            # Evaluate the existence of the destination and overwrite permission
            if dest_exist and not ovwr_perm:

                shutil.copyfile(source, dest)

                # A file was not copied because it already exists and no overwrite permission was given.
                log(morPy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morPy"]["fso_copy_file_copy_not_ovwr"]}\n'
                        f'{app_dict["loc"]["morPy"]["fso_copy_file_source"]}: {source}\n'
                        f'{app_dict["loc"]["morPy"]["fso_copy_file_dest"]}: {dest}\n'
                        f'dest_exist: {dest_exist}\n'
                        f'ovwr_perm: {ovwr_perm}')

            if dest_exist:

                shutil.copyfile(source, dest)

                # A file has been copied.
                log(morPy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morPy"]["fso_copy_file_copy"]}\n'
                        f'{app_dict["loc"]["morPy"]["fso_copy_file_source"]}: {source}\n'
                        f'{app_dict["loc"]["morPy"]["fso_copy_file_dest"]}: {dest}')

            check = True

        else:
            # A file could not be copied, because it does not exist.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["fso_copy_file_not_exist"]}\n'
                    f'{app_dict["loc"]["morPy"]["fso_copy_file_source"]}: {source}\n'
                    f'{app_dict["loc"]["morPy"]["fso_copy_file_dest"]}: {dest}\n'
                    f'source_exist: {source_exist}')

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        'source' : source,
        'dest' : dest
        }

@metrics
def fso_create_dir(morPy_trace: dict, app_dict: dict, mk_dir: str) -> dict:

    r"""
    Creates a directory and its parent directories recursively.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param mk_dir: Path to the directory or directory tree to be created.

    :return: dict
        check: Indicates whether the function executed successfully (True/False).
        morPy_trace: Operation credentials and tracing.

    :example:
        result = fso_create_dir(morPy_trace, app_dict, "path/to/new_directory")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'fso_create_dir(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False

    try:
        # Check the directory
        dir_eval = fct.pathtool(morPy_trace, mk_dir)
        dir_exist = dir_eval["dir_exists"]
        mk_dir = dir_eval["out_path"]

        if dir_exist:
            # The directory already exists.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["fso_create_dir_not_created"]}\n'
                    f'{app_dict["loc"]["morPy"]["fso_create_dir_directory"]}: {mk_dir}\n'
                    f'{app_dict["loc"]["morPy"]["fso_create_dir_direxist"]}: {dir_exist}')

        else:
            os.makedirs(mk_dir)

            # The directory has been created.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["fso_create_dir_created"]}\n'
                    f'{app_dict["loc"]["morPy"]["fso_create_dir_directory"]}: {mk_dir}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check
        }

@metrics
def fso_delete_dir(morPy_trace: dict, app_dict: dict, del_dir: str) -> dict:

    r"""
    Deletes an entire directory, including its contents. A directory check
    is performed before deletion.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param del_dir: Path to the directory to be deleted.

    :return: dict
        check: Indicates whether the function executed successfully (True/False).
        morPy_trace: Operation credentials and tracing.

    :example:
        result = fso_delete_dir(morPy_trace, app_dict, "path/to/directory_to_delete")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'fso_delete_dir(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False

    try:
        # Check the directory
        dir_eval = fct.pathtool(morPy_trace, del_dir)
        dir_exist = dir_eval["dir_exists"]
        del_dir = dir_eval["out_path"]

        if dir_exist:

            shutil.rmtree(del_dir)

            # The directory has been deleted.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["fso_delete_dir_deleted"]}\n'
                    f'{app_dict["loc"]["morPy"]["fso_create_dir_directory"]}: {del_dir}')

        else:
            # The directory does not exist.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["fso_delete_dir_notexist"]}\n'
                    f'{app_dict["loc"]["morPy"]["fso_create_dir_directory"]}: {del_dir}\n'
                    f'{app_dict["loc"]["morPy"]["fso_delete_dir_direxist"]}: {dir_exist}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check
        }

@metrics
def fso_delete_file(morPy_trace: dict, app_dict: dict, del_file: str) -> dict:

    r"""
    Deletes a file. A path check is performed before deletion.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param del_file: Path to the file to be deleted.

    :return: dict
        check: Indicates whether the function executed successfully (True/False).
        morPy_trace: Operation credentials and tracing.

    :example:
        result = fso_delete_file(morPy_trace, app_dict, "path/to/file_to_delete.txt")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'fso_delete_file(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False

    try:
        # Check the directory
        file_eval = fct.pathtool(morPy_trace, del_file)
        file_exist = file_eval["file_exists"]
        del_file = file_eval["out_path"]

        if file_exist:

            os.remove(del_file)

            # The file has been deleted.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["fso_delete_file_deleted"]}\n'
                    f'{app_dict["loc"]["morPy"]["fso_delete_file_file"]}: {del_file}')

        else:
            # The file does not exist.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["fso_delete_file_notexist"]}\n'
                    f'{app_dict["loc"]["morPy"]["fso_delete_file_file"]}: {del_file}\n'
                    f'{app_dict["loc"]["morPy"]["fso_delete_file_exist"]}: {file_exist}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check
        }

@metrics
def fso_walk(morPy_trace: dict, app_dict: dict, path: str, depth: int) -> dict:

    r"""
    Returns the contents of a directory.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param path: Path to the directory to be analyzed.
    :param depth: Limits the depth of the analysis:
                  -1: No limit.
                   0: Path only.

    :return: dict
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
                       ...
                   }
        morPy_trace: Operation credentials and tracing.

    :example:
        result = fso_walk(morPy_trace, app_dict, "path/to/directory", -1)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'fso_delete_file(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False
    walk_dict = {}
    root = r""
    dirs = []
    files = []
    cnt_roots = 0

    try:
        # Check the directory
        if fct.pathtool(morPy_trace, path)["dir_exists"]:
            for root, dirs, files in os.walk(path):
                # Exit if depth is reached
                if cnt_roots > depth:
                    break

                walk_dict.update({f'root{cnt_roots}' : {'root' : root, 'dirs' : dirs, 'files' : files}})
                cnt_roots += 1

            # Directory analyzed.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["fso_walk_path_done"]}\n'
                    f'{app_dict["loc"]["morPy"]["fso_walk_path_dir"]}: {path}')

        else:
            # The directory does not exist.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["fso_walk_path_notexist"]}\n'
                    f'{app_dict["loc"]["morPy"]["fso_walk_path_dir"]}: {path}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        'walk_dict' : walk_dict
        }

@metrics
def regex_findall(morPy_trace: dict, app_dict: dict, search_obj: object, pattern: str) -> dict:

    r"""
    Searches for a regular expression in a given object and returns a list of found expressions.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        result: List of expressions found in the input, or None if nothing was found.
        morPy_trace: Operation credentials and tracing.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = regex_findall(morPy_trace, app_dict, string, pattern)["result"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'regex_findall(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    search_obj = f'{search_obj}'
    pattern =    f'{pattern}'
    result = None

    # Searching for regular expressions.
    log(morPy_trace, app_dict, "debug",
    lambda: f'{app_dict["loc"]["morPy"]["regex_findall_init"]}\n'
            f'{app_dict["loc"]["morPy"]["regex_findall_pattern"]}: {pattern}\n'
            f'search_obj: {search_obj}')

    try:
        # Search for the pattern
        result_matches = re.findall(pattern, search_obj)
        result = result_matches if result_matches else None

        # Search completed.
        log(morPy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morPy"]["regex_findall_compl"]}\n'
                f'{app_dict["loc"]["morPy"]["regex_findall_result"]}: {result}')

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'result' : result
        }

@metrics
def regex_find1st(morPy_trace: dict, app_dict: dict, search_obj: object, pattern: str) -> dict:

    r"""
    Searches for a regular expression in a given object and returns the first match.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        result: The first match found in the input, or None if nothing was found.
        morPy_trace: Operation credentials and tracing.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = regex_find1st(morPy_trace, app_dict, string, pattern)["result"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'regex_find1st(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False
    search_string = f'{search_obj}'
    pattern = f'{pattern}'
    result = None

    try:
        # Searching for regular expressions.
        log(morPy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morPy"]["regex_find1st_init"]}\n'
                f'{app_dict["loc"]["morPy"]["regex_find1st_pattern"]}: {pattern}\n'
                f'search_obj: {search_string}')

        if search_string is not None:

            result_match = re.search(pattern, search_string)
            result = result_match.group() if result_match else None

            # Search completed.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["regex_find1st_compl"]}\n'
                    f'{app_dict["loc"]["morPy"]["regex_find1st_result"]}: {result}')

        else:
            result = [search_obj]

            # String is NoneType. No Regex executed.
            log(morPy_trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["morPy"]["regex_find1st_none"]}\n'
                    f'{app_dict["loc"]["morPy"]["regex_find1st_result"]}: {result}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        'result' : result
        }

@metrics
def regex_split(morPy_trace: dict, app_dict: dict, search_obj: object, delimiter: str) -> dict:

    r"""
    Splits an object into a list using a given delimiter.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to be split (converted to a string).
    :param delimiter: The character or string used to split `search_obj` into a list.
                      Special characters may require a preceding backslash (e.g., '\\.'
                      to use '.' as a delimiter).

    :return: dict
        result: The list of parts split from the input.
        morPy_trace: Operation credentials and tracing.

    :example:
        string = "apple.orange.banana"
        split = r"\\."
        result = regex_split(morPy_trace, app_dict, string, split)["result"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'regex_split(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False
    search_string = f'{search_obj}'
    delimiter =    f'{delimiter}'


    try:
        # Splitting a string by a given delimiter.
        log(morPy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morPy"]["regex_split_init"]}\n'
                f'{app_dict["loc"]["morPy"]["regex_split_delimiter"]}: {delimiter}\n'
                f'search_obj: {search_string}')

        if search_string is not None:

            result = re.split(delimiter, search_string)

            # String has been split.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["regex_split_compl"]}\n'
                    f'{app_dict["loc"]["morPy"]["regex_split_result"]}: {result}')

        else:
            result = [search_obj]

            # String is NoneType. No Split executed.
            log(morPy_trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["morPy"]["regex_split_none"]}\n'
                    f'{app_dict["loc"]["morPy"]["regex_split_result"]}: {result}')

            check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        'result' : result
        }

@metrics
def regex_replace(morPy_trace: dict, app_dict: dict, search_obj: object, search_for: str, replace_by: str) -> dict:

    r"""
    Substitutes characters or strings in an input object based on a regular expression.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object in which to search and replace (converted to a string).
    :param search_for: The regular expression pattern to search for.
    :param replace_by: The character or string to substitute in place of the matches.

    :return: dict
        morPy_trace: Operation credentials and tracing.
        result: The modified string with substitutions applied.

    :example:
        string = "apple.orange.banana"
        search_for = r"\\."
        replace_by = r"-"
        result = regex_replace(morPy_trace, app_dict, string, search_for, replace_by)["result"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'regex_replace(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False
    search_obj = f'{search_obj}'
    search_for = f'{search_for}'
    replace_by = f'{replace_by}'

    try:
        # Changing a string by given parameters.
        log(morPy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morPy"]["regex_replace_init"]}\n'
                f'search_for: {search_for}\n'
                f'replace_by: {replace_by}\n'
                f'search_obj: {search_obj}')

        result = re.sub(search_for, replace_by, search_obj)

        # String substituted.
        log(morPy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morPy"]["regex_replace_compl"]}\n'
                f'{app_dict["loc"]["morPy"]["regex_replace_result"]}: {result}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        'result' : result
        }

@metrics
def regex_remove_special(morPy_trace: dict, app_dict: dict, inp_string: str, spec_lst: list) -> dict:

    r"""
    Removes or replaces special characters in a given string. The `spec_lst` parameter
    specifies which characters to replace and their replacements. If no replacement is
    specified, a standard list is used to remove special characters without substitution.

    This function can also perform multiple `regex_replace` actions on the same string,
    as any valid regular expression can be used in the `spec_lst`.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param inp_string: The string to be altered.
    :param spec_lst: A list of 2-tuples defining the special characters to replace and
                     their replacements. Example:
                     [(special1, replacement1), ...]. Use `[('', '')]` to invoke the
                     standard replacement list.

    :return: dict
        result: The modified string with special characters replaced or removed.
        morPy_trace: Operation credentials and tracing.

    :example:
        result = regex_remove_special(
            morPy_trace, app_dict, "Hello!@#$%^&*()", [("@", "AT"), ("!", "")]
        )
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'regex_remove_special(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False
    load_std = False
    inp_string = f'{inp_string}'

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
        log(morPy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morPy"]["regex_remove_special_init"]}\n'
                f'inp_string: {inp_string}\n'
                f'spec_lst: {spec_lst}\n'
                f'load_std: {load_std}')

        # Initialize the resulting string
        result = inp_string

        # Loop through the tuples list and remove/replace characters of the
        # input string
        for tpl in spec_lst:

            # Convert specials to raw string and perform search/replace
            result = re.sub(f'{tpl[0]}', f'{tpl[1]}', result)

        # String substituted.
        log(morPy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morPy"]["regex_remove_special_compl"]}\n'
                f'inp_string: {inp_string}\n'
                f'{app_dict["loc"]["morPy"]["regex_remove_special_result"]}: {result}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        'result' : result
        }

@metrics
def textfile_write(morPy_trace: dict, app_dict: dict, filepath: str, content: str) -> dict:

    r"""
    Appends content to a text file, creating the file if it does not already exist.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param filepath: Path to the text file, including its name and file extension.
    :param content: The content to be written to the file, converted to a string if necessary.

    :return: dict
        check: Indicates whether the function executed successfully (True/False).
        morPy_trace: Operation credentials and tracing.

    :example:
        result = textfile_write(morPy_trace, app_dict, "path/to/file.txt", "This is some text.")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'textfile_write(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False
    content = f'{content}'
    filepath = os.path.abspath(filepath)

    try:
        # Append to a textfile
        if os.path.isfile(filepath):

            with open(filepath, 'a') as ap:
                ap.write(f'\n{content}')

            # Textfile has been appended to.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["textfile_write_appended"]}\n'
                    f'{app_dict["loc"]["morPy"]["textfile_write_content"]}: {content}')

        # Create and write a textfile
        else:
            with open(filepath, 'w') as wr:
                wr.write(content)

            # Textfile has been created.
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morPy"]["textfile_write_created"]}\n'
                    f'{app_dict["loc"]["morPy"]["textfile_write_content"]}: {content}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        }

@metrics
def testprint(morPy_trace: dict, app_dict: dict, input: str) -> None:

    r"""
    Prints any value provided. This function is intended for debugging purposes.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param input: The value to be printed, converted to a string if necessary.

    :return: None

    :example:
        testprint(morPy_trace, app_dict, "This is a test value.")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    # module = 'common'
    # operation = 'testprint(~)'
    # morPy_trace = fct.tracing(module, operation, morPy_trace)

    value     = f'{input}'
    intype    = f'{type(input)}'

    print(f'<TEST> value: {value}\n'
          f'<TEST> type: {intype}\n')

@metrics
def wait_for_input(morPy_trace: dict, app_dict: dict, msg_text: str) -> dict:

    r"""
    Pauses program execution until a user provides input. The input is then
    returned to the calling module. Take note, that the returned user input
    will always be a string.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param msg_text: The text to be displayed as a prompt before user input.

    :return: dict
        usr_input: The input provided by the user.
        morPy_trace: Operation credentials and tracing.

    :example:
        result = wait_for_input(morPy_trace, app_dict, "Please enter your name: ")["usr_input"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'wait_for_input(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False
    usr_input = None

    try:
        # Set global interrupt
        mp.interrupt(morPy_trace, app_dict)

        # user input
        usr_input = input(f'{msg_text}\n')

        # A user input was made.
        log(morPy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morPy"]["wait_for_input_compl"]}\n'
                f'{app_dict["loc"]["morPy"]["wait_for_input_message"]}: {msg_text}\n'
                f'{app_dict["loc"]["morPy"]["wait_for_input_usr_inp"]}: {usr_input}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        'usr_input' : usr_input
        }

@metrics
def wait_for_select(morPy_trace: dict, app_dict: dict, msg_text: str, collection: tuple=None) -> dict:

    r"""
    Pauses program execution until a user provides input. The input needs to
    be part of a tuple, otherwise it is repeated or aborted. Take note, that the
    returned user input will always be a string.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param msg_text: The text to be displayed as a prompt before user input.
    :param collection: Tuple, that holds all valid user input options. If None,
        evaluation will be skipped.

    :return: dict
        usr_input: The input provided by the user.
        morPy_trace: Operation credentials and tracing.

    :example:
        msg_text = "Select 1. this or 2. that"
        collection = (1, 2)
        result = wait_for_select(morPy_trace, app_dict, msg_text, collection)["usr_input"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'common'
    operation = 'wait_for_select(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    check = False
    usr_input = None

    try:
        # Set global interrupt
        mp.interrupt(morPy_trace, app_dict)

        # user input
        usr_input = input(f'{msg_text}\n')

        if collection:
            # Make collection 'str'
            collection = tuple(map(str, collection))

            while usr_input not in collection:
                # Invalid selection. Repeat?
                rep = (
                    f'{app_dict["loc"]["morPy"]["wait_for_select_selection_invalid"]}\n'
                    f'[{app_dict["loc"]["morPy"]["wait_for_select_yes_selector"]}] '
                    f'{app_dict["loc"]["morPy"]["wait_for_select_yes"]} | '
                    f'[{app_dict["loc"]["morPy"]["wait_for_select_quit_selector"]}] '
                    f'{app_dict["loc"]["morPy"]["wait_for_select_quit"]}'
                )
                usr_response = input(f'{rep}\n')

                if usr_response == "y":
                    usr_input = input(f'{msg_text}\n')
                elif usr_response == "q":
                    app_dict["proc"]["morPy"]["cl_orchestrator"]._terminate = True
                    break
                else:
                    pass

        # A user input was made.
        log(morPy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morPy"]["wait_for_select_compl"]}\n'
                f'{app_dict["loc"]["morPy"]["wait_for_select_message"]}: {msg_text}\n'
                f'{app_dict["loc"]["morPy"]["wait_for_select_usr_inp"]}: {usr_input}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        'usr_input' : usr_input
        }