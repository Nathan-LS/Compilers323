from .TokenBase import TokenBase


class TokenReal(TokenBase):
    @classmethod
    def reserved(cls):
        return
        yield

    @classmethod
    def accepting_states(cls):
        yield 6
