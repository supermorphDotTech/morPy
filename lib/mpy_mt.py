"""
Author:     Bastian Neuwirth
Date:       12.10.2022
Version:    0.1
Descr.:     This module delivers routines to handle Multithreading and
            acts as a fork. See the mpy_param.py module to adjust how
            multithreading will be utilized. To add tasks to the queue,
            call the priority queue instance with

                [mpy_mt.]mpy_thread_queue(mpy_trace, prj_dict, name, priority, task)

            A task represents a worker or thread in use. In order to make
            your program multithreading enabled, you need to divide it
            into several tasks that in return will be worked off by as
            many workers as available to runtime.
"""

import threading
from heapq import heappop, heappush
from itertools import count

def mpy_thread_queue(mpy_trace, prj_dict, name, priority, task):

    """ This function handles the task queue (instance 'mpy_PriorityQueue' of cl_mtPriorityQueue)
        of this framework. Its main purpose is to provide an easy handling of multithreaded
        programming in the way, that the developer just needs to fill the queue with tasks
        and tailor the multithreading parameters to the projects needs. However, when being
        bound to single threaded execution the queue will just execute sequentially, while
        prioritizing the tasks.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        name - Name of the task/thread.
        priority - Integer value. Sets the priority of the given task. Lower numbers indicate
                   a higher priority. Negative integers should be avoided.
        task - Statement, function or class/module to be run by the thread. A string
               is expected and will be executed via the exec()-function. The module has
               got to be referenced (if any) in order to work. Example:

                   task = 'prj_module1.prj_function1([mpy_trace], [prj_dict], [...], [log])'
    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_fct, mpy_msg
    import sys, gc

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_mt'
    operation = 'mpy_thread_queue(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False
    name = str(name)
    task = str(task)
    thr_available = prj_dict['mt_max_threads']

#   Check for multithreading / Fallback to ST mode
    try:

        if prj_dict['mt_enabled'] == True:

        #   Enqueue a new task
            try:

            #   Check for the priority and correct it, if necessary.
                priority = prio_correction(mpy_trace, prj_dict, priority, task)['priority']

            #   Create a log
            #   Enqueing task.
                log_message = prj_dict['mpy_thread_queue_enqueue'] + '\n' \
                              + prj_dict['mpy_thread_queue_task'] + ': ' + str(task) + '\n' \
                              + prj_dict['mpy_thread_queue_priority'] + ': ' + str(priority)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

                prj_dict['mpy_PriorityQueue'].enqueue(mpy_trace, prj_dict, name, priority, task)

        #   Error detection
            except Exception as e:
                log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                              + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                              + prj_dict['mpy_thread_queue_enqueue_err'] + '\n' \
                              + prj_dict['mpy_thread_queue_task'] + ': ' + str(task) + '\n' \
                              + prj_dict['mpy_thread_queue_priority'] + ': ' + str(priority)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

        #   Start a thread, if there are threads available. If all threads are already in use, skip
        #   this step as the threads will keep pulling tasks.
            try:

            #   Create a log
            #   Checking threads availability.
                log_message = prj_dict['mpy_thread_queue_dbg_threads_available'] + '\n' \
                              + prj_dict['mpy_thread_queue_dbg_threads_max'] + ': ' + str(prj_dict['mt_max_threads'])
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

            #   Check for available threads by counting the listed thread ID's and compare them
            #   to the maximum amount of threads available.
                if prj_dict['mt_threads_id_lst']:

                    if len(prj_dict['mt_threads_id_lst']) < thr_available:

                    #   Start a thread.
                        worker = cl_thread(mpy_trace, prj_dict)
                        worker.start()

                    #   Append worker to a list of threads. It is mostly used to join threads later.
                        prj_dict['mpy_workers_running'].append(worker)

                    #   Create a log
                    #   Task successfully enqueued. Thread created.
                        log_message = prj_dict['mpy_thread_queue_dbg_enqueue_done'] + '\n' \
                                      + prj_dict['mpy_thread_queue_dbg_threads_used'] + ': ' + str(len(prj_dict['mt_threads_id_lst'])) + '\n' \
                                      + prj_dict['mpy_thread_queue_dbg_threads_max'] + ': ' + str(prj_dict['mt_max_threads'])
                        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

                    else:

                    #   Create a log
                    #   No free thread available. Skipping thread invoke.
                        log_message = prj_dict['mpy_thread_queue_dbg_thread_skip'] + '\n' \
                                      + prj_dict['mpy_thread_queue_dbg_threads_used'] + ': ' + str(len(prj_dict['mt_threads_id_lst'])) + '\n' \
                                      + prj_dict['mpy_thread_queue_dbg_threads_max'] + ': ' + str(prj_dict['mt_max_threads'])
                        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

                else:

                #   Start a thread.
                    worker = cl_thread(mpy_trace, prj_dict)
                    worker.start()

                #   Append worker to a list of threads. It is mostly used to join threads later.
                    prj_dict['mpy_workers_running'].append(worker)

                #   Create a log
                #   New Thread ID list created. Task successfully enqueued.
                    log_message = prj_dict['mpy_thread_queue_dbg_enq_new_done'] + '\n' \
                                  + prj_dict['mpy_thread_queue_dbg_threads_used'] + ': ' + str(len(prj_dict['mt_threads_id_lst'])) + '\n' \
                                  + prj_dict['mpy_thread_queue_dbg_threads_max'] + ': ' + str(prj_dict['mt_max_threads'])
                    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

                check = True

        #   Error detection
            except Exception as e:
                log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                              + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                              + prj_dict['mpy_thread_queue_thread_err'] + '\n' \
                              + prj_dict['mpy_thread_queue_task'] + ': {}'. format(task) + '\n' \
                              + prj_dict['mpy_thread_queue_priority'] + ': {}'. format(priority)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

    #   Run fallback mode - single threaded
        else:

            exec(thread_imports(mpy_trace, prj_dict, task)['imp_order'])
            exec(task)

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                      + prj_dict['mpy_thread_queue_thread_err'] + '\n' \
                      + prj_dict['mpy_thread_queue_task'] + ': {}'. format(task) + '\n' \
                      + prj_dict['mpy_thread_queue_priority'] + ': {}'. format(priority)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return{
            'check' : check
            }

def mpy_threads_joinall(mpy_trace, prj_dict):

    """ This function stops execution of the code until all threads have finished their work.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_fct, mpy_msg
    import sys, gc

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_mt'
    operation = 'mpy_threads_joinall(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False

    try:

    #   Create a log
    #   Waiting for all threads to finish up their work.
        log_message = prj_dict['mpy_threads_joinall_start'] + '\n' \
                      + prj_dict['mpy_threads_joinall_eval'] + ': ' + str(prj_dict['mpy_workers_running'])
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        for thread in prj_dict['mpy_workers_running']:

            thread.join()

    #   Clear the list of invoked threads
        prj_dict['mpy_workers_running'] = []

    #   Create a log
    #   All threads/tasks finished.
        log_message = prj_dict['mpy_threads_joinall_end'] + '\n' \
                      + prj_dict['mpy_threads_joinall_eval'] + ': ' + str(prj_dict['mpy_workers_running'])
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return{
            'check' : check
            }

