import unittest
from src.__main__ import Main as srcMain
from src.SyntaxAnalyzer import SyntaxAnalyzer
import os
import sys


class InstructionGeneration(unittest.TestCase):
    def setUp(self):
        self.test_files = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TestTextFiles')

    def helper_run(self, filename):
        input_name = os.path.join(self.test_files, filename)
        output_path = os.path.join(self.test_files, "instructions_" + filename)
        assert_name = os.path.join(self.test_files, "assert_" + filename)
        sys.argv.extend(['-i', input_name])
        argp = srcMain.get_args()
        with open(input_name, 'r') as input_file:
            sa = SyntaxAnalyzer(input_file, argp)
            sa.run_analyzer()
        with open(output_path) as ofile:
            with open(assert_name) as afile:
                for line in afile:
                    self.assertEqual(ofile.readline().strip(), line.strip())

    def helper_test_files(self):
        for f in os.listdir(self.test_files):
            if f.startswith('test_'):
                yield f

    def test_file_write(self):
        for f in self.helper_test_files():
            with self.subTest(filename=f):
                self.helper_run(f)

    def tearDown(self):
        for file in os.listdir(self.test_files):
            if not file.startswith('test_') and not file.startswith('assert_') and not file.startswith('instructions_'):
                os.remove(os.path.join(self.test_files, file))
