"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Multiprocessing functionality for morPy.
"""

import lib.conf as conf
from lib.decorators import log

import importlib
import sys
from UltraDict import UltraDict
from collections.abc import MutableMapping

class AttributeGuard:
    r"""
    This class serves to guard attributes of a base class against
    attribute changes of subclasses, which would detach the attribute
    in the subclass from the base class.
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
        self.loc = {}
        try:
            self.lang = conf.settings().get('localization', '')
            loc_morpy = importlib.import_module(self.lang)
            messages = getattr(loc_morpy, 'loc_morpy')().get('AttributeGuard', {})
            for key, value in messages.items():
                self.loc.update({key: value})
        # Fallback to english if localization is not available
        except (AttributeError, ImportError):
            self.lang = 'lib.morPy_en_US'
            messages = {
                "AttributeGuard_no_mod": "can not modify an attribute of",
                "AttributeGuard_no_del": "Deletion prohibited!",
            }
            for key, value in messages.items():
                self.loc.update({key: value})
        except Exception as e:
            raise RuntimeError(
                f'CRITICAL {self._name}._init_conf(): Failed to initialize.\n'
                f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n'
            )

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        # Only allow setting the value from the root class
        if instance is None:
            raise AttributeError(f'None {self.loc["AttributeGuard_no_mod"]} {self._root}')
        else:
            if type(instance).__name__ != self._root:
                raise AttributeError(f'{type(instance).__name__} {self.loc["AttributeGuard_no_mod"]} {self._root}')
        self._value = value

    def __delete__(self, instance):
        # Prohibit deletion
        raise AttributeError(f'{self.loc["AttributeGuard_no_del"]}')

