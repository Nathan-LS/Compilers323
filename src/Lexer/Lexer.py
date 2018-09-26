from . import *


class Lexer(object):

    @classmethod
    def lex_state_mapper(cls, ch: str, alpha_state: int, digit_state: int, operator_state: int, undefined_state: int):
        """helper function for different state mappings"""
        if ch.isalpha():
            return alpha_state
        elif ch.isdigit():
            return digit_state
        elif TokenOperator.is_symbol(ch):
            return operator_state
        else:
            return undefined_state

    @classmethod
    def lex_recursive_generator(cls, file_ptr, current_state=1, token_str=''):
        """yields all token instances given a file pointer"""
        next_char: str = file_ptr.read(1)
        if TokenBase.is_reserved(next_char) and TokenBase.is_in_accepting_states(current_state): # hit whitespace or char that signals an end of token i.e =, >, etc
            yield TokenBase.get_token(current_state, token_str)  # make the token given the token_str and current state
            current_state = 1  # reset to starting state
            token_str = ''
        elif TokenOperator.is_accepting_state(current_state):  # if in accepting state for a single char ie op, yield immediately
            yield TokenBase.get_token(current_state, token_str)
            current_state = 1
            token_str = ''
        else:
            pass
        if next_char == '':  # recursive base case but we must yield the previous token if any before exiting
            return
        next_state = current_state
        if not TokenBase.is_symbol(next_char):  # skips whitespace, tabs, newline
            token_str += next_char
            if current_state == 1:
                next_state = cls.lex_state_mapper(next_char, 2, 3, 4, 5)
            elif current_state == 2:
                next_state = cls.lex_state_mapper(next_char, 2, 5, 5, 5)
            elif current_state == 3:
                next_state = cls.lex_state_mapper(next_char, 5, 3, 5, 5)
            elif current_state == 4:
                next_state = cls.lex_state_mapper(next_char, 5, 5, 5, 5)
            else:
                next_state = cls.lex_state_mapper(next_char, 5, 5, 5, 5)
        yield from cls.lex_recursive_generator(file_ptr, next_state, token_str)

    @classmethod
    def lexer(cls, file_ptr):
        yield from cls.lex_recursive_generator(file_ptr)
