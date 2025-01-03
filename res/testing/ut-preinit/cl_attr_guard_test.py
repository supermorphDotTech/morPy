r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Unittests for the cl_attr_guard class.
"""

import unittest

from mpy_dict import cl_attr_guard

class cl_attr_guard_test(unittest.TestCase):

    def setUp(self):
        # Define the base class
        class RootClass:
            # Use cl_attr_guard as a class attribute
            guarded_attr = cl_attr_guard("initial_value", "RootClass")

        # Define a subclass
        class SubClass(RootClass):
            pass

        self.RootClass = RootClass
        self.SubClass = SubClass

    def test_rootclass_can_get_attr(self):
        root_instance = self.RootClass()
        self.assertEqual(root_instance.guarded_attr, "initial_value")

    def test_rootclass_can_set_attr(self):
        root_instance = self.RootClass()
        root_instance.guarded_attr = "new_value"
        self.assertEqual(root_instance.guarded_attr, "new_value")

    def test_rootclass_cannot_delete_attr(self):
        root_instance = self.RootClass()
        with self.assertRaises(AttributeError) as context:
            del root_instance.guarded_attr
        self.assertEqual(str(context.exception), "Deletion prohibited!")

    def test_subclass_can_get_attr(self):
        sub_instance = self.SubClass()
        self.assertEqual(sub_instance.guarded_attr, "initial_value")

    def test_subclass_cannot_set_attr(self):
        sub_instance = self.SubClass()
        with self.assertRaises(AttributeError) as context:
            sub_instance.guarded_attr = "new_value"
        expected_error = f'SubClass can not modify an attribute of RootClass'
        self.assertEqual(str(context.exception), expected_error)

    def test_subclass_cannot_delete_attr(self):
        sub_instance = self.SubClass()
        with self.assertRaises(AttributeError) as context:
            del sub_instance.guarded_attr
        self.assertEqual(str(context.exception), "Deletion prohibited!")

    def test_multiple_instances(self):
        root_instance1 = self.RootClass()
        root_instance2 = self.RootClass()
        root_instance1.guarded_attr = "value1"
        root_instance2.guarded_attr = "value2"
        # Since the value is stored in the descriptor, and the descriptor is shared among class instances,
        # the value should be shared among instances
        self.assertEqual(root_instance1.guarded_attr, "value2")
        self.assertEqual(root_instance2.guarded_attr, "value2")

    def test_class_attribute_access(self):
        # Accessing the attribute via the class should get the current value
        self.assertEqual(self.RootClass.guarded_attr, "initial_value")
        # Changing the value via the class should also work
        self.RootClass.guarded_attr = "class_value"
        self.assertEqual(self.RootClass.guarded_attr, "class_value")
        root_instance = self.RootClass()
        self.assertEqual(root_instance.guarded_attr, "class_value")

    def test_subclass_cannot_modify_class_attr(self):
        # Modify the class attribute in the subclass
        self.SubClass.guarded_attr = "new_value"
        # Verify that RootClass.guarded_attr remains unchanged
        self.assertEqual(self.RootClass.guarded_attr, "initial_value")
        # Verify that SubClass.guarded_attr is "new_value"
        self.assertEqual(self.SubClass.guarded_attr, "new_value")

    def test_subclass_cannot_set_instance_attr(self):
        sub_instance = self.SubClass()
        with self.assertRaises(AttributeError) as context:
            sub_instance.guarded_attr = "new_value"
        expected_error = f'SubClass can not modify an attribute of RootClass'
        self.assertEqual(str(context.exception), expected_error)

    def test_deletion_prohibited_in_subclass(self):
        sub_instance = self.SubClass()
        with self.assertRaises(AttributeError) as context:
            del sub_instance.guarded_attr
        self.assertEqual(str(context.exception), "Deletion prohibited!")

    def test_deletion_prohibited_in_rootclass(self):
        root_instance = self.RootClass()
        with self.assertRaises(AttributeError) as context:
            del root_instance.guarded_attr
        self.assertEqual(str(context.exception), "Deletion prohibited!")

    def test_error_message_when_subclass_attempts_modification(self):
        sub_instance = self.SubClass()
        try:
            sub_instance.guarded_attr = "test"
        except AttributeError as e:
            self.assertIn("SubClass can not modify an attribute of RootClass", str(e))

    def test_rootclass_name_change(self):
        # Change the __name__ of RootClass
        original_name = self.RootClass.__name__
        self.RootClass.__name__ = "NewRootClassName"
        root_instance = self.RootClass()
        with self.assertRaises(AttributeError) as context:
            root_instance.guarded_attr = "new_value"
        expected_error = f'NewRootClassName can not modify an attribute of RootClass'
        self.assertEqual(str(context.exception), expected_error)
        # Restore the original name
        self.RootClass.__name__ = original_name

    def test_descriptor_direct_access(self):
        # Directly accessing the descriptor's _value
        descriptor = self.RootClass.__dict__['guarded_attr']
        descriptor._value = "directly_modified_value"
        self.assertEqual(self.RootClass.guarded_attr, "directly_modified_value")
        root_instance = self.RootClass()
        self.assertEqual(root_instance.guarded_attr, "directly_modified_value")