r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Unit tests for the morPy framework. These tests have
            to be conducted outside the framework context, as their
            function is too basic.
"""

import sys
import pathlib
import os
import importlib
import traceback
import unittest

def immediate_output(message):

    r"""
    Print to console when a message is executed, rather than being
    interrupted and ripped apart by other prints.
    """

    print(message)
    sys.stdout.flush()

if __name__ == "__main__":

    r"""
    This is the unit test routine for the most basic classes and functions, that
    have to be tested outside of the morPy framework. At the heart of the framework
    stands the app_dict that is being sub-classed several layers. These layers
    have to be tested and debugged one by one. The testing agenda is:
        1) cl_attr_guard():
            guard attributes of a base class against
            attribute changes of sub-classes
        2) cl_shared_dict(dict):
            Shared memory dictionary to support multiprocessing. Pickling
            is avoided for simple data types. Complex types are pickled, with exceptions to
            non-picklable objects/data.
        3) cl_mem_managed_dict(cl_shared_dict):
            Sub-class of cl_shared_dict(dict), that adds memory management capabilities.
        4) cl_mpy_dict(cl_mem_managed_dict):
            Sub-class of cl_mem_managed_dict(cl_shared_dict), that adds locking mechanisms
            in order to maintain the structure and integrity of app_dict.
    """

    base_path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()
    sys.path.append(os.path.join(f'{base_path}'))
    sys.path.append(os.path.join(f'{base_path}', 'lib'))
    sys.path.append(os.path.join(f'{base_path}', 'loc'))
    sys.path.append(os.path.join(f'{base_path}', 'res', 'ut'))
    sys.path.append(os.path.join(f'{base_path}', 'res', 'ut-preinit'))

    final_report_header = 'The morPy pre-initialization unit tests\nhave finished.'
    final_report = ''

    # List of test modules to run
    test_modules = ['cl_attr_guard_test', 'cl_mpy_dict_root_test']

    # Initialize a flag to track overall success
    all_tests_passed = True

    for subject in test_modules:

        try:
            immediate_output(f'\n\n{subject} >>> IMPORT')

            # Import the test module
            test_module = importlib.import_module(subject)
            immediate_output(f'\n{subject} >>> IMPORT DONE')

        except Exception as e:
            all_tests_passed = False
            message = f'{subject} >>> FAILED TO IMPORT: {e}'
            final_report += f'{message}\n'
            immediate_output(message)
            # Print the full traceback
            traceback.print_exc()
            break

        try:
            # Load tests from the module
            suite = unittest.TestLoader().loadTestsFromModule(test_module)

            # Create a test runner and run the suite
            runner = unittest.TextTestRunner(verbosity=2)
            immediate_output(f'{subject} >>> RUN TEST')
            result = runner.run(suite)
            immediate_output(f'{subject} >>> FINISHED TEST')

            if result.wasSuccessful():
                # Proceed with further testing or execution
                message = f'{subject} >>> PASSED'
                final_report += f'{message}\n'
                immediate_output(message)
            else:
                # Record that not all tests passed
                all_tests_passed = False
                # Log failures and errors
                message = f'{subject} >>> FAILED\nFailures: {len(result.failures)}\nErrors: {len(result.errors)}'
                final_report += f'{message}\n'
                break

        except Exception as e:
            all_tests_passed = False
            message = f'{subject} >>> FAILED TO IMPORT: {e}'
            final_report += f'{message}\n'
            immediate_output(message)
            # Print the full traceback
            traceback.print_exc()
            break

    # Final report
    if all_tests_passed:
        immediate_output(f'\n{40*"#"}\n{final_report_header}\n{16*"#"} PASSED {16*"#"}\n')
        immediate_output(final_report)
    else:
        immediate_output(f'\n{40*"#"}\n{final_report_header}\n{16*"#"} FAILED {16*"#"}\n')
        immediate_output(final_report)
        sys.exit(1)  # Exit with non-zero status code to indicate failure