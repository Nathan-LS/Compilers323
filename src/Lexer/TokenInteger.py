from .TokenBase import TokenBase


class TokenInteger(TokenBase):
    @classmethod
    def symbols(cls):
        return
        yield

    @classmethod
    def accepting_states(cls):
        yield 4
