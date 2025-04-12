r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Enables a spawning child process to unpickle callables.
"""

from lib.mp import reattach_ultradict_refs, join_or_task, child_exit_routine

class SpawnWrapper:
    r"""
    A generic wrapper that can be used to store any module-level callable
    along with its arguments so that it can be dynamically imported and executed
    in another process.
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
        # Dynamically import the module and retrieve the function.
        mod = __import__(self.module_name, fromlist=[self.func_name])
        func = getattr(mod, self.func_name)
        func(*self.args, **self.kwargs)

        # Wait until all child processes are joined or take on a task.
        join_or_task(self.trace, self.app_dict, reset_trace=True, reset_w_prefix=f'{self.module_name}.{self.func_name}')

        child_exit_routine(self.trace, self.app_dict)

    def __repr__(self):
        return (f"<TaskWrapper {self.module_name}.{self.func_name} "
                f"args={self.args} kwargs={self.kwargs}>")