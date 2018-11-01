from Tokens import *
import argparse


class Lexer(object):
    def __init__(self, file_ptr, argp: argparse.ArgumentParser):
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
        self.__line_number = 1
        self.__bt_index = 0
        self.__current_index = 0
        self.__tokens = []
        self.__filename = argp.input
        self.__print = argp.tokens

    @property
    def starting_state(self):
        return 1

    def lex_state_mapper(self, ch: str, current_state):
        """helper function for different state mappings"""
        if ch.isalpha():
            return self.__matrix[current_state-1][0]
        elif ch.isdigit():
            return self.__matrix[current_state-1][1]
        elif ch in TokenOperator.symbols():
            return self.__matrix[current_state-1][2]
        elif ch in TokenSeparator.symbols():
            return self.__matrix[current_state-1][3]
        elif ch == '.':
            return self.__matrix[current_state-1][4]
        else:
            return self.__matrix[current_state-1][5]

    def peek(self):
        prev_pos = self.__file_ptr.tell()
        next_peek_char = self.__file_ptr.read(1)
        self.__file_ptr.seek(prev_pos)
        return next_peek_char

    def __lexer(self, current_state=1, token_str=''):
        """returns the next token"""
        next_char: str = self.peek()
        if current_state != self.starting_state:
            next_str = token_str + next_char   # get next char and check if a double char string is a valid op or sep
            if next_str in TokenOperator.symbols():  # if combined with next char is valid symbol for operator
                self.__file_ptr.read(1)  # advance file pointer and return the token
                return TokenOperator(next_str, self.__line_number)
            elif next_str in TokenSeparator.symbols():  # if combined with next char is valid symbol for separator
                self.__file_ptr.read(1)
                return TokenSeparator(next_str, self.__line_number)
            elif current_state in TokenSeparator.accepting_states() or current_state in TokenOperator.accepting_states():
                return TokenBase.get_token(current_state, token_str, self.__line_number)
            else:  # the next str is invalid for op/sep special case continue moving on till next end of token symbol
                pass
        if TokenBase.is_symbol(next_char):  # hit whitespace or char that signals an end of token i.e =, >, etc
            if TokenBase.is_an_accepting_state(current_state):
                if token_str in TokenKeyword.symbols():  # special case check for keywords
                    return TokenKeyword(token_str, self.__line_number)
                else:
                    return TokenBase.get_token(current_state, token_str, self.__line_number)  # make the token given the token_str and current state
            elif current_state != self.starting_state:  # cannot yield starting state, get more chars
                return TokenUndefined(token_str, self.__line_number)
            else:
                pass
        if next_char == '':  # recursive base case but we must yield the previous token if any before exiting
            raise StopIteration  # raise StopIteration in caller
        next_char = self.__file_ptr.read(1)
        if next_char == '\n':
            self.__line_number += 1
        next_state = current_state
        if next_char not in TokenBase.symbols():  # skips whitespace, tabs, newline
            token_str += next_char
            next_state = self.lex_state_mapper(next_char, current_state)
        return self.__lexer(next_state, token_str)

    def lexer(self)->TokenBase:
        try:
            tok = self.__tokens[self.__current_index]
            if self.__print:
                print(tok)
            return tok
        except IndexError:
            tok = self.__lexer()
            self.__tokens.append(tok)
            if self.__print:
                print(tok)
            return tok
        finally:
            self.__current_index += 1

    def __iter__(self):
        return self

    def __next__(self)->TokenBase:
        return self.lexer()

    def write_tokens(self):
        """write the tokens to the file tokens_filename.txt"""
        fname = "tokens_{}".format(self.__filename)
        with open(fname, 'w') as f:
            for t in self.__tokens:
                f.write(str(t) + '\n')
        print("Wrote {} tokens to the file: '{}'".format(len(self.__tokens), fname))

    def bt_set(self):
        """set the back tracker to remember the current position"""
        self.__bt_index = self.__current_index

    def bt_clear(self):
        """clear the current back tracking position"""
        self.bt_set()

    def bt_return(self):
        """return to a previously added back track index"""
        self.__current_index = self.__bt_index



