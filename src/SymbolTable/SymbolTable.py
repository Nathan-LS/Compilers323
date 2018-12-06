import threading
import CompilerExceptions
import os
from Tokens import TokenBase


class SymbolTableSingleton(type):
    __init_lock = threading.Lock()
    __instance = None

    def __call__(cls, *args, **kwargs):
        with cls.__init_lock:
            if not cls.__instance:
                cls.__instance = super(SymbolTableSingleton, cls).__call__(*args, **kwargs)
            return cls.__instance


class SymbolTable(metaclass=SymbolTableSingleton):
    def __init__(self, starting_address=5000):
        self.declared_symbol = {}  # key: identifier string, val: type
        self.symbol_table = {}  # key: identifier string, val: memory address
        self.memory = {}  # key: memory address, val: identifier string
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
        self.current_identifier_type = token_type

    def reset_type(self):
        self.current_identifier_type = None

    def insert_identifier(self, identifier: TokenBase)->None:
        if self.symbol_table.get(identifier.lexeme) is None:
            self.symbol_table[identifier.lexeme] = self.memory_address
            self.memory[self.memory_address] = identifier.lexeme
            self.declared_symbol[identifier.lexeme] = self.current_identifier_type
            self.memory_address += 1
            if self.current_identifier_type is None:
                raise CompilerExceptions.UndeclaredVariable(identifier)
        else:
            if self.current_identifier_type is not None:
                raise CompilerExceptions.RedeclaredVariable(identifier)

    def write_symbols(self, filename, console_print=False):
        fname = (os.path.join(os.path.dirname(filename), "symbols_{}".format(os.path.basename(filename))))  # prefix syntax to file name
        pending_print = ["{:<15} {:<20} {:<5}".format('Identifier', 'Memory Location', 'Type')]
        for key, val in self.memory.items():
            pending_print.append('{:<15} {:<20} {:<5}'.format(val, key, str(self.declared_symbol.get(val))))
        with open(fname, 'w') as f:  # open file for write
            for s in pending_print:  # iterate through list of productions used and output to the file
                f.write(s)
                f.write('\n')
                if console_print:
                    print(s)
            print("Wrote {} symbols to the file: ""'{}'.".format(len(self.symbol_table), fname))

