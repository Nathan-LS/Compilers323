from .TokenBase import TokenBase


class TokenUndefined(TokenBase):
    @classmethod
    def symbols(cls):
        return
        yield

    @classmethod
    def accepting_states(cls):
        yield 9
