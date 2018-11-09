from abc import ABC, abstractmethod


class TokenBase(ABC):
    def __init__(self, lexeme, line_number):
        self.lexeme = lexeme
        self.line = line_number

    def is_type(self, class_type):
        return isinstance(self, class_type)

    def is_lexeme(self, lexeme_str: str):
        return self.lexeme == lexeme_str

    @classmethod
    def __get_subclasses(cls):
        """yield Base class and all child classes"""
        yield cls
        yield from cls.__subclasses__()

    @classmethod
    def is_symbol(cls, ch):
        """returns true if the char is a symbols symbol among any subclasses"""
        for TokenClasses in cls.__get_subclasses():
            if ch in TokenClasses.symbols():
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
    def get_token(cls, current_state, token_str, line_number):
        """make a token instance given given a state"""
        for TokenClasses in cls.__get_subclasses():
            if current_state in TokenClasses.accepting_states():
                return TokenClasses(token_str, line_number)

    @classmethod
    @abstractmethod
    def symbols(cls):
        """generator for symbols chars that signify new tokens"""
        yield ''
        yield ' '
        yield '\n'
        yield '\t'

    @classmethod
    @abstractmethod
    def accepting_states(cls):
        """yields integer accepting states for this particular token"""
        return
        yield

    @classmethod
    def type_name(cls):
        return cls.__name__.replace("Token", '')

    def __str__(self):
        """magic method for token printout to either console or a file output"""
        return "token: {:<12} lexeme: {:<12} line:{}".format(self.type_name(), "'{}'".format(self.lexeme), self.line)
