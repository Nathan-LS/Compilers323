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
    def is_reserved(cls, ch):
        """returns true if the char is a reserved symbol among any subclasses"""
        for TokenClasses in cls.__get_subclasses():
            if ch in TokenClasses.reserved():
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
        """make a token instance given given a state"""
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
    def states_return_immediate(cls):
        """single char states that must be yielded immediately. i.e. op, sep"""
        yield 7  # operator
        yield 8  # separator

    @classmethod
    @abstractmethod
    def accepting_states(cls):
        """yields integer accepting states for this particular token"""
        return
        yield

    def __str__(self):
        """magic method for token printout to either console or a file output"""
        return "token: {:<12} lexeme: '{}'".format(self.__class__.__name__.replace("Token", ''), self.__lexeme)
