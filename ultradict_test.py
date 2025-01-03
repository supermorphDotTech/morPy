import sys

from multiprocessing import Process, current_process, active_children
from functools import partial
from math import sqrt

def u_dict_build(create: bool=False):
    """ Create a nested UltraDict """
    from UltraDict import UltraDict

    app_dict = UltraDict(
        name="app_dict",
        create=create,
        shared_lock=True
    )

    app_dict["nested_udict"] = UltraDict(
        name="app_dict[conf]",
        create=create,
        shared_lock=True
    )

    return app_dict

def parallel_task(app_dict):
    """ Task to be run in parallel with writes to app_dict """
    try:
        if not app_dict:
            raise RuntimeError("No connection to app_dict.")

        # get the current process instance
        process = current_process()

        i = 0
        total = 10**2
        tmp_val = 0

        # Hold on until all processes are ready
        while not app_dict["run"]:
            pass

        while i < total:
            i += 1
            # Read and write app_dict and nested dictionaries
            with app_dict.lock:
                app_dict["test_count"] += 1
                # app_dict["nested_udict"].update({f'{app_dict["test_count"]}' : process.name})

                #### DEBUG BLOCK BELOW ####
                # print(f'BEFORE: {process.name} => {app_dict["nested_udict"].name} => {app_dict}')
                # app_dict.print_status()
                # app_dict['nested_udict'].print_status()
                # app_dict["test_count"] += 1
                #### DEBUG BLOCK ABOVE ####

                with app_dict["nested_udict"].lock:
                    app_dict["nested_udict"][app_dict["test_count"]] = process.name

                #### DEBUG BLOCK BELOW ####
                # print(f'AFTER: {process.name} => {app_dict["nested_udict"].name} => {app_dict}')
                # app_dict.print_status()
                # app_dict['nested_udict'].print_status()
                #### DEBUG BLOCK ABOVE ####

            print(f'{app_dict["test_count"]} :: {process.name}')
            while tmp_val < total:
                tmp_val = (sqrt(sqrt(i)*i) / i) + tmp_val**2

    except Exception as e:
        print(f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n')

def spawn_wrapper(task):
    """ Wrapper for the task tuple / wrapped by the spawned process"""
    app_dict = u_dict_build() # Rebuild UltraDict with create=False

    task[1] = app_dict # Reassign app_dict to the process
    run = partial(*task,) # Wrap the task
    run()

if __name__ == '__main__':
    # Build the app_dict
    app_dict = u_dict_build(create=True)

    # If True, workers will start executing
    app_dict["run"] = False

    # Some value in shared memory
    app_dict["test_count"] = 0

    task = [parallel_task, app_dict]

    i = 0
    j = 10 # Processes to be started
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