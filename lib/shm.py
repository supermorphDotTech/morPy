#
# UltraDict
#
# A sychronized, streaming Python dictionary that uses shared memory as a backend
#
# Copyright [2022] [Ronny Rentner] [ultradict.code@ronny-rentner.de]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__all__ = ['UltraDict']

import multiprocessing, multiprocessing.shared_memory, multiprocessing.synchronize
import collections, os, pickle, sys, time, weakref
import importlib.util, importlib.machinery

try:
    # Needed for the shared locked
    import atomics
except ModuleNotFoundError:
    pass

try:
    import ultraimport

    Exceptions = ultraimport('__dir__/Exceptions.py')
    try:
        log = ultraimport('__dir__/utils/log.py', 'log', package=1)
        log.log_targets = [sys.stderr]
    except ultraimport.ResolveImportError:
        import logging as log
except ModuleNotFoundError:
    from . import Exceptions

    try:
        from .utils import log

        log.log_targets = [sys.stderr]
    except ModuleNotFoundError:
        import logging as log


def remove_shm_from_resource_tracker():
    """
    Monkey-patch multiprocessing.resource_tracker so SharedMemory won't be tracked
    More details at: https://bugs.python.org/issue38119
    """
    # pylint: disable=protected-access, import-outside-toplevel
    from multiprocessing import resource_tracker
    def fix_register(name, rtype):
        if rtype == "shared_memory":
            return None
        return resource_tracker._resource_tracker.register(name, rtype)

    resource_tracker.register = fix_register

    def fix_unregister(name, rtype):
        if rtype == "shared_memory":
            return None
        return resource_tracker._resource_tracker.unregister(name, rtype)

    resource_tracker.unregister = fix_unregister
    if "shared_memory" in resource_tracker._CLEANUP_FUNCS:
        del resource_tracker._CLEANUP_FUNCS["shared_memory"]


remove_shm_from_resource_tracker()


# --- Notifying wrappers to support in-place modifications ---
class NotifyingDict(dict):
    """
    A dict wrapper that calls a notification callback after every mutating operation.
    Intended for use inside UltraDict to support in-place modifications.
    """
    __slots__ = ('_parent', '_parent_key')

    def __init__(self, initial=None, *, parent=None, parent_key=None, **kwargs):
        if initial is None:
            initial = {}
        super().__init__(initial, **kwargs)
        self._parent = parent
        self._parent_key = parent_key

    def _notify(self):
        if self._parent is not None and self._parent_key is not None:
            # Reassign ourselves to the parent so that changes are recorded.
            self._parent.__setitem__(self._parent_key, self)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._notify()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._notify()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._notify()

    def clear(self):
        super().clear()
        self._notify()

    def pop(self, key, default=None):
        result = super().pop(key, default)
        self._notify()
        return result

    def popitem(self):
        result = super().popitem()
        self._notify()
        return result

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
            return default
        return self[key]

    def __reduce__(self):
        return (dict, (dict(self),))


class NotifyingSet(set):
    """
    A set wrapper that calls a notification callback after every mutating operation.
    Intended for use inside UltraDict to support in-place modifications.
    """
    __slots__ = ('_parent', '_parent_key')

    def __init__(self, initial=None, *, parent=None, parent_key=None):
        if initial is None:
            initial = set()
        super().__init__(initial)
        self._parent = parent
        self._parent_key = parent_key

    def _notify(self):
        if self._parent is not None and self._parent_key is not None:
            self._parent.__setitem__(self._parent_key, self)

    def add(self, element):
        super().add(element)
        self._notify()

    def update(self, *others):
        super().update(*others)
        self._notify()

    def remove(self, element):
        super().remove(element)
        self._notify()

    def discard(self, element):
        super().discard(element)
        self._notify()

    def pop(self):
        result = super().pop()
        self._notify()
        return result

    def clear(self):
        super().clear()
        self._notify()

    def __reduce__(self):
        return (set, (set(self),))


