r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module delivers routines to handle Multithreading and
            acts as a fork. See the mpy_param.py module to adjust how
            multithreading will be utilized. To add tasks to the queue,
            call the priority queue instance with

                [mt.]mpy_thread_queue(morpy_trace, app_dict, name, priority, task)

            A task represents a worker or thread in use. In order to make
            your program multithreading enabled, you need to divide it
            into several tasks that in return will be worked off by as
            many workers as available to runtime.
"""

import lib.fct as morpy_fct
import lib.common as common
from lib.decorators import log

import sys
import threading
import math
from heapq import heappop, heappush
from itertools import count

def mpy_thread_queue(morpy_trace: dict, app_dict: dict, name: str, priority: int, task: str) -> dict:

    r"""
    Handles the task queue (`mt_priority_queue` instance of `cl_priority_queue`)
    for this framework. It simplifies multithreaded programming by allowing the developer
    to fill the queue with tasks and configure threading parameters. In single-threaded
    mode, tasks are executed sequentially while still prioritizing based on the queue.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param name: Name of the task/thread.
    :param priority: Integer value indicating the task's priority. Lower numbers indicate
                     higher priority. Avoid using negative integers.
    :param task: String representing the statement, function, or class/module to be executed
                 by the thread. This string is executed using the `exec()` function, and
                 any required module must be properly referenced. Example:
                     task = 'app_module1.app_function1([morpy_trace], [app_dict], [...], [log])'

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        mpy_thread_queue(morpy_trace, app_dict, "Task1", 10, "module.function(args)")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'mt'
    operation = 'thread_queue(~)'
    morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

    check = False
    name = f'{name}'
    task = f'{task}'
    thr_available = app_dict["mt_max_threads"]

    try:

        # Check for multithreading / Fallback to ST mode
        if app_dict["mt_enabled"]:
            # Enqueue a new task
            try:
                # Check for the priority and correct it, if necessary.
                priority = prio_correction(morpy_trace, app_dict, priority, task)["priority"]

                # Enqueueing task.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["thread_queue_enqueue"]}\n'
                        f'{app_dict["loc"]["morpy"]["thread_queue_task"]}: {task}\n'
                        f'{app_dict["loc"]["morpy"]["thread_queue_priority"]}: {priority}')

                app_dict["mt_priority_queue"].enqueue(morpy_trace, app_dict, name, priority, task)

            except Exception as e:
                log(morpy_trace, app_dict, "critical",
                lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{type(e).__name__}: {e}')

            # Start a thread, if there are threads available. If all threads are already in use, skip
            # this step as the threads will keep pulling tasks.
            try:

                # Checking threads availability.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["thread_queue_dbg_threads_available"]}\n'
                        f'{app_dict["loc"]["morpy"]["thread_queue_dbg_threads_max"]}: {app_dict["mt_max_threads"]}')

                # Check for available threads by counting the listed thread ID's and compare them
                # to the maximum amount of threads available.
                if app_dict["mt_threads_id_lst"]:
                    if len(app_dict["mt_threads_id_lst"]) < thr_available:

                        # Start a thread.
                        worker = cl_thread(morpy_trace, app_dict)
                        worker.start()

                        # Append worker to a list of threads. It is mostly used to join threads later.
                        app_dict["workers_running"].append(worker)

                        # Task successfully enqueued. Thread created.
                        log(morpy_trace, app_dict, "debug",
                        lambda: f'{app_dict["loc"]["morpy"]["thread_queue_dbg_enqueue_done"]}\n'
                                f'{app_dict["loc"]["morpy"]["thread_queue_dbg_threads_used"]}: {len(app_dict["mt_threads_id_lst"])}\n'
                                f'{app_dict["loc"]["morpy"]["thread_queue_dbg_threads_max"]}: {app_dict["mt_max_threads"]}')

                    else:
                        # No free thread available. Skipping thread invoke.
                        log(morpy_trace, app_dict, "debug",
                        lambda: f'{app_dict["loc"]["morpy"]["thread_queue_dbg_thread_skip"]}\n'
                                f'{app_dict["loc"]["morpy"]["thread_queue_dbg_threads_used"]}: {len(app_dict["mt_threads_id_lst"])}\n'
                                f'{app_dict["loc"]["morpy"]["thread_queue_dbg_threads_max"]}: {app_dict["mt_max_threads"]}')

                else:
                    # Start a thread.
                    worker = cl_thread(morpy_trace, app_dict)
                    worker.start()

                    # Append worker to a list of threads. It is mostly used to join threads later.
                    app_dict["workers_running"].append(worker)

                    # New Thread ID list created. Task successfully enqueued.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{app_dict["loc"]["morpy"]["thread_queue_dbg_enq_new_done"]}\n'
                            f'{app_dict["loc"]["morpy"]["thread_queue_dbg_threads_used"]}: {len(app_dict["mt_threads_id_lst"])}\n'
                            f'{app_dict["loc"]["morpy"]["thread_queue_dbg_threads_max"]}: {app_dict["mt_max_threads"]}')

                check = True

            except Exception as e:
                log(morpy_trace, app_dict, "critical",
                lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                        f'{type(e).__name__}: {e}')

        # Run fallback mode - single threaded
        else:
            exec(thread_imports(morpy_trace, app_dict, task)["imp_order"])
            exec(task)

    except Exception as e:
        log(morpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check
        }