class MorPyDict(dict):
    r"""
	This is the dictionary class for the morPy framework and provides all key functions
    of it. It utilizes an instance of UltraDict to provide inter-process shared
    dictionary capabilities and memory management.

    Instances work like standard Python dictionaries and deliver security features
    to tighten or lock the dictionaries, restricting modifications.

    TODO flat setup of app_dict with a map to imitate nesting
    TODO set up the map(reference to dicts) as a tuple of immutables to "share" in memory (more like save in UltraDict without pickling)
    TODO write a reduced map to the created UltraDict, to only reflect it's own nesting
    TODO Find a way to keep all maps updated

    MAP:
    app_dict._types_dict_map = ()

    # __setitem__ logic
    if isinstance(key, dict):
        branch_update = False # Prepare the flag to signal, whether a branch needs to be updated
        udict_name = f'app_dict[{key}]'
        for path in app_dict._types_dict_map:
            if key == path[0]:
                branch_update = True # Proactive branch update, even if no further nesting, because there is no other comm between UltraDict and app_dict
                udict_inst = UltraDict(create=False, name=udict_name)


        app_dict._types_dict_map = ()
    """

    # Set access supported types
    _access_types = ('normal', 'tightened', 'locked')

    def __init__(self, name: str='Instance of MorPyDict', access: str='normal'):

        r"""
        :param name: Name of the dictionary for tracing
        :param access: Access types are
            'normal' (default) - works like any Python dictionary
            'tightened' - Keys may not be altered (no delete or add)
            'locked' - Keys and values are locked, changes are prohibited entirely

        :return:
            -

        :example:
            app_dict["global"]["app"]["my_dict"] = MorPyDict(
                name=app_dict["conf"],
                access="tightened"
            )
        """

        try:
            super().__init__()
            self._name = name  # Name variable for messages

            # Initialize a mock morPy_trace
            self.morPy_trace = {
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
            raise RuntimeError(
                f'CRITICAL {self._name}.__init__(): Failed to initialize MorPyDict.\n'
                f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n'
            )
            sys.exit()

    def _init_conf(self):
        # Initialize localization and app configuration
        self.loc = {}
        try:
            self.lang = conf.settings().get('localization', '')
            loc_morpy = importlib.import_module(self.lang)
            messages = getattr(loc_morpy, 'loc_morpy')().get('MorPyDict', {})
            for key, value in messages.items():
                self.loc.update({key: value})
        # Fallback to english if localization is not available
        except (AttributeError, ImportError):
            self.lang = 'en_US'
            messages = {
                'MorPyDict_denied' : 'Prohibited method',
                'MorPyDict_new_key' : 'Keys can not be added.',
                'MorPyDict_del_key' : 'Keys can not be deleted.',
                'MorPyDict_clear' : 'Dictionary can not be cleared.',
                'MorPyDict_lock' : 'Dictionary is locked.',
                'MorPyDict_item' : 'Item',
                'MorPyDict_key' : 'Key',
                'MorPyDict_val' : 'Value',
                "MorPyDict_key_str": "Keys must be strings.",
                "MorPyDict_empty": "Dictionary is empty.",
            }
            for key, value in messages.items():
                self.loc.update({key : value})
        except Exception as e:
            raise RuntimeError(
                f'CRITICAL {self._name}._init_conf(): Failed to initialize.\n'
                f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n'
            )

    def _set_access(self, _access='normal'):
        try:
            # Evaluate access type
            if _access not in self._access_types:
                _access = 'normal'
            self._access = _access
        except Exception as e:
            raise RuntimeError(
                f'CRITICAL {self._name}._set_access():\n'
                f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n'
            )

    def _init_loc(self):
        # Define access level restrictions
        try:
            self._loc_msg()
        except Exception as e:
            raise RuntimeError(
                f'CRITICAL {self._name}._init_loc():\n'
                f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n'
            )

    def _loc_msg(self):
        try:
            # Define localized messages for prohibited actions based on the dictionary access level
            # Error Guard and fallback messages for testing
            self.loc = {} if not self.loc else self.loc
            self.loc["MorPyDict_key_str"] = "Keys must be strings."
            self.loc["MorPyDict_empty"] = "Dictionary is empty."
            self.msg__setitem__ = ''
            self.msg__delitem__ = ''
            self.msg_clear = ''
            self.msg_pop = ''
            self.msg_popitem = ''
            self.msg_update = ''
            self.msg_setdefault = ''
            self.loc["MorPyDict_err_unlink"] = "Error unlinking UltraDict instance"

            if self._access == 'tightened':
                # Prohibited method .setitem() Keys cannot be added.
                self.msg__setitem__ = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.setitem()\n'
                    f'{self.loc["MorPyDict_new_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .delitem() Keys cannot be deleted.
                self.msg__delitem__ = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.delitem()\n'
                    f'{self.loc["MorPyDict_del_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .clear() Dictionary cannot be cleared.
                self.msg_clear = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.clear()\n'
                    f'{self.loc["MorPyDict_clear"]}'
                )
                # Prohibited method .pop() Keys cannot be deleted.
                self.msg_pop = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.pop()\n'
                    f'{self.loc["MorPyDict_del_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .popitem() Keys cannot be deleted.
                self.msg_popitem = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.popitem()\n'
                    f'{self.loc["MorPyDict_del_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .update() Keys cannot be added.
                self.msg_update = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.update()\n'
                    f'{self.loc["MorPyDict_new_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .setdefault() Keys cannot be added.
                self.msg_setdefault = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.setdefault()\n'
                    f'{self.loc["MorPyDict_new_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
            elif self._access == 'locked':
                # Prohibited method .setitem() Dictionary is locked.
                self.msg__setitem__ = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.setitem()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .delitem() Dictionary is locked.
                self.msg__delitem__ = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.delitem()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .clear() Dictionary is locked.
                self.msg_clear = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.clear()\n'
                    f'{self.loc["MorPyDict_lock"]}'
                )
                # Prohibited method .pop() Dictionary is locked.
                self.msg_pop = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.pop()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .popitem() Dictionary is locked.
                self.msg_popitem = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.popitem()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .update() Dictionary is locked.
                self.msg_update = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.update()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .setdefault() Dictionary is locked.
                self.msg_setdefault = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.setdefault()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Error unlinking UltraDict instance
                self.err_unlink = (
                    f'{self.loc["MorPyDict_err_unlink"]}: {self._name}.setdefault()\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
        except Exception as e:
            raise RuntimeError(
                f'CRITICAL {self._name}._loc_msg():\n'
                f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n'
            )

    def _update_self(self, _access=None, localization_force=False):
        # Allow for reinitialization without data loss.

        # Evaluate access type change
        if _access == self._access:
            pass
        else:
            self._set_access(_access=_access)

        # Evaluate localization reinitialization
        if conf.settings:
            loc_conf = conf.settings().get('localization', '')
            if loc_conf != self.lang or localization_force:
                self._init_loc()
        else:
            pass  # Handle cases where conf.settings() is not available

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            # Keys must be strings.
            raise TypeError(f'{self.loc["MorPyDict_key_str"]}:')
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
            raise TypeError(f'{self.loc["MorPyDict_key_str"]}:')
        return super().__getitem__(key)

    def __delitem__(self, key):
        if not isinstance(key, str):
            # Keys must be strings.
            raise TypeError(f'{self.loc["MorPyDict_key_str"]}:')
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
            raise TypeError(f'{self.loc["MorPyDict_key_str"]}:')
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
                raise TypeError(f'{self.loc["MorPyDict_empty"]}:')
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
            raise TypeError(f'{self.loc["MorPyDict_key_str"]}:')
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
                if msg:
                    msg.log(self._morPy_trace, self.loc, msg, 'warning')
                return super().__getitem__(key)
        else:
            return super().setdefault(key, default)

class MorPyDictUltra(UltraDict):
    r"""
	morPy specific dictionary supporting multiprocessing.
    """

    # Set access supported types
    _access_types = ('normal', 'tightened', 'locked')

    def __init__(self, *args, name: str=None, access: str='normal',
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

        :example:
            app_dict["global"]["app"]["my_dict"] = MorPyDict(
                morPy_trace,
                app_dict["conf"],
                access="tightened",
                recurse_register = app_dict[global][app]._name
            )
        """

        try:
            if name is not None:
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

                # Pass initialization arguments to UltraDict
                self._name = kwargs.setdefault('name', name)
                self.create = kwargs.setdefault('create', create)
                self.shared_lock = kwargs.setdefault('shared_lock', True)
                self.recurse = kwargs.setdefault('recurse', False)
                self.buffer_size = kwargs.setdefault('buffer_size', 1_000_000)
                self.full_dump_size = kwargs.setdefault('full_dump_size', 1_000_000)
                self.auto_unlink = kwargs.setdefault('auto_unlink', False)
                # self.recurse_register = kwargs.setdefault('recurse_register', name)
                # self.serializer = kwargs.setdefault('serializer', dill)

                # Initialize the UltraDict super class
                super().__init__(*args, **kwargs)
                self._name = name

                # Initialize localization and app configuration
                self._init_conf()

                # Access control
                self._set_access(access)

                # Initialize localization messages
                self._init_loc()

                if not self.lock:
                    raise RuntimeError("UltraDict ERROR\nself.lock")
                    sys.exit()

            else:
                raise RuntimeError("UltraDict ERROR\nname=None")

        except Exception as e:
            msg = (f'CRITICAL {self._name}.__init__(): Failed to initialize.\n'
                   f'Line: {sys.exc_info()[-1].tb_lineno}\n'
                   f'{type(e).__name__}: {e}')

            raise RuntimeError(msg)
            sys.exit()

    def _init_conf(self):
        # Initialize localization and app configuration
        self.loc = {}
        try:
            self.lang = conf.settings().get('localization', '')
            loc_morpy = importlib.import_module(self.lang)
            messages = getattr(loc_morpy, 'loc_morpy')().get('MorPyDict', {})
            for key, value in messages.items():
                self.loc.update({key: value})
        # Fallback to english if localization is not available
        except (AttributeError, ImportError):
            self.lang = 'en_US'
            messages = {
                'MorPyDict_denied' : 'Prohibited method',
                'MorPyDict_new_key' : 'Keys can not be added.',
                'MorPyDict_del_key' : 'Keys can not be deleted.',
                'MorPyDict_clear' : 'Dictionary can not be cleared.',
                'MorPyDict_lock' : 'Dictionary is locked.',
                'MorPyDict_item' : 'Item',
                'MorPyDict_key' : 'Key',
                'MorPyDict_val' : 'Value',
                "MorPyDict_key_str": "Keys must be strings.",
                "MorPyDict_empty": "Dictionary is empty.",
            }
            for key, value in messages.items():
                self.loc.update({key : value})
        except Exception as e:
            raise RuntimeError(
                f'CRITICAL {self._name}._init_conf(): Failed to initialize.\n'
                f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n'
            )

    def _set_access(self, _access='normal'):
        try:
            # Evaluate access type
            if _access not in self._access_types:
                _access = 'normal'
            self._access = _access
        except Exception as e:
            raise RuntimeError(
                f'CRITICAL {self._name}._set_access():\n'
                f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n'
            )

    def _init_loc(self):
        # Define access level restrictions
        try:
            self._loc_msg()
        except Exception as e:
            raise RuntimeError(
                f'CRITICAL {self._name}._init_loc():\n'
                f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n'
            )

    def _loc_msg(self):
        try:
            # Define localized messages for prohibited actions based on the dictionary access level
            # Error Guard and fallback messages for testing
            self.loc = {} if not self.loc else self.loc
            self.loc["MorPyDict_key_str"] = "Keys must be strings."
            self.loc["MorPyDict_empty"] = "Dictionary is empty."
            self.msg__setitem__ = ''
            self.msg__delitem__ = ''
            self.msg_clear = ''
            self.msg_pop = ''
            self.msg_popitem = ''
            self.msg_update = ''
            self.msg_setdefault = ''
            self.loc["MorPyDict_err_unlink"] = "Error unlinking UltraDict instance"

            if self._access == 'tightened':
                # Prohibited method .setitem() Keys cannot be added.
                self.msg__setitem__ = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.setitem()\n'
                    f'{self.loc["MorPyDict_new_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .delitem() Keys cannot be deleted.
                self.msg__delitem__ = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.delitem()\n'
                    f'{self.loc["MorPyDict_del_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .clear() Dictionary cannot be cleared.
                self.msg_clear = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.clear()\n'
                    f'{self.loc["MorPyDict_clear"]}'
                )
                # Prohibited method .pop() Keys cannot be deleted.
                self.msg_pop = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.pop()\n'
                    f'{self.loc["MorPyDict_del_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .popitem() Keys cannot be deleted.
                self.msg_popitem = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.popitem()\n'
                    f'{self.loc["MorPyDict_del_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .update() Keys cannot be added.
                self.msg_update = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.update()\n'
                    f'{self.loc["MorPyDict_new_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .setdefault() Keys cannot be added.
                self.msg_setdefault = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.setdefault()\n'
                    f'{self.loc["MorPyDict_new_key"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
            elif self._access == 'locked':
                # Prohibited method .setitem() Dictionary is locked.
                self.msg__setitem__ = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.setitem()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .delitem() Dictionary is locked.
                self.msg__delitem__ = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.delitem()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .clear() Dictionary is locked.
                self.msg_clear = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.clear()\n'
                    f'{self.loc["MorPyDict_lock"]}'
                )
                # Prohibited method .pop() Dictionary is locked.
                self.msg_pop = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.pop()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .popitem() Dictionary is locked.
                self.msg_popitem = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.popitem()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .update() Dictionary is locked.
                self.msg_update = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.update()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Prohibited method .setdefault() Dictionary is locked.
                self.msg_setdefault = (
                    f'{self.loc["MorPyDict_denied"]}: {self._name}.setdefault()\n'
                    f'{self.loc["MorPyDict_lock"]}\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
                # Error unlinking UltraDict instance
                self.err_unlink = (
                    f'{self.loc["MorPyDict_err_unlink"]}: {self._name}.setdefault()\n'
                    f'{self.loc["MorPyDict_key"]}:'
                )
        except Exception as e:
            raise RuntimeError(
                f'CRITICAL {self._name}._loc_msg():\n'
                f'Line: {sys.exc_info()[-1].tb_lineno}\n{e}\n'
            )

    def _update_self(self, _access=None, localization_force=False):
        # Allow for reinitialization without data loss.

        # Evaluate access type change
        if _access == self._access:
            pass
        else:
            self._set_access(_access=_access)

        # Evaluate localization reinitialization
        if conf.settings:
            loc_conf = conf.settings().get('localization', '')
            if loc_conf != self.lang or localization_force:
                self._init_loc()
        else:
            pass  # Handle cases where conf.settings() is not available

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
        # TODO make verbose warning for regular dict (can't be shared)
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
                if log:
                    log(self.mpy_trace, self.loc, msg, 'warning')
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

# A helper class for wrapping nested dictionaries.
class _NestedDict(dict):
    """
    A helper dict subclass used for nested dictionaries.
    It behaves just like a standard dict but intercepts assignments
    so that any mapping value is wrapped and stored in the shared flat storage.
    """

    def __init__(self, qualified_name, flat_storage, initial=None):
        self._qualified_name = qualified_name
        self._flat_storage = flat_storage
        super().__init__()
        if initial is not None:
            for key, value in initial.items():
                if isinstance(value, dict) and not isinstance(value, _NestedDict):
                    new_qname = f"{self._qualified_name}{FlatDict.SEPARATOR}{key}"
                    value = _NestedDict(new_qname, self._flat_storage, initial=value)
                    self._flat_storage[new_qname] = value
                super().__setitem__(key, value)

    def __setitem__(self, key, value):
        full = f"{self._qualified_name}{FlatDict.SEPARATOR}{key}"
        if isinstance(value, dict) and not isinstance(value, _NestedDict):
            value = _NestedDict(full, self._flat_storage, initial=value)
            self._flat_storage[full] = value
        else:
            if full in self._flat_storage:
                del self._flat_storage[full]
        super().__setitem__(key, value)

    def __delitem__(self, key):
        full = f"{self._qualified_name}{FlatDict.SEPARATOR}{key}"
        if full in self._flat_storage:
            del self._flat_storage[full]
        super().__delitem__(key)


class FlatDict(MutableMapping):
    """
    A flat mapping that mimics nested dictionaries via a shared flat storage.

    This version has been extended so that its interface (including attributes and methods)
    is 100% compatible with MorPyDictUltra (which is a subclass of UltraDict). In particular,
    FlatDict now supports an access mode (normal, tightened, locked) and implements methods
    such as update(), setdefault(), pop(), popitem(), clear() and _update_self().
    """
    SEPARATOR = "::"
    _access_types = ('normal', 'tightened', 'locked')

    def __init__(self, name, storage=None, access='normal', create=False, **kwargs):
        """
        :param name: The name (or full name) for this dict (e.g. "app_dict").
        :param storage: A shared dict where all nested dicts are stored.
                        If None, a new storage dict is created.
        :param access: Access type: 'normal' (default), 'tightened', or 'locked'.
        :param create: Flag for creating new nested structures.
        """
        self._name = name
        self._storage = storage if storage is not None else {}
        if name not in self._storage:
            self._storage[name] = {}
        self._access = access if access in self._access_types else 'normal'
        self.create = create  # extra flag to mimic UltraDict.create
        # Initialize localization/configuration dictionaries
        self.loc = {}
        self._init_conf()
        self._init_loc()

    def _init_conf(self):
        """
        Initialize localization and configuration.
        This code attempts to import the localization module specified in conf.settings().
        On failure it falls back to default English messages.
        """
        try:
            self.lang = conf.settings().get('localization', '')
            loc_morpy = importlib.import_module(self.lang)
            messages = getattr(loc_morpy, 'loc_morpy')().get('MorPyDict', {})
            for key, value in messages.items():
                self.loc[key] = value
        except (AttributeError, ImportError):
            self.lang = 'en_US'
            default_msgs = {
                'MorPyDict_denied': 'Prohibited method',
                'MorPyDict_new_key': 'Keys can not be added.',
                'MorPyDict_del_key': 'Keys can not be deleted.',
                'MorPyDict_clear': 'Dictionary can not be cleared.',
                'MorPyDict_lock': 'Dictionary is locked.',
                'MorPyDict_item': 'Item',
                'MorPyDict_key': 'Key',
                'MorPyDict_val': 'Value',
                "MorPyDict_key_str": "Keys must be strings.",
                "MorPyDict_empty": "Dictionary is empty.",
            }
            self.loc.update(default_msgs)
        except Exception as e:
            raise RuntimeError(f'CRITICAL {self._name}._init_conf(): {e}\n'
                               f'Line: {sys.exc_info()[-1].tb_lineno}')

    def _init_loc(self):
        """
        Initialize localized messages for the various dictionary operations.
        """
        try:
            self._loc_msg()
        except Exception as e:
            raise RuntimeError(f'CRITICAL {self._name}._init_loc(): {e}\n'
                               f'Line: {sys.exc_info()[-1].tb_lineno}')

    def _loc_msg(self):
        """
        Setup localized messages depending on the current access type.
        """
        # Ensure certain keys exist
        self.loc.setdefault("MorPyDict_denied", "Prohibited method")
        self.loc.setdefault("MorPyDict_new_key", "Keys can not be added.")
        self.loc.setdefault("MorPyDict_del_key", "Keys can not be deleted.")
        self.loc.setdefault("MorPyDict_clear", "Dictionary can not be cleared.")
        self.loc.setdefault("MorPyDict_lock", "Dictionary is locked.")
        self.loc.setdefault("MorPyDict_key", "Key")
        self.loc.setdefault("MorPyDict_key_str", "Keys must be strings.")
        self.loc.setdefault("MorPyDict_empty", "Dictionary is empty.")
        self.loc.setdefault("MorPyDict_err_unlink", "Error unlinking UltraDict instance")
        if self._access == 'tightened':
            self.msg__setitem__ = (f'{self.loc["MorPyDict_denied"]}: {self._name}.setitem()\n'
                                   f'{self.loc["MorPyDict_new_key"]}\n'
                                   f'{self.loc["MorPyDict_key"]}:')
            self.msg__delitem__ = (f'{self.loc["MorPyDict_denied"]}: {self._name}.delitem()\n'
                                   f'{self.loc["MorPyDict_del_key"]}\n'
                                   f'{self.loc["MorPyDict_key"]}:')
            self.msg_clear = f'{self.loc["MorPyDict_denied"]}: {self._name}.clear()\n{self.loc["MorPyDict_clear"]}'
            self.msg_pop = (f'{self.loc["MorPyDict_denied"]}: {self._name}.pop()\n'
                            f'{self.loc["MorPyDict_del_key"]}\n'
                            f'{self.loc["MorPyDict_key"]}:')
            self.msg_popitem = (f'{self.loc["MorPyDict_denied"]}: {self._name}.popitem()\n'
                                f'{self.loc["MorPyDict_del_key"]}\n'
                                f'{self.loc["MorPyDict_key"]}:')
            self.msg_update = (f'{self.loc["MorPyDict_denied"]}: {self._name}.update()\n'
                               f'{self.loc["MorPyDict_new_key"]}\n'
                               f'{self.loc["MorPyDict_key"]}:')
            self.msg_setdefault = (f'{self.loc["MorPyDict_denied"]}: {self._name}.setdefault()\n'
                                   f'{self.loc["MorPyDict_new_key"]}\n'
                                   f'{self.loc["MorPyDict_key"]}:')
        elif self._access == 'locked':
            self.msg__setitem__ = (f'{self.loc["MorPyDict_denied"]}: {self._name}.setitem()\n'
                                   f'{self.loc["MorPyDict_lock"]}\n'
                                   f'{self.loc["MorPyDict_key"]}:')
            self.msg__delitem__ = (f'{self.loc["MorPyDict_denied"]}: {self._name}.delitem()\n'
                                   f'{self.loc["MorPyDict_lock"]}\n'
                                   f'{self.loc["MorPyDict_key"]}:')
            self.msg_clear = f'{self.loc["MorPyDict_denied"]}: {self._name}.clear()\n{self.loc["MorPyDict_lock"]}'
            self.msg_pop = (f'{self.loc["MorPyDict_denied"]}: {self._name}.pop()\n'
                            f'{self.loc["MorPyDict_lock"]}\n'
                            f'{self.loc["MorPyDict_key"]}:')
            self.msg_popitem = (f'{self.loc["MorPyDict_denied"]}: {self._name}.popitem()\n'
                                f'{self.loc["MorPyDict_lock"]}\n'
                                f'{self.loc["MorPyDict_key"]}:')
            self.msg_update = (f'{self.loc["MorPyDict_denied"]}: {self._name}.update()\n'
                               f'{self.loc["MorPyDict_lock"]}\n'
                               f'{self.loc["MorPyDict_key"]}:')
            self.msg_setdefault = (f'{self.loc["MorPyDict_denied"]}: {self._name}.setdefault()\n'
                                   f'{self.loc["MorPyDict_lock"]}\n'
                                   f'{self.loc["MorPyDict_key"]}:')
        else:
            # For normal access, no extra messages are needed.
            self.msg__setitem__ = ''
            self.msg__delitem__ = ''
            self.msg_clear = ''
            self.msg_pop = ''
            self.msg_popitem = ''
            self.msg_update = ''
            self.msg_setdefault = ''

    def _update_self(self, _access=None, localization_force=False):
        """
        Allow reinitialization without data loss.
        This method can be used to change the access level (and optionally force a reinit of the localization).
        """
        if _access and _access in self._access_types:
            self._access = _access
        self._init_loc()

    def __getitem__(self, key):
        # Allow direct full-name access if key contains the separator.
        if self.SEPARATOR in key:
            if key in self._storage:
                return self._storage[key]
            raise KeyError(key)
        # First, check the local (leaf) container.
        local = self._storage[self._name]
        if key in local:
            return local[key]
        # Then check if a nested dict exists.
        full = f"{self._name}{self.SEPARATOR}{key}"
        if full in self._storage:
            return self._storage[full]
        raise KeyError(key)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f'{self.loc["MorPyDict_key_str"]}:')
        if self._access == 'tightened':
            if key not in self._storage[self._name]:
                msg = f'{self.msg__setitem__} {key}'
                raise KeyError(msg)
        elif self._access == 'locked':
            msg = f'{self.msg__setitem__} {key}'
            raise PermissionError(msg)

        # Direct full-name assignment if key contains the separator.
        if self.SEPARATOR in key:
            if type(value) is dict and not isinstance(value, _NestedDict):
                value = _NestedDict(key, self._storage, initial=value)
            self._storage[key] = value
            self._storage[self._name].pop(key, None)
            return

        # Only wrap plain dicts. Subclasses like MorPyDictUltra will be left unchanged.
        if type(value) is MorPyDictUltra and not isinstance(value, _NestedDict):
            full = f"{self._name}{self.SEPARATOR}{key}"
            value = _NestedDict(full, self._storage, initial=value)
            self._storage[full] = value
            self._storage[self._name].pop(key, None)
            self._storage[self._name][key] = value
        else:
            self._storage[self._name][key] = value
            full = f"{self._name}{self.SEPARATOR}{key}"
            self._storage.pop(full, None)

    def __delitem__(self, key):
        if not isinstance(key, str):
            raise TypeError(f'{self.loc["MorPyDict_key_str"]}:')
        if self._access in ('tightened', 'locked'):
            msg = f'{self.msg__delitem__} {key}'
            raise PermissionError(msg)
        if key in self._storage[self._name]:
            full = f"{self._name}{self.SEPARATOR}{key}"
            del self._storage[self._name][key]
            if full in self._storage:
                del self._storage[full]
        else:
            raise KeyError(key)

    def __iter__(self):
        return iter(self._storage[self._name])

    def __len__(self):
        return len(self._storage[self._name])

    def __contains__(self, key):
        if self.SEPARATOR in key:
            return key in self._storage
        if key in self._storage[self._name]:
            return True
        full = f"{self._name}{self.SEPARATOR}{key}"
        return full in self._storage

    def __repr__(self):
        local = self._storage[self._name]
        return f"{self.__class__.__name__}({local})"

    def update(self, *args, **kwargs):
        new_items = dict(*args, **kwargs)
        if self._access == 'tightened':
            for key in new_items.keys():
                if key not in self._storage[self._name]:
                    msg = f'{self.msg_update} {key}'
                    raise PermissionError(msg)
            for key, value in new_items.items():
                self.__setitem__(key, value)
        elif self._access == 'locked':
            raise PermissionError(self.msg_update)
        else:
            for key, value in new_items.items():
                self.__setitem__(key, value)

    def setdefault(self, key, default=None):
        if not isinstance(key, str):
            raise TypeError(f'{self.loc["MorPyDict_key_str"]}:')
        if self._access == 'tightened':
            if key not in self._storage[self._name]:
                msg = f'{self.msg_setdefault} {key}'
                raise PermissionError(msg)
            else:
                return self.__getitem__(key)
        elif self._access == 'locked':
            msg = f'{self.msg_setdefault} {key}'
            if key not in self._storage[self._name]:
                raise PermissionError(msg)
            else:
                return self.__getitem__(key)
        else:
            if key not in self._storage[self._name]:
                self.__setitem__(key, default)
            return self.__getitem__(key)

    def clear(self):
        if self._access in ('tightened', 'locked'):
            raise PermissionError(self.msg_clear)
        else:
            self._storage[self._name].clear()
            keys_to_del = [k for k in self._storage if k.startswith(f"{self._name}{self.SEPARATOR}")]
            for k in keys_to_del:
                del self._storage[k]

    def pop(self, key, default=None):
        if not isinstance(key, str):
            raise TypeError(f'{self.loc["MorPyDict_key_str"]}:')
        if self._access in ('tightened', 'locked'):
            msg = f'{self.msg_pop} {key}'
            raise PermissionError(msg)
        else:
            if key in self._storage[self._name]:
                full = f"{self._name}{self.SEPARATOR}{key}"
                result = self._storage[self._name].pop(key)
                if full in self._storage:
                    del self._storage[full]
                return result
            else:
                if default is not None:
                    return default
                raise KeyError(key)

    def popitem(self):
        if self._access in ('tightened', 'locked'):
            if self._storage[self._name]:
                last_key = next(reversed(self._storage[self._name]))
                msg = f'{self.msg_popitem} {last_key}'
                raise PermissionError(msg)
            else:
                raise TypeError(f'{self.loc["MorPyDict_empty"]}:')
        else:
            if self._storage[self._name]:
                key = next(reversed(self._storage[self._name]))
                value = self._storage[self._name].pop(key)
                full = f"{self._name}{self.SEPARATOR}{key}"
                if full in self._storage:
                    del self._storage[full]
                return key, value
            else:
                raise KeyError("dictionary is empty")

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def print_status(self):
        """
        A helper method for debugging that returns the representation of the FlatDict.
        """
        return self.__repr__()

    def get_recurse_register(self):
        """
        If a 'recurse_register' attribute has been set, return it. Otherwise, return None.
        """
        return getattr(self, 'recurse_register', None)