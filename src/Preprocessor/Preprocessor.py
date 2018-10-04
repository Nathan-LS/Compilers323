import re
import sys
import traceback


class Preprocessor(object):
    def __init__(self, file_name):
        self.input_name = file_name
        self.input_file = self.__get_input_pointer()
        self.output_file = self.__get_preprocessor_file_pointer()
        self.__make_preprocessor_file()

    def __get_input_pointer(self):
        try:
            return open(self.input_name, 'r')
        except FileNotFoundError:
            print("The file '{}' was not found.".format(self.input_name))
            sys.exit(1)
        except Exception as ex:
            print("File error: '{}' when opening the file: '{}'".format(ex, self.input_name))
            traceback.print_exc()
            sys.exit(1)

    def __get_preprocessor_file_pointer(self, read_mode=False):
        try:
            mode = 'r' if read_mode else 'w'
            return open('preprocessor_{}'.format(self.input_name), mode)
        except Exception as ex:
            print("File error: '{}' when opening the temp preprocessor file.".format(ex))
            traceback.print_exc()
            sys.exit(1)

    def __remove_comments(self):
        for line in self.input_file:
            yield re.sub('\[\*.*?\*\]', '', line)

    def __make_preprocessor_file(self):
        for line in self.__remove_comments():
            self.output_file.write(line)
        self.input_file.close()
        self.output_file.close()
        self.output_file = self.__get_preprocessor_file_pointer(read_mode=True)

    def get_file(self):
        return self.output_file

    def __del__(self):
        self.input_file.close()
        self.output_file.close()
