from .TokenBase import TokenBase


class TokenIdentifier(TokenBase):
    @classmethod
    def accepting_states(cls):
        """examples"""
        yield 1
        yield 2