class NotifyingList(list):
    """
    A list wrapper that calls a notification callback after every mutating operation.
    Intended for use inside UltraDict to support in-place modifications.
    """
    __slots__ = ('_parent', '_parent_key')

    def __init__(self, initial=None, *, parent=None, parent_key=None):
        if initial is None:
            initial = []
        super().__init__(initial)
        self._parent = parent
        self._parent_key = parent_key

    def _notify(self):
        if self._parent is not None and self._parent_key is not None:
            self._parent.__setitem__(self._parent_key, self)

    def __setitem__(self, index, value):
        super().__setitem__(index, value)
        self._notify()

    def __delitem__(self, index):
        super().__delitem__(index)
        self._notify()

    def append(self, item):
        super().append(item)
        self._notify()

    def extend(self, iterable):
        super().extend(iterable)
        self._notify()

    def insert(self, index, item):
        super().insert(index, item)
        self._notify()

    def pop(self, index=-1):
        result = super().pop(index)
        self._notify()
        return result

    def remove(self, item):
        super().remove(item)
        self._notify()

    def clear(self):
        super().clear()
        self._notify()

    def sort(self, *args, **kwargs):
        super().sort(*args, **kwargs)
        self._notify()

    def reverse(self):
        super().reverse()
        self._notify()

    def __iadd__(self, other):
        result = super().__iadd__(other)
        self._notify()
        return result

    def __imul__(self, other):
        result = super().__imul__(other)
        self._notify()
        return result

    def __reduce__(self):
        return (list, (list(self),))


# --- End of Notifying wrappers ---

