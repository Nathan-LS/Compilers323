from .TokenBase import TokenBase


class TokenSeparator(TokenBase):
    @classmethod
    def reserved(cls):
        yield '('
        yield ')'

    @classmethod
    def accepting_states(cls):
        yield 7
