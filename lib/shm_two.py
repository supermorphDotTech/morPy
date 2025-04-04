"""
lib/shm_two.py

MorPyDict: A shared-memory dict‐like object for multiprocessing.

Key properties:
  - No Manager is used.
  - The entire dictionary is stored as a pickle in a shared memory block,
    preceded by a 4‐byte little-endian length header.
  - All operations are guarded by a multiprocessing.RLock.
  - Extra keyword arguments (saved in self._init_kwargs) are preserved for nested creation.
  - When setting a value, if its type name is "AuthenticationString", it is converted to a plain string.
  - If a value is itself a MorPyDict, it is stored as a marker tuple
    ("MORPYDICT", shared_memory_name, size) and cached so that the live object remains available.
  - Missing keys auto‑create a new nested MorPyDict only if the instance flag auto_create_missing is True.
    (If auto_create_missing is False – the default – __missing__ raises a KeyError unless the key is one of the
    container keys that we want to auto‑create as a plain dict.)
  - When pickled (via __reduce__), only the safe shared memory name and size are saved.
    The _rebuild class method then reattaches and reinitializes the lock.

Requires:
  - lib/fct.py must define:
        def hashify(string: str) -> str:
            import hashlib
            return hashlib.sha256(string.encode('utf-8')).hexdigest()
"""

import pickle
import time
import multiprocessing
from multiprocessing import shared_memory
from collections.abc import MutableMapping
from lib.fct import hashify  # hashify returns SHA-256 hex digest of a string

class MorPyDict(MutableMapping):
    def __init__(self, name=None, size=1024*1024, create=True, **kwargs):
        """
        Initialization with shared memory and dictionary setup.
        """
        self._init_kwargs = kwargs.copy()
        self.lock = multiprocessing.RLock()
        self.size = size

        # Generate a safe shared memory name.
        if name is not None:
            name = "__" + hashify(name)
        self._safe_name = name

        # Cache for live nested MorPyDict objects.
        self._nested_cache = {}
        # Flag: if True, missing keys (other than container keys) auto‐create a nested MorPyDict.
        self.auto_create_missing = False

        if create:
            self.shm = shared_memory.SharedMemory(create=True, size=self.size, name=name)
            # Initialize shared memory with an empty dict.
            self._write_dict({})
        else:
            self.shm = shared_memory.SharedMemory(name=name)

    def _write_dict(self, d):
        """Serialize the dictionary and write it into shared memory.
        The first 4 bytes hold the length (little-endian) of the pickle."""
        plain_d = dict(d)
        data = pickle.dumps(plain_d)
        total = len(data) + 4
        if total > self.size:
            raise ValueError("Data too large for shared memory segment")
        self.shm.buf[:4] = len(data).to_bytes(4, byteorder='little')
        self.shm.buf[4:4+len(data)] = data
        self.shm.buf[4+len(data):self.size] = b'\x00' * (self.size - 4 - len(data))

    def _read_dict(self):
        """Read and deserialize the dictionary from shared memory."""
        length = int.from_bytes(self.shm.buf[:4], byteorder='little')
        if length == 0:
            return {}
        data = bytes(self.shm.buf[4:4+length])
        return pickle.loads(data)

    # --- Dictionary interface ---
    def __getitem__(self, key):
        # First check if a live nested instance is cached.
        if key in self._nested_cache:
            return self._nested_cache[key]
        with self.lock:
            d = self._read_dict()
            if key not in d:
                return self.__missing__(key)
            val = d[key]
        # If the value is stored as a marker tuple, attempt to rebuild a live instance.
        if isinstance(val, tuple) and len(val) == 3 and val[0] == "MORPYDICT":
            try:
                live = self.__class__._rebuild(val[1], val[2])
                self._nested_cache[key] = live
                return live
            except FileNotFoundError:
                # If reattachment fails, return an empty dict as a fallback.
                return {}
        return val

    def __setitem__(self, key, value):
        # If value is a live MorPyDict, store it as a marker tuple and cache it.
        if isinstance(value, MorPyDict):
            self._nested_cache[key] = value
            value = ("MORPYDICT", value.shm.name, value.size)
        # Convert "AuthenticationString" to a plain string.
        if type(value).__name__ == "AuthenticationString":
            value = str(value)
        with self.lock:
            d = self._read_dict()
            d[key] = value
            self._write_dict(d)
        # If a nested instance existed and now value is not a marker, remove it.
        if key in self._nested_cache and not isinstance(value, tuple):
            del self._nested_cache[key]

    def __delitem__(self, key):
        with self.lock:
            d = self._read_dict()
            del d[key]
            self._write_dict(d)
        if key in self._nested_cache:
            del self._nested_cache[key]

    def __iter__(self):
        with self.lock:
            d = self._read_dict()
            return iter(d.copy())

    def __len__(self):
        with self.lock:
            d = self._read_dict()
            return len(d)

    def __repr__(self):
        with self.lock:
            d = self._read_dict()
            return repr(d)

    def clear(self):
        """Clear the entire dictionary."""
        with self.lock:
            self._write_dict({})
        self._nested_cache.clear()

    def update(self, *args, **kwargs):
        """Update the dictionary with provided key/value pairs."""
        with self.lock:
            d = self._read_dict()
            d.update(*args, **kwargs)
            self._write_dict(d)

    def close(self):
        """Close the underlying shared memory."""
        self.shm.close()

    def unlink(self):
        """Unlink (destroy) the underlying shared memory (do this only when safe)."""
        self.shm.unlink()

    # --- Context Manager ---
    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()

    # --- Pickling support ---
    def __reduce__(self):
        """
        When pickled, only the safe shared memory name and size are saved.
        _rebuild then reattaches and reinitializes the lock.
        """
        return (self.__class__._rebuild, (self.shm.name, self.size))

    @classmethod
    def _rebuild(cls, shm_name, size):
        instance = cls(name=shm_name, size=size, create=False)
        return instance

    # --- Auto-create missing keys ---
    def __missing__(self, key):
        """
        Handle missing keys.
        If the key is in the container list, create a plain dict.
        Otherwise, create a nested MorPyDict if auto_create_missing is enabled.
        """
        CONTAINER_KEYS = {"process_q", "obj_ref"}  # Added 'obj_ref' here

        # Handle container keys that are known to be dictionaries
        if key in CONTAINER_KEYS:
            value = {}
            with self.lock:
                d = self._read_dict()
                d[key] = value
                self._write_dict(d)
            return value

        # For all other keys, auto-create a nested MorPyDict if allowed.
        if self.auto_create_missing:
            new_mp = MorPyDict(size=self.size, create=True, **self._init_kwargs)
            self._nested_cache[key] = new_mp
            marker = ("MORPYDICT", new_mp.shm.name, new_mp.size)
            with self.lock:
                for _ in range(3):
                    try:
                        d = self._read_dict()
                        d[key] = marker
                        self._write_dict(d)
                        break
                    except Exception:
                        time.sleep(0.001)
                else:
                    raise KeyError(f"Failed to create key {key}")
            return new_mp
        else:
            raise KeyError(key)