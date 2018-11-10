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
            return open('preprocessor_temp_file.txt', mode)
        except Exception as ex:
            print("File error: '{}' when opening the temp preprocessor file.".format(ex))
            traceback.print_exc()
            sys.exit(1)

    def __remove_comments(self):
        reg = re.compile('\[\*.*?\*\]', re.DOTALL)
        raw_file = self.input_file.read()
        new_str = raw_file
        for subs in re.findall(reg, raw_file):
            replace_string = ""
            for new_l in range(1, len(subs.splitlines())):
                replace_string += '\n'
            new_str = new_str.replace(subs, replace_string)
        return new_str

    def __make_preprocessor_file(self):
        self.output_file.write(self.__remove_comments())
        self.input_file.close()
        self.output_file.close()
        self.output_file = self.__get_preprocessor_file_pointer(read_mode=True)

    def get_file(self):
        return self.output_file

    def close(self):
        self.input_file.close()
        self.output_file.close()