def mpy_mt_abort(mpy_trace, prj_dict):

    """ This function aborts all pending tasks. However, the priority queue still exists and new threads
        would eventually pick up the aborted tasks.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_fct, mpy_msg
    import sys, gc

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_mt'
    operation = 'mpy_mt_abort(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False

    try:

    #   Create a log
    #   Waiting for all threads to finish up their work.
        log_message = prj_dict['mpy_mt_abort_start']
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Set the threads exit flag
        prj_dict['mpy_mt_exit'] = True

    #   Wait for all threads to finish up
        mpy_threads_joinall(mpy_trace, prj_dict)

    #   Reset the threads exit flag
        prj_dict['mpy_mt_exit'] = False

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return{
            'check' : check
            }

class cl_mtPriorityQueue(object):

    """ This class defines the globally used queue of this framework. It is possible
        to make use of queue nesting by instanciating another PriorityQueue with a
        different name. The workforce amongst all nested PriorityQueues may be divided
        accordingly and can vary from project to project. However, the main instance
        used throughout this framework should not be tempered with.
    :param
        -
    :return
        -
    """

    def __init__(self, mpy_trace, prj_dict, name):

        """ This method initializes basic parameters of the PriorityQueue. This
            queue will fetch from the highest priority set available and return the
            oldest task. The highest priority is determined by the lowest integer.
        :param
            mpy_trace - operation credentials and tracing
            prj_dict - morPy global dictionary
            name - Define the name of the PriorityQueue Instance
        :return
            -
        """

        import mpy_fct, mpy_msg
        import sys, gc

    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_mt'
        operation = 'cl_mtPriorityQueue.__init__(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    #   Preparing parameters
        name = str(name)

        try:

        #   Define the attributes of the class
            self.name = name
            self.elements = []
            self.counter = count()

        #   Create a reference to the priority queue
            prj_dict['mpy_PriorityQueue'] = self

        #   Create a log
        #   Priority queue initialized.
            log_message = prj_dict['cl_mtPriorityQueue_init_done'] + '\n' \
                          + prj_dict['cl_mtPriorityQueue_name'] + ': ' + self.name
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'init')

    #   Error detection
        except Exception as e:
            log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                          + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                          + prj_dict['cl_mtPriorityQueue_name'] + ': {}'. format(self.name)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

        finally:

        #   Garbage collection
            del mpy_trace
            gc.collect()

    def enqueue(self, mpy_trace, prj_dict, name, priority, task):

        """ This method adds items/tasks to the cl_mtPriorityQueue.
        :param
            mpy_trace - operation credentials and tracing
            prj_dict - morPy global dictionary
            name - Name of the task/thread.
            priority - Integer value. Sets the priority of the given task. Lower numbers indicate
                       a higher priority. Negative integers should be avoided.
            task - Statement, function or class/module to be run by the thread. A string
                   is expected and will be executed via the exec()-function.
        :return - dictionary
            check - The function ended with no errors
        """

        import mpy_fct, mpy_msg
        import sys, gc

    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_mt'
        operation = 'cl_mtPriorityQueue.enqueue(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    #   Preparing parameters
        check = False
        name = str(name)
        task = str(task)

        try:

        #   Create a log
        #   Pushing task to priority queue.
            log_message = prj_dict['cl_mtPriorityQueue_enqueue_start'] + '\n' \
                          + prj_dict['cl_mtPriorityQueue_name'] + ': {}'. format(self.name) + '\n' \
                          + prj_dict['cl_mtPriorityQueue_enqueue_priority'] + ': ' + str(priority) + '\n' \
                          + prj_dict['cl_mtPriorityQueue_enqueue_task'] + ': ' + task
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Define the task to be queued
            task_qed = (name, -priority, next(self.counter), task)

        #   Push the task to the actual heap
            heappush(self.elements, task_qed)

            check = True

    #   Error detection
        except Exception as e:
            log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                          + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                          + prj_dict['cl_mtPriorityQueue_name'] + ': {}'. format(self.name) + '\n' \
                          + prj_dict['cl_mtPriorityQueue_enqueue_priority'] + ': {}'. format(priority) + '\n' \
                          + prj_dict['cl_mtPriorityQueue_enqueue_task'] + ': {}'. format(task)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

        finally:

        #   Garbage collection
            del mpy_trace
            gc.collect()

            return{
                'check' : check
                }

    def dequeue(self, mpy_trace, prj_dict):

        """ This method pops a task from the cl_mtPriorityQueue and returns it for execution.
        :param
            mpy_trace - operation credentials and tracing
            prj_dict - morPy global dictionary
        :return - dictionary
            check - The function ended with no errors
            task_dqed - List element of the dequeued task to execute next
                        [0] name
                        [1] priority
                        [2] counter
                        [3] task
        """

        import mpy_fct, mpy_msg
        import sys, gc

    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_mt'
        operation = 'cl_mtPriorityQueue.dequeue(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    #   Preparing parameters
        check = False

        try:

        #   FIXME Wait for an interrupt to end
            while prj_dict['mpy_interrupt'] == True:
                pass

        #   Return the highest priority and oldest task from priority queue
            task_dqed = heappop(self.elements)

        #   Retrieve the first element of the queue indicating the name
            name = task_dqed[0]

        #   Retrieve the second element of the queue indicating the priority
            priority = task_dqed[1]

        #   Retrieve the third element of the queue indicating the age (counter)
            counter = task_dqed[2]

        #   Retrieve the fourth element of the queue indicating the actual task
            task = task_dqed[3]

        #   Create a log
        #   Pushing task to priority queue.
            log_message = prj_dict['cl_mtPriorityQueue_dequeue_start'] + '\n' \
                          + prj_dict['cl_mtPriorityQueue_name'] + ': {}'. format(self.name) + '\n' \
                          + prj_dict['cl_mtPriorityQueue_dequeue_name'] + ': ' + str(name) + '\n' \
                          + prj_dict['cl_mtPriorityQueue_dequeue_priority'] + ': ' + str(priority) + '\n' \
                          + prj_dict['cl_mtPriorityQueue_dequeue_cnt'] + ': ' + str(counter) + '\n' \
                          + prj_dict['cl_mtPriorityQueue_dequeue_task'] + ': ' + str(task)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

            check = False

    #   Error detection
        except Exception as e:
            log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                          + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                          + prj_dict['cl_mtPriorityQueue_name'] + ': {}'. format(self.name)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

        finally:

        #   Garbage collection
            del mpy_trace
            gc.collect()

            return{
                'check' : check, \
                'task_dqed' : task_dqed
                }

def mt_init(mpy_trace, prj_dict):

    """ This function is needed to initialize multi threading (MT). If MT is disabled,
        the entire program is meant to fall back to a sequential program - therefore
        it is suitable for single threaded (ST) runtime execution. If MT is enabled,
        this functions determines all relevant parameters such as the amount of threads
        to run on. For further parameterization and details, see the mpy_param.py
        module.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    import mpy_fct, mpy_msg
    import sys, gc, math

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_mt'
    operation = 'mt_init(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False
    sys_threads = prj_dict['threads'] # Total threads available to the system

    try:

    #   Initialize threading exit flag
        prj_dict['mpy_mt_exit'] = False

    #   Initialize total thread counter to be used as a unique task ID
        prj_dict['mpy_mt_tasks_cnt'] = 0

    #   Initialize list for running workers
        prj_dict['mpy_workers_running'] = []

    #   Initialize the interrupt flag
        prj_dict['mpy_interrupt'] = False

    #   Evaluate, if MT is enabled
        if prj_dict['mt_enabled'] == True:

        #   Determine the maximum thread count available for runtime
        #   Absolute determination
            if prj_dict['mt_max_threads_set_abs'] == True:

                max_threads = prj_dict['mt_max_threads_cnt_abs']

        #   Determine the maximum thread count available for runtime
        #   Relative determination
            else:

                max_threads = sys_threads * prj_dict['mt_max_threads_cnt_abs']

            #   Round down
                if prj_dict['mt_max_threads_rel_floor'] == True:

                    max_threads = math.floor(max_threads)

            #   Round up
                else:

                    max_threads = math.ceil(max_threads)

        #   Log preparation.
        #   Multithreading enabled.
            mt_init_message = prj_dict['mt_init_done'] + ' ' \
                              + prj_dict['mt_init_enabled_yes']

    #   Fallback to ST, if MT is disabled
        else:

            max_threads = 1

        #   Log preparation.
        #   Multithreading disabled. Fallback to single threaded mode.
            mt_init_message = prj_dict['mt_init_done'] + ' ' \
                               + prj_dict['mt_init_enabled_no']

    #   Correct the maximum thread count, if architecturally there are less available.
        if sys_threads < max_threads:

            max_threads = sys_threads

    #   Set the maximum thread count for runtime in prj_dict
        prj_dict['mt_max_threads'] = max_threads

    #   Create an empty list of thread IDs
        prj_dict['mt_threads_id_lst'] = []

    #   Create a log
    #   Multithreading initialized.
        log_message = mt_init_message + '\n' \
                        + prj_dict['mt_init_thr_available'] + ': ' + str(sys_threads) + '\n' \
                        + prj_dict['mt_init_thr_max'] + ': ' + str(max_threads)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Initialize and create the queue instance for this frameworks runtime
        cl_mtPriorityQueue(mpy_trace, prj_dict, 'mpy_mtPriorityQueue')

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return{
            'check' : check
            }

