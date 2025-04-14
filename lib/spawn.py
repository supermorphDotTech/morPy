r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Enables a spawning child process to unpickle callables.
"""

from lib.mp import reattach_ultradict_refs, join_or_task

class SpawnWrapper:
    r"""
    Encapsulates a callable task along with its arguments so that it can be dynamically imported
    and executed in a spawned child process. This wrapper resets the trace for the new process
    and provides a call method to invoke the task.
    """

    __slots__ = [
        'app_dict',
        'args',
        'kwargs',
        'func',
        'func_name',
        'module_name',
        'task',
        'trace',
        'pid'
    ]

    def __init__(self, task):
        r"""
        Extracts the function, arguments, and keyword arguments from the provided task (after
        reattaching UltraDict references) and resets the trace for the spawned process. Also
        stores the module and function name for later dynamic import.
        """

        self.task = reattach_ultradict_refs(task)
        self.func = self.task[0]
        self.trace = self.task[1]
        self.app_dict = self.task[2]
        self.pid = self.trace["process_id"]

        # If the last element is a dict, treat it as keyword arguments.
        if len(self.task) > 3 and isinstance(self.task[-1], dict):
            self.args = self.task[1:-1]
            self.kwargs = self.task[-1]
        else:
            self.args = self.task[1:]
            self.kwargs = dict()

        self._set_function(self.func)

    def _set_function(self, func):
        # The callable must be defined at module level.
        if not hasattr(func, '__module__') or not hasattr(func, '__name__'):
            raise ValueError("Task function must be defined at module level!")
        self.module_name = func.__module__
        self.func_name = func.__name__

    def __call__(self):
        r"""
        Dynamically imports the module where the target function is defined, retrieves the function
        by name, and then executes it with the stored arguments. After execution, it synchronizes
        with the parent via join_or_task and finally invokes the child exit routine.
        """

        # Dynamically import the module and retrieve the function.
        mod = __import__(self.module_name, fromlist=[self.func_name])
        func = getattr(mod, self.func_name)
        func(*self.args, **self.kwargs)

        # Wait until all child processes are joined or take on a task.
        join_or_task(self.trace, self.app_dict, reset_trace=True, reset_w_prefix=f'{self.module_name}.{self.func_name}')

        # Clean up after self - tidy up process references
        with self.app_dict["morpy"]["proc_available"].lock:
            with self.app_dict["morpy"]["proc_busy"].lock:
                # Remove from busy processes
                self.app_dict["morpy"]["proc_busy"].pop(self.trace['process_id'])
                # Add to processes available IDs
                self.app_dict["morpy"]["proc_available"][self.trace['process_id']] = None

        with self.app_dict["morpy"]["proc_waiting"].lock:
            self.app_dict["morpy"]["proc_waiting"].pop(self.pid, None)

    def __repr__(self):
        return (f"<TaskWrapper {self.module_name}.{self.func_name} "
                f"args={self.args} kwargs={self.kwargs}>")