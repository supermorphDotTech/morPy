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
from multiprocessing import Process
from multiprocessing import active_children
from functools import partial

class cl_orchestrator:
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
        module: str = 'mp'
        operation: str = 'cl_orchestrator.__init__(~)'
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

        module: str = 'mp'
        operation: str = 'cl_orchestrator._init(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Set app termination flag
            self._terminate = False

            # Determine processes and memory to use
            self._init_processes(morpy_trace, app_dict)
            self._init_memory(morpy_trace, app_dict)
            self._init_app_dict(morpy_trace, app_dict)
            self._init_run(morpy_trace, app_dict)

            # Multiprocessing initialized.
            log_no_q(morpy_trace, app_dict, "init",
            lambda: f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_done"]}')

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
        TODO when made compatible, take care of self._run(), init.init() and common.PriorityQueue._init()
        """

        module: str = 'mp'
        operation: str = 'cl_orchestrator._init_processes(~)'
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
                    f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_not_bool"]}\n'
                    f'processes_count_absolute : {processes_count_absolute}'
                )

            # Guard for configured values in conf.py
            if isinstance(processes_absolute, int) or processes_absolute is None:
                processes_absolute = processes_absolute or system_logical_cpus
            else:
                # Value is not an integer. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_not_int"]}\n'
                    f'processes_absolute : {processes_absolute}'
                )

            # Guard for configured values in conf.py
            if isinstance(processes_relative, float) or processes_relative is None:
                processes_relative = processes_relative or 1.0
            else:
                # Value is not a float. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_not_float"]}\n'
                    f'processes_relative : {processes_relative}'
                )

            # Guard for configured values in conf.py
            if isinstance(processes_relative_math, str) or processes_relative_math is None:
                processes_relative_math = processes_relative_math or "round"
                if processes_relative_math not in ("round", "floor", "ceil"):
                    # Rounding corrected.
                    log_no_q(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_processes_rel_math_corr"]} {processes_relative_math} > round')

                    processes_relative_math = "round"
            else:
                # Value is not a string. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_not_str"]}\n'
                    f'processes_relative_math : {processes_relative_math}'
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
                        lambda: f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_err_rounding_val"]}\n{processes_relative_math=}')
                        self.processes_max = round(processes_relative * system_logical_cpus)

            # Maximum amount of parallel processes determined
            log_no_q(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_cpus_determined"]}\n'
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

        module: str = 'mp'
        operation: str = 'cl_orchestrator._init_memory(~)'
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
                # Value is not a boolean. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_not_bool"]}\n'
                    f'self.memory_min : {self.memory_min}'
                )

            # Guard for configured values in conf.py
            if isinstance(memory_count_absolute, bool) or memory_count_absolute is None:
                memory_count_absolute = memory_count_absolute or False
            else:
                # Value is not a boolean. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_not_bool"]}\n'
                    f'memory_count_absolute : {memory_count_absolute}'
                )

            # Guard for configured values in conf.py
            if isinstance(memory_absolute, int) or memory_absolute is None:
                # Change unit from MB to Byte
                memory_absolute = memory_absolute*1024*1024 if memory_absolute else sys_memory_bytes
            else:
                # Value is not an integer. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_not_int"]}\n'
                    f'memory_absolute : {memory_absolute}'
                )

            # Guard for configured values in conf.py
            if isinstance(memory_relative, float) or memory_relative is None:
                memory_relative = memory_relative or 1.0
            else:
                # Value is not a float. Check conf.py for correction.
                raise ValueError(
                    f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_not_float"]}\n'
                    f'memory_relative : {memory_relative}'
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

            # Maximum memory set.
            log_no_q(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["cl_orchestrator_init_memory_set"]}\n'
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

        module: str = 'mp'
        operation: str = 'cl_orchestrator._init_app_dict(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Initialize the total task counter
            app_dict["proc"]["morpy"]["task_counter"] = 0

            # Prepare a dictionary to reference processes
            app_dict["proc"]["morpy"]["proc_refs"] = {}

            # Get global process sets for membership testing
            processes_available = app_dict["proc"]["morpy"]["proc_available"]
            processes_busy = app_dict["proc"]["morpy"]["proc_busy"]

            p = 0
            while p < self.processes_max:
                # Check for process IDs reserved during early initialization of morPy
                if p in processes_busy:
                    pass
                elif p in processes_available:
                    pass
                else:
                    # Append to available processes
                    app_dict["proc"]["morpy"]["proc_available"].add(p)
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
        Setup attributes for cyclical orchestrator _run.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        module: str = 'mp'
        operation: str = 'cl_orchestrator._init_run(~)'
        morpy_trace_init_run = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # Set attributes for _run
            self.process_q = app_dict["proc"]["morpy"]["process_q"]
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

        module: str = 'mp'
        operation: str = 'cl_orchestrator._app_run(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            from app.init import app_init
            from app.run import app_run
            from app.exit import app_exit

            # App starting.
            log_no_q(morpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["morpy"]["cl_orchestrator_app_run_start"]}')

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

        module: str = 'mp'
        operation: str = 'cl_orchestrator._run(~)'
        # TODO Find out, why morpy_trace["process_id"] is overwritten in app trace
        # The enforced deepcopy morpy_fct.tracing() is a workaround.
        morpy_trace_app = morpy_fct.tracing(module, operation, morpy_trace)
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            # TODO provide case for 2-core mode
            #   > 1 core for orchestrator and 1 core for app, so no additional spawns
            # TODO Add logging thread

            # Start the app
            app_task = [self._app_run, morpy_trace_app, app_dict]
            app_dict["proc"]["morpy"]["process_q"].enqueue(
                morpy_trace, app_dict, priority=-1, task=app_task, autocorrect=False
            )

            if self.processes_max > 1:
                while not self._terminate:
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
            check: Indicates if the task was dequeued successfully

        :example:
            self._main_loop(morpy_trace, app_dict)
        """

        module: str = 'mp'
        operation: str = 'cl_orchestrator._main_loop(~)'
        morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

        check: bool = False

        try:
            while (not self._terminate) or (len(self.process_q.heap) > 0):
                # Check process queue for tasks
                if len(self.process_q.heap) > 0:
                    task_dqued = self.process_q.dequeue(morpy_trace, app_dict)
                    task = task_dqued["task"]
                    priority = task_dqued["priority"]
                    is_process = task_dqued["is_process"]
                    func = task[0]
                    args = task[1:]
                    # Run a new parallel process
                    if is_process:
                        app_dict["proc"]["morpy"]["proc_joined"] = False
                        run_parallel(morpy_trace, app_dict, task=task, priority=priority)
                        self._terminate = False
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
                if app_dict["global"]["morpy"]["exit"]:
                    self._terminate = True

                # Evaluate if spawned processes need to end. As long as the app is running in
                # a different process, the orchestrator will not terminate. Also, a critical exception
                # may end the app.
                if len(app_dict["proc"]["morpy"]["proc_busy"]) == 0:
                    self._terminate = True

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
def run_parallel(morpy_trace: dict, app_dict: dict, task: list=None, priority=None, task_sys_id=None) -> dict:
    r"""
    This function is takes a task from the morPy priority queue, reserves a process ID, modifies the
    morpy_trace of the task and ultimately starts the parallel process.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param task: The dequeued task list
    :param priority: Integer representing task priority (lower is higher priority)
    :param task_sys_id: System ID only for internal use. Handled by
        @process_control, not used in function call.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was dequeued successfully

    :example:
        # The priority, counter, task_sys_id and task arguments are passed directly to the
        # process_control decorator and are delivered by common.PriorityQueue.dequeue().

        dequeued = app_dict["proc"]["morpy"]["queue"].dequeue(morpy_trace, app_dict)
        priority = dequeued["priority"]
        counter = dequeued["counter"]
        task_sys_id = dequeued["task_sys_id"]
        task = dequeued["task"]
        run_parallel(morpy_trace, app_dict, task=task, priority=priority)
    """

    import lib.fct as morpy_fct

    module: str = 'mp'
    operation: str = 'run_parallel(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False
    id_check: bool = False
    id_search: int = 0
    process_id: int = -1
    id_err_avl: bool = False
    id_err_busy: bool = False
    id_err_dict: bool = False

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
        processes_max = app_dict["proc"]["morpy"]["cl_orchestrator"].processes_max

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
                processes_available = app_dict["proc"]["morpy"]["proc_available"]
                processes_busy = app_dict["proc"]["morpy"]["proc_busy"]

                process_id = min(processes_available)

                # Membership testing / avoid conflicts during process ID fetch
                if process_id in processes_available:
                    # Pop process ID from available list
                    app_dict["proc"]["morpy"]["proc_available"].remove(process_id)
                else:
                    # Process ID conflict. Possible concurrent process creation. Process creation skipped.
                    id_err_avl = True

                # Membership testing / adding process to busy
                if process_id in processes_busy:
                    # Process ID conflict. ID# seemed available, is busy. Process creation skipped.
                    id_err_busy = True
                else:
                    # Add process ID to busy list
                    app_dict["proc"]["morpy"]["proc_busy"].add(process_id)

                # Processes available / processes busy
                log_no_q(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["run_parallel_proc_avl"]}:'
                        f'{app_dict["proc"]["morpy"]["proc_available"]}\n'
                        f'{app_dict["loc"]["morpy"]["run_parallel_proc_busy"]}:'
                        f'{app_dict["proc"]["morpy"]["proc_busy"]}')

                # Process ID conflict. A process may have terminated dirty. Process creation skipped.
                if f'P{process_id}' in app_dict["proc"]["morpy"]:
                    # Refresh processes busy list
                    processes_busy = app_dict["proc"]["morpy"]["proc_busy"]
                    # Repair processes busy list, if required
                    if process_id not in processes_busy:
                        app_dict["proc"]["morpy"]["proc_busy"].add(process_id)
                    id_err_dict = True
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
                app_dict["proc"]["morpy"]["task_counter"] += 1

                # Tracing update and ID assignment for the new process
                task[1].update({"process_id" : process_id})
                task[1].update({"thread_id" : 0})
                task[1].update({"task_id" : app_dict["proc"]["morpy"]["task_counter"]})

                # Remove app_dict from the task to prevent pickling external to UltraDict
                task[2] = {}

                # Run the task
                if task is not None:
                    # Check for remnants of old process, prevent collisions due to shelving
                    watcher(morpy_trace, app_dict, task, single_check=True)

                    p = Process(target=partial(spawn, task))
                    p.start()

                    # Create references to the process
                    app_dict["proc"]["morpy"]["proc_refs"].update({f'{process_id}': p.name})

                    # Enqueue a process watcher
                    process_watcher = (watcher, morpy_trace, app_dict, task)
                    app_dict["proc"]["morpy"]["process_q"].enqueue(
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
                # [CONDITIONAL] Process ID conflict. A process may have terminated dirty. Process creation skipped.
                message = f'{app_dict["loc"]["morpy"]["run_parallel_id_abort"]}'

                if id_err_avl or id_err_busy or id_err_dict:
                    message = f'{message}\n{app_dict["loc"]["morpy"]["run_parallel_issues"]}'
                    if id_err_avl:
                        message = f'{message}\n{app_dict["loc"]["morpy"]["run_parallel_id_err_avl"]}'
                    elif id_err_busy:
                        message = f'{message}\n{app_dict["loc"]["morpy"]["run_parallel_id_err_busy"]}'
                    elif id_err_dict:
                        message = f'{message}\n{app_dict["loc"]["morpy"]["run_parallel_id_err_dict"]}'
                    raise RuntimeError(message)

                # Self repair of available and busy process sets
                # Update set for processes available
                processes_available = app_dict["proc"]["morpy"]["proc_available"]
                for p_avl in processes_available:
                    if f'P{p_avl}' in app_dict["proc"]["morpy"]:
                        app_dict["proc"]["morpy"]["proc_available"].pop(p_avl)

                # Update set for processes busy
                processes_busy = app_dict["proc"]["morpy"]["processes_busy"]
                for p_busy in processes_busy:
                    if f'P{p_avl}' not in app_dict["proc"]["morpy"]:
                        app_dict["proc"]["morpy"]["p_busy"].pop(p_busy)

                # Delete process remnants in app_dict
                for p_app in app_dict["proc"]["app"]:
                    if p_app not in app_dict["proc"]["morpy"]:
                        # Process remnant found. Cleaning up after supposed process crash.
                        log_no_q(morpy_trace, app_dict, "warning",
                        lambda: f'{app_dict["loc"]["morpy"]["run_parallel_clean_up_remnants"]}\n'
                                f'app_dict[proc][app][P{e}]')
                        del app_dict["proc"]["app"][p_app]

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
        check: Indicates if the task was dequeued successfully
        process_partial: Process to be spawned, packed with partial

    :example:
        dequeued = app_dict["proc"]["morpy"]["queue"].dequeue(morpy_trace, app_dict)
        task = dequeued["task"]
        p = Process(target=spawn, args=task,)
        p.start()
    """

    from lib.init import build_app_dict

    module: str = 'lib.mp'
    morpy_trace: dict = None
    app_dict: dict = None

    try:
        morpy_trace = task[1]
        app_dict = build_app_dict(morpy_trace)

        # Assign referenced app_dict to task (process) and run it
        task[2] = app_dict
        func, *args = task
        result = func(*args)

        # Remove own process reference
        app_dict["proc"]["morpy"]["proc_refs"].pop(morpy_trace['process_id'], None)
        app_dict["proc"]["morpy"]["proc_busy"].remove(morpy_trace['process_id'])

    except Exception as e:
        # Remove own process reference
        try:
            app_dict["proc"]["morpy"]["proc_refs"].pop(morpy_trace['process_id'], None)
            app_dict["proc"]["morpy"]["proc_busy"].remove(morpy_trace['process_id'])
        except:
            pass

        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

@metrics
def watcher(morpy_trace: dict, app_dict: dict, task: tuple, single_check: bool=False) -> dict:
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
        app_dict["proc"]["morpy"]["process_q"].enqueue(
            morpy_trace, app_dict, priority=priority, task=process_watcher, autocorrect=False, is_process=False
        )

    :example 2:
        watcher(morpy_trace, app_dict, task, single_check=True)
    """

    import lib.fct as morpy_fct
    import copy
    from multiprocessing import active_children

    morpy_trace_in = copy.deepcopy(morpy_trace)
    module: str = 'mp'
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
        if f'{process_id}' in app_dict["proc"]["morpy"]["proc_refs"].keys():
            p_name = app_dict["proc"]["morpy"]["proc_refs"][f'{process_id}']

            for p in active:
                if p.name == p_name:
                    is_active = True
                    break

            # If process is still alive enqueue watcher again
            if is_active:
                # Process Watcher: Process still alive.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["watcher_is_alive"]}:\n'
                        f'{app_dict["proc"]["morpy"]["proc_refs"]}',
                        verbose=True)

                if not single_check:
                    task = (watcher, morpy_trace_in, app_dict, task)
                    app_dict["proc"]["morpy"]["process_q"].enqueue(
                        morpy_trace, app_dict, priority=priority, task=task, autocorrect=False, is_process=False
                    )

            # Clean up process references, if process is not running.
            else:
                # Process Watcher: Process ended, cleaning up.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["watcher_end"]}:\n'
                        f'{app_dict["proc"]["morpy"]["proc_refs"]}',
                        verbose=True)

                # Cleanup app_dict
                if process_id not in app_dict["proc"]["morpy"]["proc_available"]:
                    app_dict["proc"]["morpy"]["proc_available"].add(process_id)
                if process_id in app_dict["proc"]["morpy"]["proc_busy"]:
                    app_dict["proc"]["morpy"]["proc_busy"].remove(process_id)
                app_dict["proc"]["morpy"]["proc_refs"].pop(f'{process_id}', None)

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
        check: Indicates if the task was dequeued successfully

    :example:
        task = (join_all_by_master, morpy_trace, app_dict, child_pid)
        app_dict["proc"]["morpy"]["process_q"].enqueue(
            morpy_trace, app_dict, priority=0, task=task, autocorrect=False, is_process=False
    """

    module: str = 'mp'
    operation: str = 'join_all_by_master(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # Make a copy of the process references to avoid race conditions.
        proc_refs: dict = copy.deepcopy(app_dict["proc"]["morpy"]["proc_refs"])

        # Remove child and master process references from pool
        proc_refs.pop(str(child_pid), None)
        proc_refs.pop(str(morpy_trace["process_id"]), None)  # Should not be in the pool

        if len(proc_refs.keys()) > 0:
            # Waiting for processes to finish before transitioning app phase.
            log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["join_all_by_master_start"]}:\n'
                        f'{app_dict["proc"]["morpy"]["proc_refs"]}')

            from multiprocessing import active_children

            # Loop until all known process references have been joined.
            for p_id, p_name in proc_refs:
                for proc in active_children():
                    if proc.name == p_name:
                        proc.join()

                proc_refs.pop(p_id, None)

        # Signal all processes joined
        app_dict["proc"]["morpy"]["proc_joined"] = True

    except Exception as e:
        from lib.exceptions import MorPyException
        raise MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")

    finally:
        return {
            'morpy_trace': morpy_trace,
            'check': check,
        }

@metrics
def join_processes_for_transition(morpy_trace: dict, app_dict: dict, child_pid: int | str = None) -> dict:
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
        check: Indicates if the task was dequeued successfully

    :example:
        join_processes_for_transition(morpy_trace, app_dict)
    """

    import time

    module: str = 'mp'
    operation: str = 'join_processes_for_transition(~)'
    morpy_trace: dict = morpy_fct.tracing(module, operation, morpy_trace)

    check: bool = False

    try:
        # Check, if join is necessary
        if not app_dict["proc"]["morpy"]["proc_joined"]:
            task = (join_all_by_master, morpy_trace, app_dict, child_pid)
            app_dict["proc"]["morpy"]["process_q"].enqueue(
                morpy_trace, app_dict, priority=0, task=task, autocorrect=False, is_process=False
            )

        # Wait for processes to join
        while not app_dict["proc"]["morpy"]["proc_joined"]:
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
        check: Indicates if the task was dequeued successfully

    :example:
        interrupt(morpy_trace, app_dict)


    TODO finish this function
    """

    module: str = 'mp'
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