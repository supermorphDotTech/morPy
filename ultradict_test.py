import sys
import time

from multiprocessing import Process, current_process, active_children
from functools import partial
from math import sqrt

def u_dict_build(create: bool=False):
    """ Create a nested UltraDict """
    from UltraDict import UltraDict

    app_dict = UltraDict(
        name="app_dict",
        create=create,
        shared_lock=True,
        buffer_size=1_000_000,
        full_dump_size=1_000_000,
        auto_unlink=False,
        recurse=True
    )

    app_dict["nested_udict"] = UltraDict(
        name="nested_udict",
        create=create,
        shared_lock=True,
        buffer_size=1_000_000,
        full_dump_size=1_000_000,
        auto_unlink=False
    )

    return app_dict

def fibonacci(n):
    n = n * 50
    if n <= 0:
        return []  # Return an empty list if n is non-positive.
    elif n == 1:
        return [0]

    sequence = [0, 1]
    while len(sequence) < n:
        # Append the sum of the last two numbers in the sequence.
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

def parallel_task(app_dict):
    """ Task to be run in parallel with writes to app_dict """
    try:
        if not app_dict:
            raise RuntimeError("No connection to app_dict.")

        # get the current process instance
        process = current_process()

        i = 0
        total = 10**3
        tmp_val = 0

        # Hold on until all processes are ready
        while not app_dict["run"]:
            time.sleep(.1)

        while i < total:
            i += 1
            fib_seq = fibonacci(i)
            # Read and write app_dict and nested dictionaries
            with app_dict.lock:
                app_dict["test_count"] += 1

            with app_dict["nested_udict"].lock:
                app_dict["nested_udict"]["test_count"] += 1

            print(f'root={app_dict["test_count"]} :: nested={app_dict["nested_udict"]["test_count"]} :: fibonacci={len(fib_seq)} :: {process.name}\n')
            while tmp_val < total:
                tmp_val = (sqrt(sqrt(i)*i) / i) + tmp_val**2

    except Exception as e:
        print(f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n')

def spawn_wrapper(task):
    """ Wrapper for the task tuple / wrapped by the spawned process"""

    app_dict = u_dict_build()

    task = [task[0], app_dict] # Reassign app_dict to the process
    func, *args = task
    result = func(*args)

if __name__ == '__main__':
    # Build the app_dict
    app_dict = u_dict_build(create=True)

    # If True, workers will start executing
    app_dict["run"] = False

    # Some value in shared memory
    app_dict["test_count"] = 0
    app_dict["nested_udict"]["test_count"] = 0

    task = [parallel_task,]

    i = 0
    j = 14 # Processes to be started
    processes = []
    while i < j:
        p = Process(target=partial(spawn_wrapper, task))
        p.start()
        processes.append(p)
        i += 1

    # Release workers for calculations
    app_dict["run"] = True

    print(f'\nJoining processes.\n')
    # Now join everyone
    for p in processes:
        p.join()