from . import *


class Lexer(object):

    @classmethod
    def lex_state_mapper(cls, ch: str, alpha_state: int, digit_state: int, operator_state: int, separator_state: int, decimal_state: int, undefined_state: int):
        """helper function for different state mappings"""
        if ch.isalpha():
            return alpha_state
        elif ch.isdigit():
            return digit_state
        elif TokenOperator.is_symbol(ch):
            return operator_state
        elif TokenSeparator.is_symbol(ch):
            return separator_state
        elif ch == '.':
            return decimal_state
        else:
            return undefined_state

    @classmethod
    def lex_recursive_generator(cls, file_ptr, current_state=1, token_str=''):
        """yields all token instances given a file pointer"""
        next_char: str = file_ptr.read(1)
        if TokenBase.is_reserved(next_char):  # hit whitespace or char that signals an end of token i.e =, >, etc
            if TokenBase.is_an_accepting_state(current_state):
                if TokenKeyword.is_reserved(token_str):  # special case check for keywords
                    yield TokenKeyword(token_str)
                else:
                    yield TokenBase.get_token(current_state, token_str)  # make the token given the token_str and current state
                current_state = 1  # reset to starting state
                token_str = ''
            elif current_state != 1:  # cannot yield starting state, get more chars
                yield TokenUndefined(token_str)
                current_state = 1
                token_str = ''
            else:
                pass
        elif current_state in TokenBase.states_yield_immediate():  # if in accepting state for a single char ie op, yield immediately
            yield TokenBase.get_token(current_state, token_str)
            current_state = 1
            token_str = ''
        else:
            pass
        if next_char == '':  # recursive base case but we must yield the previous token if any before exiting
            return  # raise StopIteration
        next_state = current_state
        if not TokenBase.is_symbol(next_char):  # skips whitespace, tabs, newline
            token_str += next_char
            if current_state == 1:
                next_state = cls.lex_state_mapper(next_char, 2, 3, 6, 7, 8, 8)
            elif current_state == 2:
                next_state = cls.lex_state_mapper(next_char, 2, 2, 8, 8, 8, 8)
            elif current_state == 3:
                next_state = cls.lex_state_mapper(next_char, 8, 3, 8, 8, 4, 8)
            elif current_state == 4:
                next_state = cls.lex_state_mapper(next_char, 8, 5, 8, 8, 8, 8)
            elif current_state == 5:
                next_state = cls.lex_state_mapper(next_char, 8, 5, 8, 8, 8, 8)
            elif current_state == 6:
                next_state = cls.lex_state_mapper(next_char, 8, 8, 8, 8, 8, 8)
            elif current_state == 7:
                next_state = cls.lex_state_mapper(next_char, 8, 8, 8, 8, 8, 8)
            else:
                next_state = cls.lex_state_mapper(next_char, 8, 8, 8, 8, 8, 8)
        yield from cls.lex_recursive_generator(file_ptr, next_state, token_str)

    @classmethod
    def lexer(cls, file_ptr):
        yield from cls.lex_recursive_generator(file_ptr)
