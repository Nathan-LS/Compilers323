import argparse
import sys
from Lexer import Lexer
from Preprocessor import Preprocessor
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
    def write_lexer(cls, args, file_ptr):
        try:
            with open(args.output, 'w') as f:
                for t in Lexer(file_ptr):
                    f.writelines("{}\n".format(t))
            print("Successfully wrote tokens to the file: '{}'".format(args.output))
        except Exception as ex:
            print("File output error: '{}' when writing to the file: '{}'".format(ex, args.output))
            traceback.print_exc()

    @classmethod
    def print_lexer(cls, file_ptr):
        try:
            for t in Lexer(file_ptr):
                print(t)
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    @classmethod
    def process_file(cls, args):
        if args.input == args.output:
            print("Error. You cannot output the tokens into your input file.")
            sys.exit(1)
        else:
            preprocessor_file = Preprocessor(args.input)
            if args.output:
                cls.write_lexer(args, preprocessor_file.get_file())
            else:
                cls.print_lexer(preprocessor_file.get_file())

    @classmethod
    def main(cls):
        args = cls.get_args()
        cls.process_file(args)


if __name__ == "__main__":
    Main.main()
