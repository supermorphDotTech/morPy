r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Unittests for the cl_mpy_dict() class and it's nested
            dictionary classes of cl_mpy_dict().
"""

import unittest

from mpy_dict import cl_mpy_dict
from unittest.mock import patch, MagicMock


class cl_mpy_dict_test(unittest.TestCase):

    def setUp(self):
        # Mock mpy_conf and mpy_msg if they are used in the classes
        patcher_conf = patch('importlib.import_module', return_value=MagicMock())
        self.mock_import_module = patcher_conf.start()
        self.addCleanup(patcher_conf.stop)

        # Initialize dictionaries with different access levels
        self.normal_dict = cl_mpy_dict(name='NormalDict', access='normal')
        self.tightened_dict = cl_mpy_dict(name='TightenedDict', access='tightened')
        self.locked_dict = cl_mpy_dict(name='LockedDict', access='locked')

        # Pre-populate tightened and locked dictionaries with some data
        self.tightened_dict['existing_key'] = 'existing_value'
        self.locked_dict['existing_key'] = 'existing_value'

    def test_initialization_normal(self):
        self.assertEqual(self.normal_dict._access, 'normal')
        self.assertEqual(self.normal_dict._name, 'NormalDict')
        self.assertEqual(len(self.normal_dict), 0)

    def test_initialization_tightened(self):
        self.assertEqual(self.tightened_dict._access, 'tightened')
        self.assertEqual(self.tightened_dict._name, 'TightenedDict')
        self.assertIn('existing_key', self.tightened_dict)

    def test_initialization_locked(self):
        self.assertEqual(self.locked_dict._access, 'locked')
        self.assertEqual(self.locked_dict._name, 'LockedDict')
        self.assertIn('existing_key', self.locked_dict)

    def test_setitem_normal(self):
        self.normal_dict['key1'] = 'value1'
        self.assertIn('key1', self.normal_dict)
        self.assertEqual(self.normal_dict['key1'], 'value1')

    def test_setitem_tightened_existing_key(self):
        self.tightened_dict['existing_key'] = 'new_value'
        self.assertEqual(self.tightened_dict['existing_key'], 'new_value')

    def test_setitem_tightened_new_key(self):
        with self.assertRaises(PermissionError) as context:
            self.tightened_dict['new_key'] = 'value'
        self.assertIn('Prohibited method', str(context.exception))
        self.assertNotIn('new_key', self.tightened_dict)

    def test_setitem_locked(self):
        with self.assertRaises(PermissionError) as context:
            self.locked_dict['existing_key'] = 'new_value'
        self.assertIn('Prohibited method', str(context.exception))
        self.assertEqual(self.locked_dict['existing_key'], 'existing_value')

    def test_setitem_non_string_key(self):
        with self.assertRaises(TypeError) as context:
            self.normal_dict[123] = 'value'
        self.assertIn('Keys must be strings.', str(context.exception))

    def test_getitem_normal(self):
        self.normal_dict['key1'] = 'value1'
        self.assertEqual(self.normal_dict['key1'], 'value1')

    def test_getitem_non_string_key(self):
        with self.assertRaises(TypeError) as context:
            _ = self.normal_dict[123]
        self.assertIn('Keys must be strings.', str(context.exception))

    def test_delitem_normal(self):
        self.normal_dict['key_to_delete'] = 'value'
        del self.normal_dict['key_to_delete']
        self.assertNotIn('key_to_delete', self.normal_dict)

    def test_delitem_tightened(self):
        with self.assertRaises(PermissionError) as context:
            del self.tightened_dict['existing_key']
        self.assertIn('Prohibited method', str(context.exception))
        self.assertIn('existing_key', self.tightened_dict)

    def test_delitem_locked(self):
        with self.assertRaises(PermissionError) as context:
            del self.locked_dict['existing_key']
        self.assertIn('Prohibited method', str(context.exception))
        self.assertIn('existing_key', self.locked_dict)

    def test_clear_normal(self):
        self.normal_dict['key1'] = 'value1'
        self.normal_dict.clear()
        self.assertEqual(len(self.normal_dict), 0)

    def test_clear_tightened(self):
        with self.assertRaises(PermissionError) as context:
            self.tightened_dict.clear()
        self.assertIn('Prohibited method', str(context.exception))
        self.assertGreater(len(self.tightened_dict), 0)

    def test_clear_locked(self):
        with self.assertRaises(PermissionError) as context:
            self.locked_dict.clear()
        self.assertIn('Prohibited method', str(context.exception))
        self.assertGreater(len(self.locked_dict), 0)

    def test_pop_normal_existing_key(self):
        self.normal_dict['key1'] = 'value1'
        value = self.normal_dict.pop('key1')
        self.assertEqual(value, 'value1')
        self.assertNotIn('key1', self.normal_dict)

    def test_pop_normal_non_existing_key_with_default(self):
        value = self.normal_dict.pop('non_existing', 'default')
        self.assertEqual(value, 'default')

    def test_pop_tightened(self):
        with self.assertRaises(PermissionError) as context:
            self.tightened_dict.pop('existing_key')
        self.assertIn('Prohibited method', str(context.exception))

    def test_pop_locked(self):
        with self.assertRaises(PermissionError) as context:
            self.locked_dict.pop('existing_key')
        self.assertIn('Prohibited method', str(context.exception))

    def test_pop_non_string_key(self):
        with self.assertRaises(TypeError) as context:
            self.normal_dict.pop(123)
        self.assertIn('Keys must be strings.', str(context.exception))

    def test_popitem_normal(self):
        self.normal_dict['key1'] = 'value1'
        self.normal_dict['key2'] = 'value2'
        key, value = self.normal_dict.popitem()
        self.assertIn(key, ['key1', 'key2'])
        self.assertIn(value, ['value1', 'value2'])
        self.assertNotIn(key, self.normal_dict)

    def test_popitem_tightened(self):
        self.tightened_dict['another_key'] = 'another_value'
        with self.assertRaises(PermissionError) as context:
            self.tightened_dict.popitem()
        self.assertIn('Prohibited method', str(context.exception))

    def test_popitem_locked(self):
        self.locked_dict['another_key'] = 'another_value'
        with self.assertRaises(PermissionError) as context:
            self.locked_dict.popitem()
        self.assertIn('Prohibited method', str(context.exception))

    def test_popitem_empty_locked_or_tightened(self):
        empty_tightened = cl_mpy_dict(name='EmptyTightened', access='tightened')
        with self.assertRaises(PermissionError):
            empty_tightened.popitem()

        empty_locked = cl_mpy_dict(name='EmptyLocked', access='locked')
        with self.assertRaises(PermissionError):
            empty_locked.popitem()

    def test_update_normal(self):
        self.normal_dict.update({'key1': 'value1', 'key2': 'value2'})
        self.assertIn('key1', self.normal_dict)
        self.assertIn('key2', self.normal_dict)

    def test_update_tightened_existing_keys(self):
        self.tightened_dict.update({'existing_key': 'new_value'})
        self.assertEqual(self.tightened_dict['existing_key'], 'new_value')

    def test_update_tightened_new_keys(self):
        with self.assertRaises(PermissionError) as context:
            self.tightened_dict.update({'new_key': 'value'})
        self.assertIn('Prohibited method', str(context.exception))
        self.assertNotIn('new_key', self.tightened_dict)

    def test_update_locked(self):
        with self.assertRaises(PermissionError) as context:
            self.locked_dict.update({'existing_key': 'new_value'})
        self.assertIn('Prohibited method', str(context.exception))
        self.assertEqual(self.locked_dict['existing_key'], 'existing_value')

    def test_update_non_string_key(self):
        with self.assertRaises(TypeError):
            self.normal_dict.update({123: 'value'})

    def test_setdefault_normal_existing_key(self):
        self.normal_dict['key1'] = 'value1'
        result = self.normal_dict.setdefault('key1', 'new_value')
        self.assertEqual(result, 'value1')
        self.assertEqual(self.normal_dict['key1'], 'value1')

    def test_setdefault_normal_new_key(self):
        result = self.normal_dict.setdefault('new_key', 'value')
        self.assertEqual(result, 'value')
        self.assertIn('new_key', self.normal_dict)

    def test_setdefault_tightened_existing_key(self):
        self.tightened_dict['existing_key'] = 'value'
        result = self.tightened_dict.setdefault('existing_key', 'new_value')
        self.assertEqual(result, 'value')

    def test_setdefault_tightened_new_key(self):
        with self.assertRaises(PermissionError) as context:
            self.tightened_dict.setdefault('new_key', 'value')
        self.assertIn('Prohibited method', str(context.exception))
        self.assertNotIn('new_key', self.tightened_dict)

    def test_setdefault_locked_existing_key(self):
        self.locked_dict['existing_key'] = 'value'
        result = self.locked_dict.setdefault('existing_key', 'new_value')
        self.assertEqual(result, 'value')

    def test_setdefault_locked_new_key(self):
        with self.assertRaises(PermissionError) as context:
            self.locked_dict.setdefault('new_key', 'value')
        self.assertIn('Prohibited method', str(context.exception))
        self.assertNotIn('new_key', self.locked_dict)

    def test_setdefault_non_string_key(self):
        with self.assertRaises(TypeError):
            self.normal_dict.setdefault(123, 'value')

    def test_repr_normal(self):
        self.normal_dict['key1'] = 'value1'
        repr_str = repr(self.normal_dict)
        self.assertIn('name=NormalDict', repr_str)
        self.assertIn('access=normal', repr_str)
        self.assertIn("'key1': 'value1'", repr_str)

    def test_repr_tightened(self):
        repr_str = repr(self.tightened_dict)
        self.assertIn('name=TightenedDict', repr_str)
        self.assertIn('access=tightened', repr_str)

    def test_repr_locked(self):
        repr_str = repr(self.locked_dict)
        self.assertIn('name=LockedDict', repr_str)
        self.assertIn('access=locked', repr_str)

    def test_keys_must_be_strings(self):
        with self.assertRaises(TypeError):
            self.normal_dict[1] = 'one'
        with self.assertRaises(TypeError):
            _ = self.normal_dict[1]

    def test_len_and_containment(self):
        self.normal_dict['key1'] = 'value1'
        self.normal_dict['key2'] = 'value2'
        self.assertEqual(len(self.normal_dict), 2)
        self.assertIn('key1', self.normal_dict)
        self.assertNotIn('key3', self.normal_dict)

    def test_iteration(self):
        self.normal_dict['key1'] = 'value1'
        self.normal_dict['key2'] = 'value2'
        keys = set()
        for key in self.normal_dict:
            keys.add(key)
        self.assertEqual(keys, {'key1', 'key2'})

    def test_get_recurse_register(self):
        # Assuming get_recurse_register returns None if not set
        self.assertIsNone(self.normal_dict.get_recurse_register())

    def test_print_status(self):
        # Assuming print_status returns some status string, mock if necessary
        # Here we just check that it doesn't raise an error
        try:
            status = self.normal_dict.print_status()
        except Exception as e:
            self.fail(f'print_status() raised an exception: {e}')