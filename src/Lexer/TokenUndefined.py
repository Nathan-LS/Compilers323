from .TokenBase import TokenBase


class TokenUndefined(TokenBase):
    @classmethod
    def reserved(cls):
        return
        yield

    @classmethod
    def accepting_states(cls):
        yield 9
