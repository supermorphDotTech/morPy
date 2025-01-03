r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Unit tests for the morPy framework.
"""

import mpy_bulk_ops

import unittest
from unittest.mock import patch, MagicMock

class cl_ut_find_replace_saveas(unittest.TestCase):
    r"""
    Unit test class for the find_replace_saveas function.
    """

    def ut_find_replace_saveas_setUp(self):
        r"""
        Set up the testing environment.
        """
        self.mpy_trace = "test_trace"
        self.app_dict = {
            "find_replace_saveas_start": "Operation start.",
            "find_replace_saveas_f_ex_skip": "File already exists. Operation skipped.",
            "find_replace_saveas_tpl_err": "Input must be a tuple of tuples.",
            "err_line": "Line",
            "err_excp": "Exception"
        }
        self.search_obj = MagicMock()
        self.replace_tpl = (("replace1", "with1"), ("replace2", "with2"))
        self.save_as = "/tmp/test_output.txt"
        self.overwrite = 2

    @patch("mpy_bulk_ops.mpy_fct.tracing")
    @patch("mpy_bulk_ops.mpy_msg.log")
    @patch("mpy_bulk_ops.mpy_fct.pathtool")
    @patch("mpy_bulk_ops.mpy_common.fso_delete_file")
    @patch("mpy_bulk_ops.mpy_common.regex_replace")
    @patch("mpy_bulk_ops.mpy_common.textfile_write")
    
    def ut_find_replace_saveas(self, mock_textfile_write, mock_regex_replace, mock_fso_delete_file, mock_pathtool, mock_log, mock_tracing):
        r"""
        Test find_replace_saveas function.
        """
        mock_tracing.return_value = self.mpy_trace
        mock_pathtool.return_value = {"file_exists": False}
        self.search_obj.readlines.return_value = ["Let's replace1 and replace2!"]

        result = mpy_bulk_ops.find_replace_saveas(
            self.mpy_trace,
            self.app_dict,
            self.search_obj,
            self.replace_tpl,
            self.save_as,
            self.overwrite
        )

        self.assertTrue(result['check'])
        mock_tracing.assert_called_once_with('mpy_bulk_ops', 'find_replace_saveas(~)', self.mpy_trace)
        mock_log.assert_any_call(self.mpy_trace, self.app_dict, self.app_dict["find_replace_saveas_start"], 'debug')
        mock_regex_replace.assert_any_call(self.mpy_trace, self.app_dict, "Let's replace1 and replace2!", "replace1", "with1")
        mock_textfile_write.assert_called()

    @patch("mpy_bulk_ops.mpy_msg.log")
    @patch("mpy_bulk_ops.mpy_fct.pathtool")
    
    def ut_find_replace_saveas_file_exists_no_overwrite(self, mock_pathtool, mock_log):
        r"""
        Test scenario where the file exists and overwrite is False.
        """
        mock_pathtool.return_value = {"file_exists": True}
        
        result = mpy_bulk_ops.find_replace_saveas(
            self.mpy_trace,
            self.app_dict,
            self.search_obj,
            self.replace_tpl,
            self.save_as,
            overwrite=False
        )

        self.assertFalse(result['check'])
        mock_log.assert_any_call(self.mpy_trace, self.app_dict, self.app_dict["find_replace_saveas_f_ex_skip"], 'warning')

    @patch("mpy_bulk_ops.mpy_msg.log")
    
    def ut_find_replace_saveas_invalid_replace_tpl(self, mock_log):
        r"""
        Test scenario where replace_tpl is not a tuple of tuples.
        """
        invalid_replace_tpl = ("not_a_tuple_of_tuples",)

        result = mpy_bulk_ops.find_replace_saveas(
            self.mpy_trace,
            self.app_dict,
            self.search_obj,
            invalid_replace_tpl,
            self.save_as,
            self.overwrite
        )

        self.assertFalse(result['check'])
        mock_log.assert_any_call(self.mpy_trace, self.app_dict, self.app_dict["find_replace_saveas_tpl_err"], 'error')