class UltraDict(collections.UserDict, dict):
    """
    UltraDict

    A sychronized, streaming Python dictionary that uses shared memory as a backend
    """

    Exceptions = Exceptions
    log = log

    class RLock(multiprocessing.synchronize.RLock):
        """ Not yet used """
        pass

    class SharedLock():
        """
        Lock stored in shared_memory to provide an additional layer of protection,
        e.g. when using spawned processes.

        Internally uses atomics package of patomics for atomic locking.
        This is needed if you write to the shared memory with independent processes.
        """
        __slots__ = ('parent', 'has_lock', 'ctx', 'lock_atomic', 'lock_remote',
                     'pid', 'pid_bytes', 'pid_remote', 'pid_remote_ctx', 'pid_remote_atomic',
                     'next_acquire_parameters')

        def __init__(self, parent, lock_name, pid_name):
            self.has_lock = 0
            self.next_acquire_parameters = ()
            self.lock_remote = getattr(parent, lock_name)
            self.pid_remote = getattr(parent, pid_name)
            self.init_pid()
            try:
                self.ctx = atomics.atomicview(buffer=self.lock_remote[0:1], atype=atomics.BYTES)
                self.pid_remote_ctx = atomics.atomicview(buffer=self.pid_remote[0:4], atype=atomics.BYTES)
            except NameError as e:
                self.cleanup()
                raise e
            self.lock_atomic = self.ctx.__enter__()
            self.pid_remote_atomic = self.pid_remote_ctx.__enter__()

            def after_fork():
                if self.has_lock:
                    raise Exception("Release the SharedLock before you fork the process")
                self.init_pid()

            if sys.platform != 'win32':
                os.register_at_fork(after_in_child=after_fork)

        def init_pid(self):
            self.pid = multiprocessing.current_process().pid
            self.pid_bytes = self.pid.to_bytes(4, 'little')

        def acquire_with_timeout(self, block=True, sleep_time=0.000001, timeout=1.0, steal_after_timeout=False):
            time_start = None
            blocking_pid = None
            while True:
                try:
                    return self.acquire(block=False, sleep_time=sleep_time)
                except Exceptions.CannotAcquireLock as e:
                    if not time_start:
                        time_start = e.timestamp
                        blocking_pid = e.blocking_pid
                    assert blocking_pid != self.pid
                    time_passed = time.monotonic() - time_start
                    if time_passed >= timeout:
                        if steal_after_timeout:
                            if blocking_pid == e.blocking_pid:
                                self.steal_from_dead(from_pid=blocking_pid, release=True)
                            time_start = None
                            blocking_pid = None
                            continue
                        raise Exceptions.CannotAcquireLockTimeout(blocking_pid=e.blocking_pid,
                                                                  timestamp=time_start) from None

        def acquire(self, block=True, sleep_time=0.000001, timeout=None, steal_after_timeout=False):
            if self.has_lock:
                self.has_lock += 1
                return True
            if timeout:
                return self.acquire_with_timeout(sleep_time=sleep_time, timeout=timeout,
                                                 steal_after_timeout=steal_after_timeout)
            while True:
                if self.test_and_inc():
                    assert self.has_lock == 0
                    self.has_lock = 1
                    assert self.pid_remote[0:4] == b'\x00\x00\x00\x00'
                    self.pid_remote[:] = self.pid_bytes
                    return True
                if sleep_time:
                    time.sleep(sleep_time)
                if not block:
                    raise Exceptions.CannotAcquireLock(blocking_pid=self.get_remote_pid())

        def test_and_inc(self):
            old = self.lock_atomic.exchange(b'\x01')
            if old != b'\x00':
                return False
            return True

        def test_and_dec(self):
            old = self.lock_atomic.exchange(b'\x00')
            if old != b'\x01':
                raise Exception("Failed to release lock")
            return True

        def release(self, *args):
            if self.has_lock > 0:
                owner = int.from_bytes(self.pid_remote, 'little')
                if owner != self.pid:
                    raise Exception(f"Our lock for pid {self.pid} was stolen by pid {owner}")
                self.has_lock -= 1
                if not self.has_lock:
                    self.pid_remote[:] = b'\x00\x00\x00\x00'
                    self.test_and_dec()
                return True
            return False

        def reset(self):
            self.lock_remote[:] = b'\x00'
            self.pid_remote[:] = b'\x00\x00\x00\x00'
            self.has_lock = 0

        def reset_acquire_parameters(self):
            self.next_acquire_parameters = ()

        def steal(self, from_pid=0, release=False):
            if self.has_lock:
                raise Exception(
                    "Cannot steal the lock because we have already acquired it. Use release() to release the lock.")
            if not self.get_remote_lock():
                return False
            if from_pid != self.get_remote_pid():
                return False
            result = self.pid_remote_atomic.cmpxchg_strong(expected=from_pid.to_bytes(4, 'little'),
                                                           desired=self.pid_bytes)
            if result.success:
                self.has_lock = 1
                if release:
                    self.release()
            return result.success

        def steal_from_dead(self, from_pid=0, release=False):
            try:
                import psutil
            except ModuleNotFoundError:
                raise Exceptions.MissingDependency("Install `psutil` Python package to use shared_lock=True") from None
            try:
                p = psutil.Process(from_pid)
                if p and p.is_running() and p.status() not in [psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD]:
                    raise Exception(
                        f"Trying to steal lock from process that is still alive, something seems really wrong from_pid={from_pid} pid={self.pid} p={p}")
            except psutil.NoSuchProcess:
                pass
            except Exception as e:
                raise e
            return self.steal(from_pid=from_pid, release=release)

        def status(self):
            return {
                'has_lock': self.has_lock,
                'lock_remote': int.from_bytes(self.lock_remote, 'little'),
                'pid': self.pid,
                'pid_remote': int.from_bytes(self.pid_remote, 'little'),
            }

        def print_status(self, status=None):
            import pprint
            if not status:
                status = self.status()
            pprint.pprint(status)

        def cleanup(self):
            if hasattr(self, 'ctx'):
                try:
                    self.ctx.__exit__(None, None, None)
                except Exception:
                    pass
                del self.ctx
            if hasattr(self, 'pid_remote_ctx'):
                try:
                    self.pid_remote_ctx.__exit__(None, None, None)
                except Exception:
                    pass
                del self.pid_remote_ctx
            if hasattr(self, 'lock_atomic'):
                del self.lock_atomic
            if hasattr(self, 'pid_remote_atomic'):
                del self.pid_remote_atomic
            if hasattr(self, 'lock_remote'):
                del self.lock_remote
            if hasattr(self, 'pid_remote'):
                del self.pid_remote
            if hasattr(self, 'pid_bytes'):
                del self.pid_bytes
            if hasattr(self, 'pid'):
                del self.pid

        def __repr__(self):
            return f"{self.__class__.__name__} @{hex(id(self))} lock_remote={int.from_bytes(self.lock_remote, 'little')}, has_lock={self.has_lock}, pid={self.pid}, pid_remote={int.from_bytes(self.pid_remote, 'little')}"

        def __enter__(self):
            self.acquire(*self.next_acquire_parameters)
            self.reset_acquire_parameters()
            return self

        def __exit__(self, type, value, traceback):
            self.release()
            return False

        def __call__(self, block=True, timeout=None, sleep_time=0.000001, steal_after_timeout=False):
            self.next_acquire_parameters = (block, timeout, sleep_time, steal_after_timeout)
            return self

    __slots__ = ('name', 'control', 'buffer', 'buffer_size', 'lock', 'shared_lock',
                 'update_stream_position', 'update_stream_position_remote',
                 'full_dump_counter', 'full_dump_memory', 'full_dump_size',
                 'serializer',
                 'lock_pid_remote', 'lock_remote',
                 'full_dump_counter_remote', 'full_dump_static_size_remote',
                 'shared_lock_remote', 'recurse', 'recurse_remote', 'recurse_register',
                 'full_dump_memory_name_remote', 'data', 'closed', 'auto_unlink', 'finalizer')

    @staticmethod
    def get_memory(*, create=True, name=None, size=0):
        """
        Attach an existing SharedMemory object with `name`.
        If `create` is True, create the object if it does not exist.
        """
        assert size > 0 or not create
        if name:
            try:
                memory = multiprocessing.shared_memory.SharedMemory(name=name)
                if create:
                    raise Exceptions.AlreadyExists(f"Cannot create memory '{name}' because it already exists")
                return memory
            except FileNotFoundError:
                pass
        if create or create is None:
            memory = multiprocessing.shared_memory.SharedMemory(create=True, size=size, name=name)
            memory.created_by_ultra = True
            return memory
        raise Exceptions.CannotAttachSharedMemory(f"Could not get memory '{name}'")

    def __init__(self, *args, name=None, create=None, buffer_size=10_000, serializer=pickle, shared_lock=None,
                 full_dump_size=None,
                 auto_unlink=None, recurse=None, recurse_register=None, **kwargs):
        # pylint: disable=too-many-branches, too-many-statements
        if sys.platform == 'win32':
            buffer_size = -(buffer_size // -4096) * 4096
            if full_dump_size:
                full_dump_size = -(full_dump_size // -4096) * 4096
        assert buffer_size < 2 ** 32
        if recurse:
            assert serializer == pickle
        self.data = {}
        self.update_stream_position = 0
        self.full_dump_counter = 0
        self.closed = False
        self.auto_unlink = auto_unlink
        self.control = self.get_memory(create=create, name=name, size=1000)
        self.name = self.control.name

        def finalize(weak_self, name):
            resolved_self = weak_self()
            if resolved_self is not None:
                resolved_self.close(from_finalizer=True)

        self.finalizer = weakref.finalize(self, finalize, weakref.ref(self), self.name)
        self.init_remotes()
        self.serializer = serializer
        self.buffer = self.get_memory(create=create, name=self.name + '_memory', size=buffer_size)
        self.buffer_size = self.buffer.size
        self.full_dump_memory = None
        self.full_dump_size = None
        if hasattr(self.control, 'created_by_ultra'):
            if auto_unlink is None:
                self.auto_unlink = True
            if recurse:
                self.recurse_remote[0:1] = b'1'
            if shared_lock:
                self.shared_lock_remote[0:1] = b'1'
            if full_dump_size:
                self.full_dump_size = full_dump_size
                self.full_dump_static_size_remote[:] = full_dump_size.to_bytes(4, 'little')
                self.full_dump_memory = self.get_memory(create=True, name=self.name + '_full', size=full_dump_size)
                self.full_dump_memory_name_remote[:] = self.full_dump_memory.name.encode('utf-8').ljust(255)
        else:
            size = int.from_bytes(self.full_dump_static_size_remote, 'little')
            shared_lock_remote = self.shared_lock_remote[0:1] == b'1'
            if shared_lock is None:
                shared_lock = shared_lock_remote
            elif shared_lock != shared_lock_remote:
                raise Exceptions.ParameterMismatch(
                    f"shared_lock={shared_lock} was set but the creator has used shared_lock={shared_lock_remote}")
            recurse_remote = self.recurse_remote[0:1] == b'1'
            if recurse is None:
                recurse = recurse_remote
            elif recurse != recurse_remote:
                raise Exceptions.ParameterMismatch(
                    f"recure={recurse} was set but the creator has used recurse={recurse_remote}")
            if size > 0:
                self.full_dump_size = size
                self.full_dump_memory = self.get_memory(create=False, name=self.name + '_full')
        if shared_lock:
            try:
                self.lock = self.SharedLock(self, 'lock_remote', 'lock_pid_remote')
            except NameError as e:
                raise Exceptions.MissingDependency("Install `atomics` Python package to use shared_lock=True") from None
        else:
            self.lock = multiprocessing.RLock()
        self.shared_lock = shared_lock
        self.recurse = recurse
        if self.recurse:
            if recurse_register is not None:
                if type(recurse_register) == str:
                    self.recurse_register = UltraDict(name=recurse_register)
                elif type(recurse_register) == UltraDict:
                    self.recurse_register = recurse_register
                else:
                    raise Exception("Bad type for recurse_register")
            else:
                self.recurse_register = UltraDict(name=f'{self.name}_register',
                                                  recurse=False, auto_unlink=False, shared_lock=self.shared_lock)
                if self.auto_unlink:
                    self.recurse_register.finalizer.detach()
        else:
            self.recurse_register = None
        super().__init__(*args, **kwargs)
        self.apply_update()
        if sys.platform == 'win32':
            if not shared_lock:
                log.warning('You are running on win32, potentially without locks. Consider setting shared_lock=True')
        self.data = self.data

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def init_remotes(self):
        self.update_stream_position_remote = self.control.buf[0:4]
        self.lock_pid_remote = self.control.buf[4:8]
        self.lock_remote = self.control.buf[8:10]
        self.full_dump_counter_remote = self.control.buf[10:14]
        self.full_dump_static_size_remote = self.control.buf[14:18]
        self.shared_lock_remote = self.control.buf[18:19]
        self.recurse_remote = self.control.buf[19:20]
        self.full_dump_memory_name_remote = self.control.buf[20:275]

    def del_remotes(self):
        remotes = [r for r in dir(self) if r.endswith('_remote')]
        for r in remotes:
            if hasattr(self, r):
                delattr(self, r)

    def __setitem__(self, key, item):
        # Modified __setitem__ to wrap mutable objects so in-place modifications are caught.
        if isinstance(item, dict) and not isinstance(item, (self.__class__, NotifyingDict)):
            item = NotifyingDict(item, parent=self, parent_key=key)
        elif isinstance(item, set) and not isinstance(item, (self.__class__, NotifyingSet)):
            item = NotifyingSet(item, parent=self, parent_key=key)
        elif isinstance(item, list) and not isinstance(item, NotifyingList):
            item = NotifyingList(item, parent=self, parent_key=key)
        with self.lock:
            self.apply_update()
            self.data.__setitem__(key, item)
            self.append_update(key, item)

    def __getitem__(self, key):
        self.apply_update()
        value = self.data.__getitem__(key)
        return value

    def __delitem__(self, key):
        with self.lock:
            self.apply_update()
            self.data.__delitem__(key)
            self.append_update(key, b'', delete=True)

    def has_key(self, key):
        self.apply_update()
        return key in self.data

    def __eq__(self, other):
        return self.apply_update() == other.apply_update()

    def __contains__(self, key):
        self.apply_update()
        return key in self.data

    def __len__(self):
        self.apply_update()
        return len(self.data)

    def __iter__(self):
        self.apply_update()
        return iter(self.data)

    def __repr__(self):
        try:
            self.apply_update()
        except Exceptions.AlreadyClosed:
            pass
        return self.data.__repr__()

    def status(self):
        ret = {attr: getattr(self, attr) for attr in self.__slots__ if hasattr(self, attr) and attr != 'data'}
        ret['update_stream_position_remote'] = int.from_bytes(self.update_stream_position_remote, 'little')
        ret['lock_pid_remote'] = int.from_bytes(self.lock_pid_remote, 'little')
        ret['lock_remote'] = int.from_bytes(self.lock_remote, 'little')
        ret['shared_lock_remote'] = self.shared_lock_remote[0:1] == b'1'
        ret['recurse_remote'] = self.recurse_remote[0:1] == b'1'
        ret['lock'] = self.lock
        ret['full_dump_counter_remote'] = int.from_bytes(self.full_dump_counter_remote, 'little')
        ret['full_dump_memory_name_remote'] = bytes(self.full_dump_memory_name_remote).decode('utf-8').strip(
            '\x00').strip()
        return ret

    def print_status(self, status=None, stderr=False):
        import pprint
        if not status:
            status = self.status()
        pprint.pprint(status, stream=sys.stderr if stderr else sys.stdout)

    def cleanup(self):
        if hasattr(self, 'lock') and hasattr(self.lock, 'cleanup'):
            self.lock.cleanup()
            del self.lock
        if hasattr(self, 'full_dump_memory'):
            try:
                self.full_dump_memory.close()
            except Exception:
                pass
            del self.full_dump_memory
        data = self.data
        del self.data
        self.del_remotes()
        self.apply_update = self.raise_already_closed
        self.append_update = self.raise_already_closed
        return data

    def close(self, unlink=False, from_finalizer=False):
        """
        Close this UltraDict, releasing shared memory and atomic resources.
        If unlink is True, also unlink the shared memory blocks.
        """
        if self.closed:
            return
        try:
            self.cleanup()
        except Exception:
            pass
        # Try to close shared memory objects (ignoring BufferErrors)
        for attr in ['control', 'buffer']:
            mem = getattr(self, attr, None)
            if mem is not None:
                try:
                    mem.close()
                except Exception:
                    pass
                if unlink:
                    try:
                        mem.unlink()
                    except Exception:
                        pass
        if self.full_dump_memory is not None:
            try:
                self.full_dump_memory.close()
            except Exception:
                pass
            if unlink:
                try:
                    self.full_dump_memory.unlink()
                except Exception:
                    pass
        self.closed = True

    def raise_already_closed(self, *args, **kwargs):
        raise Exceptions.AlreadyClosed('UltraDict already closed, you can only access the `UltraDict.data` buffer!')

    def keys(self):
        self.apply_update()
        return self.data.keys()

    def values(self):
        self.apply_update()
        return self.data.values()

    def items(self):
        self.apply_update()
        return self.data.items()

    def pop(self, key, default=None):
        with self.lock:
            self.apply_update()
            ret = self.data.pop(key, default)
            self.append_update(key, b'', delete=True)
            return ret

    def update(self, other=None, *args, **kwargs):
        if other is not None:
            for k, v in other.items() if isinstance(other, collections.abc.Mapping) else other:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def dump(self):
        with self.lock:
            self.apply_update()
            marshalled = self.serializer.dumps(self.data)
            length = len(marshalled)
            if self.full_dump_size and self.full_dump_memory:
                full_dump_memory = self.full_dump_memory
            else:
                full_dump_memory = self.get_memory(create=True, name=self.name + '_full', size=length + 6)
            if length + 6 > full_dump_memory.size:
                self.apply_update()
                self.dump()
                return
            marshalled = b'\xFF' + length.to_bytes(4, 'little') + b'\xFF' + marshalled
            full_dump_memory.buf[0:1] = b'\xFF'
            full_dump_memory.buf[1:5] = length.to_bytes(4, 'little')
            full_dump_memory.buf[5:6] = b'\xFF'
            full_dump_memory.buf[6:6 + length] = marshalled[6:6 + length]
            self.full_dump_counter += 1
            current = int.from_bytes(self.full_dump_counter_remote, 'little')
            self.full_dump_counter_remote[:] = int(current + 1).to_bytes(4, 'little')
            self.update_stream_position = 0
            self.update_stream_position_remote[:] = b'\x00\x00\x00\x00'
            if not (self.full_dump_size and self.full_dump_memory):
                try:
                    full_dump_memory.close()
                except Exception:
                    pass
            if self.full_dump_size is None:
                self.full_dump_memory_name_remote[:] = full_dump_memory.name.encode('utf-8').ljust(255)
            self.full_dump_memory = full_dump_memory
            return full_dump_memory

    def get_full_dump_memory(self, max_retry=3, retry=0):
        try:
            name = bytes(self.full_dump_memory_name_remote).decode('utf-8').strip().strip('\x00')
            assert len(name) >= 1
            return self.get_memory(create=False, name=name)
        except Exceptions.CannotAttachSharedMemory as e:
            if retry < max_retry:
                return self.get_full_dump_memory(max_retry=max_retry, retry=retry + 1)
            elif retry == max_retry:
                with self.lock:
                    return self.get_full_dump_memory(max_retry=max_retry, retry=retry + 1)
            else:
                raise e

    def load(self, force=False):
        full_dump_counter = int.from_bytes(self.full_dump_counter_remote, 'little')
        try:
            if force or (self.full_dump_counter < full_dump_counter):
                if self.full_dump_size and self.full_dump_memory:
                    full_dump_memory = self.full_dump_memory
                else:
                    full_dump_memory = self.get_full_dump_memory()
                buf = full_dump_memory.buf
                pos = 0
                assert bytes(buf[pos:pos + 1]) == b'\xFF'
                pos += 1
                length = int.from_bytes(bytes(buf[pos:pos + 4]), 'little')
                assert length > 0, (
                self.status(), full_dump_memory, bytes(buf[:]).decode('utf-8').strip().strip('\x00'), len(buf))
                pos += 4
                assert bytes(buf[pos:pos + 1]) == b'\xFF'
                pos += 1
                self.data = self.serializer.loads(bytes(buf[pos:pos + length]))
                self.full_dump_counter = full_dump_counter
                self.update_stream_position = 0
                if sys.platform != 'win32' and not self.full_dump_memory:
                    try:
                        full_dump_memory.close()
                    except Exception:
                        pass
            else:
                raise Exception("Cannot load full dump, no new data available")
        except AssertionError as e:
            full_dump_delta = int.from_bytes(self.full_dump_counter_remote, 'little') - self.full_dump_counter
            if full_dump_delta > 1:
                return self.load(force=True)
            self.print_status()
            raise e

    def append_update(self, key, item, delete=False):
        marshalled = self.serializer.dumps((not delete, key, item))
        length = len(marshalled)
        with self.lock:
            start_position = int.from_bytes(self.update_stream_position_remote, 'little')
            end_position = start_position + length + 6
            if end_position > self.buffer_size:
                self.apply_update()
                if not delete:
                    self.data.__setitem__(key, item)
                self.dump()
                return
            marshalled = b'\xFF' + length.to_bytes(4, 'little') + b'\xFF' + marshalled
            self.buffer.buf[start_position:end_position] = marshalled
            self.update_stream_position = end_position
            self.update_stream_position_remote[:] = end_position.to_bytes(4, 'little')

    def apply_update(self):
        if self.full_dump_counter < int.from_bytes(self.full_dump_counter_remote, 'little'):
            self.load(force=True)
        if self.update_stream_position < int.from_bytes(self.update_stream_position_remote, 'little'):
            pos = self.update_stream_position
            try:
                while pos < int.from_bytes(self.update_stream_position_remote, 'little'):
                    assert bytes(self.buffer.buf[pos:pos + 1]) == b'\xFF'
                    pos += 1
                    length = int.from_bytes(bytes(self.buffer.buf[pos:pos + 4]), 'little')
                    pos += 4
                    assert bytes(self.buffer.buf[pos:pos + 1]) == b'\xFF'
                    pos += 1
                    mode, key, value = self.serializer.loads(bytes(self.buffer.buf[pos:pos + length]))
                    if mode:
                        self.data.__setitem__(key, value)
                    else:
                        self.data.__delitem__(key)
                    pos += length
                    self.update_stream_position = pos
            except (AssertionError, pickle.UnpicklingError) as e:
                if self.full_dump_counter < int.from_bytes(self.full_dump_counter_remote, 'little'):
                    log.warning(
                        f"Full dumps too fast full_dump_counter={self.full_dump_counter} full_dump_counter_remote={int.from_bytes(self.full_dump_counter_remote, 'little')}. Consider increasing buffer_size.")
                    return self.apply_update()
                with self.lock:
                    if self.full_dump_counter < int.from_bytes(self.full_dump_counter_remote, 'little'):
                        log.warning(
                            f"Full dumps too fast full_dump_counter={self.full_dump_counter} full_dump_counter_remote={int.from_bytes(self.full_dump_counter_remote, 'little')}. Consider increasing buffer_size.")
                        return self.apply_update()
                raise e

    def __reduce__(self):
        from functools import partial
        return (
        partial(self.__class__, name=self.name, auto_unlink=self.auto_unlink, recurse_register=self.recurse_register),
        ())
