r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Multiprocessing functionality for morPy.
"""

import lib.fct as morpy_fct
from lib.decorators import metrics, log

import sys
import time
from UltraDict import UltraDict
from multiprocessing import Process, active_children
from functools import partial
from heapq import heappush, heappop
from typing import Any, Callable, List

class MorPyOrchestrator:
    r"""
    Manages and coordinates tasks across multiple processes. It sets up internal queues, tracks
    available versus busy processes, and synchronizes task execution in multiprocessing environments.
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
        Initializes the orchestrator by reading the maximum process count from the configuration, determining
        whether multiprocessing is enabled, and initializing internal data structures (heap, task tracking).
        It then prepares process tracking structures for busy and available process IDs and calls _init_run
        to record the invoking context.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

<<<<<<< Updated upstream
        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._init(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
=======
        app_dict["morpy"]["orchestrator"]["terminate"] = False
>>>>>>> Stashed changes

        try:
            # Set app termination flag
            app_dict["morpy"]["orchestrator"]["terminate"] = False

            # Determine if multiprocessing is enabled
            self.processes_max: int = app_dict["morpy"]["processes_max"]
            if self.processes_max > 1:
                self._mp: bool = True
            else:
                self._mp: bool = False
            app_dict["morpy"]["orchestrator"]["mp"] = self._mp

            # Construct arguments for heap and tasks
            if self._mp:
                self.heap = list()
                self.curr_task = dict()
                self.curr_task["priority"] = None
                self.curr_task["counter"] = None
                self.curr_task["task_sys_id"] = None
                self.curr_task["task"] = None
                self.curr_task["is_process"] = None

                # Build references to available and busy process IDs
                self._init_processes(morpy_trace, app_dict)

            # Set up first tasks
            self._init_run(morpy_trace, app_dict)

            # MorPyOrchestrator initialized.
            log(morpy_trace, app_dict, "init",
            lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_done"]}')

            check = True

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
        Prepares shared dictionaries for tracking process states. It iterates over possible
        process IDs (except the master) and registers those not already marked as busy as
        available for task assignment.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._init_processes(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        try:
            # Get global process sets for membership testing
            processes_available = app_dict["morpy"]["proc_available"]
            processes_busy = app_dict["morpy"]["proc_busy"]
            proc_master = app_dict["morpy"]["proc_master"]

            p = 0
            while p < self.processes_max:
                # Check for process IDs reserved during early initialization of morPy.
                if p in processes_busy:
                    pass
                elif p in processes_available:
                    pass
                else:
                    if p != proc_master:
                        # Append to available processes without a reference to a running process.
                        app_dict["morpy"]["proc_available"][p] = None

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
<<<<<<< Updated upstream
        Setup attributes for orchestrator._run().
=======
        Captures the calling context (module name and operation) from the trace and stores it
        within the orchestrator for later logging and diagnostics.
>>>>>>> Stashed changes

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator._init_run(~)'
        morpy_trace_init_run = morpy_fct.tracing(module, operation, morpy_trace)

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
    def run(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Starts the application by enqueuing the main task for multiprocessing if enabled;
        otherwise, it runs the app sequentially. In multiprocessing mode it calls the
        internal loop (_mp_loop) to continuously process tasks.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

<<<<<<< Updated upstream
        module: str = 'lib.mp'
        operation: str = 'MorPyOrchestrator.run(~)'
        # TODO Find out, why morpy_trace["process_id"] is overwritten in app trace
        # The enforced deepcopy morpy_fct.tracing() is a workaround.
        morpy_trace_app: dict = morpy_fct.tracing(module, operation, morpy_trace)
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)
=======
        # Start the app - multiprocessing loop
        if self._mp:
            app_task = [app_run, trace, app_dict]
            heap_shelve(trace, app_dict, priority=-90, task=app_task, autocorrect=False, force=self._mp)

            # Enter the multiprocessing loop
            self._mp_loop(trace, app_dict)
>>>>>>> Stashed changes

        check: bool = False

        try:
            # Start the app - multiprocessing loop
            if self._mp:
                app_task = [app_run, morpy_trace_app, app_dict]
                heap_shelve(morpy_trace, app_dict, priority=-90, task=app_task, autocorrect=False, force=self._mp)
                terminate = False
                self._mp_loop(morpy_trace, app_dict)

            # Start the app - single process
            else:
                app_run(morpy_trace_app, app_dict)

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
    def heap_pull(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Transfers any tasks that have been shelved in the shared heap_shelf into the orchestrator’s
        own heap queue. Then it pops the highest‑priority task and stores its details in the
        orchestrator’s current task record.

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
            TODO write example
        """

        module: str = 'lib.mp'
        operation: str = 'heap_pull(~)'
        morpy_trace_pull = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False
        pulled_tasks = set()

        try:
            # Pull tasks from shelf and feed the heap
            with app_dict["morpy"]["heap_shelf"].lock:
                for pid, task_shelved in app_dict["morpy"]["heap_shelf"].items():
                    heappush(self.heap, task_shelved)
                    pulled_tasks.add(pid)

                # Clean up and remove pulled tasks from shelf
                for key in pulled_tasks:
                    del app_dict["morpy"]["heap_shelf"][key]

            if len(self.heap) > 0:
                task_pulled = heappop(self.heap)
                self.curr_task["priority"] = task_pulled[0]
                self.curr_task["counter"] = task_pulled[1]
                self.curr_task["task_sys_id"] = task_pulled[2]
                self.curr_task["task"] = task_pulled[3]
                self.curr_task["is_process"] = task_pulled[4]

                # Pulling task from heap. Priority: INT Counter: INT
                log(morpy_trace_pull, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["heap_pull_start"]}\n'
                        f'{app_dict["loc"]["morpy"]["heap_pull_priority"]}: {self.curr_task["priority"]}\n'
                        f'{app_dict["loc"]["morpy"]["heap_pull_cnt"]}: {self.curr_task["counter"]}',
                verbose=True)

                check = True

            else:
                # Can not pull from an empty priority queue. Skipped...
                log(morpy_trace_pull, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["heap_pull_void"]}')

        except Exception as e:
            from lib.exceptions import MorPyException
            raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

        return {
            'morpy_trace': morpy_trace_pull,
            'check': check
        }

    @metrics
    def _mp_loop(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Executes the orchestrator’s main processing loop. It continuously checks for new tasks
        in the heap, either processing them by spawning new processes or by executing tasks
        directly. It also monitors exit conditions and cleans up orphaned processes.

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
        terminate: bool = False
        check_join: bool = False

        try:
            heap_len = len(self.heap) + len(app_dict["morpy"]["heap_shelf"].keys())

            while not terminate or heap_len > 0:
                # Check process queue for tasks
                if heap_len > 0:
                    self.heap_pull(morpy_trace, app_dict)
                    task = self.curr_task["task"]
                    task_id = self.curr_task["counter"]

                    if task:
                        is_process = self.curr_task["is_process"]
                        priority = self.curr_task["priority"]
                        # Run a new parallel process
                        if is_process:
                            with app_dict["morpy"].lock:
                                exit_flag = app_dict["morpy"]["exit"]

                            # Only run new processes if not exiting.
                            if not exit_flag:
                                app_dict["morpy"]["proc_joined"] = False
                                run_parallel(morpy_trace, app_dict, task=task, priority=priority, task_id=task_id)
                                terminate = False
                                with app_dict["morpy"]["orchestrator"].lock:
                                    app_dict["morpy"]["orchestrator"]["terminate"] = terminate
                        # Run an orchestrator task directly
                        else:
                            # Recreate UltraDict references in task
                            task_recreated = reattach_ultradict_refs(task)
                            execute = task_to_partial(task_recreated)
                            execute()

                        # Clean up after cycle
                        del task

                else:
                    # Sleep if heap is empty / wait for shelved process acceptance
                    time.sleep(0.2)  # 0.2 seconds = 200 milliseconds

                    # Check on child processes: signal join or pass tasks
                    with app_dict["morpy"].lock:
                        with app_dict["morpy"]["proc_waiting"].lock:
                            if (not app_dict["morpy"]["proc_joined"]
                                and len(app_dict["morpy"]["proc_waiting"].keys())):
                                check_join = True
                    if not app_dict["morpy"]["proc_joined"] and heap_len == 0:
                        check_child_processes(morpy_trace, app_dict, check_join=True)

                # TODO make use of program exit with critical exceptions
                # TODO make sure no memory leaks are introduced when exiting
                with app_dict["morpy"].lock:
                    # Check for the global exit flag
                    exit_flag = app_dict["morpy"]["exit"]

                    # Exit request detected. Termination in Progress.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_exit_request"]}',
                            verbose=True)


                    # Finish writing logs first
                    if exit_flag:
                        logs_written = False if any(task[0] == -100 for task in self.heap) else True

                        if logs_written:
                            no_children = True if len(app_dict["morpy"]["proc_busy"]) < 2 else False
                            if no_children:
                                terminate = True
                                self.heap = []
                                heap_len = 0

                                with app_dict["morpy"]["orchestrator"].lock:
                                    app_dict["morpy"]["orchestrator"]["terminate"] = terminate

                                # App terminating after exit request. No logs left from child processes.
                                log(morpy_trace, app_dict, "debug",
                                lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_exit_request_complete"]}')


                # In case of global exit, delete the heap.
                # if exit_flag:
                #     with app_dict["morpy"].lock:
                #         app_dict["morpy"]["heap"] = []

                # Fail-safe check if really no child processes are running anymore.
                if terminate and not exit_flag:
                    # TODO call check_child_processes()
                    # terminate = RESULT
                    # exit_flag = RESULT
                    pass

                if terminate:
                    with app_dict["morpy"]["orchestrator"].lock:
                        app_dict["morpy"]["orchestrator"]["terminate"] = terminate

                # Calculate open tasks
                with app_dict["morpy"]["heap_shelf"].lock:
                    heap_len = len(self.heap) + len(app_dict["morpy"]["heap_shelf"].keys())

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
def app_run(morpy_trace: dict, app_dict: dict) -> dict:
    r"""
    Coordinates the sequential execution of the three main phases: app initialization, main run,
    and exit. In multiprocessing mode, the tasks are enqueued and managed by the orchestrator;
    in single‑process mode, they are executed directly.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    """

    module: str = 'lib.mp'
    operation: str = 'app_run(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    udict: bool = False

    try:
        from app.init import app_init
        from app.run import app_run
        from app.exit import app_exit

        udict = True if isinstance(app_dict, UltraDict) else False

        # --- APP INITIALIZATION --- #

        # App initializing.
        log(morpy_trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["morpy"]["app_run_init"]}')

        # Execute
        app_init_return = app_init(morpy_trace, app_dict)["app_init_return"]

        # Join all spawned processes before transitioning into the next phase.
        join_or_task(morpy_trace, app_dict, reset_trace=True, reset_w_prefix=f'{module}.{operation}')

        # Set the "initialization complete" flag
        # TODO Up until this point prints to console are mirrored on splash screen
        if isinstance(app_dict["morpy"], UltraDict):
            with app_dict["morpy"].lock:
                app_dict["morpy"]["init_complete"] = True
        else:
            app_dict["morpy"]["init_complete"] = True

        # Un-join
        if udict:
            with app_dict["morpy"].lock:
                app_dict["morpy"]["proc_joined"] = False

        # --- APP RUN --- #

        # App starting.
        log(morpy_trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["morpy"]["app_run_start"]}')

        app_run_return = app_run(morpy_trace, app_dict, app_init_return)["app_run_return"]

        # Join all spawned processes before transitioning into the next phase.
        join_or_task(morpy_trace, app_dict, reset_trace=True, reset_w_prefix=f'{module}.{operation}')

        # Un-join
        if udict:
            with app_dict["morpy"].lock:
                app_dict["morpy"]["proc_joined"] = False

        # --- APP EXIT --- #

        # App exiting.
        log(morpy_trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["morpy"]["app_run_exit"]}')

        # Exit the app and signal morPy to exit
        app_exit(morpy_trace, app_dict, app_run_return)

        # Join all spawned processes before transitioning into the next phase.
        join_or_task(morpy_trace, app_dict, reset_trace=True, reset_w_prefix=f'{module}.{operation}')

        # Signal morPy orchestrator of app termination
        if isinstance(app_dict["morpy"], UltraDict):
            with app_dict["morpy"].lock:
                app_dict["morpy"]["exit"] = True
        else:
            app_dict["morpy"]["exit"] = True

        check: bool = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    return {
        'morpy_trace': morpy_trace,
        'check': check,
    }

@metrics
def heap_shelve(morpy_trace: dict, app_dict: dict, priority: int=100, task: Callable | list | tuple=None,
                    autocorrect: bool=True, is_process: bool=True, force: bool = False, task_id: int=None) -> dict:
    r"""
    Queues a new task into the shared memory shelf for later execution. The task may be provided in
    multiple formats; it is normalized into a list, sanitized by substituting UltraDict references,
    and then stored along with its priority and an incremented task ID. If the caller is not the
    master process (or if forced), the task is queued; otherwise, it is executed immediately.

    :param morpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param priority: Integer representing task priority (lower is higher priority)
    :param task: Callable, list or tuple packing the task. Formats:
        callable: partial(func, *args, **kwargs)
        list: [func, *args, {"kwarg1": val1, "kwarg2": val2, ...}]
        tuple: (func, *args, {"kwarg1": val1, "kwarg2": val2, ...})
    :param autocorrect: If False, priority can be smaller than zero. Priority
        smaller zero is reserved for the morPy Core.
    :param is_process: If True, task is run in a new process (not by morPy orchestrator)
    :param force: If True, enforces queueing instead of direct execution. Used by morPy
        orchestrator to spawn the first app process.
    :param task_id: Value representing a task ID. Here it is only used to recover and re-shelve a task.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was enqueued successfully

    :example:
        from lib.mp import heap_shelve
        from functools import partial
        task = partial(my_func, morpy_trace, app_dict)
        heap_shelve(morpy_trace, app_dict, priority=25, task=task)
    """

    module: str = 'lib.mp'
    operation: str = 'heap_shelve(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # Check for Interrupt / exit
        stop_while_interrupt(morpy_trace, app_dict)

        if task:
            # Transform task to a list, if possible
            task = normalize_task(task)
            proc_master = app_dict["morpy"]["proc_master"]

            # Skip queuing, if in single core mode
            if not (morpy_trace["process_id"] == proc_master) or force:
                with app_dict["morpy"].lock:
                    with app_dict["morpy"]["heap_shelf"].lock:
                        morpy_dict = app_dict["morpy"]

                        # Substitute UltraDict references in task to avoid recursion issues.
                        task_sanitized = substitute_ultradict_refs(morpy_trace, app_dict, task)["task_sanitized"]

                        # Check and autocorrect process priority
                        if priority < 0 and autocorrect:
                            # Invalid argument given to process queue. Autocorrected.
                            log(morpy_trace, app_dict, "debug",
                            lambda: f'{app_dict["loc"]["morpy"]["heap_shelve_prio_corr"]}\n'
                                    f'{app_dict["loc"]["morpy"]["heap_shelve_priority"]}: {priority} to 0')
                            priority = 0

                        # Pushing task to priority queue.
                        log(morpy_trace, app_dict, "debug",
                        lambda: f'{app_dict["loc"]["morpy"]["heap_shelve_start"]}\n'
                                f'{app_dict["loc"]["morpy"]["heap_shelve_priority"]}: {priority}')

                        next_task_id = task_id if task_id is not None else app_dict["morpy"]["tasks_created"] + 1
                        task_sys_id = id(task)

                        # Push task to heap shelf
                        task_qed = (priority, next_task_id, task_sys_id, task_sanitized, is_process)

                        morpy_dict["heap_shelf"][next_task_id] = task_qed

                        # Updating global tasks created last in case an error occurs
                        if not task_id:
                            morpy_dict["tasks_created"] += 1

            # If run by morPy orchestrator or in single core mode, execute without queueing.
            else:
                # Transform task to a list if possible
                task = normalize_task(task)
                execute = task_to_partial(task)
                execute()

            check: bool = True
        else:
            # Task can not be None. Skipping enqueue.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["heap_shelve_none"]}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    return {
        'morpy_trace': morpy_trace,
        'check': check
    }

@metrics
def substitute_ultradict_refs(morpy_trace: dict, app_dict: dict, task: list) -> dict:
    r"""
    Recursively searches through a task (which may be a list, tuple, or dict) and replaces any
    UltraDict instance with a placeholder tuple (containing its unique name and configuration
    flags) to prevent serialization recursion errors.

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

    try:
        # Substitute UltraDict references to mitigate RecursionError
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

def reattach_ultradict_refs(task) -> list:
    r"""
    Recursively converts placeholder tuples back into UltraDict instances by re‑creating them
    from their stored configuration, restoring the original task structure for execution.

        ("__morPy_shared_ref__::{name}",
        UltraDict.shared_lock,
        UltraDict.auto_unlink,
        UltraDict.recurse)

    The UltraDict is reattached by calling its constructor with these parameters and create=False.
    """

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
    return task_recreated

@metrics
def run_parallel(morpy_trace: dict, app_dict: dict, task: list=None, priority: int=None, task_id: int=None) -> dict:
    r"""
<<<<<<< Updated upstream
    Takes a task from the morPy heap, reserves a process ID, modifies the
    morpy_trace of the task and ultimately starts the parallel process.
=======
    Attempts to reserve an available process ID; if successful, updates the task’s trace with that
    ID and spawns a new process (using SpawnWrapper) to run the task in parallel. If no process is
    available, the task is re‑queued.
>>>>>>> Stashed changes

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param task: The pulled task list
    :param priority: Integer representing task priority (lower is higher priority)
    :param task_id: Value representing the unique, continuing task ID

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was pulled successfully

    :example:
        TODO provide example


    TODO make compatible with forking/free-threading
    """

    module: str = 'lib.mp'
    operation: str = 'run_parallel(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    shelved: bool = False

    try:
        # Start preparing task for spawning process.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["run_parallel_start_prep"]}')

        # See, if processes are waiting with an empty shelf.
        with app_dict["morpy"]["proc_waiting"].lock:
            proc_waiting = app_dict["morpy"]["proc_waiting"]
            for process in proc_waiting.keys():
                # Only unpack the task to check, if it is Nine
                task_shelved = proc_waiting[process][0]
                # Put the task on the shelf and return.
                if task_shelved is None:
                    proc_waiting[process] = (task, priority, task_id)
                    shelved = True
                    break

        # Exit, if task has been shelved
        if shelved:
            # A task was shelved to a running process.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["run_parallel_shelved"]}')

            return {
                'morpy_trace': morpy_trace,
                'check': True,
            }

        with app_dict["morpy"]["proc_available"].lock:
            with app_dict["morpy"]["proc_busy"].lock:
                proc_available_keys = app_dict["morpy"]["proc_available"].keys()
                processes_busy = app_dict["morpy"]["proc_busy"]
                process_id = None

                # Look up for an available process ID and create a shell for the new process.
                if len(proc_available_keys) > 0:
                    process_id = min(proc_available_keys)
                    processes_busy[process_id] = None
                    app_dict["morpy"]["proc_available"].pop(process_id)

        if process_id:
            with app_dict["morpy"].lock:
                # Process ID determined.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["run_parallel_search_iter_end"]}:\n'
                        f'{process_id=}')

                proc_master = app_dict["morpy"]["proc_master"]

                # Execute the task
                if process_id != proc_master:

                    # Parallel process starting.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["run_parallel_start"]}: {process_id}')

                    if not task_id:
                        app_dict["morpy"]["tasks_created"] += 1
                        task_id = app_dict["morpy"]["tasks_created"]

                    # Tracing update and ID assignment for the new process
                    task[1].update({"process_id" : process_id})
                    task[1].update({"thread_id" : 0})
                    task[1].update({"task_id" : task_id})
                    task[1].update({"tracing" : ""})

                    # Run the task
                    from lib.spawn import SpawnWrapper
                    task_spawn = SpawnWrapper(task)
                    p = Process(target=task_spawn)
                    p.start()

                    # Store the reference of the process
                    with app_dict["morpy"]["proc_busy"].lock:
                        app_dict["morpy"]["proc_busy"][process_id] = f'{p.name}'

                    # Parallel process running.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["run_parallel_exit"]}: {process_id}')

        else:
            # Enqueue the task again to prevent data loss
            existing_id = task[1].get("task_id", None)
            heap_shelve(
                morpy_trace, app_dict, priority=priority, task=task, force=True, task_id= existing_id
            )

            # All processes busy, failed to allocate process ID. Re-queueing the task.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["run_parallel_allocate_fail"]}')

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    finally:
        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

@metrics
def check_child_processes(morpy_trace: dict, app_dict: dict, check_join: bool = False) -> dict:
    r"""
    Compares the process IDs of child processes currently active (using multiprocessing.active_children)
    with those stored in the busy process register. If discrepancies are found (i.e. a process is missing
    or rogue processes exist), logs appropriate warnings, cleans up the internal registers, and attempts
    to terminate any stray processes.

    This function compares the list of active child processes with the
    process references stored in app_dict["morpy"]["proc_busy"]. If a process
    is referenced but no longer active, it logs an error and removes that reference.
    It also attempts to terminate any processes that are still running but are not
    referenced in proc_busy (rogue processes).

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
        proc_master = app_dict["morpy"]["proc_master"]

        with app_dict["morpy"]["proc_busy"].lock:
            proc_busy = app_dict["morpy"]["proc_busy"]

        # Build a set of active child process names
        for child in active_children():
            child_processes.update({child.name : child})

        # Compare morPy process references with active_children()
        for p_id, p_name in proc_busy.items():
            if p_id != proc_master:
                try:
                    child_processes.pop(p_name)
                except KeyError:
                    # Check whether the app needs to exit
                    severity = "critical" if app_dict["morpy"]["conf"]["processes_are_critical"] else "warning"

                    # A child process was terminated unexpectedly. Process references will be restored,
                    # but the task and data may be lost.
                    log(morpy_trace, app_dict, severity,
                    lambda: f'{app_dict["loc"]["morpy"]["check_child_processes_term_err"]}\n'
                            f'{app_dict["loc"]["morpy"]["check_child_processes_aff"]} "{p_id}: {p_name}"')

                    with app_dict["morpy"].lock:
                        app_dict["morpy"]["exit"] = True

                    # Collect leftover process IDs
                    proc_left_over.add(p_id)

        # Try to terminate roque processes.
        roque_proc_names = child_processes.keys()
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
                except ProcessLookupError | OSError:
                    pass

        # Sanitize the process references
        if len(proc_left_over) > 0:
            with app_dict["morpy"]["proc_available"].lock:
                with app_dict["morpy"]["proc_busy"].lock:
                    for proc_remnant_id in proc_left_over:
                        # Remove process from busy
                        app_dict["morpy"]["proc_busy"].pop(proc_remnant_id)
                        # Add available process ID
                        app_dict["morpy"]["proc_available"][proc_remnant_id] = None

            # Attempt task recovery
            with app_dict["morpy"]["proc_waiting"].lock:
                proc_waiting = app_dict["morpy"]["proc_waiting"]

                for proc_remnant_id in proc_left_over:
                    if proc_waiting.get(proc_remnant_id, None):
                        # Proactively Recover a task from shelve
                        task_recovered, priority, task_id = proc_waiting[proc_remnant_id]
                        if task_recovered:
                            heap_shelve(morpy_trace, app_dict, priority=priority, task=task_recovered,
                                        task_id=task_id)
                            # A shelved task was recovered from a terminated task.
                            log(morpy_trace, app_dict, "warning",
                            lambda: f'{app_dict["loc"]["morpy"]["check_child_processes_recovery"]}'
                                    f'{roque_proc_names}')

                        proc_waiting.pop(proc_remnant_id)

<<<<<<< Updated upstream
        if check_join:
            with app_dict["morpy"]["proc_waiting"].lock:
                proc_waiting = app_dict["morpy"]["proc_waiting"]

            # Have in mind, that the orchestrator is never waiting (therefore +1).
            if len(app_dict["morpy"]["proc_busy"].keys()) == (len(proc_waiting.keys()) + 1):
                app_dict["morpy"]["proc_joined"] = True

                # All child processes are joined.
                log(morpy_trace, app_dict, "debug",
=======
    if check_join:
        # No join, if there are tasks on the heap shelf
        with app_dict["morpy"]["heap_shelf"].lock:
            if len(app_dict["morpy"]["heap_shelf"]) > 1:
                return

        # No join, if waiting processes already got a new task assigned
        with app_dict["morpy"]["proc_waiting"].lock:
            proc_waiting = app_dict["morpy"]["proc_waiting"]
        for _p, _t in proc_waiting.items():
            if _t[0] is not None:
                return

        # Have in mind, that the orchestrator is never waiting (therefore +1).
        if len(app_dict["morpy"]["proc_busy"].keys()) == (len(proc_waiting.keys()) + 1):
            app_dict["morpy"]["proc_joined"] = True

            # All child processes are joined.
            log(trace, app_dict, "debug",
>>>>>>> Stashed changes
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
    Waits in a loop until all spawned tasks have completed or a new task appears for the current process.
    This function is used to synchronize transitions between app phases (e.g. after initialization,
    before running, or before exiting).

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
                    task, priority, task_id = proc_waiting.get(my_pid, (None, None, None))

                    # Unsubscribe from waiting dictionary if a task was assigned.
                    if task:
                        proc_waiting.pop(my_pid)

                if task:
                    # Check for Interrupt / exit
                    stop_while_interrupt(morpy_trace, app_dict)

                    # Assign task ID to own trace and claim task
                    morpy_trace["task_id"] = task_id
                    task[1] = morpy_trace

                    # Recreate UltraDict references in task and run it.
                    task_recreated = reattach_ultradict_refs(task)
                    execute = task_to_partial(task_recreated)
                    execute()

                    # Clean up
                    del task
                    del task_recreated

                # Check for Interrupt / exit
                stop_while_interrupt(morpy_trace, app_dict)

                # Re-/subscribe to waiting dictionary.
                with app_dict["morpy"]["proc_waiting"].lock:
                    proc_waiting = app_dict["morpy"]["proc_waiting"]
                    if not proc_waiting.get(my_pid, None):
                        # Add task to waiting dictionary without a shelved task.
                        proc_waiting.update({my_pid: (None, None, None)})

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
    Immediately sets the global interrupt flag so that tasks will pause once they reach a safe checkpoint.

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
        log(morpy_trace, app_dict, "warning",
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
    Causes the calling thread or process to sleep until the global interrupt flag is cleared
    (or an exit is signaled).

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
        if app_dict["morpy"]["processes_max"] > 1:
            with app_dict["morpy"].lock:
                interrupt_flag = app_dict["morpy"]["interrupt"]

            if interrupt_flag:
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
                        with app_dict["morpy"]["proc_available"].lock:
                            with app_dict["morpy"]["proc_busy"].lock:
                                # Remove from busy processes
                                app_dict["morpy"]["proc_busy"].pop(morpy_trace['process_id'])
                                # Add to processes available IDs (hygiene only, no other use at app exit)
                                app_dict["morpy"]["proc_available"]["process_id"] = None

                        with app_dict["morpy"]["proc_waiting"].lock:
                            proc_waiting = app_dict["morpy"]["proc_waiting"]
                            if proc_waiting.get(morpy_trace['process_id'], None):
                                proc_waiting.remove(morpy_trace['process_id'])
                    except Exception as e:
                        print(e)

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
    Creates or attaches to a shared UltraDict instance with specified parameters (name, creation flag,
    shared lock usage, buffer size, auto‑unlink behavior, recursion). Returns the UltraDict instance
    for shared inter‑process access.

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

    connect_udict = UltraDict(
        name=name,
        create=create,
        shared_lock=shared_lock,
        buffer_size=size,
        full_dump_size=size,
        auto_unlink=auto_unlink,
        recurse=recurse
    )

    return connect_udict

<<<<<<< Updated upstream
=======

@core_wrap
def child_exit_routine(trace: dict, app_dict: dict | UltraDict) -> None:
    r"""
    Performs cleanup of a terminating child process by removing its references from busy and waiting
    process registers. After cleanup, the function terminates the process with sys.exit().

    :param trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    """

    try:
        # Remove own process references
        with app_dict["morpy"]["proc_available"].lock:
            with app_dict["morpy"]["proc_busy"].lock:
                # Remove from busy processes
                app_dict["morpy"]["proc_busy"].pop(trace["process_id"])
                # Add to processes available IDs (hygiene only, no other use at app exit)
                app_dict["morpy"]["proc_available"][trace["process_id"]] = None

        with app_dict["morpy"]["proc_waiting"].lock:
            proc_waiting = app_dict["morpy"]["proc_waiting"]
            if proc_waiting.get(trace['process_id'], None):
                proc_waiting.pop(trace['process_id'])

    # In case of a KeyError, the processes references were already cleaned up. This
    # may happen when an exit is requested and the spawned process still cleans up
    # regularly.
    except KeyError:
        pass

    sys.exit()


>>>>>>> Stashed changes
def is_udict(obj) -> bool:
    r"""
    Checks whether a given object is an instance of UltraDict and returns True if so.

    :param obj: Any object.

    :return: True, if object is an UltraDict.

    TODO distribute throughout the code.
    """

    from UltraDict import UltraDict

    check: bool = False

    if isinstance(obj, UltraDict):
        check = True

    return check

def normalize_task(task):
    r"""
    Converts a task given as a callable, list, tuple, or functools.partial into a standard
    list format [func, arg1, …, {keyword arguments}]. If already in list form, it is
    returned unchanged.

    :param task: Callable, list or tuple packing the task. Formats:
        callable: partial(func, *args, **kwargs)
        list: [func, *args, **kwargs]
        tuple: (func, *args, **kwargs)

    :return task_out: Task packed as a list.
    """

    if isinstance(task, list):
        return task
    elif isinstance(task, tuple):
        return list(task)
    elif isinstance(task, partial):
        normalized = [task.func] + list(task.args)
        if task.keywords:
            normalized.append(task.keywords)
        return normalized
    else:
        # For other callables, we return them as-is.
        return task


def task_to_partial(task: List[Any]) -> Callable:
    r"""
    Takes a task represented as a standard list and converts it into a callable using functools.partial.
    If the last element is a dictionary, it is treated as keyword arguments; otherwise, all subsequent
    elements are positional arguments.

    The task list is expected to have the following structure:
      [function, arg1, arg2, ..., kwargs]

    If the last element is a dictionary, it is unpacked as keyword arguments.
    Otherwise, all elements after the first are treated as positional arguments.

    :param task: List representing the task.

    :return: A callable (partial) that can be directly invoked.
    """

    if not task:
        raise ValueError(f'{task=}')

    func = task[0]

    # If the last element is a dict, treat it as keyword arguments.
    if len(task) > 3 and isinstance(task[-1], dict):
        pos_args = task[1:-1]
        kwargs = task[-1]
        return partial(func, *pos_args, **kwargs)
    else:
        return partial(func, *task[1:])