import argparse
import sys


class Main(object):
    @classmethod
    def get_args(cls):
        argp = argparse.ArgumentParser()
        argp.add_argument("--file", "-f", help="File input to compile and run.", type=str, required=True)
        return argp.parse_args()

    @classmethod
    def process_file(cls, file):
        try:
            with open(file, 'r') as f:
                pass  # do something with file
        except FileNotFoundError:
            print("The file '{}' was not found.".format(file))
            sys.exit(1)
        except Exception as ex:
            print("File error: '{}' was opening the file: '{}'".format(ex, file))
            sys.exit(1)

    @classmethod
    def main(cls):
        args = cls.get_args()
        cls.process_file(args.file)


if __name__ == "__main__":
    Main.main()