def mpy_threads_joinall(morpy_trace: dict, app_dict: dict) -> dict:

    r"""
    Waits for all threads to complete execution before resuming code execution.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        mpy_threads_joinall(morpy_trace, app_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'mt'
    operation = 'threads_joinall(~)'
    morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

    check = False

    try:
        # Waiting for all threads to finish up their work.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["threads_joinall_start"]}\n'
                      f'{app_dict["loc"]["morpy"]["threads_joinall_eval"]}: {app_dict["workers_running"]}')

        for thread in app_dict["workers_running"]:
            thread.join()

        # Clear the list of invoked threads
        app_dict["workers_running"] = []

        # All threads/tasks finished.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["threads_joinall_end"]}\n'
                f'{app_dict["loc"]["morpy"]["threads_joinall_eval"]}: {app_dict["workers_running"]}')

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check
        }

def mt_abort(morpy_trace: dict, app_dict: dict) -> dict:

    r"""
    Aborts all pending tasks. The priority queue remains intact, allowing new
    threads to potentially pick up the aborted tasks.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        mt_abort(morpy_trace, app_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'mt'
    operation = 'mt_abort(~)'
    morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

    check = False

    try:
        # Waiting for all threads to finish up their work.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["mt_abort_start"]}')

        # Set the threads exit flag
        app_dict["mt_exit"] = True

        # Wait for all threads to finish up
        mpy_threads_joinall(morpy_trace, app_dict)

        # Reset the threads exit flag
        app_dict["mt_exit"] = False

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check
        }

