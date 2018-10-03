from . import *


class Lexer(object):
    def __init__(self, file_ptr):
        self.__file_ptr = file_ptr
        row1 = [2, 4, 7, 8, 9, 9]
        row2 = [2, 3, 9, 9, 9, 9]
        row3 = [2, 3, 9, 9, 9, 9]
        row4 = [9, 4, 9, 9, 5, 9]
        row5 = [9, 6, 9, 9, 9, 9]
        row6 = [9, 6, 9, 9, 9, 9]
        row7 = [9, 9, 9, 9, 9, 9]
        row8 = [9, 9, 9, 9, 9, 9]
        row9 = [9, 9, 9, 9, 9, 9]
        self.__matrix = [row1, row2, row3, row4, row5, row6, row7, row8, row9]  # state table from example2.md

    def lex_state_mapper(self, ch: str, current_state):
        """helper function for different state mappings"""
        if ch.isalpha():
            return self.__matrix[current_state-1][0]
        elif ch.isdigit():
            return self.__matrix[current_state-1][1]
        elif ch in TokenOperator.reserved():
            return self.__matrix[current_state-1][2]
        elif ch in TokenSeparator.reserved():
            return self.__matrix[current_state-1][3]
        elif ch == '.':
            return self.__matrix[current_state-1][4]
        else:
            return self.__matrix[current_state-1][5]

    @classmethod
    def peek(cls, file_ptr):
        prev_pos = file_ptr.tell()
        next_peek_char = file_ptr.read(1)
        file_ptr.seek(prev_pos)
        return next_peek_char

    def lex_recursive_generator(self, file_ptr, current_state=1, token_str=''):
        """returns all token instances given a file pointer. Returns None when EOF"""
        next_char: str = self.peek(file_ptr)
        if TokenBase.is_reserved(next_char):  # hit whitespace or char that signals an end of token i.e =, >, etc
            if TokenBase.is_an_accepting_state(current_state):
                if TokenKeyword.is_reserved(token_str):  # special case check for keywords
                    return TokenKeyword(token_str)
                else:
                    return TokenBase.get_token(current_state, token_str)  # make the token given the token_str and current state
            elif current_state != 1:  # cannot yield starting state, get more chars
                return TokenUndefined(token_str)
            else:
                pass
        elif current_state in TokenBase.states_return_immediate():  # if in accepting state for a single char ie op, yield immediately
            return TokenBase.get_token(current_state, token_str)
        else:
            pass
        if next_char == '':  # recursive base case but we must yield the previous token if any before exiting
            return None  # raise StopIteration in caller
        next_char = file_ptr.read(1)
        next_state = current_state
        if next_char not in TokenBase.reserved():  # skips whitespace, tabs, newline
            token_str += next_char
            next_state = self.lex_state_mapper(next_char, current_state)
        return self.lex_recursive_generator(file_ptr, next_state, token_str)

    def __iter__(self):
        return self

    def __next__(self):
        return self.lexer()

    def lexer(self):
        token = self.lex_recursive_generator(self.__file_ptr)
        if token is None:
            raise StopIteration
        else:
            return token
