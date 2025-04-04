r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Multiprocessing functionality for morPy.

TODO provide a general purpose lock
    > Find a way to lock file objects and dirs
"""

import lib.fct as morpy_fct
from lib.decorators import metrics, log

import sys
import time
from UltraDict import UltraDict
from multiprocessing import Process, active_children
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

            # Determine if multiprocessing is enabled
            self.processes_max: int = app_dict["morpy"]["processes_max"]
            self._mp: bool = True if self.processes_max > 1 else False
            app_dict["morpy"]["orchestrator"]["mp"] = self._mp

            # Set up first tasks
            self._init_app_dict(morpy_trace, app_dict)
            self._init_run(morpy_trace, app_dict)

            # MorPyOrchestrator initialized.
            log(morpy_trace, app_dict, "init",
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

            # Activate the process queue
            if self._mp:
                process_q_init(morpy_trace, app_dict)

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
            log(morpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_app_run_start"]}')

            # Initialize and run the app
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

        try:
            # Start the app
            app_task = [self._app_run, morpy_trace_app, app_dict]
            process_enqueue(morpy_trace, app_dict, priority=-90, task=app_task, autocorrect=False, force=self._mp)

            if self._mp:
                terminate = False
                while not terminate:
                    self._mp_loop(morpy_trace, app_dict)
                    with app_dict["morpy"]["orchestrator"].lock:
                        terminate = app_dict["morpy"]["orchestrator"]["terminate"]

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
    def _mp_loop(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Main loop of the morPy orchestrator. This loop will stay alive
        for the most part of runtime if multiprocessing is enabled.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates if the task was pulled successfully

        :example:
            self._mp_loop(morpy_trace, app_dict)
        """

        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._mp_loop(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            with app_dict["morpy"].lock:
                heap_len = len(app_dict["morpy"]["heap"])

            terminate = False
            while not terminate or heap_len > 0:
                # Check process queue for tasks
                if heap_len > 0:
                    task_pull = process_pull(morpy_trace, app_dict)
                    task = task_pull["task"]

                    if task:
                        is_process = task_pull["is_process"]
                        priority = task_pull["priority"]
                        # Run a new parallel process
                        if is_process:
                            with app_dict["morpy"].lock:
                                exit_flag = app_dict["morpy"]["exit"]

                            # Only run new processes if not exiting.
                            if not exit_flag:
                                app_dict["morpy"]["proc_joined"] = False
                                run_parallel(morpy_trace, app_dict, task=task, priority=priority)
                                terminate = False
                                with app_dict["morpy"]["orchestrator"].lock:
                                    app_dict["morpy"]["orchestrator"]["terminate"] = terminate
                        # Run an orchestrator task directly
                        else:
                            # Recreate UltraDict references in task
                            task_recreated = reattach_ultradict_refs(morpy_trace, app_dict, task)["task_recreated"]
                            func = task_recreated[0]
                            args = task_recreated[1:]
                            func(*args)

                    with app_dict["morpy"].lock:
                        heap_len = len(app_dict["morpy"]["heap"])

                else:
                    # First, see if lost tasks need to be recovered
                    check_child_processes(morpy_trace, app_dict)
                    # Sleep if heap is empty / wait for shelved process acceptance
                    time.sleep(0.2)  # 0.2 seconds = 200 milliseconds

                    with app_dict["morpy"].lock:
                        heap_len = len(app_dict["morpy"]["heap"])

                    # If heap is still empty, mark processes as joined.
                    if heap_len > 0:
                        check_child_processes(morpy_trace, app_dict, check_join=True)

                with app_dict["morpy"].lock:
                    heap = app_dict["morpy"]["heap"]

                # TODO make use of program exit with critical exceptions
                # TODO make sure no memory leaks are introduced when exiting
                with app_dict["morpy"].lock:
                    # Check for the global exit flag
                    exit_flag = app_dict["morpy"]["exit"]
                    if exit_flag:
                        no_children = True if len(app_dict["morpy"]["proc_busy"]) < 2 else False
                        no_heap = True if len(heap) == 0 else False
                        if no_children and no_heap:
                            terminate = True

                # In case of global exit, delete the heap.
                # if exit_flag:
                #     with app_dict["morpy"].lock:
                #         app_dict["morpy"]["heap"] = []

                # Fail-safe check if really no child processes are running anymore.
                if terminate and not exit_flag:
                    # TODO call check_child_processes()
                    # terminate = RESULT
                    pass

                if terminate:
                    with app_dict["morpy"]["orchestrator"].lock:
                        app_dict["morpy"]["orchestrator"]["terminate"] = terminate

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
def process_q_init(morpy_trace: dict, app_dict: dict) -> dict:
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

    try:
        with app_dict["morpy"].lock:
            morpy_dict = app_dict["morpy"]
            morpy_dict["heap"] = []
            morpy_dict["process_q_counter"] = 0

            # Priority queue initialized.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["process_q_init_done"]}')

            check = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    return {
        'morpy_trace': morpy_trace,
        'check': check
    }

@metrics
def process_enqueue(morpy_trace: dict, app_dict: dict, priority: int=100, task: list=None, autocorrect: bool=True,
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
        # Check for Interrupt / exit
        stop_while_interrupt(morpy_trace, app_dict)

        if task:
            # Skip queuing, if in single core mode
            if not (morpy_trace["process_id"] == app_dict["morpy"]["proc_master"]) or force:
                from lib.fct import hashify
                from datetime import datetime

                with app_dict["morpy"].lock:
                    morpy_dict = app_dict["morpy"]
                    heap = morpy_dict["heap"]
                    counter = morpy_dict["process_q_counter"]
                    tasks_created = morpy_dict["tasks_created"]

                    # Substitute UltraDict references in task to avoid recursion issues.
                    task_sanitized = substitute_ultradict_refs(morpy_trace, app_dict, task)["task_sanitized"]

                    # Check and autocorrect process priority
                    if priority < 0 and autocorrect:
                        # Invalid argument given to process queue. Autocorrected.
                        log(morpy_trace, app_dict, "debug",
                        lambda: f'{app_dict["loc"]["morpy"]["process_enqueue_prio_corr"]}\n'
                                f'{app_dict["loc"]["morpy"]["process_enqueue_priority"]}: {priority} to 0')
                        priority = 0

                    # Pushing task to priority queue.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["process_enqueue_start"]}\n'
                            f'{app_dict["loc"]["morpy"]["process_enqueue_priority"]}: {priority}')

                    next_task_id = app_dict["morpy"]["tasks_created"] + 1
                    task_sys_id = id(task)

                    # Push task to queue
                    task_qed = (priority, next_task_id, task_sys_id, task_sanitized, is_process)

                    heappush(heap, task_qed)
                    app_dict["morpy"]["heap"] = heap # reassign to trigger synchronization

                    # Updating global tasks created last in case an error occurs
                    counter += 1
                    morpy_dict["process_q_counter"] = counter
                    tasks_created += 1
                    morpy_dict["tasks_created"] = tasks_created
                    morpy_trace["task_id"] = tasks_created

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
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    return {
        'morpy_trace': morpy_trace,
        'check': check
    }

@metrics
def process_pull(morpy_trace: dict, app_dict: dict) -> dict:
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
        with app_dict["morpy"].lock:
            morpy_dict = app_dict["morpy"]
            heap = morpy_dict["heap"]

            if len(heap) > 0:
                task_pulled = heappop(heap)
                app_dict["morpy"]["heap"] = heap # reassign to trigger synchronization

                priority, counter, task_sys_id, task, is_process = task_pulled

                # Pulling task from NAME priority: INT counter: INT
                log(morpy_trace_pull, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["process_pull_start"]}\n'
                        f'{app_dict["loc"]["morpy"]["process_pull_priority"]}: {priority}\n'
                        f'{app_dict["loc"]["morpy"]["process_pull_cnt"]}: {counter}',
                        verbose = True)

                check = True

            else:
                # Can not pull from an empty priority queue. Skipped...
                log(morpy_trace_pull, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["process_pull_void"]}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    return {
        'morpy_trace': morpy_trace_pull,
        'check': check,
        'priority' : priority,
        'counter' : counter,
        'task_id' : morpy_trace["task_id"],
        'task_sys_id' : task_sys_id,
        'task': task,
        'is_process': is_process
    }

