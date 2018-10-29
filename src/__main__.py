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
        argp.add_argument("--tokens", "-t", help="Output the tokens from the lexer to the program console.", action="store_true", default=False)
        return argp.parse_args()

    @classmethod
    def lexer_demo(cls, args, file_ptr):
        try:
            lex = Lexer(file_ptr, args.input, args.tokens)
            for t in lex:
                pass
            lex.write_tokens()
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    @classmethod
    def process_file(cls, args):
        preprocessor_file = Preprocessor(args.input)
        cls.lexer_demo(args, preprocessor_file.get_file())
        preprocessor_file.close()

    @classmethod
    def main(cls):
        args = cls.get_args()
        cls.process_file(args)


if __name__ == "__main__":
    Main.main()
