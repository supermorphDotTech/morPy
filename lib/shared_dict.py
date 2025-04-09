r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Shared dictionary for morPy.
"""

import pickle
import os
import uuid
import struct
import multiprocessing
from multiprocessing import shared_memory
from collections.abc import MutableMapping

DEFAULT_DATA_SIZE = 10_240  # bytes for the pickled dict; adjust as needed.
CONTROL_SIZE = 16  # bytes used for control data (here we only store an integer version)

class SharedDict(MutableMapping):
    """
    SharedDict

    A high-performance shared-memory dictionary that can be attached across
    multiple processes without a separate managing process.

    Key features:
      - Uses separate shared memory blocks for control (metadata) and data.
      - Employs a fast interprocess lock (multiprocessing.Lock) for atomic updates.
      - Maintains a local cache, and on each operation, synchronizes any pending updates.
      - Supports basic dictionary operations. In-place modifications (e.g. on mutable values)
        require using special wrappers or explicit calls to sync().

    This implementation is completely independent and legally detached from UltraDict.
    """
    def __init__(self, name=None, create=True, data_size=DEFAULT_DATA_SIZE):
        self.lock = multiprocessing.Lock()

        # Determine names for shared memory segments.
        # Use the provided base name or generate a unique one.
        if name is None:
            name = uuid.uuid4().hex
        self.base_name = name
        self.ctrl_name = f"{name}_ctrl"
        self.data_name = f"{name}_data"
        self.data_size = data_size

        if create:
            # Create shared memory segments.
            # Control segment holds a single unsigned int (4 bytes) as version.
            try:
                self.shm_ctrl = shared_memory.SharedMemory(name=self.ctrl_name, create=True, size=CONTROL_SIZE)
                self.shm_data = shared_memory.SharedMemory(name=self.data_name, create=True, size=self.data_size)
            except FileExistsError:
                raise RuntimeError(f"Shared memory with base name '{name}' already exists")
            # Initialize control (set version to 0)
            with self.lock:
                self._set_version(0)
            # Initialize data: start with an empty dict.
            self._local_cache = {}
            self._write_data(self._local_cache)
            self._version = 0
        else:
            # Attach to existing shared memory segments.
            try:
                self.shm_ctrl = shared_memory.SharedMemory(name=self.ctrl_name, create=False)
                self.shm_data = shared_memory.SharedMemory(name=self.data_name, create=False)
            except FileNotFoundError:
                raise RuntimeError(f"Shared memory with base name '{name}' not found")
            # Load the current state.
            self._local_cache, self._version = self._read_data()

    @property
    def ctrl_buf(self):
        return self.shm_ctrl.buf

    @property
    def data_buf(self):
        return self.shm_data.buf

    def _set_version(self, version):
        # Store version as 4-byte little-endian integer at beginning of control buffer.
        self.ctrl_buf[:4] = version.to_bytes(4, byteorder='little')

    def _get_version(self):
        return int.from_bytes(self.ctrl_buf[:4], byteorder='little')

    def _write_data(self, d):
        # Serialize the dict using pickle.
        data_bytes = pickle.dumps(d)
        if len(data_bytes) > self.data_size:
            raise MemoryError(f"Pickled data size ({len(data_bytes)} bytes) exceeds allocated space ({self.data_size} bytes)")
        # Clear the buffer first.
        self.data_buf[:self.data_size] = b'\x00' * self.data_size
        self.data_buf[:len(data_bytes)] = data_bytes

    def _read_data(self):
        # Read the entire data buffer and remove trailing null bytes.
        data_bytes = bytes(self.data_buf[:self.data_size]).rstrip(b'\x00')
        if data_bytes:
            d = pickle.loads(data_bytes)
        else:
            d = {}
        return d, self._get_version()

    def _sync_from_shared(self):
        """
        Load from the shared memory if there is a newer version available.
        """
        with self.lock:
            current_version = self._get_version()
            if current_version != self._version:
                self._local_cache, self._version = self._read_data()

    def _save_to_shared(self):
        """
        Save the local cache to shared memory, and update the version.
        """
        with self.lock:
            self._write_data(self._local_cache)
            self._version += 1
            self._set_version(self._version)

    def sync(self):
        """
        Public method to force a synchronization from shared memory.
        """
        self._sync_from_shared()

    # --- MutableMapping interface ---
    def __getitem__(self, key):
        self._sync_from_shared()
        return self._local_cache[key]

    def __setitem__(self, key, value):
        self._sync_from_shared()
        self._local_cache[key] = value
        self._save_to_shared()

    def __delitem__(self, key):
        self._sync_from_shared()
        del self._local_cache[key]
        self._save_to_shared()

    def __iter__(self):
        self._sync_from_shared()
        return iter(self._local_cache)

    def __len__(self):
        self._sync_from_shared()
        return len(self._local_cache)

    def __repr__(self):
        self._sync_from_shared()
        return repr(self._local_cache)

    # --- Clean up ---
    def close(self):
        """
        Close the local shared memory segments.
        """
        self.shm_ctrl.close()
        self.shm_data.close()

    def unlink(self):
        """
        Unlink (destroy) the shared memory segments.
        Only call this when you are sure no other process will use them.
        """
        self.shm_ctrl.unlink()
        self.shm_data.unlink()

# -- Example usage --
if __name__ == '__main__':
    import time
    import multiprocessing

    def worker(shared_name):
        # Attach to the existing SharedDict:
        sd = SharedDict(name=shared_name, create=False)
        # Read and update a value:
        sd.sync()
        try:
            counter = sd.get('counter', 0)
        except Exception:
            counter = 0
        print(f"Worker {os.getpid()} read counter: {counter}")
        sd['counter'] = counter + 1
        print(f"Worker {os.getpid()} updated counter to: {sd['counter']}")
        sd.close()

    # Create a SharedDict:
    sd = SharedDict(name="example_shared", create=True)
    sd['counter'] = 0
    print("Initial SharedDict:", sd)

    # Spawn a few worker processes to update the dict:
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=("example_shared",))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # Final value:
    sd.sync()
    print("Final SharedDict:", sd)
    sd.close()

    # If you are the owner, you can unlink the shared memory:
    sd.unlink()
