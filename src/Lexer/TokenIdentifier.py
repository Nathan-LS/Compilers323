from .TokenBase import TokenBase


class TokenIdentifier(TokenBase):
    @classmethod
    def symbol_check(cls, c: str):
        """returns if a given char is in the symbol table for this class"""
        return c.isalpha()

    @classmethod
    def accepting_states(cls):
        """examples"""
        yield 1
        yield 2
