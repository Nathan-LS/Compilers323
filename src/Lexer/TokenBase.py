from abc import ABC, abstractmethod


class TokenBase(ABC):
    def __init__(self, lexeme):
        self.__lexeme = lexeme

    @classmethod
    def __get_subclasses(cls):
        """yield Base class and all child classes"""
        yield cls
        yield from cls.__subclasses__()

    @classmethod
    def is_symbol(cls, ch):
        """returns true if the given char belongs to a token type"""
        return ch in cls.reserved()

    @classmethod
    def is_reserved(cls, ch):
        """returns true if the char is a reserved symbol"""
        for TokenClasses in cls.__get_subclasses():
            if TokenClasses.is_symbol(ch):
                return True
        return False

    @classmethod
    def is_an_accepting_state(cls, current_state):
        """determine if the given state is actually an accepting state among any subclasses"""
        for TokenClasses in cls.__get_subclasses():
            if current_state in TokenClasses.accepting_states():
                return True
        return False

    @classmethod
    def get_token(cls, current_state, token_str):
        """make a token given a state"""
        for TokenClasses in cls.__get_subclasses():
            if current_state in TokenClasses.accepting_states():
                return TokenClasses(token_str)

    @classmethod
    @abstractmethod
    def reserved(cls):
        """generator for reserved chars that signify new tokens"""
        yield ''
        yield ' '
        yield '\n'
        yield '\t'

    @classmethod
    def states_yield_immediate(cls):
        """single char states that must be yielded immediately. i.e. op, sep"""
        yield 6  # operator
        yield 7  # separator

    @classmethod
    @abstractmethod
    def accepting_states(cls):
        """yields integer accepting states for this particular token"""
        return
        yield

    def __str__(self):
        return "token: {:<12} lexeme: '{}'".format(self.__class__.__name__.replace("Token", ''), self.__lexeme)