@metrics
def substitute_ultradict_refs(morpy_trace: dict, app_dict: dict, task: list) -> dict:
    r"""
    Recursively traverse a task (which can be a list, tuple, or dict) and replace any
    UltraDict instance with a tuple placeholder. The tuple is structured as follows:

        (
            "__morPy_shared_ref__::{UltraDict.name}",
            UltraDict.shared_lock,   # (bool) whether a shared lock is used
            UltraDict.auto_unlink,   # (bool) whether the dict auto-unlinks on close
            UltraDict.recurse        # (bool) whether recursion (nested UltraDicts) is allowed
        )

    This substitution preserves the original structure so that later the task can be
    reconstructed exactly.
    """

    module: str = 'lib.mp'
    operation: str = 'substitute_ultradict_refs(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        def substitute(obj):
            if isinstance(obj, UltraDict):
                name_val = obj.name
                return (f"__morPy_shared_ref__::{name_val}",
                        obj.shared_lock,
                        obj.auto_unlink,
                        obj.recurse)
            elif isinstance(obj, list):
                return [substitute(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(substitute(item) for item in obj)
            elif isinstance(obj, dict):
                return {substitute(key): substitute(value) for key, value in obj.items()}
            else:
                return obj

        task_sanitized = substitute(task)
        check = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return {
        "morpy_trace": morpy_trace,
        "check": check,
        "task_sanitized": task_sanitized
    }

@metrics
def reattach_ultradict_refs(morpy_trace: dict, app_dict: dict, task) -> dict:
    r"""
    Recursively traverse a task (which can be a list, tuple, or dict) and replace any
    placeholder tuple with the actual UltraDict instance. A placeholder tuple must have the form:

        (
            "__morPy_shared_ref__::{name}",
            UltraDict.shared_lock,
            UltraDict.auto_unlink,
            UltraDict.recurse
        )

    The UltraDict is reattached by calling its constructor with these parameters and create=False.
    """

    module: str = 'lib.mp'
    operation: str = 'reattach_ultradict_refs(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        def reattach(obj):
            placeholder_prefix = "__morPy_shared_ref__::"
            if (isinstance(obj, tuple) and len(obj) == 4 and
                    isinstance(obj[0], str) and obj[0].startswith(placeholder_prefix)):
                name_val = obj[0][len(placeholder_prefix):]
                shared_lock_val = obj[1]
                auto_unlink_val = obj[2]
                recurse_val = obj[3]
                return UltraDict(
                    name=name_val,
                    create=False,
                    shared_lock=shared_lock_val,
                    auto_unlink=auto_unlink_val,
                    recurse=recurse_val
                )
            elif isinstance(obj, list):
                return [reattach(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(reattach(item) for item in obj)
            elif isinstance(obj, dict):
                return {reattach(key): reattach(value) for key, value in obj.items()}
            else:
                return obj

        task_recreated = reattach(task)
        check = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return {
        "morpy_trace": morpy_trace,
        "check": check,
        "task_recreated": task_recreated
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
        TODO provide example


    TODO make compatible with forking/free-threading
    """

    import lib.fct as morpy_fct

    module: str = 'lib.mp'
    operation: str = 'run_parallel(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    id_check: bool = False
    id_search: int = 0
    process_id: int = -1
    shelved: bool = False

    try:
        if isinstance(task, tuple):
            task = list(task)
            # The 'task' provided is a tuple. Autocorrected to list.
            log(morpy_trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["morpy"]["run_parallel_task_corr"]}\n{task=}')

        # Start preparing task for spawning process.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["run_parallel_start_prep"]}')

        # Fetch the maximum processes to be utilized by morPy
        processes_max = app_dict["morpy"]["processes_max"]

        if callable(task[0]):

            # See, if processes are waiting with an empty shelf.
            with app_dict["morpy"]["proc_waiting"].lock:
                proc_waiting = app_dict["morpy"]["proc_waiting"]
                for process in proc_waiting:
                    task_shelved, priority = proc_waiting[process]
                    # Put the task on the shelf and return.
                    if not task_shelved:
                        proc_waiting[process] = (task, priority)
                        shelved = True

            # Exit, if task has been shelved
            if shelved:
                # A task was shelved to a running process.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["run_parallel_shelved"]}')

                return {
                    'morpy_trace': morpy_trace,
                    'check': check,
                }

            with app_dict["morpy"].lock:
                processes_available = app_dict["morpy"]["proc_available"]
                processes_busy = app_dict["morpy"]["proc_busy"]
                process_id = None
                proc_master = app_dict["morpy"]["proc_master"]

                # Try up to 2 * processes_max attempts
                for attempt in range(2 * processes_max):
                    if not processes_available:
                        break  # No IDs available
                    process_id = min(processes_available)
                    # Remove candidate immediately from available_ids
                    processes_available.remove(process_id)
                    # If candidate is not busy, reserve it
                    if process_id not in processes_busy:
                        processes_busy.add(process_id)
                        break

                app_dict["morpy"]["proc_available"] = processes_available # reassign to trigger synchronization
                app_dict["morpy"]["proc_busy"] = processes_busy # reassign to trigger synchronization

            if process_id:
                # Process ID determined.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["run_parallel_search_iter_end"]}:\n'
                        f'{id_check=}\n{id_search=}')
                # Execute the task
                if process_id != proc_master:

                    # Parallel process starting.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["run_parallel_start"]}: {process_id}')

                    # Increment the total task count
                    with app_dict["morpy"]["orchestrator"].lock:
                        app_dict["morpy"]["orchestrator"]["task_counter"] += 1

                    # Tracing update and ID assignment for the new process
                    task[1].update({"process_id" : process_id})
                    task[1].update({"thread_id" : 0})
                    task[1].update({"task_id" : app_dict["morpy"]["orchestrator"]["task_counter"]})
                    task[1].update({"tracing" : ""})

                    # Run the task
                    if task is not None:
                        p = Process(target=partial(spawn, task))
                        p.start()

                        # Create references to the process
                        with app_dict["morpy"]["proc_refs"].lock:
                            proc_refs = app_dict["morpy"]["proc_refs"]
                            proc_refs.update({process_id : p.name})
                            app_dict["morpy"]["proc_refs"] = proc_refs # reassign to trigger synchronization

            else:
                # Enqueue the task again to prevent data loss
                process_enqueue(
                    morpy_trace, app_dict, priority=priority, task=[task, morpy_trace, app_dict]
                )

                # All processes busy, failed to allocate process ID. Re-queueing the task.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["run_parallel_allocate_fail"]}:\n'
                        f'{id_check=}\n{id_search=}')

            # Parallel process running.
            log(morpy_trace, app_dict, "debug",
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

def spawn(task: list) -> None:
    r"""
    This function registers a task in app_dict and executes it.

    :param task: Task represented by a list

    :return: dict
        morpy_trace: operation credentials and tracing information
        check: Indicates if the task was pulled successfully
        process_partial: Process to be spawned, packed with partial

    :example:
        TODO example

    TODO redirect stdout and stderr for this process to only show it's own and not duplicate in master process
        > Make custom I/O stream optional, because for app it is not generally desired.
    """

    import inspect

    morpy_trace: dict = None
    app_dict: dict = shared_dict(name="app_dict")
    my_id: int = None

    try:
        # Extract morpy_trace and app_dict (which must be provided by the parent).
        morpy_trace = task[1]
        my_id = morpy_trace["process_id"]

        # Recreate UltraDict references in task
        task_recreated = reattach_ultradict_refs(morpy_trace, app_dict, task)["task_recreated"]
        func = task_recreated[0]
        base_args = task_recreated[1:3]  # morpy_trace, app_dict
        extras = task_recreated[3:]  # any extra arguments

        sig = inspect.signature(func)
        full_args = base_args + tuple(extras)

        try:
            # First, try to bind everything as positional.
            sig.bind(*full_args)
            execution = lambda: func(*full_args)
        except TypeError:
            # If that fails and the last extra is a dict, then treat it as keyword arguments.
            if extras and isinstance(extras[-1], dict):
                pos_args = extras[:-1]
                kwargs = extras[-1]
                # Try binding with these assumptions.
                sig.bind(*(base_args + tuple(pos_args)), **kwargs)
                execution = lambda: func(*base_args, *pos_args, **kwargs)
            else:
                raise

        execution()

        module = morpy_trace["module"]
        operation = morpy_trace["operation"]

        # Wait until all are joined or take on a task.
        join_or_task(morpy_trace, app_dict, reset_trace=True, reset_w_prefix=f'{module}.{operation}')

        # Remove own process reference.
        # Always get the proc_refs lock first to prevent deadlocks and data loss.
        with app_dict["morpy"]["proc_refs"].lock:
            proc_refs = app_dict["morpy"]["proc_refs"]
            proc_refs.pop(my_id, None)
            app_dict["morpy"]["proc_refs"] = proc_refs # reassign to trigger synchronization

            with app_dict["morpy"].lock:
                proc_busy = app_dict["morpy"]["proc_busy"]
                proc_busy.remove(my_id)
                app_dict["morpy"]["proc_busy"] = proc_busy # reassign to trigger synchronization

    except Exception as e:
        # Remove own process references if left after exception
        try:
            # Always get the proc_refs lock first to prevent deadlocks and data loss.
            with app_dict["morpy"]["proc_refs"].lock:
                proc_refs = app_dict["morpy"]["proc_refs"]
                proc_refs.pop(my_id, None)
                app_dict["morpy"]["proc_refs"] = proc_refs # reassign to trigger synchronization

                with app_dict["morpy"].lock:
                    proc_busy = app_dict["morpy"]["proc_busy"]
                    proc_busy.remove(my_id)
                    app_dict["morpy"]["proc_busy"] = proc_busy  # reassign to trigger synchronization

                with app_dict["morpy"]["proc_waiting"].lock:
                    proc_waiting = app_dict["morpy"]["proc_waiting"]
                    if proc_waiting.get(my_id, None):
                        proc_waiting.remove(my_id)
                        app_dict["morpy"]["proc_waiting"] = proc_waiting # reassign to trigger synchronization

            from lib.exceptions import MorPyException
            morpy_trace["module"] = 'lib.mp'
            morpy_trace["operation"] = 'spawn(~)'
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")
        except:
            pass

@metrics
def check_child_processes(morpy_trace: dict, app_dict: dict, check_join: bool = False) -> dict:
    r"""
    Orchestrator routine to check on child processes and correct
    the process references in app_dict if necessary.

    This function compares the list of active child processes with the
    process references stored in app_dict["morpy"]["proc_refs"]. If a process
    is referenced but no longer active, it logs an error and removes that reference.
    It also attempts to terminate any processes that are still running but are not
    referenced in proc_refs (rogue processes).

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param check_join: If True, the orchestrator will check if all processes are
        joined. This may end processes, that could otherwise accept a shelved task.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the function ended without errors.

    :example:
        check_child_processes(morpy_trace, app_dict)
    """

    module: str = 'lib.mp'
    operation: str = 'check_child_processes(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    child_processes: dict = {}
    proc_left_over: set = set()

    try:
        # Always get the proc_refs lock first to prevent deadlocks and data loss.
        with (app_dict["morpy"]["proc_refs"].lock):
            proc_refs = app_dict["morpy"]["proc_refs"]

            # Build a set of active child process names
            for child in active_children():
                child_processes.update({child.name : child})

            # Compare morPy process references with active_children()
            for p_id, p_name in proc_refs.items():
                try:
                    child_processes.pop(p_name)
                except KeyError:
                    # A child process was terminated unexpectedly. Process references will be restored.
                    log(morpy_trace, app_dict, "error",
                    lambda: f'{app_dict["loc"]["morpy"]["check_child_processes_term_err"]}\n'
                            f'{app_dict["loc"]["morpy"]["check_child_processes_aff"]} "{p_id}: {p_name}"')

                    # Collect leftover process IDs
                    proc_left_over.add(p_id)

            # Try to terminate roque processes.
            roque_proc_names: list = child_processes.keys()
            if len(roque_proc_names) > 0:
                # At least one process still running, although considered terminated.
                # Recovery is not possible, trying to terminate.
                log(morpy_trace, app_dict, "warning",
                lambda: f'{app_dict["loc"]["morpy"]["check_child_processes_rogues"]}\n'
                        f'{app_dict["loc"]["morpy"]["check_child_processes_norec"]}'
                        f'{roque_proc_names}')

                for rogue_name, rogue_obj in child_processes.items():
                    try:
                        rogue_obj.terminate()
                    except:
                        pass

            # Finally, sanitize the process references
            with app_dict["morpy"].lock:
                proc_busy = app_dict["morpy"]["proc_busy"]

                for proc_remnant_id in proc_left_over:
                    del proc_refs[proc_remnant_id]
                    app_dict["morpy"]["proc_refs"] = proc_refs # reassign to trigger synchronization

                    proc_available = app_dict["morpy"]["proc_available"]
                    proc_available.add(proc_remnant_id)
                    app_dict["morpy"]["proc_available"] = proc_available # reassign to trigger synchronization

                    proc_busy.discard(proc_remnant_id)
                    app_dict["morpy"]["proc_busy"] = proc_busy # reassign to trigger synchronization

                    with app_dict["morpy"]["proc_waiting"].lock:
                        proc_waiting = app_dict["morpy"]["proc_waiting"]

                        if proc_waiting.get(proc_remnant_id, None):
                            # Proactively Recover a task from shelve
                            task_recovered, priority = proc_waiting[proc_remnant_id]
                            if task_recovered:
                                process_enqueue(morpy_trace, app_dict, priority=priority, task=task_recovered)
                                # A shelved task was recovered from a terminated task.
                                log(morpy_trace, app_dict, "warning",
                                lambda: f'{app_dict["loc"]["morpy"]["check_child_processes_recovery"]}'
                                        f'{roque_proc_names}')

                            proc_waiting.remove(proc_remnant_id)
                            app_dict["morpy"]["proc_waiting"] = proc_waiting  # reassign to trigger synchronization

                if check_join:
                    with app_dict["morpy"]["proc_waiting"].lock:
                        proc_waiting = app_dict["morpy"]["proc_waiting"]

                    # Have in mind, that the orchestrator is never waiting.
                    if len(proc_busy) == len(proc_waiting.keys()) + 1:
                        app_dict["morpy"]["proc_joined"] = True

                        # All child processes are joined.
                        log(morpy_trace, app_dict, "debug",
                        lambda: f'{app_dict["loc"]["morpy"]["check_child_processes_joined"]}')

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
def join_or_task(morpy_trace: dict, app_dict: dict, reset_trace: bool = False, reset_w_prefix: str=None) -> dict:
    r"""
    Join all processes orchestrated by morPy. This can not be used, to arbitrarily join processes.
    It is tailored to be used at the end of app.init, app.run and app.exit! The function is to
    join all processes of one of the steps (init - run - exit) before transitioning into the next.

    Cleanup of process references is performed by enqueued watcher() functions.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param reset_trace: If True, the trace will be reset/lost.
    :param reset_w_prefix: If reset_trace is True, a custom preset can be set in order to retain
        a customized trace.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was pulled successfully

    :example:
        join_or_task(morpy_trace, app_dict)

    TODO add idle_timeout to stop waiting for task shelving
    """

    import time

    module: str = 'lib.mp'
    operation: str = 'join_or_task(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace, reset=reset_trace,
                                          reset_w_prefix=reset_w_prefix)

    check: bool = False
    my_pid: int = morpy_trace["process_id"]

    try:
        # Check for Interrupt / exit
        stop_while_interrupt(morpy_trace, app_dict)

        # Skip if run by master / single process mode
        proc_master = app_dict["morpy"]["proc_master"]
        if my_pid != proc_master:
            # Waiting for processes to finish or task to run.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["join_or_task_start"]}')

            proc_joined = False
            while not proc_joined:
                time.sleep(0.05)    # 0.05 seconds = 50 milliseconds

                # Check for a shelved task
                with app_dict["morpy"]["proc_waiting"].lock:
                    proc_waiting = app_dict["morpy"]["proc_waiting"]
                    task, priority = proc_waiting.get(my_pid, (None, None))

                    # Unsubscribe from waiting dictionary if a task was assigned.
                    if task:
                        proc_waiting.pop(my_pid)
                        app_dict["morpy"]["proc_waiting"] = proc_waiting  # reassign to trigger synchronization

                if task:
                    # Check for Interrupt / exit
                    stop_while_interrupt(morpy_trace, app_dict)

                    # Recreate UltraDict references in task and run it.
                    task_recreated = reattach_ultradict_refs(morpy_trace, app_dict, task)["task_recreated"]
                    func = task_recreated[0]
                    args = task_recreated[1:]
                    func(*args)

                    # Clean up
                    del task
                    del task_recreated
                    del func
                    del args

                # Check for Interrupt / exit
                stop_while_interrupt(morpy_trace, app_dict)

                # Re-/subscribe to waiting dictionary.
                with app_dict["morpy"]["proc_waiting"].lock:
                    proc_waiting = app_dict["morpy"]["proc_waiting"]
                    if not proc_waiting.get(my_pid, None):
                        # Add task to waiting dictionary without a shelved task.
                        proc_waiting.update({my_pid: (None, None)})
                        app_dict["morpy"]["proc_waiting"] = proc_waiting  # reassign to trigger synchronization

                # Check, if processes have been joined yet.
                with app_dict["morpy"].lock:
                    proc_joined = app_dict["morpy"]["proc_joined"]

        check = True

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
    """

    module: str = 'lib.mp'
    operation: str = 'interrupt(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # Global interrupt has been set.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["interrupt_set"]}')

        if isinstance(app_dict, UltraDict):
            with app_dict["morpy"]:
                app_dict["morpy"]["interrupt"] = True
        else:
            app_dict["morpy"]["interrupt"] = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    finally:
        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

@metrics
def stop_while_interrupt(morpy_trace: dict, app_dict: dict) -> dict:
    r"""
    Wait until the global interrupt flag is set to False.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was pulled successfully

    :example:
        stop_while_interrupt(morpy_trace, app_dict)

    TODO distribute this function throughout the framework
    FIXME upon interrupt and then "exit"
        > Orchestrator does not start exit routine
        > Processes may not terminate
    """

    module: str = 'lib.mp'
    operation: str = 'stop_while_interrupt(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    exit_flag: bool = False

    try:
        with app_dict["morpy"].lock:
            interrupt_flag = app_dict["morpy"]["interrupt"]

        # Global interrupt. Process is waiting for release.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["stop_while_interrupt"]}')

        while interrupt_flag and not exit_flag:
            time.sleep(0.05)
            with app_dict["morpy"].lock:
                interrupt_flag = app_dict["morpy"]["interrupt"]
                exit_flag = app_dict["morpy"]["exit"]

        if exit_flag:
            with app_dict["morpy"]:
                proc_master = app_dict["morpy"]["proc_master"]

            # If process is orchestrator, gracefully exit
            # TODO make sure logs are still written
            if morpy_trace["process_id"] != proc_master:
                # TODO enqueue a log for "aborted task"
                # Remove own process references
                try:
                    # Always get the proc_refs lock first to prevent deadlocks and data loss.
                    with app_dict["morpy"]["proc_refs"].lock:
                        proc_refs = app_dict["morpy"]["proc_refs"]
                        proc_refs.pop(morpy_trace['process_id'], None)
                        app_dict["morpy"]["proc_refs"] = proc_refs # reassign to trigger synchronization

                        with app_dict["morpy"].lock:
                            proc_busy = app_dict["morpy"]["proc_busy"]
                            proc_busy.remove(morpy_trace['process_id'])
                            app_dict["morpy"]["proc_busy"] = proc_busy  # reassign to trigger synchronization

                        with app_dict["morpy"]["proc_waiting"].lock:
                            proc_waiting = app_dict["morpy"]["proc_waiting"]
                            if proc_waiting.get(morpy_trace['process_id'], None):
                                proc_waiting.remove(morpy_trace['process_id'])
                                app_dict["morpy"]["proc_waiting"] = proc_waiting # reassign to trigger synchronization
                except:
                    pass

                # TODO Make sure that this abrupt exit does not leave shared data in an inconsistent state or lead to orphaned tasks.
                sys.exit()

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
    r"""
    Create and return an UltraDict instance using shared memory.

    :param name: The name to be used for the shared memory block.
    :param create: If True, create a new shared memory block; if False, attach to an existing one.
    :param shared_lock: If True, the UltraDict will use a shared lock for cross‐process synchronization.
    :param size: The size (in bytes) of the memory buffer to be allocated.
    :param auto_unlink: If True, the shared memory will be automatically unlinked when the dict is closed.
    :param recurse: If True, allow nested UltraDict instances.

    :return shared_dict: UltraDict instance configured with the given parameters.

    TODO find a way to recreate buffer and dump sizes
    """

    from UltraDict import UltraDict

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

def is_udict(obj) -> bool:
    r"""
    Simple type check in the object provided. Returns True, if object is an UltraDict.

    :param obj: Any object.

    :return: True, if object is an UltraDict.

    TODO distribute throughout the code.
    """

    from UltraDict import UltraDict

    is_udict: bool = False

    if isinstance(obj, UltraDict):
        is_udict = True

    return is_udict
