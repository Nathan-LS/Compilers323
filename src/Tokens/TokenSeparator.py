from .TokenBase import TokenBase


class TokenSeparator(TokenBase):
    @classmethod
    def symbols(cls):
        yield '('
        yield ')'
        yield ','
        yield '{'
        yield '}'
        yield ';'
        yield ':'
        yield '$$'

    @classmethod
    def accepting_states(cls):
        yield 8
