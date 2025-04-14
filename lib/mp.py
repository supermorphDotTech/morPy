r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Multiprocessing functionality for morPy.
"""

import lib.fct as morpy_fct
from morPy import log, conditional_lock
from lib.decorators import core_wrap

import sys
import time
from UltraDict import UltraDict
from multiprocessing import Process, active_children
from functools import partial
from heapq import heappush, heappop
from typing import Any, Callable, List


class MorPyOrchestrator:
    r"""
    Class of morPy orchestrators.
    """

    __slots__ = [
        '_mp',
        'curr_task',
        'heap',
        'trace',
        'processes_max',
        'ref_module',
        'ref_operation'
    ]


    @core_wrap
    def __init__(self, trace: dict, app_dict: dict) -> None:
        r"""
        Initialization helper method for parallel processing setup.

        :param trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

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
            self._init_processes(trace, app_dict)

        # Set up first tasks
        self._init_run(trace, app_dict)

        # MorPyOrchestrator initialized.
        log(trace, app_dict, "init",
            lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_init_done"]}')


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @core_wrap
    def _init_processes(self, trace: dict, app_dict: dict) -> None:
        r"""
        Prepare nested dictionaries and store data in app_dict.

        :param trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        # Get global process sets for membership testing
        with app_dict["morpy"]["proc_busy"].lock:
            processes_busy = app_dict["morpy"]["proc_busy"]

        with app_dict["morpy"].lock:
            proc_master = app_dict["morpy"]["proc_master"]

        with app_dict["morpy"]["proc_available"].lock:
            processes_available = app_dict["morpy"]["proc_available"]

            for p in range(0, self.processes_max + 1):
                # Check for process IDs reserved during early initialization of morPy.
                if p in processes_busy:
                    pass
                elif p in processes_available:
                    pass
                else:
                    if p != proc_master:
                        # Append to available processes without a reference to an already running process.
                        processes_available[p] = None

            app_dict["morpy"]["proc_available"] = processes_available


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @core_wrap
    def _init_run(self, trace: dict, app_dict: dict) -> None:
        r"""
        Setup attributes for orchestrator.run().

        :param trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        # Set attributes for run
        self.ref_module: str = trace["module"]
        self.ref_operation: str = trace["operation"]
        self.trace: dict = trace


    @core_wrap
    def run(self, trace: dict, app_dict: dict) -> None:
        r"""
        Routine of the morPy orchestrator. Cyclic program.

        :param trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        # Start the app - multiprocessing loop
        if self._mp:
            app_task = [app_run, trace, app_dict]
            heap_shelve(trace, app_dict, priority=-90, task=app_task, autocorrect=False, force=self._mp)
            self._mp_loop(trace, app_dict)

        # Start the app - single process
        else:
            app_run(trace, app_dict)


    @core_wrap
    def heap_pull(self, trace: dict, app_dict: dict) -> None:
        r"""
        Pushes tasks from the shared memory app_dict["morpy"]["heap_shelf"]
        to the internal heap. Removes and returns the highest priority task
        from the heap.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        pulled_tasks = set()

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
            log(trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["heap_pull_start"]}\n'
                        f'{app_dict["loc"]["morpy"]["heap_pull_priority"]}: {self.curr_task["priority"]}\n'
                        f'{app_dict["loc"]["morpy"]["heap_pull_cnt"]}: {self.curr_task["counter"]}',
                        verbose=True)

        else:
            # Can not pull from an empty priority queue. Skipped...
            log(trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["heap_pull_void"]}')


    @core_wrap
    def _mp_loop(self, trace: dict, app_dict: dict) -> None:
        r"""
        Main loop of the morPy orchestrator. This loop will stay alive
        for the most part of runtime if multiprocessing is enabled.

        :param trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        terminate: bool         = False
        exit_in_progress: bool  = False
        heap_len: int           = len(self.heap) + len(app_dict["morpy"]["heap_shelf"].keys())

        while not terminate or heap_len > 0:
            # Check process queue for tasks
            if heap_len > 0:
                self.heap_pull(trace, app_dict)
                task: list | tuple | partial | None = self.curr_task["task"]
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
                            run_parallel(trace, app_dict, task=task, priority=priority, task_id=task_id)
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
                    if not app_dict["morpy"]["proc_joined"] and heap_len == 0:
                        check_child_processes(trace, app_dict, check_join=True)

            # Check exit request issued by any process
            with app_dict["morpy"].lock:
                # Check for the global exit flag
                exit_flag = app_dict["morpy"]["exit"]

            # Log the exit routine beginning only once.
            if exit_flag and not exit_in_progress:
                # Exit request detected. Termination in Progress.
                log(trace, app_dict, "exit",
                    lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_exit_request"]}')
                exit_in_progress = True

            # Finish writing logs first
            if exit_flag:
                logs_written = False if any(task[0] == -100 for task in self.heap) else True

                if logs_written:
                    with app_dict["morpy"]["proc_busy"].lock:
                        no_children = True if len(app_dict["morpy"]["proc_busy"]) < 2 else False
                    if no_children:
                        terminate = True
                        self.heap = []

                        with app_dict["morpy"]["orchestrator"].lock:
                            app_dict["morpy"]["orchestrator"]["terminate"] = terminate

                        # App terminating after exit request. No logs left from child processes.
                        log(trace, app_dict, "debug",
                            lambda: f'{app_dict["loc"]["morpy"]["MorPyOrchestrator_exit_request_complete"]}')

            # Calculate open tasks
            with app_dict["morpy"]["heap_shelf"].lock:
                heap_len = len(self.heap) + len(app_dict["morpy"]["heap_shelf"].keys())


@core_wrap
def app_run(trace: dict, app_dict: dict) -> None:
    r"""
    Sequential app init, run and exit routine.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    """

    from app.init import init
    from app.run import run
    from app.exit import finalize

    # --- APP INITIALIZATION --- #

    # Execute
    app_dict_n_shared = init(trace, app_dict)["app_dict_n_shared"]

    # Join all spawned processes before transitioning into the next phase.
    join_or_task(trace, app_dict, reset_trace=True, reset_w_prefix=f'{trace["module"]}.{trace["operation"]}')

    # Set the "initialization complete" flag
    # TODO Up until this point prints to console are mirrored on splash screen
    if isinstance(app_dict["morpy"], UltraDict):
        with app_dict["morpy"].lock:
            app_dict["morpy"]["init_complete"] = True
    else:
        app_dict["morpy"]["init_complete"] = True

    # Un-join
    with conditional_lock(app_dict["morpy"]):
        app_dict["morpy"]["proc_joined"] = False

    # --- APP RUN --- #

    app_dict_n_shared = run(trace, app_dict, app_dict_n_shared)["app_dict_n_shared"]

    # Join all spawned processes before transitioning into the next phase.
    join_or_task(trace, app_dict, reset_trace=True, reset_w_prefix=f'{trace["module"]}.{trace["operation"]}')

    # Un-join
    with conditional_lock(app_dict["morpy"]):
        app_dict["morpy"]["proc_joined"] = False

    # --- APP EXIT --- #

    # Exit the app and signal morPy to terminate
    finalize(trace, app_dict, app_dict_n_shared)

    # Join all spawned processes before transitioning into the next phase.
    join_or_task(trace, app_dict, reset_trace=True, reset_w_prefix=f'{trace["module"]}.{trace["operation"]}')

    # Signal morPy orchestrator of app termination
    if isinstance(app_dict["morpy"], UltraDict):
        with app_dict["morpy"].lock:
            app_dict["morpy"]["exit"] = True
    else:
        app_dict["morpy"]["exit"] = True


@core_wrap
def heap_shelve(trace: dict, app_dict: dict, priority: int=100, task: Callable | list | tuple=None,
                    autocorrect: bool=True, is_process: bool=True, force: bool = False, task_id: int=None) -> None:
    r"""
    Adds a task to the morPy process queue.

    :param trace: Operation credentials and tracing information
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

    :example:
        from lib.mp import heap_shelve
        task = [my_func, trace, app_dict]
        heap_shelve(trace, app_dict, priority=25, task=task)
    """

    # Check for Interrupt / exit
    stop_while_interrupt(trace, app_dict)

    if task:
        # Transform task to a list, if possible
        task = normalize_task(task)
        proc_master = app_dict["morpy"]["proc_master"]

        # Skip queuing, if in single core mode
        if not (trace["process_id"] == proc_master) or force:
            with app_dict["morpy"].lock:
                with app_dict["morpy"]["heap_shelf"].lock:
                    morpy_dict = app_dict["morpy"]

                    # Substitute UltraDict references in task to avoid recursion issues.
                    task_sanitized = substitute_ultradict_refs(trace, app_dict, task)["task_sanitized"]

                    # Check and autocorrect process priority
                    if priority < 0 and autocorrect:
                        # Invalid argument given to process queue. Autocorrected.
                        log(trace, app_dict, "debug",
                            lambda: f'{app_dict["loc"]["morpy"]["heap_shelve_prio_corr"]}\n'
                                    f'{app_dict["loc"]["morpy"]["heap_shelve_priority"]}: {priority} to 0')
                        priority = 0

                    # Pushing task to priority queue.
                    log(trace, app_dict, "debug",
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

    else:
        # Task can not be None. Skipping enqueue.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["heap_shelve_none"]}')


# Suppress linting for mandatory arguments.
# noinspection PyUnusedLocal
@core_wrap
def substitute_ultradict_refs(trace: dict, app_dict: dict, task: list) -> dict:
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

    :param trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param task: List-type task, supposedly with UltraDict references.

    :return task_sanitized: List-type task with substituted UltraDict references.
    """

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

    return {
        "task_sanitized": task_sanitized
    }