class cl_thread(threading.Thread):

    """ This class is a subclass of the Thread class. Therefore all methods of the
        threading module may be used with this class, although it is handled by
        this framework independently, anyway.
    :param
        -
    :return
        -
    """

    def __init__(self, mpy_trace, prj_dict):

        """ This method initializes basic paramters of a cl_thread instance.
        :param
            mpy_trace - operation credentials and tracing
            prj_dict - morPy global dictionary
        :return
            -
        """

        import mpy_fct, mpy_msg
        import sys, gc

    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_mt'
        operation = 'cl_thread.__init__(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        try:

        #   Create a log
        #   A worker thread is being created.
            log_message = prj_dict['cl_thread_init_start']
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Define the attributes of the class
            self.ID = thread_id(mpy_trace, prj_dict)['thread_id']
            self.name = 'VOID'
            self.trace = mpy_trace
            self.prj_dict = prj_dict
            self.log = mpy_trace['log_enable']

        #   Increment the task counter
            prj_dict['mpy_mt_tasks_cnt'] + 1

        #   Invoke an instance of threading.Thread
            threading.Thread.__init__(self)

        #   Lock the thread
            self.lock = threading.Lock()

        #   Create a log
        #   Worker thread created. ID reserved.
            log_message = prj_dict['cl_thread_init_done'] + '\n' \
                          + prj_dict['cl_thread_id'] + ': ' + str(self.ID) + '\n' \
                          + prj_dict['cl_thread_lock'] + ': ' + str(self.lock)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Error detection
        except Exception as e:
            log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                          + prj_dict['err_excp'] + ': {}'. format(e)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

        finally:

        #   Garbage collection
            del mpy_trace
            gc.collect()

    def run(self):

        """ This method runs a task handed to the thread. It will continually fetch
            tasks until the priority queue is empty
        :param
            -
        :return - dictionary
            check - The function ended with no errors
        """

        import mpy_fct, mpy_msg
        import sys, gc

    #   Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_mt'
        operation = 'cl_thread.run(~)'
        mpy_trace = mpy_fct.tracing(module, operation, self.trace)
        log_enable = mpy_trace['log_enable']

    #   Preparing parameters
        check = False
        task_ID = -1
        task = 'VOID'

        try:

        #   Acquire a thread lock - reserve a worker for the task
            self.lock.acquire()

        #   Create a log
        #   A task is starting. Thread has been locked.
            log_message = self.prj_dict['cl_thread_run_start'] + '\n' \
                            + 'ID: ' + str(self.ID) + '\n' \
                            + self.prj_dict['cl_thread_lock'] + ': ' + str(self.lock)
            mpy_msg.log(mpy_trace, self.prj_dict, log_message, 'debug')

        #   Fetch a task as long as the queue is not empty.
            while len(self.prj_dict['mpy_PriorityQueue'].elements) > 0 and \
                self.prj_dict['mpy_mt_exit'] == False:

            #   Wait for an interrupt before fetching a task
                while self.prj_dict['mpy_interrupt'] == True:
                    pass

                task_dqed = self.prj_dict['mpy_PriorityQueue'].dequeue(mpy_trace, self.prj_dict)['task_dqed']

            #   Fetching the name of the task to identify the thread with it.
                self.name = task_dqed[0]

            #   Defining the thread specific trace
                mpy_trace['thread_id'] = self.ID

            #   Fetching the task.
                task = task_dqed[3]

            #   Disable logging for the next segment
                mpy_trace['log_enable'] = False

            #   Exchange the traceback of the task from mpy_trace to mpy_trace
                task = mpy_msg.log_regex_replace(mpy_trace, self.prj_dict, task, 'mpy_trace', 'mpy_trace')

            #   Exchange the prj_dict reference of the task
                task = mpy_msg.log_regex_replace(mpy_trace, self.prj_dict, task, 'prj_dict', 'self.prj_dict')

            #   Exchange the log reference of the task
                task = mpy_msg.log_regex_replace(mpy_trace, self.prj_dict, task, 'log', 'self.log')

            #   Reset logging for the next segment
                mpy_trace['log_enable'] = log_enable

            #   Count the tasks invoked during runtime
                task_ID = self.prj_dict['mpy_mt_tasks_cnt'] + 1

            #   Create a log
            #   Fetched a new task. Thread renamed with the task name.
                log_message = self.prj_dict['cl_thread_run_task_fetched'] + '\n' \
                                + 'ID: ' + str(self.ID) + '\n' \
                                + self.prj_dict['cl_thread_name'] + ': ' + str(self.name) + '\n' \
                                + self.prj_dict['cl_thread_prio'] + ': ' + str(task_dqed[1]) + '\n' \
                                + self.prj_dict['cl_thread_run_tasks_total'] + ': ' + str(task_ID) + '\n' \
                                + self.prj_dict['cl_thread_run_task'] + ': ' + str(task)
                mpy_msg.log(mpy_trace, self.prj_dict, log_message, 'debug')


            #   Import a module, if necessary for execution
                imp_eval = thread_imports(mpy_trace, self.prj_dict, task)

            #   Evaluate the necessity to import a module
                imp_true = imp_eval['imp_true']

                if imp_true == True:

                    imp_order = imp_eval['imp_order']
                    exec(imp_order)

                #   Create a log
                #   Modules were imported.
                    log_message = self.prj_dict['cl_thread_run_modules'] + '\n' \
                                    + 'ID: ' + str(self.ID) + '\n' \
                                    + self.prj_dict['cl_thread_name'] + ': ' + str(self.name) + '\n' \
                                    + 'imp_true: ' + str(imp_true) + '\n' \
                                    + 'imp_order: ' + str(imp_order)
                    mpy_msg.log(mpy_trace, self.prj_dict, log_message, 'debug')

                else:

                #   Create a log
                #   Checked for modules to be imported.
                    log_message = self.prj_dict['cl_thread_run_nomodules'] + '\n' \
                                  + 'ID: ' + str(self.ID) + '\n' \
                                  + self.prj_dict['cl_thread_name'] + ': ' + str(self.name) + '\n' \
                                  + 'imp_true: ' + str(imp_true)
                    mpy_msg.log(mpy_trace, self.prj_dict, log_message, 'debug')

            #   Execute the task
                exec(task)

        #   Clear the thread ID from the regarding list for another task to get started (if any).
            self.prj_dict['mt_threads_id_lst'].remove(self.ID)

        #   Release the thread lock - set the worker available again
            self.lock.release()

        #   Create a log
        #   Task ended.
            log_message = self.prj_dict['cl_thread_run_end'] + '\n' \
                          + 'ID: ' + str(self.ID) + '\n' \
                          + self.prj_dict['cl_thread_name'] + ': ' + str(self.name)
            mpy_msg.log(mpy_trace, self.prj_dict, log_message, 'debug')

            check = True

    #   Error detection
        except Exception as e:

            log_message = self.prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                          + self.prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                          + self.prj_dict['cl_thread_id'] + ': {}'. format(self.ID) + '\n' \
                          + self.prj_dict['cl_thread_name'] + ': {}'. format(self.name) + '\n' \
                          + self.prj_dict['cl_thread_run_task_id'] + ': {}'. format(task_ID) + '\n' \
                          + self.prj_dict['cl_thread_run_task'] + ': {}'. format(task)
            mpy_msg.log(mpy_trace, self.prj_dict, log_message, 'critical')

        finally:

        #   Garbage collection
            del mpy_trace
            gc.collect()

            return{
                'check' : check
                }

