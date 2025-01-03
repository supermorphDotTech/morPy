import multiprocessing
import unittest
import UltraDict  # Assuming UltraDict is the key focus module

class CLMPYDictTest(unittest.TestCase):
    def setUp(self):
        """Set up the shared UltraDict for testing."""
        self.shared_dict = UltraDict(shared_lock=True)
        self.manager = multiprocessing.Manager()
        self.lock = self.manager.Lock()
        self.cl_mpy_dict_root = UltraDict(shared_lock=True)

    def test_initialization(self):
        """Test initialization of the UltraDict with shared_lock=True."""
        self.assertTrue(self.shared_dict._shared_lock is not None)
        self.assertTrue(self.cl_mpy_dict_root._shared_lock is not None)

    def test_write_and_read(self):
        """Test writing to and reading from UltraDict."""
        key, value = "test_key", "test_value"
        self.shared_dict[key] = value
        self.assertEqual(self.shared_dict[key], value)

    def test_thread_safe_access(self):
        """Test thread-safe access with shared locks."""
        def writer(shared_dict, key, value):
            with shared_dict._shared_lock:
                shared_dict[key] = value

        threads = []
        for i in range(5):
            t = multiprocessing.Process(target=writer, args=(self.shared_dict, f"key_{i}", f"value_{i}"))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Verify all keys are written
        for i in range(5):
            self.assertEqual(self.shared_dict[f"key_{i}"], f"value_{i}")

    def test_nested_dict_operations(self):
        """Test operations with nested dictionaries in UltraDict."""
        nested_key = "nested_dict"
        self.shared_dict[nested_key] = UltraDict(shared_lock=True)

        # Add key-value pairs to the nested dictionary
        nested_dict = self.shared_dict[nested_key]
        nested_dict["sub_key"] = "sub_value"

        self.assertEqual(nested_dict["sub_key"], "sub_value")

    def test_locked_access(self):
        """Test locked access to the UltraDict."""
        def lock_test(shared_dict):
            shared_dict._shared_lock.acquire()
            try:
                shared_dict["locked_key"] = "locked_value"
            finally:
                shared_dict._shared_lock.release()

        lock_test(self.shared_dict)
        self.assertEqual(self.shared_dict["locked_key"], "locked_value")

    def test_process_safety(self):
        """Test process-safe access to UltraDict."""
        def worker_process(shared_dict, lock, key, value):
            with lock:
                shared_dict[key] = value

        processes = []
        for i in range(5):
            p = multiprocessing.Process(target=worker_process, args=(self.shared_dict, self.lock, f"proc_key_{i}", f"proc_value_{i}"))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        # Verify all keys are written
        for i in range(5):
            self.assertEqual(self.shared_dict[f"proc_key_{i}"], f"proc_value_{i}")

if __name__ == "__main__":
    unittest.main()