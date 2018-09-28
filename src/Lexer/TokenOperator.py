from .TokenBase import TokenBase


class TokenOperator(TokenBase):
    @classmethod
    def reserved(cls):
        yield '+'
        yield '-'
        yield '='
        yield '>'
        yield '<'

    @classmethod
    def accepting_states(cls):
        yield 7
