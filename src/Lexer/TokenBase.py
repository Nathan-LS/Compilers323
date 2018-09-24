from abc import ABC, abstractmethod, ABCMeta


class TokenBase(ABC):
    def __init__(self, lexeme):
        self.__lexeme = lexeme

    @classmethod
    @abstractmethod
    def symbol_check(cls, c: str):
        """returns if a given char is in the symbol table for this class"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def accepting_states(cls):
        """yields integer accepting states for this particular token"""
        raise NotImplementedError

    def __str__(self):
        return "token: {}, lexeme: '{}'".format(self.__class__.__name__, self.__lexeme)