class cl_priority_queue(object):

    r"""
    Defines the globally used priority queue for this framework. Supports queue
    nesting by instantiating additional `PriorityQueue` objects with unique names.
    Workforce distribution among nested queues can vary based on application needs.
    However, the main instance used throughout this framework should not be altered.
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, name: str) -> None:

        r"""
        Initializes the basic parameters of the PriorityQueue. Tasks are fetched
        from the highest priority set available, with the highest priority determined
        by the lowest integer. Tasks within the same priority level are returned in
        the order they were added (FIFO).

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param name: Name of the PriorityQueue instance.

        :return: None

        :example:
            queue = cl_priority_queue(morpy_trace, app_dict, "MainQueue")
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module = 'mt'
        operation = 'cl_priority_queue.__init__(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        name = f'{name}'

        try:
            # Define the attributes of the class
            self.name = name
            self.elements = []
            self.counter = count()

            # Create a reference to the priority queue
            app_dict["mt_priority_queue"] = self

            # Priority queue initialized.
            log(morpy_trace, app_dict, "init",
            lambda: f'{app_dict["loc"]["morpy"]["cl_priority_queue_init_done"]}\n'
                    f'{app_dict["loc"]["morpy"]["cl_priority_queue_name"]}: {self.name}')

        except Exception as e:
            log(morpy_trace, app_dict, "critical",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

    def enqueue(self, morpy_trace: dict, app_dict: dict, name: str, priority: int, task: str) -> dict:

        r"""
        Adds items/tasks to the `cl_priority_queue`.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param name: Name of the task/thread.
        :param priority: Integer value indicating the task's priority. Lower numbers indicate
                         higher priority. Avoid using negative integers.
        :param task: String representing the statement, function, or class/module to be executed
                     by the thread. This string is executed using the `exec()` function.

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).

        :example:
            queue.enqueue(morpy_trace, app_dict, "Task1", 10, "module.function(args)")
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module = 'mt'
        operation = 'cl_priority_queue.enqueue(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False
        name = f'{name}'
        task = f'{task}'

        try:
            # Pushing task to priority queue.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["cl_priority_queue_enqueue_start"]}\n'
                    f'{app_dict["loc"]["morpy"]["cl_priority_queue_name"]}: {self.name}\n'
                    f'{app_dict["loc"]["morpy"]["cl_priority_queue_enqueue_priority"]}: {priority}\n'
                    f'{app_dict["loc"]["morpy"]["cl_priority_queue_enqueue_task"]}: {task}')

            # Define the task to be queued
            task_qed = (name, -priority, next(self.counter), task)

            # Push the task to the actual heap
            heappush(self.elements, task_qed)

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "critical",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

        return{
            'morpy_trace' : morpy_trace,
            'check' : check
            }

    def dequeue(self, morpy_trace: dict, app_dict: dict) -> dict:

        r"""
        Pops a task from the `cl_priority_queue` and returns it for execution.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).
            task_dqed: List element of the dequeued task to execute next:
                [0] name - Name of the task/thread.
                [1] priority - Priority of the task (lower numbers indicate higher priority).
                [2] counter - Internal counter to ensure FIFO order for tasks with the same priority.
                [3] task - The task statement/function to be executed.

        :example:
            dequeued_task = queue.dequeue(morpy_trace, app_dict)
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module = 'mt'
        operation = 'cl_priority_queue.dequeue(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:

            # Wait for an interrupt to end
            while app_dict["global"]["morpy"]["interrupt"] == True:
                pass

            # Return the highest priority and oldest task from priority queue
            task_dqed = heappop(self.elements)

            # Retrieve the first element of the queue indicating the name
            name = task_dqed[0]

            # Retrieve the second element of the queue indicating the priority
            priority = task_dqed[1]

            # Retrieve the third element of the queue indicating the age (counter)
            counter = task_dqed[2]

            # Retrieve the fourth element of the queue indicating the actual task
            task = task_dqed[3]

            # Pushing task to priority queue.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["cl_priority_queue_dequeue_start"]}\n'
                    f'{app_dict["loc"]["morpy"]["cl_priority_queue_name"]}: {self.name}\n'
                    f'{app_dict["loc"]["morpy"]["cl_priority_queue_dequeue_name"]}: {name}\n'
                    f'{app_dict["loc"]["morpy"]["cl_priority_queue_dequeue_priority"]}: {priority}\n'
                    f'{app_dict["loc"]["morpy"]["cl_priority_queue_dequeue_cnt"]}: {counter}\n'
                    f'{app_dict["loc"]["morpy"]["cl_priority_queue_dequeue_task"]}: {task}')

            check = False

        except Exception as e:
            log(morpy_trace, app_dict, "critical",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            'task_dqed' : task_dqed
            }

