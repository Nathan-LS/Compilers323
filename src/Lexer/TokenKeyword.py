from .TokenBase import TokenBase


class TokenKeyword(TokenBase):
    @classmethod
    def symbols(cls):
        yield 'int'
        yield 'if'
        yield 'else'
        yield 'ifend'
        yield 'while'
        yield 'return'
        yield 'get'
        yield 'put'

    @classmethod
    def accepting_states(cls):
        return
        yield