def prio_correction(mpy_trace, prj_dict, priority, task):

    """ This function checks the plausibility of given task prioirities. Any priority smaller
        than 10 will be set to 10, except for morPy pre-configured modules. The morPy modules
        are trusted to handled priorities from 0 to 9.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        priority - Integer value. Sets the priority of the given task. Lower numbers indicate
                   a higher priority. Negative integers should be avoided.
        task - Statement, function or class/module to be run by the thread. A string
               is expected and will be executed via the exec()-function. The module has
               got to be referenced (if any) in order to work. Example:

                   task = 'prj_module1.prj_function1([mpy_trace], [prj_dict], [...], [log])'

    :return - dictionary
        check - The function ended with no errors
        priority - Integer value. Sets the priority of the given task. Lower numbers indicate
                   a higher priority. Negative integers should be avoided.
    """

    import mpy_fct, mpy_msg, mpy_common
    import sys, gc

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_mt'
    operation = 'prio_correction(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False
    prio_in = priority
    task = str(task)
    prio_trusted = False
    prio_module_lst = ('mpy_msg')

    try:

    #   Split the task and extract the module
        task_split = mpy_common.regex_split(mpy_trace, prj_dict, task, '\.')
        module = task_split[0]

        for mod in prio_module_lst:

            if module == mod:

                prio_trusted = True
                break

    #   Evaluate the priority
        if prio_in < 10:

            if prio_trusted == False:

                priority = 10

            #   Create a log
            #   The priority of a task has been corrected.
                log_message = prj_dict['prio_correction_warn'] + '\n' \
                              + prj_dict['prio_correction_prio_in'] + ': ' + str(prio_in) + '\n' \
                              + prj_dict['prio_correction_prio_out'] + ': ' + str(priority)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'warning')

            else:

                if prio_in < 0:

                    priority = 0

                #   Create a log
                #   The priority of a morPy-task has been corrected.
                    log_message = prj_dict['prio_correction_err'] + '\n' \
                                  + prj_dict['prio_correction_prio_in'] + ': ' + str(prio_in) + '\n' \
                                  + prj_dict['prio_correction_prio_out'] + ': ' + str(priority)
                    mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return{
            'check' : check, \
            'priority' : priority
            }

