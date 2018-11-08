from Tokens import *
from CompilerExceptions import *
import argparse
import Lexer
from colorama import Fore


class SyntaxAnalyzer(object):
    def __init__(self, file_ptr, argp: argparse.ArgumentParser):
        self.Lexer = Lexer.Lexer(file_ptr, argp)
        self.print_out: bool = argp.syntax
        self.filename: str = argp.input
        self.productions_pending_print = []

    def run_analyzer(self):
        try:
            self.r_Rat18F()
            self.print_production("Syntax ok", color=Fore.GREEN)
        except CSyntaxError as ex:
            self.print_production(str(ex), color=Fore.RED)
        finally:  # regardless of errors finish obtaining all tokens and write them to file
            self.Lexer.finish_iterations()
            self.Lexer.write_tokens()
            self.write_productions()

    def write_productions(self):
        fname = "syntax_{}".format(self.filename)
        with open(fname, 'w') as f:
            for sa in self.productions_pending_print:
                f.write(str(sa) + '\n')
        print("Wrote {} syntax analysis productions to the file: '{}'".format(len(self.productions_pending_print), fname))

    def print_production(self, production_rule: str, color=""):
        """
        :param production_rule: A str production rule to output to console and add to pending file write buffer
        :param color: a colorama fore color for console output. Ex. Fore.Green, Fore.Red
        :return: None
        """
        if self.print_out:
            print(color + production_rule)
        self.productions_pending_print.append(production_rule)

    def t_lexeme(self, val, bt_pos=None):
        try:
            if self.Lexer.lexer_peek(bt_pos).is_lexeme(val):
                self.Lexer.lexer(bt_pos)
            else:
                raise CSyntaxError(self.Lexer.lexer_peek(), val)
        except StopIteration:  # end of all tokens/file
            raise CSyntaxErrorEOF(expect=val)

    def t_type(self, val, bt_pos=None):
        try:
            if self.Lexer.lexer_peek(bt_pos).is_type(val):
                self.Lexer.lexer(bt_pos)
            else:
                raise CSyntaxError(self.Lexer.lexer_peek(), val.type_name())
        except StopIteration:  # end of all tokens/file
            raise CSyntaxErrorEOF(expect=val)

    def r_Rat18F(self):
        self.print_production('Rat18F -> $$ ID = ID + ID $$')
        p = self.Lexer.bt_get()
        self.t_lexeme('$$')
        self.t_type(TokenIdentifier)
        self.t_lexeme('=')
        self.t_type(TokenIdentifier)
        self.t_lexeme('+')
        self.t_type(TokenIdentifier)
        self.t_lexeme('$$')

    def r_OptFunctionDefinitions(self):
        pass

    def r_FunctionDefinitions(self):
        pass

    def r_Function(self):
        pass

    def r_OptParameterList(self):
        pass

    def r_ParameterList(self):
        pass

    def r_Parameter(self):
        pass

    def r_Qualifier(self):
        pass

    def r_Body(self):
        pass

    def r_OptDeclarationList(self):
        pass

    def r_DeclarationList(self):
        pass

    def r_Declaration(self):
        pass

    def r_IDs(self):
        pass

    def r_StatementList(self):
        pass

    def r_Statement(self):
        pass

    def r_Compound(self):
        pass

    def r_Assign(self):
        pass

    def r_If(self):
        pass

    def r_Return(self):
        pass

    def r_Print(self):
        pass

    def r_Scan(self):
        pass

    def r_While(self):
        pass

    def r_Condition(self):
        pass

    def r_Relop(self):
        pass

    def r_Expression(self):
        pass

    def r_Term(self):
        pass

    def r_Factor(self):
        pass

    def r_Primary(self):
        pass

    def r_Empty(self):
        pass


