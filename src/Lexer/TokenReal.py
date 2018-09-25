from .TokenBase import TokenBase


class TokenReal(TokenBase):
    @classmethod
    def accepting_states(cls):
        """examples"""
        yield 1
        yield 2
