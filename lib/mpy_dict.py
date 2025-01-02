"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Multiprocessing functionality for morPy.
"""

import mpy_msg
import importlib
import sys
import traceback

from UltraDict import UltraDict
from mpy_conf import parameters
import multiprocessing

class cl_attr_guard:

    r"""
    This class serves to guard attributes of a base class against
    attribute changes of sub-classes, which would detach the attribute
    in the sub-class from the base class.
    """

    def __init__(self, value, root):

        r"""
        :param value: Attribute to be accessed or changed
        :param root: Name of the owner class (root class) that is granted
            to modify the attribute.
        """

        self._value = value
        self._root = f'{root}'
        self._name = self.__class__.__name__
        self._init_conf()

    def _init_conf(self):
        # Initialize localization and app configuration
        try:
            # Initialize localization and configuration messages
            self.loc = {}
            if parameters:
                self.lang = parameters().get('localization', '')
                loc_mpy = importlib.import_module(self.lang)
                messages = getattr(loc_mpy, 'loc_mpy')().get('cl_attr_guard', {})
                for key, value in messages.items():
                    self.loc.update({key: value})
            else:
                self.lang = 'mpy_en_US'
                messages = {
                    "cl_attr_guard_no_mod": "can not modify an attribute of",
                    "cl_attr_guard_no_del": "Deletion prohibited!",
                }
                for key, value in messages.items():
                    self.loc.update({key: value})
        except Exception as e:
            print(f'CRITICAL {self._name}._init_conf(): {e}')

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        # Only allow setting the value from the root class
        if instance is None:
            raise AttributeError(f'None {self.loc["cl_attr_guard_no_mod"]} {self._root}')
        else:
            if type(instance).__name__ != self._root:
                raise AttributeError(f'{type(instance).__name__} {self.loc["cl_attr_guard_no_mod"]} {self._root}')
        self._value = value

    def __delete__(self, instance):
        # Prohibit deletion
        raise AttributeError(f'{self.loc["cl_attr_guard_no_del"]}')

class cl_mpy_dict(dict):

    r"""
	This is the dictionary class for the morPy framework and provides all key functions
    of it. It utilizes an instance of UltraDict to provide inter-process shared
    dictionary capabilities and memory management.

    Instances work like standard Python dictionaries and deliver security features
    to tighten or lock the dictionaries, restricting modifications.
    """

    def __init__(self, *args, name: str='Instance of cl_mpy_dict', access: str='normal',
                 create: bool=False, recurse_register=None, **kwargs):

        r"""
        :param name: Name of the dictionary for tracing
        :param access: Access types are
            'normal' (default) - works like any Python dictionary
            'tightened' - Keys may not be altered (no delete or add)
            'locked' - Keys and values are locked, changes are prohibited entirely
        :param create: If True, a (nested) dictionary is created. Otherwise, purely
            references to the UltraDict.
        :param recurse_register: If not None, recursion is activated for UltraDict. Expects
            the recurse_register of the root UltraDict.

        :return:
            -

        :example:
            app_dict["global"]["app"]["my_dict"] = cl_mpy_dict(
                mpy_trace,
                app_dict["conf"],
                access="tightened",
                recurse_register = app_dict[global][app]._name
            )
        """

        try:
            self._name = name  # Name variable for messages

            # Initialize a mock mpy_trace
            self.mpy_trace = {
                'module': '',
                'operation': name,
                'tracing': 'morPy',
                'process_id': None,
                'thread_id': None,
                'task_id': None,
                'log_enable': False,
                'interrupt_enable': False,
            }

            # Initialize localization and app configuration
            self._init_conf()

            # Access control
            self._set_access(access)

            # Initialize localization messages
            self._init_loc()

        except Exception as e:
            print(f'CRITICAL {self._name}.__init__(): Failed to initialize UltraDict. {e}')
            sys.exit()

    def _init_conf(self):
        # Initialize localization and app configuration
        try:
            # Initialize localization and configuration messages
            self.loc = {}
            if parameters:
                self.lang = parameters().get('localization', '')
                loc_mpy = importlib.import_module(self.lang)
                messages = getattr(loc_mpy, 'loc_mpy')().get('cl_mpy_dict', {})
                for key, value in messages.items():
                    self.loc.update({key : value})
            # Fallback to english if localization is not available
            else:
                self.lang = 'mpy_en_US'
                messages = {
                    'cl_mpy_dict_denied' : 'Prohibited method',
                    'cl_mpy_dict_new_key' : 'Keys can not be added.',
                    'cl_mpy_dict_del_key' : 'Keys can not be deleted.',
                    'cl_mpy_dict_clear' : 'Dictionary can not be cleared.',
                    'cl_mpy_dict_lock' : 'Dictionary is locked.',
                    'cl_mpy_dict_item' : 'Item',
                    'cl_mpy_dict_key' : 'Key',
                    'cl_mpy_dict_val' : 'Value',
                    "cl_mpy_dict_key_str": "Keys must be strings.",
                    "cl_mpy_dict_empty": "Dictionary is empty.",
                }
                for key, value in messages.items():
                    self.loc.update({key : value})
        except Exception as e:
            print(f'CRITICAL {self._name}._init_conf(): {e}')

    def _set_access(self, _access='normal'):
        try:
            # Evaluate access type
            self._access_types = ('normal', 'tightened', 'locked')
            if _access not in self._access_types:
                _access = 'normal'
            self._access = _access
        except Exception as e:
            print(f'CRITICAL {self._name}._set_access()\n{e}')

    def _init_loc(self):
        # Define access level restrictions
        try:
            self._loc_msg()
        except Exception as e:
            print(f'CRITICAL {self._name}._init_loc(): {e}')

    def _loc_msg(self):
        try:
            # Define localized messages for prohibited actions based on the dictionary access level
            # Error Guard and fallback messages for testing
            self.loc = {} if not self.loc else self.loc
            self.loc["cl_mpy_dict_key_str"] = "Keys must be strings."
            self.loc["cl_mpy_dict_empty"] = "Dictionary is empty."
            self.msg__setitem__ = ''
            self.msg__delitem__ = ''
            self.msg_clear = ''
            self.msg_pop = ''
            self.msg_popitem = ''
            self.msg_update = ''
            self.msg_setdefault = ''
            self.loc["cl_mpy_dict_err_unlink"] = "Error unlinking UltraDict instance"

            if self._access == 'tightened':
                # Prohibited method .setitem() Keys cannot be added.
                self.msg__setitem__ = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.setitem()\n'
                    f'{self.loc["cl_mpy_dict_new_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .delitem() Keys cannot be deleted.
                self.msg__delitem__ = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.delitem()\n'
                    f'{self.loc["cl_mpy_dict_del_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .clear() Dictionary cannot be cleared.
                self.msg_clear = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.clear()\n'
                    f'{self.loc["cl_mpy_dict_clear"]}'
                )
                # Prohibited method .pop() Keys cannot be deleted.
                self.msg_pop = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.pop()\n'
                    f'{self.loc["cl_mpy_dict_del_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .popitem() Keys cannot be deleted.
                self.msg_popitem = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.popitem()\n'
                    f'{self.loc["cl_mpy_dict_del_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .update() Keys cannot be added.
                self.msg_update = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.update()\n'
                    f'{self.loc["cl_mpy_dict_new_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .setdefault() Keys cannot be added.
                self.msg_setdefault = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.setdefault()\n'
                    f'{self.loc["cl_mpy_dict_new_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
            elif self._access == 'locked':
                # Prohibited method .setitem() Dictionary is locked.
                self.msg__setitem__ = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.setitem()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .delitem() Dictionary is locked.
                self.msg__delitem__ = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.delitem()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .clear() Dictionary is locked.
                self.msg_clear = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.clear()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}'
                )
                # Prohibited method .pop() Dictionary is locked.
                self.msg_pop = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.pop()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .popitem() Dictionary is locked.
                self.msg_popitem = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.popitem()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .update() Dictionary is locked.
                self.msg_update = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.update()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .setdefault() Dictionary is locked.
                self.msg_setdefault = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.setdefault()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Error unlinking UltraDict instance
                self.err_unlink = (
                    f'{self.loc["cl_mpy_dict_err_unlink"]}: {self._name}.setdefault()\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
        except Exception as e:
            print(f'CRITICAL {self._name}._loc_msg(): {e}')

    def _update_self(self, _access=None, localization_force=False):
        # Allow for reinitialization without data loss.

        # Evaluate access type change
        if _access == self._access:
            pass
        else:
            self._set_access(_access=_access)

        # Evaluate localization reinitialization
        if parameters:
            loc_conf = parameters().get('localization', '')
            if loc_conf != self.lang or localization_force:
                self._init_loc()
        else:
            pass  # Handle cases where mpy_conf.parameters() is not available

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            # Keys must be strings.
            raise TypeError(f'{self.loc["cl_mpy_dict_key_str"]}:')
        if self._access == 'tightened':
            msg = f'{self.msg__setitem__} {key}'
            if key not in super().keys():
                raise KeyError(msg)
            else:
                super().__setitem__(key, value)

        elif self._access == 'locked':
            msg = f'{self.msg__setitem__} {key}'
            raise PermissionError(msg)
        else:
            super().__setitem__(key, value)

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise TypeError(f'{self.loc["cl_mpy_dict_key_str"]}:')
        return super().__getitem__(key)

    def __delitem__(self, key):
        if not isinstance(key, str):
            # Keys must be strings.
            raise TypeError(f'{self.loc["cl_mpy_dict_key_str"]}:')
        if self._access in ('tightened', 'locked'):
            msg = f'{self.msg__delitem__} {key}'
            raise PermissionError(msg)
        else:
            super().__delitem__(key)

    def clear(self):
        if self._access in ('tightened', 'locked'):
            msg = f'{self.msg_clear}'
            raise PermissionError(msg)
        else:
            super().clear()

    def pop(self, key, default=None):
        if not isinstance(key, str):
            # Keys must be strings.
            raise TypeError(f'{self.loc["cl_mpy_dict_key_str"]}:')
        if self._access in ('tightened', 'locked'):
            msg = f'{self.msg_pop} {key}'
            raise PermissionError(msg)
        else:
            return super().pop(key, default)

    def popitem(self):
        if self._access in ('tightened', 'locked'):
            if self:
                last_key = next(reversed(self))
                msg = f'{self.msg_popitem} {last_key}'
                raise PermissionError(msg)
            else:
                # Dictionary is empty.
                raise TypeError(f'{self.loc["cl_mpy_dict_empty"]}:')
        else:
            return super().popitem()

    def update(self, *args, **kwargs):
        if self._access == 'tightened':
            new_items = dict(*args, **kwargs)
            for key in new_items.keys():
                if key not in super().keys():
                    msg = f'{self.msg_update} {key}'
                    raise PermissionError(msg)
            super().update(*args, **kwargs)
        elif self._access == 'locked':
            msg = f'{self.msg_update}'
            raise PermissionError(msg)
        else:
            super().update(*args, **kwargs)

    def setdefault(self, key, default=None):
        if not isinstance(key, str):
            # Keys must be strings.
            raise TypeError(f'{self.loc["cl_mpy_dict_key_str"]}:')
        if self._access == 'tightened':
            if key not in super().keys():
                msg = f'{self.msg_setdefault} {key}'
                raise PermissionError(msg)
            else:
                return super().setdefault(key, default)
        elif self._access == 'locked':
            msg = f'{self.msg_setdefault} {key}'
            if key not in super().keys():
                raise PermissionError(msg)
            else:
                if mpy_msg:
                    mpy_msg.log(self._mpy_trace, self.loc, msg, 'warning')
                return super().__getitem__(key)
        else:
            return super().setdefault(key, default)

class cl_mpy_dict_root(UltraDict):

    r"""
	This is the dictionary class for the morPy framework and provides all key functions
    of it. It utilizes an instance of UltraDict to provide inter-process shared
    dictionary capabilities and memory management.

    This subclass of UltraDict handles access control and localization. Take note, that
    this subclass is rebuilt by a spawned process and not referenced from the host
    process. Therefore, if the orchestrator manipulates access control, it is not reflected
    in spawned processes, therefore further hardening access.

    Instances work like standard Python dictionaries, despite security features
    to tighten or lock the dictionaries, restricting modifications.
    """

    def __init__(self, *args, name: str='app_dict', access: str='normal',
                 create: bool=False, recurse_register=None, **kwargs):

        r"""
        :param name: Name of the dictionary for tracing
        :param access: Access types are
            'normal' (default) - works like any Python dictionary
            'tightened' - Keys may not be altered (no delete or add)
            'locked' - Keys and values are locked, changes are prohibited entirely
        :param create: If True, a (nested) dictionary is created. Otherwise, purely
            references to the UltraDict.
        :param recurse_register: If not None, recursion is activated for UltraDict. Expects
            the recurse_register of the root UltraDict.

        :return:
            -

        :example 1: Create a root dictionary
            app_dict = cl_mpy_dict_root(create=True)

        :example 2: Create a nested dictionary
            app_dict["global"]["app"]["my_dict"] = cl_mpy_dict_root(
                name = app_dict[global][app][my_dict],
                access="tightened"
            )
        """

        try:
            # Initialize a mock mpy_trace
            self.mpy_trace = {
                'module': '',
                'operation': name,
                'tracing': 'morPy',
                'process_id': None,
                'thread_id': None,
                'task_id': None,
                'log_enable': False,
                'interrupt_enable': False,
            }

            # Inherit from UltraDict
            # TODO This is only MS Windows compatible yet
            # alteration in super().__init__()

            # Pass initialization arguments to UltraDict
            self._name = kwargs.setdefault('name', name)
            self.create = kwargs.setdefault('create', create)
            self.shared_lock = kwargs.setdefault('shared_lock', True)
            self.recurse = kwargs.setdefault('recurse', False)
            # self.recurse_register = kwargs.setdefault('recurse_register', name)
            # self.serializer = kwargs.setdefault('serializer', dill)
            # self.auto_unlink = kwargs.setdefault('auto_unlink', False)

            # Initialize the UltraDict super class
            super().__init__(*args, **kwargs)

            # Initialize localization and app configuration
            self._init_conf()

            # Access control
            self._set_access(access)

            # Initialize localization messages
            self._init_loc()

            if not self.lock:
                raise RuntimeError(f'UltraDict ERROR\nself.lock')
                sys.exit()

        except Exception as e:
            raise RuntimeError(f'CRITICAL {self._name}.__init__(): Failed to initialize UltraDict.\n{e}')
            sys.exit()

    def _init_conf(self):
        # Initialize localization and app configuration
        try:
            # Initialize localization and configuration messages
            self.loc = {}
            if parameters:
                self.lang = parameters().get('localization', '')
                loc_mpy = importlib.import_module(self.lang)
                messages = getattr(loc_mpy, 'loc_mpy')().get('cl_mpy_dict', {})
                for key, value in messages.items():
                    self.loc.update({key : value})
            # Fallback to english if localization is not available
            else:
                self.lang = 'mpy_en_US'
                messages = {
                    'cl_mpy_dict_denied' : 'Prohibited method',
                    'cl_mpy_dict_new_key' : 'Keys can not be added.',
                    'cl_mpy_dict_del_key' : 'Keys can not be deleted.',
                    'cl_mpy_dict_clear' : 'Dictionary can not be cleared.',
                    'cl_mpy_dict_lock' : 'Dictionary is locked.',
                    'cl_mpy_dict_item' : 'Item',
                    'cl_mpy_dict_key' : 'Key',
                    'cl_mpy_dict_val' : 'Value',
                    "cl_mpy_dict_key_str": "Keys must be strings.",
                    "cl_mpy_dict_empty": "Dictionary is empty.",
                }
                for key, value in messages.items():
                    self.loc.update({key : value})
        except Exception as e:
            print(f'CRITICAL {self._name}._init_conf(): {e}')

    def _set_access(self, _access='normal'):
        try:
            # Evaluate access type
            self._access_types = ('normal', 'tightened', 'locked')
            if _access not in self._access_types:
                _access = 'normal'
            self._access = _access
        except Exception as e:
            print(f'CRITICAL {self._name}._set_access()\n{e}')

    def _init_loc(self):
        # Define access level restrictions
        try:
            self._loc_msg()
        except Exception as e:
            print(f'CRITICAL {self._name}._init_loc(): {e}')

    def _loc_msg(self):
        try:
            # Define localized messages for prohibited actions based on the dictionary access level
            # Error Guard and fallback messages for testing
            self.loc = {} if not self.loc else self.loc
            self.loc["cl_mpy_dict_key_str"] = "Keys must be strings."
            self.loc["cl_mpy_dict_empty"] = "Dictionary is empty."
            self.msg__setitem__ = ''
            self.msg__delitem__ = ''
            self.msg_clear = ''
            self.msg_pop = ''
            self.msg_popitem = ''
            self.msg_update = ''
            self.msg_setdefault = ''
            self.loc["cl_mpy_dict_err_unlink"] = "Error unlinking UltraDict instance"

            if self._access == 'tightened':
                # Prohibited method .setitem() Keys cannot be added.
                self.msg__setitem__ = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.setitem()\n'
                    f'{self.loc["cl_mpy_dict_new_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .delitem() Keys cannot be deleted.
                self.msg__delitem__ = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.delitem()\n'
                    f'{self.loc["cl_mpy_dict_del_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .clear() Dictionary cannot be cleared.
                self.msg_clear = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.clear()\n'
                    f'{self.loc["cl_mpy_dict_clear"]}'
                )
                # Prohibited method .pop() Keys cannot be deleted.
                self.msg_pop = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.pop()\n'
                    f'{self.loc["cl_mpy_dict_del_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .popitem() Keys cannot be deleted.
                self.msg_popitem = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.popitem()\n'
                    f'{self.loc["cl_mpy_dict_del_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .update() Keys cannot be added.
                self.msg_update = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.update()\n'
                    f'{self.loc["cl_mpy_dict_new_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .setdefault() Keys cannot be added.
                self.msg_setdefault = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.setdefault()\n'
                    f'{self.loc["cl_mpy_dict_new_key"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
            elif self._access == 'locked':
                # Prohibited method .setitem() Dictionary is locked.
                self.msg__setitem__ = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.setitem()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .delitem() Dictionary is locked.
                self.msg__delitem__ = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.delitem()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .clear() Dictionary is locked.
                self.msg_clear = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.clear()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}'
                )
                # Prohibited method .pop() Dictionary is locked.
                self.msg_pop = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.pop()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .popitem() Dictionary is locked.
                self.msg_popitem = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.popitem()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .update() Dictionary is locked.
                self.msg_update = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.update()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Prohibited method .setdefault() Dictionary is locked.
                self.msg_setdefault = (
                    f'{self.loc["cl_mpy_dict_denied"]}: {self._name}.setdefault()\n'
                    f'{self.loc["cl_mpy_dict_lock"]}\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
                # Error unlinking UltraDict instance
                self.err_unlink = (
                    f'{self.loc["cl_mpy_dict_err_unlink"]}: {self._name}.setdefault()\n'
                    f'{self.loc["cl_mpy_dict_key"]}:'
                )
        except Exception as e:
            print(f'CRITICAL {self._name}._loc_msg(): {e}')

    def _update_self(self, _access=None, localization_force=False):
        lock = self._get_lock()
        # Allow for reinitialization without data loss.

        # Evaluate access type change
        if _access == self._access:
            pass
        else:
            with lock:
                self._set_access(_access=_access)

        # Evaluate localization reinitialization
        if parameters:
            loc_conf = parameters().get('localization', '')
            if loc_conf != self.lang or localization_force:
                with lock:
                    self._init_loc()
        else:
            pass  # Handle cases where mpy_conf.parameters() is not available

    def _get_lock(self):
        r""" Retrieve lock depending on super class """
        if isinstance(self, UltraDict):
            return self.lock
        else:
            return None

    def _get_super(self):
        r""" Setup methods depending on super class """
        if isinstance(self, UltraDict):
            return self.lock, super()
        else:
            return None, None

    def __setitem__(self, key, value):
        lock, super_class = self._get_super()
        if not isinstance(key, str):
            # Keys must be strings.
            raise TypeError(f'{self.loc["cl_mpy_dict_key_str"]}:')
        if self._access == 'tightened':
            msg = f'{self.msg__setitem__} {key}'
            if key not in super_class.keys():
                raise KeyError(msg)
            else:
                with lock:
                    super_class.__setitem__(key, value)

        elif self._access == 'locked':
            msg = f'{self.msg__setitem__} {key}'
            raise PermissionError(msg)
        else:
            with lock:
                super_class.__setitem__(key, value)

    def __contains__(self, key):
        lock, super_class = self._get_super()
        if not isinstance(key, str):
            raise TypeError("Keys must be strings.")
        with lock:
            return key in super_class.keys()

    def __getitem__(self, key):
        lock, super_class = self._get_super()
        if not isinstance(key, str):
            raise TypeError(f'{self.loc["cl_mpy_dict_key_str"]}:')
        with lock:
            return super_class.__getitem__(key)

    def __delitem__(self, key):
        lock, super_class = self._get_super()
        if not isinstance(key, str):
            # Keys must be strings.
            raise TypeError(f'{self.loc["cl_mpy_dict_key_str"]}:')
        if self._access in ('tightened', 'locked'):
            msg = f'{self.msg__delitem__} {key}'
            raise PermissionError(msg)
        else:
            with lock:
                super_class.__delitem__(key)

    def get(self, key, default=None):
        lock, super_class = self._get_super()
        if not isinstance(key, str):
            # Keys must be strings.
            raise TypeError(f'{self.loc["cl_mpy_dict_key_str"]}:')
        with lock:
            return super_class.get(key, default)

    def clear(self):
        lock, super_class = self._get_super()
        if self._access in ('tightened', 'locked'):
            msg = f'{self.msg_clear}'
            raise PermissionError(msg)
        else:
            with lock:
                # TODO clean up
                # # Iterate over all items and unlink if they are UltraDict instances
                # for key, item in list(super_class.data.items()):
                #     if isinstance(item, UltraDict):
                #         try:
                #             item.close(unlink=True)
                #         except Exception as e:
                #             raise RuntimeError(f'{self.loc["cl_mpy_dict_err_unlink"]}: {key}')
                # Clear the dictionary
                super_class.clear()

    def pop(self, key, default=None):
        lock, super_class = self._get_super()
        if not isinstance(key, str):
            # Keys must be strings.
            raise TypeError(f'{self.loc["cl_mpy_dict_key_str"]}:')
        if self._access in ('tightened', 'locked'):
            msg = f'{self.msg_pop} {key}'
            raise PermissionError(msg)
        else:
            with lock:
                # TODO clean up
                # # Retrieve the item before popping
                # item = super_class.data.get(key, default)
                #
                # # If the item is an instance of UltraDict, unlink it
                # if isinstance(item, UltraDict):
                #     try:
                #         item.close(unlink=True)
                #     except Exception as e:
                #         raise RuntimeError(f'{self.loc["cl_mpy_dict_err_unlink"]}: {key}')

                return super_class.pop(key, default)

    def popitem(self):
        lock, super_class = self._get_super()
        if self._access in ('tightened', 'locked'):
            if self:
                last_key = next(reversed(self))
                msg = f'{self.msg_popitem} {last_key}'
                raise PermissionError(msg)
            else:
                # Dictionary is empty.
                raise TypeError(f'{self.loc["cl_mpy_dict_empty"]}:')
        else:
            with lock:
                key, item = super_class.popitem()

                # TODO clean up
                # # If the item is an instance of UltraDict, unlink it
                # if isinstance(item, UltraDict):
                #     try:
                #         item.close(unlink=True)
                #     except Exception as e:
                #         raise RuntimeError(f'{self.loc["cl_mpy_dict_err_unlink"]}: {key}')

                return key, item

    def update(self, *args, **kwargs):
        lock, super_class = self._get_super()
        if self._access == 'tightened':
            new_items = dict(*args, **kwargs)
            with lock:
                for key in new_items.keys():
                    if key not in super_class.keys():
                        msg = f'{self.msg_update} {key}'
                        raise PermissionError(msg)
                super_class.update(*args, **kwargs)
        elif self._access == 'locked':
            msg = f'{self.msg_update}'
            raise PermissionError(msg)
        else:
            with lock:
                super_class.update(*args, **kwargs)

    def setdefault(self, key, default=None):
        lock, super_class = self._get_super()
        if not isinstance(key, str):
            # Keys must be strings.
            raise TypeError(f'{self.loc["cl_mpy_dict_key_str"]}:')
        if self._access == 'tightened':
            if key not in super_class.keys():
                msg = f'{self.msg_setdefault} {key}'
                raise PermissionError(msg)
            else:
                with lock:
                    return super_class.setdefault(key, default)
        elif self._access == 'locked':
            msg = f'{self.msg_setdefault} {key}'
            if key not in super_class.keys():
                raise PermissionError(msg)
            else:
                if mpy_msg:
                    mpy_msg.log(self._mpy_trace, self.loc, msg, 'warning')
                with lock:
                    return super_class.__getitem__(key)
        else:
            with lock:
                return super_class.setdefault(key, default)

    def get_recurse_register(self):
        # Access the recurse_register attribute if available.
        if hasattr(self, 'recurse_register'):
            return self.recurse_register
        return None

    def print_status(self):
        lock, super_class = self._get_super()
        return super_class.print_status()

    def __repr__(self):
        lock, super_class = self._get_super()
        return f'cl_mpy_dict(name={self._name}, access={self._access}, data={super_class.__repr__()})'
