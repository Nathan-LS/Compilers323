import CompilerExceptions
import os
from Tokens import TokenBase
from .Singleton import Singleton


class SymbolTable(metaclass=Singleton):
    def __init__(self, starting_address=5000):
        self.declared_symbol = {}  # key: identifier string, val: type
        self.symbol_table = {}  # key: identifier string, val: memory address
        self.memory = {}  # key: memory address, val: value
        self.memory_address = starting_address
        self.current_identifier_type = None

    def check_identifier(self, identifier: str)->bool:
        """
        check if a given identifier already exists in the symbol table. Returns True if identifier exists, otherwise false
        :param identifier: str
        :return: bool
        """
        if self.symbol_table.get(identifier) is None:
            return False
        else:
            return True

    def set_type(self, token_type: str):
        """
        set the toke type by passing in the string of a type. Ex: int, bool, etc
        :param token_type:
        :return:
        """
        self.current_identifier_type = token_type

    def reset_type(self):
        """
        clear set type
        :return:
        """
        self.current_identifier_type = None

    def insert_identifier(self, identifier: TokenBase)->None:
        if self.symbol_table.get(identifier.lexeme) is None:
            self.symbol_table[identifier.lexeme] = self.memory_address  # set key to name of identifier and val to memory location
            self.memory[self.memory_address] = None  # initially set declared variables to have no value
            self.declared_symbol[identifier.lexeme] = self.current_identifier_type  # set identifier to current type
            self.memory_address += 1  # increment current memory address index
            if self.current_identifier_type is None:  # we are inserting a new variable without declaring the type so raise syntax error
                raise CompilerExceptions.UndeclaredVariable(identifier)
        else:  # identifier already exists in the symbol table
            if self.current_identifier_type is not None:  # there is currently a deceleration occurring. Raise syntax error for attempting to redeclare the variable
                raise CompilerExceptions.RedeclaredVariable(identifier)

    def write_symbols(self, filename, console_print=False):
        fname = (os.path.join(os.path.dirname(filename), "symbols_{}".format(os.path.basename(filename))))  # prefix syntax to file name
        pending_print = ["{:<15} {:<16} {:<8} {:<6}".format('Identifier', 'Memory Location', 'Type', 'Value')]
        for key, val in self.symbol_table.items():
            pending_print.append('{:<15} {:<16} {:<8} {:<6}'.format(key, val, str(self.declared_symbol.get(key)),
                                                                    str(self.memory.get(val))))
        with open(fname, 'w') as f:  # open file for write
            for s in pending_print:  # iterate through list of productions used and output to the file
                f.write(s)
                f.write('\n')
                if console_print:
                    print(s)
            print("Wrote {} symbols to the file: ""'{}'.".format(len(self.symbol_table), fname))

    def store_memory(self, memory_location, value):
        self.memory[memory_location] = value