def mt_init(morpy_trace: dict, app_dict: dict) -> dict:

    r"""
    Initializes multi-threading (MT) for the application. If MT is disabled,
    the program defaults to single-threaded (ST) execution. This function
    determines all relevant parameters, such as the number of threads to run.
    For additional parameterization and details, see the `mpy_param.py` module.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        mt_init(morpy_trace, app_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'mt'
    operation = 'mt_init(~)'
    morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

    check = False
    sys_threads = app_dict["sys"]["threads"] # Total threads available to the system

    try:
        # Initialize threading exit flag
        app_dict["mt_exit"] = False

        # Initialize total thread counter to be used as a unique task ID
        app_dict["mt_tasks_cnt"] = 0

        # Initialize list for running workers
        app_dict["workers_running"] = []

        # Initialize the interrupt flag
        app_dict["global"]["morpy"]["interrupt"] = False

        # Evaluate, if MT is enabled
        if app_dict["conf"]["mt_enabled"]:

            # Determine the maximum thread count available for runtime
            # Absolute determination
            if app_dict["conf"]["mt_max_threads_set_abs"]:
                max_threads = app_dict["conf"]["mt_max_threads_cnt_abs"]

            # Determine the maximum thread count available for runtime
            # Relative determination
            else:

                max_threads = sys_threads * app_dict["conf"]["mt_max_threads_cnt_abs"]

                # Round down
                if app_dict["conf"]["mt_max_threads_rel_floor"]:
                    max_threads = math.floor(max_threads)
                # Round up
                else:
                    max_threads = math.ceil(max_threads)

            # Log preparation.
            # Multithreading enabled.
            mt_init_message = f'{app_dict["loc"]["morpy"]["mt_init_done"]} {app_dict["loc"]["morpy"]["mt_init_enabled_yes"]}'

        # Fallback to ST, if MT is disabled
        else:

            max_threads = 1

            # Log preparation.
            # Multithreading disabled. Fallback to single threaded mode.
            mt_init_message = f'{app_dict["loc"]["morpy"]["mt_init_done"]} {app_dict["loc"]["morpy"]["mt_init_enabled_no"]}'

        # Correct the maximum thread count, if architecturally there are less available.
        if sys_threads < max_threads:

            max_threads = sys_threads

        # Set the maximum thread count for runtime in app_dict
        app_dict["mt_max_threads"] = max_threads

        # Create an empty list of thread IDs
        app_dict["mt_threads_id_lst"] = []

        # Multithreading initialized.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{mt_init_message}\n'
                f'{app_dict["loc"]["morpy"]["mt_init_thr_available"]}: {sys_threads}\n'
                f'{app_dict["loc"]["morpy"]["mt_init_thr_max"]}: {max_threads}')

        # Initialize and create the queue instance for this frameworks runtime
        cl_priority_queue(morpy_trace, app_dict, 'mtPriorityQueue')

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check
        }

class cl_thread(threading.Thread):

    r"""
    A subclass of the `threading.Thread` class. This class supports all methods
    of the `threading` module while being managed independently by this framework.
    """

    def __init__(self, morpy_trace: dict, app_dict: dict) -> None:

        r"""
        Initializes the basic parameters of a `cl_thread` instance.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.

        :return: None

        :example:
            thread_instance = cl_thread(morpy_trace, app_dict)
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module = 'mt'
        operation = 'cl_thread.__init__(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        try:
            # A worker thread is being created.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["cl_thread_init_start"]}')

            # Define the attributes of the class
            self.ID = thread_id(morpy_trace, app_dict)["thread_id"]
            self.name = None
            self.trace = morpy_trace
            self.app_dict = app_dict
            self.log = morpy_trace["log_enable"]

            # Increment the task counter
            app_dict["mt_tasks_cnt"] += 1

            # Invoke an instance of threading.Thread
            threading.Thread.__init__(self)

            # Lock the thread
            self.lock = threading.Lock()

            # Worker thread created. ID reserved.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["cl_thread_init_done"]}\n'
                    f'{app_dict["loc"]["morpy"]["cl_thread_id"]}: {self.ID}\n'
                    f'{app_dict["loc"]["morpy"]["cl_thread_lock"]}: {self.lock}')

        except Exception as e:
            log(morpy_trace, app_dict, "critical",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

    def run(self) -> dict:

        r"""
        Executes tasks handed to the thread. Continually fetches tasks from the
        priority queue until it is empty.

        :param: None

        :return: dict
            check: Indicates whether the function executed successfully (True/False).

        :example:
            thread_instance.run()
        """

        # Define operation credentials (see init.init_cred() for all dict keys)
        module = 'mt'
        operation = 'cl_thread.run(~)'
        morpy_trace = morpy_fct.tracing(module, operation, self.trace)
        log_enable = morpy_trace["log_enable"]

        check = False
        task_ID = -1
        task = None

        try:
            # Acquire a thread lock - reserve a worker for the task
            self.lock.acquire()

            # A task is starting. Thread has been locked.
            log(self.morpy_trace, self.app_dict, "debug",
            lambda: f'{self.app_dict["cl_thread_run_start"]}\n'
                    f'ID: {self.ID}\n'
                    f'{self.app_dict["cl_thread_lock"]}: {self.lock}')

            # Fetch a task as long as the queue is not empty.
            while len(self.app_dict["mt_priority_queue"].elements) > 0 and \
                not self.app_dict["mt_exit"]:

                # Wait for an interrupt before fetching a task
                while self.app_dict["global"]["morpy"]["interrupt"]:
                    pass

                task_dqed = self.app_dict["mt_priority_queue"].dequeue(morpy_trace, self.app_dict)["task_dqed"]

                # Fetching the name of the task to identify the thread with it.
                self.name = task_dqed[0]

                # Defining the thread specific trace
                morpy_trace["thread_id"] = self.ID

                # Fetching the task.
                task = task_dqed[3]

                # Disable logging for the next segment
                morpy_trace["log_enable"] = False

                # Exchange the traceback of the task from morpy_trace to morpy_trace
                task = msg.log_regex_replace(morpy_trace, self.app_dict, task, 'morpy_trace', 'morpy_trace')

                # Exchange the app_dict reference of the task
                task = msg.log_regex_replace(morpy_trace, self.app_dict, task, 'app_dict', 'self.app_dict')

                # Exchange the log reference of the task
                task = msg.log_regex_replace(morpy_trace, self.app_dict, task, 'log', 'self.log')

                # Reset logging for the next segment
                morpy_trace["log_enable"] = log_enable

                # Count the tasks invoked during runtime
                task_ID = self.app_dict["mt_tasks_cnt"] + 1

                # Fetched a new task. Thread renamed with the task name.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{self.app_dict["cl_thread_run_task_fetched"]}\n'
                        f'ID: {self.ID}\n'
                        f'{self.app_dict["cl_thread_name"]}: {self.name}\n'
                        f'{self.app_dict["cl_thread_prio"]}: {task_dqed[1]}\n'
                        f'{self.app_dict["cl_thread_run_tasks_total"]}: {task_ID}\n'
                        f'{self.app_dict["cl_thread_run_task"]}: {task}')

                # Import a module, if necessary for execution
                imp_eval = thread_imports(morpy_trace, self.app_dict, task)

                # Evaluate the necessity to import a module
                imp_true = imp_eval["imp_true"]

                if imp_true:

                    imp_order = imp_eval["imp_order"]
                    exec(imp_order)

                    # Modules were imported.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{self.app_dict["cl_thread_run_modules"]}\n'
                            f'ID: {self.ID}\n'
                            f'{self.app_dict["cl_thread_name"]}: {self.name}\n'
                            f'imp_true: {imp_true}\n'
                            f'imp_order: {imp_order}')

                else:
                    # Checked for modules to be imported.
                    log(morpy_trace, app_dict, "debug",
                    lambda: f'{self.app_dict["cl_thread_run_nomodules"]}\n'
                                  f'ID: {self.ID}\n'
                                  f'{self.app_dict["cl_thread_name"]}: {self.name}\n'
                                  f'imp_true: {imp_true}')

                # Execute the task
                exec(task)

            # Clear the thread ID from the regarding list for another task to get started (if any).
            self.app_dict["mt_threads_id_lst"].remove(self.ID)

            # Release the thread lock - set the worker available again
            self.lock.release()

            # Task ended.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{self.app_dict["cl_thread_run_end"]}\n'
                          f'ID: {self.ID}\n'
                          f'{self.app_dict["cl_thread_name"]}: {self.name}')

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "critical",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

        return{
            'morpy_trace' : morpy_trace,
            'check' : check
            }

