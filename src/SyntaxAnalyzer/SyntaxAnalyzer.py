from Tokens import *
import argparse
import Lexer


class SyntaxAnalyzer(object):
    def __init__(self, file_ptr, argp: argparse.ArgumentParser):
        self.Lexer = Lexer.Lexer(file_ptr, argp)
        self.__print = argp.syntax

    def run_analyzer(self):
        try:
            while self.Lexer.__next__():
                pass
        except StopIteration:
            self.Lexer.write_tokens()

