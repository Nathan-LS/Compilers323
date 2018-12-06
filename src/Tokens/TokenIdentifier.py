from .TokenBase import TokenBase
from SymbolTable import *


class TokenIdentifier(TokenBase):
    def insert_symbol(self):
        SymbolTable().insert_identifier(self)

    @classmethod
    def symbols(cls):
        return
        yield

    @classmethod
    def accepting_states(cls):
        yield 2