def prio_correction(morpy_trace: dict, app_dict: dict, priority: int, task: str) -> dict:

    r"""
    Checks the plausibility of given task priorities. Any priority smaller than
    10 will be set to 10, except for morPy pre-configured modules, which handle
    priorities from 0 to 9.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param priority: Integer value indicating the priority of the given task.
                     Lower numbers indicate higher priority. Negative integers should be avoided.
    :param task: String representing the statement, function, or class/module to be executed
                 by the thread. This string is executed using the `exec()` function.
                 Example:
                     task = 'app_module1.app_function1([morpy_trace], [app_dict], [...], [log])'

    :return: dict
        check: Indicates whether the function executed successfully (True/False).
        priority: Corrected integer value for the task's priority.

    :example:
        result = prio_correction(morpy_trace, app_dict, 5, "module.function(args)")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'mt'
    operation = 'prio_correction(~)'
    morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

    # Preparing parameters
    check = False
    prio_in = priority
    task = f'{task}'
    prio_trusted = False
    prio_module_lst = ('msg')

    try:
        # Split the task and extract the module
        task_split = common.regex_split(morpy_trace, app_dict, task, r'.')
        module = task_split[0]

        for mod in prio_module_lst:

            if module == mod:

                prio_trusted = True
                break

        # Evaluate the priority
        if prio_in < 10:

            if not prio_trusted:

                priority = 10

                # The priority of a task has been corrected.
                log(morpy_trace, app_dict, "warning",
                lambda: f'{app_dict["loc"]["morpy"]["prio_correction_warn"]}\n'
                        f'{app_dict["loc"]["morpy"]["prio_correction_prio_in"]}: {prio_in}\n'
                        f'{app_dict["loc"]["morpy"]["prio_correction_prio_out"]}: {priority}')

            else:
                if prio_in < 0:

                    priority = 0

                    # The priority of a morPy-task has been corrected.
                    log(morpy_trace, app_dict, "error",
                    lambda: f'{app_dict["loc"]["morpy"]["prio_correction_err"]}\n'
                            f'{app_dict["loc"]["morpy"]["prio_correction_prio_in"]}: {prio_in}\n'
                            f'{app_dict["loc"]["morpy"]["prio_correction_prio_out"]}: {priority}')

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'priority' : priority
        }

def thread_id(morpy_trace: dict, app_dict: dict) -> dict:

    r"""
    Determines the ID of the calling thread. The ID is an integer value, where
    the highest possible value corresponds to the maximum threads available.
    Unlike the thread name, the ID is set automatically and does not represent
    the architectural thread ID determined by the operating system.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.

    :return: dict
        check: Indicates whether the function executed successfully (True/False).
        thread_id: The ID of the calling thread.

    :example:
        result = thread_id(morpy_trace, app_dict)
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'mt'
    operation = 'thread_id(~)'
    morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

    check = False
    max_threads = app_dict["mt_max_threads"]
    thread_id = 0
    threads_used = 0

    try:
        # Reserving an ID for a new thread/task.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["thread_id_init"]}\n'
                f'{app_dict["loc"]["morpy"]["mt_init_thr_max"]}: {max_threads}')

        # Check, if a list of threads exists. If not, thread_id = 0.
        if app_dict["mt_threads_id_lst"]:

            # Get the amount of actively used threads
            threads_used = len(app_dict["mt_threads_id_lst"])

            # Sort the list of taken thread IDs
            app_dict["mt_threads_id_lst"].sort()

            i = 0

            # Check, if the actual ID is already reserved
            for reserved_id in app_dict["mt_threads_id_lst"]:

                # Check, if a thread ID "reserved_id - 1" exists. If not, free thread ID number is found.
                if reserved_id - app_dict["mt_threads_id_lst"][i-1] > 1:
                    thread_id = reserved_id - 1
                    break
                else:
                    i += 1
                    pass

            # No gap in the thread ID list found. Adding 1 to the last reserved thread ID.
            else: thread_id = reserved_id + 1

            # Thread ID available. Exit loop and reserve ID for thread/task.
            app_dict["mt_threads_id_lst"].append(thread_id)

            if thread_id > app_dict["mt_max_threads"]:

                # Raise an error, if the thread ID is greater than the maximum threads utilized.
                # Overflow in thread ID list. ID exceeds maximum threads utilized.
                log(morpy_trace, app_dict, "error",
                lambda: f'{app_dict["loc"]["morpy"]["thread_id_err"]}\n'
                        f'{app_dict["loc"]["morpy"]["mt_init_thr_max"]}: {max_threads}\n'
                        f'{app_dict["loc"]["morpy"]["mt_init_thr_available"]}: {max_threads - threads_used}')

        else:
            app_dict["mt_threads_id_lst"].append(thread_id)

        # Create a log
        # Reserved an ID for a new thread/task.
        log(morpy_trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["thread_id_done"]}\n'
                f'{app_dict["loc"]["morpy"]["mt_init_thr_max"]}: {max_threads}\n'
                f'{app_dict["loc"]["morpy"]["mt_init_thr_available"]}: {max_threads - threads_used}\n'
                f'{app_dict["loc"]["morpy"]["cl_thread_id"]}: {thread_id}')

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'thread_id' : thread_id
        }

