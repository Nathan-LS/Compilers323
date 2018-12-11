import CompilerExceptions
import os
from Tokens import TokenIdentifier


class SymbolTable(object):
    def __init__(self, starting_address=5000):
        self.declared_symbol = {}  # key: identifier string, val: type
        self.symbol_table = {}  # key: identifier string, val: memory address
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

    def insert_identifier(self, identifier: TokenIdentifier)->None:
        if not self.check_identifier(identifier.lexeme):  # identifier does not exist yet
            if self.current_identifier_type is None:  # we are inserting a new variable without declaring the type so raise syntax error
                raise CompilerExceptions.UndeclaredVariable(identifier)
            self.symbol_table[identifier.lexeme] = self.memory_address  # set key to name of identifier and val to memory location
            self.declared_symbol[identifier.lexeme] = self.current_identifier_type  # set identifier to current type
            self.memory_address += 1  # increment current memory address index
        else:  # identifier already exists in the symbol table
            if self.current_identifier_type is not None:  # there is currently a deceleration occurring. Raise syntax error for attempting to redeclare the variable
                raise CompilerExceptions.RedeclaredVariable(identifier)

    def write_symbols(self, filename, console_print=False):
        fname = (os.path.join(os.path.dirname(filename), "symbols_{}".format(os.path.basename(filename))))  # prefix syntax to file name
        pending_print = ["{:<15} {:<16} {:<8}".format('Identifier', 'Memory Location', 'Type')]
        for key, val in self.symbol_table.items():
            pending_print.append('{:<15} {:<16} {:<8}'.format(key, val, str(self.declared_symbol.get(key))))
        with open(fname, 'w') as f:  # open file for write
            for s in pending_print:  # iterate through list of productions used and output to the file
                f.write(s)
                f.write('\n')
                if console_print:
                    print(s)
            print("Wrote {} symbols to the file: ""'{}'.".format(len(self.symbol_table), fname))

    def get_address(self, identifier: TokenIdentifier)->int:
        """
        Given an identifier, return the memory address. Returns -1 if the identifier does not exist/undeclared
        :param identifier:
        :return: int
        """
        mem_address = self.symbol_table.get(identifier.lexeme)
        if mem_address is None:
            return -1
        else:
            return mem_address