def thread_id(mpy_trace, prj_dict):

    """ This function is called by a thread to determine its own ID. The ID is an integer
        value and the highest possible value corresponds to the maximum threads available.
        Other than the name of the thread, the ID is set automatically and does not necessarily
        represent the architectural thread ID determined by the operating system.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
        thread_id - The ID of the newly created thread
    """

    import mpy_fct, mpy_msg
    import sys, gc

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_mt'
    operation = 'thread_id(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False
    max_threads = prj_dict['mt_max_threads']
    free_id = False
    thread_id = 0
    threads_used = 0

    try:

    #   Create a log
    #   Reserving an ID for a new thread/task.
        log_message = prj_dict['thread_id_init'] + '\n' \
                        + prj_dict['mt_init_thr_max'] + ': ' + str(max_threads)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   Check, if a list of threads exists. If not, thread_id = 0.
        if prj_dict['mt_threads_id_lst']:

        #   Get the amount of actively used threads
            threads_used = len(prj_dict['mt_threads_id_lst'])

        #   Check, if there are any running threads.
            if threads_used > 0:

            #   Sort the list of taken thread IDs
                prj_dict['mt_threads_id_lst'].sort()

                while free_id == False:

                #   Check, if the actual ID is already reserved
                    for reserved_id in prj_dict['mt_threads_id_lst']:

                        if thread_id != reserved_id:

                            free_id = True

                        else:

                            free_id = False
                            break

                #   ID not found in list. Exit loop and reserve for thread/task.
                    if free_id == True:

                        prj_dict['mt_threads_id_lst'].append(thread_id)
                        break

                    thread_id += 1

                if thread_id > prj_dict['mt_max_threads']:

                #   Raise an error, if the thread ID is greater than the maximum threads utilized.
                #   Overflow in thread ID list. ID exceeds maximum threads utilized.
                    log_message = prj_dict['thread_id_err'] + '\n' \
                                  + prj_dict['mt_init_thr_max'] + ': ' + str(max_threads) + '\n' \
                                  + prj_dict['mt_init_thr_available'] + ': ' + str(max_threads - threads_used)
                    mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    #   No threads in use yet. Start with thread_id = 0.
        else:

            prj_dict['mt_threads_id_lst'].append(thread_id)

    #   Create a log
    #   Reserved an ID for a new thread/task.
        log_message = prj_dict['thread_id_done'] + '\n' \
                        + prj_dict['mt_init_thr_max'] + ': ' + str(max_threads) + '\n' \
                        + prj_dict['mt_init_thr_available'] + ': ' + str(max_threads - threads_used) + '\n' \
                        + prj_dict['cl_thread_id'] + ': ' + str(thread_id)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return{
            'check' : check, \
            'thread_id' : thread_id
            }

