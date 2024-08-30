"""
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
    
    @patch('your_module_name.mpy_fct.tracing')  # Replace with actual module name
    @patch('your_module_name.mpy_msg.log')  # Replace with actual module name
    def ut_decode_to_plain_text_utf8(self, mock_log, mock_tracing):
        # Test decoding with UTF-8 encoding
        mpy_trace = {}
        prj_dict = {"loc": {"mpy": {"decode_to_plain_text_from": "Decoded from", 
                                    "decode_to_plain_text_to": "to plain text",
                                    "decode_to_plain_text_not": "Input is not decoded",
                                    "err_line": "Error on line",
                                    "err_excp": "Exception occurred"}}}
        src_input = io.BytesIO(b'Hello World\nThis is a test\n')
        encoding = 'utf-8'
        
        result = mpy_common.decode_to_plain_text(mpy_trace, prj_dict, src_input, encoding)
        
        self.assertEqual(result['encoding'], 'utf-8')
        self.assertEqual(result['lines'], 2)
        self.assertEqual(result['result'].read(), 'Hello World\nThis is a test\n')

    @patch('your_module_name.mpy_fct.tracing')  # Replace with actual module name
    @patch('your_module_name.mpy_msg.log')  # Replace with actual module name
    def ut_decode_to_plain_text_autodetect(self, mock_log, mock_tracing):
        # Test auto-detection of encoding
        mpy_trace = {}
        prj_dict = {"loc": {"mpy": {"decode_to_plain_text_from": "Decoded from", 
                                    "decode_to_plain_text_to": "to plain text",
                                    "decode_to_plain_text_not": "Input is not decoded",
                                    "err_line": "Error on line",
                                    "err_excp": "Exception occurred"}}}
        src_input = io.BytesIO('Hello World\nThis is a test\n'.encode('utf-16-le'))
        encoding = ''
        
        result = mpy_common.decode_to_plain_text(mpy_trace, prj_dict, src_input, encoding)
        
        self.assertEqual(result['encoding'], 'UTF-16LE')
        self.assertEqual(result['lines'], 2)
        self.assertEqual(result['result'].read(), 'Hello World\nThis is a test\n')

    @patch('your_module_name.mpy_fct.tracing')  # Replace with actual module name
    @patch('your_module_name.mpy_msg.log')  # Replace with actual module name
    def ut_decode_to_plain_text_invalid_encoding(self, mock_log, mock_tracing):
        # Test handling of invalid encoding
        mpy_trace = {}
        prj_dict = {"loc": {"mpy": {"decode_to_plain_text_from": "Decoded from", 
                                    "decode_to_plain_text_to": "to plain text",
                                    "decode_to_plain_text_not": "Input is not decoded",
                                    "err_line": "Error on line",
                                    "err_excp": "Exception occurred"}}}
        src_input = io.BytesIO(b'Hello World\nThis is a test\n')
        encoding = 'invalid-encoding'
        
        result = mpy_common.decode_to_plain_text(mpy_trace, prj_dict, src_input, encoding)
        
        self.assertEqual(result['encoding'], 'invalid-encoding')
        self.assertEqual(result['lines'], 2)
        self.assertEqual(result['result'].read(), 'Hello World\nThis is a test\n')

    @patch('your_module_name.mpy_fct.tracing')  # Replace with actual module name
    @patch('your_module_name.mpy_msg.log')  # Replace with actual module name
    def ut_decode_to_plain_text_no_encoding(self, mock_log, mock_tracing):
        # Test when no encoding is provided
        mpy_trace = {}
        prj_dict = {"loc": {"mpy": {"decode_to_plain_text_from": "Decoded from", 
                                    "decode_to_plain_text_to": "to plain text",
                                    "decode_to_plain_text_not": "Input is not decoded",
                                    "err_line": "Error on line",
                                    "err_excp": "Exception occurred"}}}
        src_input = io.BytesIO(b'Hello World\nThis is a test\n')
        encoding = ''
        
        result = mpy_common.decode_to_plain_text(mpy_trace, prj_dict, src_input, encoding)
        
        self.assertIsNotNone(result['encoding'])
        self.assertEqual(result['lines'], 2)
        self.assertEqual(result['result'].read(), 'Hello World\nThis is a test\n')