def reattach_ultradict_refs(task: list | tuple | dict | UltraDict) -> list:
    r"""
    Recursively traverse a task (which can be a list, tuple, or dict) and replace any
    placeholder tuple with the actual UltraDict instance. A placeholder tuple must have the form:

        ("__morPy_shared_ref__::{name}",
        UltraDict.shared_lock,
        UltraDict.auto_unlink,
        UltraDict.recurse)

    The UltraDict is reattached by calling its constructor with these parameters and create=False.

    :param task: Task with sanitized UltraDict references.

    :return task_recreated: Task with recreated UltraDict references.
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


@core_wrap
def run_parallel(trace: dict, app_dict: dict, task: list=None, priority: int=None, task_id: int=None) -> None:
    r"""
    Takes a task from the morPy heap, reserves a process ID, modifies the
    trace of the task and ultimately starts the parallel process.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param task: The pulled task list
    :param priority: Integer representing task priority (lower is higher priority)
    :param task_id: Value representing the unique, continuing task ID

    TODO make compatible with forking/free-threading
    """

    shelved: bool = False

    # Start preparing task for spawning process.
    log(trace, app_dict, "debug",
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
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["run_parallel_shelved"]}')
        return

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
            log(trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["run_parallel_search_iter_end"]}:\n'
                        f'{process_id=}')

            proc_master = app_dict["morpy"]["proc_master"]

            # Execute the task
            if process_id != proc_master:

                # Parallel process starting.
                log(trace, app_dict, "debug",
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
                log(trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["run_parallel_exit"]}: {process_id}')

    else:
        # Enqueue the task again to prevent data loss
        existing_id = task[1].get("task_id", None)
        heap_shelve(
            trace, app_dict, priority=priority, task=task, force=True, task_id= existing_id
        )

        # All processes busy, failed to allocate process ID. Re-queueing the task.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["run_parallel_allocate_fail"]}')


@core_wrap
def check_child_processes(trace: dict, app_dict: dict, check_join: bool = False) -> None:
    r"""
    Orchestrator routine to check on child processes and correct
    the process references in app_dict if necessary.

    This function compares the list of active child processes with the
    process references stored in app_dict["morpy"]["proc_busy"]. If a process
    is referenced but no longer active, it logs an error and removes that reference.
    It also attempts to terminate any processes that are still running but are not
    referenced in proc_busy (rogue processes).

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param check_join: If True, the orchestrator will check if all processes are
        joined. This may end processes, that could otherwise accept a shelved task.
    """

    child_processes: dict = {}
    proc_left_over: set = set()

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
                log(trace, app_dict, severity,
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
        log(trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["morpy"]["check_child_processes_rogues"]}\n'
                    f'{app_dict["loc"]["morpy"]["check_child_processes_no_rec"]}'
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
                        heap_shelve(trace, app_dict, priority=priority, task=task_recovered,
                                    task_id=task_id)
                        # A shelved task was recovered from a terminated process.
                        log(trace, app_dict, "warning",
                            lambda: f'{app_dict["loc"]["morpy"]["check_child_processes_recovery"]}'
                                    f'{roque_proc_names}')

                    proc_waiting.pop(proc_remnant_id)

    if check_join:
        with app_dict["morpy"]["heap_shelf"].lock:
            if len(app_dict["morpy"]["heap_shelf"]) > 1:
                return

        with app_dict["morpy"]["proc_waiting"].lock:
            proc_waiting = app_dict["morpy"]["proc_waiting"]

            # Return if shelved tasks exist
            for _p, _t in proc_waiting.items():
                if _t[0] is not None:
                    return

        # Have in mind, that the orchestrator is never waiting (therefore +1).
        if len(app_dict["morpy"]["proc_busy"].keys()) == (len(proc_waiting.keys()) + 1):
            app_dict["morpy"]["proc_joined"] = True

            # All child processes are joined.
            log(trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["check_child_processes_joined"]}')


@core_wrap
def join_or_task(trace: dict, app_dict: dict, reset_trace: bool = False, reset_w_prefix: str=None) -> None:
    r"""
    Join all processes orchestrated by morPy. This can not be used, to arbitrarily join processes.
    It is tailored to be used at the end of app.init, app.run and app.exit! The function is to
    join all processes of one of the steps (init - run - exit) before transitioning into the next.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param reset_trace: If True, the trace will be reset/lost.
    :param reset_w_prefix: If reset_trace is True, a custom prefix can be set in order to retain
        a customized trace.

    :example:
        join_or_task(trace, app_dict)

    TODO add idle_timeout to stop waiting for task shelving
    """

    import time

    module: str = 'lib.mp'
    operation: str = 'join_or_task(~)'
    trace: dict = morpy_fct.tracing(module, operation, trace, reset=reset_trace, reset_w_prefix=reset_w_prefix)

    my_pid: int = trace["process_id"]

    # Check for Interrupt / exit
    stop_while_interrupt(trace, app_dict)

    # Skip if run by master / single process mode
    proc_master = app_dict["morpy"]["proc_master"]
    if my_pid != proc_master:
        # Waiting for processes to finish or task to run.
        log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["join_or_task_start"]}')

        proc_joined = False
        while not proc_joined:

            # Exit if required
            with app_dict["morpy"].lock:
                exit_flag = app_dict["morpy"]["exit"]
            if exit_flag:
                child_exit_routine(trace, app_dict)
                sys.exit()

            # Wait time to avoid busy wait
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
                stop_while_interrupt(trace, app_dict)

                # Assign task ID to own trace and claim task
                trace["task_id"] = task_id
                task[1] = trace

                # Recreate UltraDict references in task and run it.
                task_recreated = reattach_ultradict_refs(task)
                execute = task_to_partial(task_recreated)
                execute()

                # Clean up
                del task
                del task_recreated

            # Check for Interrupt / exit
            stop_while_interrupt(trace, app_dict)

            # Re-/subscribe to waiting dictionary.
            with app_dict["morpy"]["proc_waiting"].lock:
                proc_waiting = app_dict["morpy"]["proc_waiting"]
                if not proc_waiting.get(my_pid, None):
                    # Add task to waiting dictionary without a shelved task.
                    proc_waiting.update({my_pid: (None, None, None)})

            # Check, if processes have been joined yet.
            with app_dict["morpy"].lock:
                proc_joined = app_dict["morpy"]["proc_joined"]


@core_wrap
def interrupt(trace: dict, app_dict: dict) -> None:
    r"""
    This function sets a global interrupt flag. Processes and threads
    will halt once they pass (the most recurring) morPy functions.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :example:
        interrupt(trace, app_dict)
    """

    # Global interrupt has been set.
    log(trace, app_dict, "warning",
        lambda: f'{app_dict["loc"]["morpy"]["interrupt_set"]}')

    if isinstance(app_dict, UltraDict):
        with app_dict["morpy"]:
            app_dict["morpy"]["interrupt"] = True
    else:
        app_dict["morpy"]["interrupt"] = True


@core_wrap
def stop_while_interrupt(trace: dict, app_dict: dict) -> None:
    r"""
    Wait until the global interrupt flag is set to False.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :example:
        stop_while_interrupt(trace, app_dict)

    TODO distribute this function throughout the framework
    """

    exit_flag: bool = False

    if app_dict["morpy"]["processes_max"] > 1:
        with app_dict["morpy"].lock:
            interrupt_flag = app_dict["morpy"]["interrupt"]

        if interrupt_flag:
            # Global interrupt. Process is waiting for release.
            log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["stop_while_interrupt"]}')

        while interrupt_flag and not exit_flag:
            time.sleep(0.05)
            with app_dict["morpy"].lock:
                interrupt_flag = app_dict["morpy"]["interrupt"]
                exit_flag = app_dict["morpy"]["exit"]

        if exit_flag:
            with app_dict["morpy"].lock:
                proc_master = app_dict["morpy"]["proc_master"]

            # If process is orchestrator, gracefully exit. Otherwise, abort task.
            if trace["process_id"] != proc_master:
                # TODO enqueue a log for "aborted task"
                # Remove own process references and exit
                child_exit_routine(trace, app_dict)
                pass


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


@core_wrap
def child_exit_routine(trace: dict, app_dict: dict | UltraDict) -> None:
    r"""
    Cleans up the registers regarding a terminating child process. This
    function also enforces the ordered locking of shared dictionaries to
    prevent deadlocks.

    :param trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    """

    try:
        # Remove own process references
        with app_dict["morpy"]["proc_available"].lock:
            with app_dict["morpy"]["proc_busy"].lock:
                # Remove from busy processes
                app_dict["morpy"]["proc_busy"].pop(trace['process_id'])
                # Add to processes available IDs (hygiene only, no other use at app exit)
                app_dict["morpy"]["proc_available"]["process_id"] = None

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


def is_udict(obj) -> bool:
    r"""
    Simple type check in the object provided. Returns True, if object is an UltraDict.

    :param obj: Any object.

    :return: True, if object is an UltraDict.
    """

    from UltraDict import UltraDict

    check: bool = False
    if isinstance(obj, UltraDict):
        check = True
    return check


def normalize_task(task: Any) -> list:
    r"""
    Converts a task defined as a partial into the list format:
        [func, *args, {**keywords}]
    If the task is already a list, it is returned unchanged.
    If the task is a tuple, it is converted to list.

    :param task: Callable, list or tuple packing the task. Formats:
        callable: partial(func, *args, **kwargs)
        list: [func, *args, **kwargs]
        tuple: (func, *args, **kwargs)

    :return task: Task packed as a list.
    """

    if isinstance(task, list):
        return task
    elif isinstance(task, tuple):
        return list(task)
    elif isinstance(task, partial):
        normalized: List[Any] = [task.func] + list(task.args)
        if task.keywords:
            normalized.append(task.keywords)
        return normalized
    else:
        # For other callables, we return them as-is.
        return task


def task_to_partial(task: List[Any]) -> Callable:
    r"""
    Convert a task list into a callable partial.

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