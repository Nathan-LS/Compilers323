import argparse
from SyntaxAnalyzer import SyntaxAnalyzer
from Preprocessor import Preprocessor
import traceback
import colorama


class Main(object):
    @classmethod
    def get_args(cls):
        argp = argparse.ArgumentParser()
        argp.add_argument("--input", "-i", help="File input to compile and run.", type=str, required=True)
        argp.add_argument("--tokens", "-t", help="Output the tokens from the lexer to the program console.",
                          action="store_true", default=False)
        argp.add_argument("--syntax", "-s", help="Output the syntax rules from the syntax analyzer to the program "
                                                 "console.", action="store_true", default=False)
        return argp.parse_args()

    @classmethod
    def run(cls, args, file_ptr):
        try:
            sa = SyntaxAnalyzer(file_ptr, args)
            sa.run_analyzer()
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    @classmethod
    def process_file(cls, args):
        """obtain the preprocessor file"""
        preprocessor_file = Preprocessor(args.input)
        cls.run(args, preprocessor_file.get_file())
        preprocessor_file.close()

    @classmethod
    def main(cls):
        """entry point to application"""
        colorama.init(autoreset=True)
        cls.process_file(cls.get_args())


if __name__ == "__main__":
    Main.main()
