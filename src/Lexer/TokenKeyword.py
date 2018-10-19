from .TokenBase import TokenBase


class TokenKeyword(TokenBase):
    @classmethod
    def symbols(cls):
        yield 'int'
        yield 'if'
        yield 'else'
        yield 'ifend'
        yield 'while'
        yield 'whileend'
        yield 'return'
        yield 'get'
        yield 'put'
        yield 'function'
        yield 'real'
        yield 'boolean'
        yield 'true'
        yield 'false'

    @classmethod
    def accepting_states(cls):
        return
        yield
