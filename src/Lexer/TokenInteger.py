from .TokenBase import TokenBase


class TokenInteger(TokenBase):
    @classmethod
    def reserved(cls):
        return
        yield

    @classmethod
    def accepting_states(cls):
        yield 3