def thread_imports(morpy_trace: dict, app_dict: dict, task: str) -> dict:

    r"""
    Determines whether a module needs to be imported when starting a task within
    a thread, using regular expressions.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param task: String representing the statement, function, or class/module to be run
                 by the thread. This string is executed using the `exec()` function.

    :return: dict
        check: Indicates whether the function executed successfully (True/False).
        imp_true: Boolean indicating if a module needs to be imported.
        imp_order: Statement to be executed by the thread, including the import
                   order or an empty string if no import is required.

    :example:
        result = thread_imports(morpy_trace, app_dict, "module.function(args)")
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'mt'
    operation = 'thread_imports(~)'
    morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

    # Preparing parameters
    check = False
    imp_true = False
    imp_order = ''

    try:
        split_test = task.find('.')

        # Only search for module imports, if a '.' was found in the task
        if split_test >= 0:

            # Split the task and extract the module
            task_split = common.regex_split(morpy_trace, app_dict, task, r'.')
            module = task_split[0]

            # Task split to identify module imports.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["thread_imports_start"]}\n'
                    f'module: {module}')

            # Evaluate the existence of the extracted module and create a statement
            try:
                # Create import order
                imp_order = f'import {module}'

                # Evaluate by execution
                exec(imp_order)

                # Set module import true if it was found
                imp_true = True

                # The calling thread imported a module.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["thread_imports_yes"]}\n'
                        f'module: {module}\n'
                        f'imp_order: {imp_order}')

            # Overwrite the import order, if the module was not found
            except ImportError or ModuleNotFoundError:

                imp_order = ''

                # No module got imported by the calling thread.
                log(morpy_trace, app_dict, "debug",
                lambda: f'{app_dict["loc"]["morpy"]["thread_imports_no"]}\n'
                        f'imp_order: {imp_order}')

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'imp_true' : imp_true,
        'imp_order' : imp_order
        }