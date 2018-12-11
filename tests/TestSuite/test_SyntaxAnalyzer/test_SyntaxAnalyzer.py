import unittest
import os
from src.SyntaxAnalyzer import SyntaxAnalyzer
from src.__main__ import Main
import CompilerExceptions
import sys


class TestSyntaxAnalyzer(unittest.TestCase):
    def setUp(self):
        self.test_files = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TestTextFiles')
        p_dir = os.path.join(os.path.abspath(__file__), os.pardir, os.pardir)
        self.valid_test_files_instrgen = os.path.join(p_dir, 'test_InstructionGeneration', 'TestTextFiles')

    def helper_valid_files(self):
        for f in os.listdir(self.test_files):
            if f.startswith('test_valid_'):
                yield os.path.join(self.test_files, f)
        for f in os.listdir(self.valid_test_files_instrgen):
            if f.startswith('test_'):
                yield os.path.join(self.valid_test_files_instrgen, f)

    def helper_invalid_files(self):
        yield {'file': 'test_invalid_P2_nested_undec.txt', 'line': 3, 'exp': None}
        yield {'file': 'test_invalid_Undeclared.txt', 'line': 9, 'exp': None}
        yield {'file': 'test_invalid_DelcareReal.txt', 'line': 3, 'exp': None}
        yield {'file': 'test_invalid_BoolUsage.txt', 'line': 6, 'exp': None}
        yield {'file': 'test_invalid_Long_Bool.txt', 'line': 42, 'exp': None}

    def helper_run_valid(self, file_path):
        sys.argv.extend(['-i', file_path])
        with open(file_path, 'r') as input_file:
            sa = SyntaxAnalyzer(input_file, Main.get_args())
            sa.r_Rat18F()

    def helper_run_invalid(self, filename, line, expect_str):
        input_path = os.path.join(self.test_files, filename)
        sys.argv.extend(['-i', input_path])
        with open(input_path, 'r') as input_file:
            sa = SyntaxAnalyzer(input_file, Main.get_args())
            with self.assertRaises(CompilerExceptions.CSyntaxError) as ex:
                sa.r_Rat18F()
            print(ex.exception)
            self.assertEqual(ex.exception.token.line, line)
            if expect_str is not None:
                self.assertEqual(ex.exception.expect, expect_str)

    def test_rat18f(self):
        for valid_file in self.helper_valid_files():
            with self.subTest(file_name=valid_file, file_type='Valid'):
                self.helper_run_valid(valid_file)
        for invalid_file in self.helper_invalid_files():
            with self.subTest(file_name=invalid_file, file_type='Invalid'):
                self.helper_run_invalid(invalid_file['file'], invalid_file['line'], invalid_file['exp'])

    def tearDown(self):
        for file in os.listdir(self.test_files):
            if not file.startswith('test_valid_') and not file.startswith('test_invalid_'):
                os.remove(os.path.join(self.test_files, file))