def thread_imports(mpy_trace, prj_dict, task):

    """ This function uses regular expressions to figure out whether
        a module needs to be imported or not when starting a task within
        a thread.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - morPy global dictionary
        task - Statement, function or class/module to be run by the thread. A string
               is expected and will be executed via the exec()-function.
    :return - dictionary
        check - The function ended with no errors
        imp_true - True, if a module was found and needs to be imported.
        imp_order - The statement which will be executed by the thread. It includes
                    an order to import a module or an empty string.
    """

    import mpy_fct, mpy_msg, mpy_common
    import sys, gc

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_mt'
    operation = 'thread_imports(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False
    imp_true = False
    imp_order = ''

    try:

        split_test = task.find('.')

    #   Only search for module imports, if a '.' was found in the task
        if split_test >= 0:

        #   Split the task and extract the module
            task_split = mpy_common.regex_split(mpy_trace, prj_dict, task, '\.')
            module = task_split[0]

        #   Create a log
        #   Task split to identify module imports.
            log_message = prj_dict['thread_imports_start'] + '\n' \
                            + 'module: ' + str(module)
            mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Evaluate the existence of the extracted module and create a statement
            try:

            #   Create import order
                imp_order = 'import ' + str(module)

            #   Evaluate by execution
                exec(imp_order)

            #   Set module import true if it was found
                imp_true = True

            #   Create a log
            #   The calling thread imported a module.
                log_message = prj_dict['thread_imports_yes'] + '\n' \
                                + 'module: ' + str(module) + '\n' \
                                + 'imp_order: ' + str(imp_order)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        #   Overwrite the import order, if the module was not found
            except ImportError or ModuleNotFoundError:

                imp_order = ''

            #   Create a log
            #   No module got imported by the calling thread.
                log_message = prj_dict['thread_imports_no'] + '\n' \
                                + 'imp_order: ' + str(imp_order)
                mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        check = True

#   Error detection
    except Exception as e:
        log_message = prj_dict['err_line'] + ': {}'. format(sys.exc_info()[-1].tb_lineno) + '\n' \
                      + prj_dict['err_excp'] + ': {}'. format(e) + '\n' \
                      + 'task: {}'. format(task)
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'critical')

    finally:

    #   Garbage collection
        del mpy_trace
        gc.collect()

        return{
            'check' : check, \
            'imp_true' : imp_true, \
            'imp_order' : imp_order
            }