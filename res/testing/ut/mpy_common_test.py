r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Unit tests for the morPy framework.
"""

import mpy_common

import io
import unittest
from unittest.mock import patch, MagicMock

class cl_ut_decode_to_plain_text(unittest.TestCase):
    
    @patch('mpy_common.mpy_fct.tracing')  # Replace with actual module name
    @patch('mpy_common.mpy_msg.log')  # Replace with actual module name
    def ut_decode_to_plain_text_utf8(self, mock_log, mock_tracing):
        # Test decoding with UTF-8 encoding
        mpy_trace = {}
        app_dict = {"loc": {"mpy": {"decode_to_plain_text_from": "Decoded from", 
                                    "decode_to_plain_text_to": "to plain text",
                                    "decode_to_plain_text_not": "Input is not decoded",
                                    "err_line": "Error on line",
                                    "err_excp": "Exception occurred"}}}
        src_input = io.BytesIO(b'Hello World\nThis is a test\n')
        encoding = 'utf-8'
        
        result = mpy_common.decode_to_plain_text(mpy_trace, app_dict, src_input, encoding)
        
        self.assertEqual(result['encoding'], 'utf-8')
        self.assertEqual(result['lines'], 2)
        self.assertEqual(result['result'].read(), 'Hello World\nThis is a test\n')

    @patch('mpy_common.mpy_fct.tracing')  # Replace with actual module name
    @patch('mpy_common.mpy_msg.log')  # Replace with actual module name
    def ut_decode_to_plain_text_autodetect(self, mock_log, mock_tracing):
        # Test auto-detection of encoding
        mpy_trace = {}
        app_dict = {"loc": {"mpy": {"decode_to_plain_text_from": "Decoded from", 
                                    "decode_to_plain_text_to": "to plain text",
                                    "decode_to_plain_text_not": "Input is not decoded",
                                    "err_line": "Error on line",
                                    "err_excp": "Exception occurred"}}}
        src_input = io.BytesIO('Hello World\nThis is a test\n'.encode('utf-16-le'))
        encoding = ''
        
        result = mpy_common.decode_to_plain_text(mpy_trace, app_dict, src_input, encoding)
        
        self.assertEqual(result['encoding'], 'UTF-16LE')
        self.assertEqual(result['lines'], 2)
        self.assertEqual(result['result'].read(), 'Hello World\nThis is a test\n')

    @patch('mpy_common.mpy_fct.tracing')  # Replace with actual module name
    @patch('mpy_common.mpy_msg.log')  # Replace with actual module name
    def ut_decode_to_plain_text_invalid_encoding(self, mock_log, mock_tracing):
        # Test handling of invalid encoding
        mpy_trace = {}
        app_dict = {"loc": {"mpy": {"decode_to_plain_text_from": "Decoded from", 
                                    "decode_to_plain_text_to": "to plain text",
                                    "decode_to_plain_text_not": "Input is not decoded",
                                    "err_line": "Error on line",
                                    "err_excp": "Exception occurred"}}}
        src_input = io.BytesIO(b'Hello World\nThis is a test\n')
        encoding = 'invalid-encoding'
        
        result = mpy_common.decode_to_plain_text(mpy_trace, app_dict, src_input, encoding)
        
        self.assertEqual(result['encoding'], 'invalid-encoding')
        self.assertEqual(result['lines'], 2)
        self.assertEqual(result['result'].read(), 'Hello World\nThis is a test\n')

    @patch('mpy_common.mpy_fct.tracing')  # Replace with actual module name
    @patch('mpy_common.mpy_msg.log')  # Replace with actual module name
    def ut_decode_to_plain_text_no_encoding(self, mock_log, mock_tracing):
        # Test when no encoding is provided
        mpy_trace = {}
        app_dict = {"loc": {"mpy": {"decode_to_plain_text_from": "Decoded from", 
                                    "decode_to_plain_text_to": "to plain text",
                                    "decode_to_plain_text_not": "Input is not decoded",
                                    "err_line": "Error on line",
                                    "err_excp": "Exception occurred"}}}
        src_input = io.BytesIO(b'Hello World\nThis is a test\n')
        encoding = ''
        
        result = mpy_common.decode_to_plain_text(mpy_trace, app_dict, src_input, encoding)
        
        self.assertIsNotNone(result['encoding'])
        self.assertEqual(result['lines'], 2)
        self.assertEqual(result['result'].read(), 'Hello World\nThis is a test\n')
        
class cl_ut_dialog_sel_file(unittest.TestCase):

    @patch('mpy_common.mpy_fct.tracing')
    @patch('mpy_common.mpy_fct.pathtool')
    @patch('mpy_common.mpy_msg.log')
    @patch('mpy_common.filedialog.askopenfilename')
    @patch('mpy_common.Tk')
    def ut_dialog_sel_file_file_selected(self, mock_tk, mock_askopenfilename, mock_log, mock_pathtool, mock_tracing):
        # Mocking initial parameters
        mpy_trace = "mock_trace"
        app_dict = {
            "loc": {
                "mpy": {
                    "dialog_sel_file_nosel": "No file selected",
                    "dialog_sel_file_choice": "Choice",
                    "dialog_sel_file_cancel": "Canceled",
                    "dialog_sel_file_asel": "A file was selected",
                    "dialog_sel_file_open": "Opened",
                    "err_line": "Error line",
                    "err_excp": "Exception"
                }
            }
        }
        init_dir = "/mock/dir"
        ftypes = (('PDF', '*.pdf'), ('Textfile', '*.txt'), ('All Files', '*.*'))
        title = "Select a file..."

        # Setting up mocks
        mock_tracing.return_value = mpy_trace
        mock_askopenfilename.return_value = "/mock/dir/mock_file.pdf"
        mock_tk_instance = MagicMock()
        mock_tk.return_value = mock_tk_instance

        # Call the function
        result = mpy_common.dialog_sel_file(mpy_trace, app_dict, init_dir, ftypes, title)

        # Assertions
        self.assertTrue(result['check'])
        self.assertEqual(result['sel_file'], "/mock/dir/mock_file.pdf")
        self.assertTrue(result['file_selected'])
        mock_tracing.assert_called_once_with('mpy_common', 'dialog_sel_file(~)', mpy_trace)
        mock_log.assert_called_once()
        mock_pathtool.assert_called_once_with(mpy_trace, "/mock/dir/mock_file.pdf")
        mock_tk_instance.withdraw.assert_called_once()
        mock_tk_instance.attributes.assert_called_once_with("-topmost", True)

    @patch('mpy_common.mpy_fct.tracing')
    @patch('mpy_common.mpy_msg.log')
    @patch('mpy_common.filedialog.askopenfilename')
    @patch('mpy_common.Tk')
    def ut_dialog_sel_file_no_file_selected(self, mock_tk, mock_askopenfilename, mock_log, mock_tracing):
        # Mocking initial parameters
        mpy_trace = "mock_trace"
        app_dict = {
            "loc": {
                "mpy": {
                    "dialog_sel_file_nosel": "No file selected",
                    "dialog_sel_file_choice": "Choice",
                    "dialog_sel_file_cancel": "Canceled",
                    "dialog_sel_file_asel": "A file was selected",
                    "dialog_sel_file_open": "Opened",
                    "err_line": "Error line",
                    "err_excp": "Exception"
                }
            }
        }
        init_dir = "/mock/dir"
        ftypes = (('PDF', '*.pdf'), ('Textfile', '*.txt'), ('All Files', '*.*'))
        title = "Select a file..."

        # Setting up mocks
        mock_tracing.return_value = mpy_trace
        mock_askopenfilename.return_value = ""
        mock_tk_instance = MagicMock()
        mock_tk.return_value = mock_tk_instance

        # Call the function
        result = mpy_common.dialog_sel_file(mpy_trace, app_dict, init_dir, ftypes, title)

        # Assertions
        self.assertFalse(result['check'])
        self.assertEqual(result['sel_file'], "")
        self.assertFalse(result['file_selected'])
        mock_tracing.assert_called_once_with('mpy_common', 'dialog_sel_file(~)', mpy_trace)
        mock_log.assert_called_once()
        mock_tk_instance.withdraw.assert_called_once()
        mock_tk_instance.attributes.assert_called_once_with("-topmost", True)
        
class cl_ut_dialog_sel_dir(unittest.TestCase):

    @patch('mpy_common.mpy_fct.tracing')
    @patch('mpy_common.mpy_fct.pathtool')
    @patch('mpy_common.mpy_msg.log')
    @patch('mpy_common.filedialog.askdirectory')
    @patch('mpy_common.Tk')
    def ut_dialog_sel_dir_directory_selected(self, mock_tk, mock_askdirectory, mock_log, mock_pathtool, mock_tracing):
        # Mocking initial parameters
        mpy_trace = "mock_trace"
        app_dict = {
            "loc": {
                "mpy": {
                    "dialog_sel_dir_nosel": "No directory selected",
                    "dialog_sel_dir_choice": "Choice",
                    "dialog_sel_dir_cancel": "Canceled",
                    "dialog_sel_dir_asel": "A directory was selected",
                    "dialog_sel_dir_open": "Opened",
                    "err_line": "Error line",
                    "err_excp": "Exception"
                }
            }
        }
        init_dir = "/mock/dir"
        title = "Select a directory..."

        # Setting up mocks
        mock_tracing.return_value = mpy_trace
        mock_askdirectory.return_value = "/mock/dir/selected_dir"
        mock_tk_instance = MagicMock()
        mock_tk.return_value = mock_tk_instance

        # Call the function
        result = mpy_common.dialog_sel_dir(mpy_trace, app_dict, init_dir, title)

        # Assertions
        self.assertTrue(result['check'])
        self.assertEqual(result['sel_dir'], "/mock/dir/selected_dir")
        self.assertTrue(result['dir_selected'])
        mock_tracing.assert_called_once_with('mpy_common', 'dialog_sel_dir(~)', mpy_trace)
        mock_log.assert_called_once()
        mock_pathtool.assert_called_once_with(mpy_trace, "/mock/dir/selected_dir")
        mock_tk_instance.withdraw.assert_called_once()

    @patch('mpy_common.mpy_fct.tracing')
    @patch('mpy_common.mpy_msg.log')
    @patch('mpy_common.filedialog.askdirectory')
    @patch('mpy_common.Tk')
    def ut_dialog_sel_dir_no_directory_selected(self, mock_tk, mock_askdirectory, mock_log, mock_tracing):
        # Mocking initial parameters
        mpy_trace = "mock_trace"
        app_dict = {
            "loc": {
                "mpy": {
                    "dialog_sel_dir_nosel": "No directory selected",
                    "dialog_sel_dir_choice": "Choice",
                    "dialog_sel_dir_cancel": "Canceled",
                    "dialog_sel_dir_asel": "A directory was selected",
                    "dialog_sel_dir_open": "Opened",
                    "err_line": "Error line",
                    "err_excp": "Exception"
                }
            }
        }
        init_dir = "/mock/dir"
        title = "Select a directory..."

        # Setting up mocks
        mock_tracing.return_value = mpy_trace
        mock_askdirectory.return_value = ""
        mock_tk_instance = MagicMock()
        mock_tk.return_value = mock_tk_instance

        # Call the function
        result = mpy_common.dialog_sel_dir(mpy_trace, app_dict, init_dir, title)

        # Assertions
        self.assertFalse(result['check'])
        self.assertEqual(result['sel_dir'], "")
        self.assertFalse(result['dir_selected'])
        mock_tracing.assert_called_once_with('mpy_common', 'dialog_sel_dir(~)', mpy_trace)
        mock_log.assert_called_once()
        mock_tk_instance.withdraw.assert_called_once()