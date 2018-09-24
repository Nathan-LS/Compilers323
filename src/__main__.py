import argparse
import sys
from Lexer import Lexer
import traceback


class Main(object):
    @classmethod
    def get_args(cls):
        argp = argparse.ArgumentParser()
        argp.add_argument("--input", "-i", help="File input to compile and run.", type=str, required=True)
        argp.add_argument("--output", "-o", help="File output to place tokens and lexemes. If no file is given, tokens "
                                                 "will be printed in the console window.", type=str, required=False)
        return argp.parse_args()

    @classmethod
    def process_file(cls, file):
        try:
            with open(file, 'r') as f:
                for i in Lexer.lexer(f):  # yield all tokens from file and print them
                    print(i)
        except FileNotFoundError:
            print("The file '{}' was not found.".format(file))
            sys.exit(1)
        except Exception as ex:
            print("File error: '{}' when opening the file: '{}'".format(ex, file))
            traceback.print_exc()
            sys.exit(1)

    @classmethod
    def main(cls):
        args = cls.get_args()
        cls.process_file(args.input)


if __name__ == "__main__":
    Main.main()
