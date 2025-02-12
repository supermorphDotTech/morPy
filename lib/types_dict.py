"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Multiprocessing functionality for morPy.
"""

import lib.conf as conf
import importlib
import sys

from UltraDict import UltraDict

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
            self.lang = 'en_US'
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
                morPy_trace,
                app_dict["conf"],
                access="tightened",
                recurse_register = app_dict[global][app]._name
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

class MorPyNestedButFlatDict(dict):
    """
    A dictionary subclass that “flattens” nested UltraDict containers.

    If you assign an UltraDict as a value for a top‐level key, its items
    will be stored internally using composite keys separated by "::".

    For example, doing:
        app_dict["dict1"]["dict1.1"] = "value"

    will (internally) store the pair:
        "dict1::dict1.1" : "value"

    Regular dict values (or UltraDicts that are manually set as plain values)
    are stored as usual.
    """

    # String separator used to identify composite keys for simulated deep nesting
    SEPARATOR = "::"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep track of top‐level keys that are “containers”
        self._ultra_keys = set()
        # If some composite keys were already set, record their top-level name.
        for key in super().keys():
            if isinstance(key, str) and self.SEPARATOR in key:
                top, _ = key.split(self.SEPARATOR, 1)
                self._ultra_keys.add(top)

    def __getitem__(self, key):
        # If a composite key is requested (e.g. "dict1::subkey"), use it directly.
        if isinstance(key, str) and self.SEPARATOR in key:
            return super().__getitem__(key)

        # If key is known to be an UltraDict container, return a proxy.
        if key in self._ultra_keys:
            return _MorPyNestedButFlatDictProxy(self, key)

        # Otherwise, do a normal lookup (no auto‐creation).
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        # Bypass flattening for the protected key.
        if key == "_flat_key_references":
            super().__setitem__(key, value)
            return

        # If the key is composite (contains the separator) then simply store.
        if isinstance(key, str) and self.SEPARATOR in key:
            super().__setitem__(key, value)
            return

        # Otherwise, key is a top-level key.
        if isinstance(value, UltraDict):
            # Flatten the UltraDict: store each subkey using a composite key.
            for subkey, subvalue in value.items():
                composite_key = f"{key}{self.SEPARATOR}{subkey}"
                super().__setitem__(composite_key, subvalue)
            # Mark this key as an UltraDict container.
            self._ultra_keys.add(key)
        else:
            # Store as a plain value.
            super().__setitem__(key, value)

    def __delitem__(self, key):
        # If key is a composite key, delete it directly.
        if isinstance(key, str) and self.SEPARATOR in key:
            super().__delitem__(key)
            return

        # If key is an UltraDict container, remove all composite keys starting with key.
        if key in self._ultra_keys:
            prefix = f"{key}{self.SEPARATOR}"
            keys_to_delete = [k for k in list(super().keys())
                              if isinstance(k, str) and k.startswith(prefix)]
            for k in keys_to_delete:
                super().__delitem__(k)
            self._ultra_keys.remove(key)
        else:
            super().__delitem__(key)

    def __contains__(self, key):
        if isinstance(key, str) and self.SEPARATOR in key:
            return super().__contains__(key)
        if key in self._ultra_keys:
            return True
        return super().__contains__(key)

    def __iter__(self):
        """
        Iterate over top-level keys.
        Composite keys (those with the separator) are hidden.
        """
        seen = set()
        for k in super().__iter__():
            if isinstance(k, str) and self.SEPARATOR in k:
                continue
            yield k
            seen.add(k)
        for k in self._ultra_keys:
            if k not in seen:
                yield k

    def keys(self):
        return list(iter(self))

    def items(self):
        return [(k, self[k]) for k in self]

    def values(self):
        return [self[k] for k in self]

    def __repr__(self):
        pairs = ", ".join(f"{k!r}: {self[k]!r}" for k in self)
        return f"MorPyNestedButFlatDict({{{pairs}}})"

class _MorPyNestedButFlatDictProxy:
    """
    A proxy for a top-level UltraDict container in a MorPyNestedButFlatDict.

    The proxy allows you to write:
        app_dict["dict1"]["dict1.1"] = value

    which is converted into the flat key:
        "dict1::dict1.1" : value
    """

    def __init__(self, parent: MorPyNestedButFlatDict, prefix: str):
        self._parent = parent
        self._prefix = prefix

    def _composite_key(self, key):
        return f"{self._prefix}{self._parent.SEPARATOR}{key}"

    def __getitem__(self, key):
        comp_key = self._composite_key(key)
        try:
            return self._parent[comp_key]
        except KeyError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        comp_key = self._composite_key(key)
        self._parent[comp_key] = value

    def __delitem__(self, key):
        comp_key = self._composite_key(key)
        del self._parent[comp_key]

    def __contains__(self, key):
        comp_key = self._composite_key(key)
        return comp_key in self._parent

    def __iter__(self):
        prefix = f"{self._prefix}{self._parent.SEPARATOR}"
        for k in self._parent.keys():
            if isinstance(k, str) and k.startswith(prefix):
                yield k[len(prefix):]

    def keys(self):
        return list(iter(self))

    def items(self):
        return [(k, self[k]) for k in self]

    def values(self):
        return [self[k] for k in self]

    def __len__(self):
        prefix = f"{self._prefix}{self._parent.SEPARATOR}"
        return sum(1 for k in self._parent.keys() if isinstance(k, str) and k.startswith(prefix))

    def __repr__(self):
        inner = ", ".join(f"{k!r}: {self[k]!r}" for k in self)
        return f"{{{inner}}}"

class MorPyDictUltra(MorPyNestedButFlatDict):
    r"""
	This is the dictionary-like class for the morPy framework required for
	multiprocessing. It is subclassed from MorPyNestedButFlatDict() which
	omits reinitialization of UltraDict.__init__(), which in turn may lead
	to recursion issues.

    Instances work like standard Python dictionaries and deliver security features
    to tighten or lock the dictionaries, restricting modifications.
    """

    _access_types = ('normal', 'tightened', 'locked')

    def __init__(self, name: str='Instance of MorPyDictUltra', access: str='normal'):
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
                morPy_trace,
                app_dict["conf"],
                access="tightened",
                recurse_register = app_dict[global][app]._name
            )
        """

        try:
            # Initialize the base dictionary.
            super().__init__()

            # Set up the protected UltraDict for flat key references.
            # We bypass our overridden __setitem__ so that protected keys can be set.
            if "_flat_key_references" not in self:
                super().__setitem__("_flat_key_references", UltraDict(name="app_dict::_flat_key_references"))

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
            self.lang = 'loc.morPy_en_US'
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
        if _access != self._access:
            self._set_access(_access=_access)

        # Evaluate localization reinitialization
        if conf.settings:
            loc_conf = conf.settings().get('localization', '')
            if loc_conf != self.lang or localization_force:
                self._init_loc()

    def __setitem__(self, key, value):
        # Allow direct modification of the protected key.
        if key == "_flat_key_references":
            super().__setitem__(key, value)
            return
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
            # Keys must be strings.
            raise TypeError(f'{self.loc["MorPyDict_key_str"]}:')
        return super().__getitem__(key)

    def __delitem__(self, key):
        # Prevent deletion of the protected key.
        if key == "_flat_key_references":
            # TODO localization
            raise PermissionError("Deletion of the protected key '_flat_key_references' is not allowed.")
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
            raise PermissionError(f'{self.msg_clear}')
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

    @property
    def _access(self):
        # Retrieve the current access mode from the protected UltraDict.
        return self["_flat_key_references"].get("_access", "normal")

    @_access.setter
    def _access(self, value):
        # Set the access mode inside the protected UltraDict.
        self["_flat_key_references"]["_access"] = value