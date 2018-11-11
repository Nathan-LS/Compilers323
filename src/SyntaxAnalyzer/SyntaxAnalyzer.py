from Tokens import *
from CompilerExceptions import *
import argparse
import Lexer
from colorama import Fore


class SyntaxAnalyzer:
    def __init__(self, file_ptr, argp):
        self.Lexer = Lexer.Lexer(file_ptr, argp)
        self.print_out: bool = argp.syntax
        self.filename: str = argp.input
        self.productions_pending_print = []

    def run_analyzer(self):
        try:
            self.r_Rat18F()
        except CSyntaxError as ex:
            self.print_p(str(ex), color=Fore.RED, force_console=True)
        finally:
            self.Lexer.finish_iterations()
            self.Lexer.write_tokens()
            self.write_productions()

    def write_productions(self):
        fname = "syntax_{}".format(self.filename)
        with open(fname, 'w') as f:
            for sa in self.productions_pending_print:
                f.write(str(sa) + '\n')
        print("Wrote {} syntax analysis productions or messages to the file: '{}'".format(len(self.productions_pending_print), fname))

    def print_p(self, production_rule: str, color="", force_console=False):
        """
        :param production_rule: A str production rule to output to console and add to pending file write buffer
        :param color: a colorama fore color for console output. Ex. Fore.Green, Fore.Red
        :param force_console: Force print to the console regardless of the Syntax Analyzer print to console flag being set
        :return: None
        """
        if self.print_out or force_console:
            print(color + production_rule)
        self.productions_pending_print.append(production_rule)

    def t_lexeme(self, lexeme):
        try:
            if self.Lexer.lexer_peek().is_lexeme(lexeme):
                return True
            return False
        except StopIteration:
            self.raise_syntax_error(lexeme)

    def t_type(self, t_type):
        try:
            if self.Lexer.lexer_peek().is_type(t_type):
                return True
            return False
        except StopIteration:
            self.raise_syntax_error(t_type.type_name())

    def raise_syntax_error(self, expected):
        try:
            raise CSyntaxError(self.Lexer.lexer_peek(), expected)
        except StopIteration:
            raise CSyntaxErrorEOF(expected)

    def r_Rat18F(self):
        self.r_OptFunctionDefinitions()
        if self.t_lexeme("$$"):
            self.Lexer.lexer()
            self.r_OptDeclarationList()
            self.r_StatementList("Must have statement list")
        else:
            self.raise_syntax_error("$$")
        if self.t_lexeme("$$"):
            self.Lexer.lexer()
        else:
            self.raise_syntax_error("$$")
        try:
            self.Lexer.lexer_peek()
            self.print_p("Error. Expected end of file marker after $$ token.", color=Fore.RED, force_console=True)
            self.raise_syntax_error('$$')
        except StopIteration:  # eof
            self.print_p("Success! There are no syntax errors here! :)", color=Fore.GREEN, force_console=True)

    def r_OptFunctionDefinitions(self):
        if self.r_FunctionDefinitions():
            return
        else:
            self.r_Empty()

    def r_FunctionDefinitions(self):
        if self.r_Function():
            self.r_FunctionDefinitionsPrime()
            return True
        return False

    def r_FunctionDefinitionsPrime(self):
        if self.r_FunctionDefinitions():
            pass
        self.r_Empty()

    def r_Function(self):
        # print(self.Lexer.peek_token().return_token())
        if self.t_lexeme("function"):
            self.Lexer.lexer()
            if self.t_type(TokenIdentifier):
                self.Lexer.lexer()
                if self.t_lexeme("("):
                    self.Lexer.lexer()
                    self.r_OptParameterList()
                    if self.t_lexeme(")"):
                        self.Lexer.lexer()
                        self.r_OptDeclarationList()
                        self.r_Body()
                        return True
                    else:
                        self.raise_syntax_error("\")\"")
                else:
                    self.raise_syntax_error("\"(\"")
            else:
                self.raise_syntax_error("Identifier")
        return False

    def r_OptParameterList(self):
        if self.r_ParameterList():
            return
        else:
            self.r_Empty()

    def r_ParameterList(self):
        if self.r_Parameter(flag="Doesn't need to pass"):
            self.r_ParameterListPrime()
            return True
        return False

    def r_ParameterListPrime(self):
        if self.t_lexeme(","):
            self.Lexer.lexer()
            self.r_Parameter()
            self.r_ParameterListPrime()
        else:
            self.r_Empty()

    def r_Parameter(self, flag="None"):
        if self.t_type(TokenIdentifier):
            self.Lexer.lexer()
            if self.t_lexeme(":"):
                self.Lexer.lexer()
                self.r_Qualifier()
                return True
            else:
                self.raise_syntax_error(":")
        elif flag == "None":
            self.raise_syntax_error("Identifier")
        else:
            return False

    def r_Qualifier(self, flag="None"):
        if self.t_lexeme("int") or self.t_lexeme("bool") or self.t_lexeme("real"):
            self.Lexer.lexer()
            return True
        elif flag != "None":
            return False
        else:
            self.raise_syntax_error("Qualifier [int, bool, real]")

    def r_Body(self):
        if self.t_lexeme("{"):
            self.Lexer.lexer()
            self.r_StatementList("Must Pass")
            if self.t_lexeme("}"):
                self.Lexer.lexer()
                return
            else:
                self.raise_syntax_error("}")
        else:
            self.raise_syntax_error("{")

    def r_StatementList(self, flag="None"):
        if self.r_Statement():
            self.r_StatementListPrime()
            return True
        elif flag == "None":
            return False
        else:
            self.raise_syntax_error("appropriate Statement preceding '{' token.")

    def r_StatementListPrime(self):
        if not self.r_StatementList():
            self.r_Empty()

    def r_Statement(self):
        if self.r_Compound() or self.r_Assign() or self.r_If() or self.r_Return() or self.r_Print() or self.r_Scan() or self.r_While():
            return True
        return False

    def r_Compound(self):
        if self.t_lexeme("{"):
            self.Lexer.lexer()
            if not self.r_StatementList("Must Pass"):
                self.raise_syntax_error("appropriate Statement preceding '{' token.")
            if self.t_lexeme("}"):
                self.Lexer.lexer()
                return True
            else:
                self.raise_syntax_error("}")
        else:
            return False

    def r_Assign(self):
        if self.t_type(TokenIdentifier):
            self.Lexer.lexer()
            if self.t_lexeme("="):
                self.Lexer.lexer()
                self.r_Expression()
                if self.t_lexeme(";"):
                    self.Lexer.lexer()
                    return True
                else:
                    self.raise_syntax_error(";")
            else:
                self.raise_syntax_error("=")
        else:
            return False

    def r_If(self):
        if self.t_lexeme("if"):
            self.Lexer.lexer()
            if self.t_lexeme("("):
                self.Lexer.lexer()
                self.r_Condition()
                if self.t_lexeme(")"):
                    self.Lexer.lexer()
                    if self.r_Statement():
                        self.r_IfPrime()
                        return True
                    else:
                        self.raise_syntax_error("appropriate statement after if conditional.")
                else:
                    self.raise_syntax_error(")")
            else:
                self.raise_syntax_error("(")
        else:
            return False

    def r_IfPrime(self):
        if self.t_lexeme("ifend"):
            self.Lexer.lexer()
            return
        elif self.t_lexeme("else"):
            self.Lexer.lexer()
            if self.r_Statement():
                if self.t_lexeme("ifend"):
                    self.Lexer.lexer()
                    return
                else:
                    self.raise_syntax_error("ifend")
            else:
                self.raise_syntax_error("appropriate statement after if conditional.")
        else:
            self.raise_syntax_error("ifend or else statement.")

    def r_Return(self):
        if self.t_lexeme("return"):
            self.Lexer.lexer()
            self.r_ReturnPrime()
            return True
        return False

    def r_ReturnPrime(self):
        if self.t_lexeme(";"):
            self.Lexer.lexer()
        else:
            self.r_Expression()
            if self.t_lexeme(";"):
                self.Lexer.lexer()
            else:
                self.raise_syntax_error(";")

    def r_Print(self):
        if self.t_lexeme("put"):
            self.Lexer.lexer()
            if self.t_lexeme("("):
                self.Lexer.lexer()
                self.r_Expression()
                if self.t_lexeme(")"):
                    self.Lexer.lexer()
                    if self.t_lexeme(";"):
                        self.Lexer.lexer()
                        return True
                    else:
                        self.raise_syntax_error(";")
                else:
                    self.raise_syntax_error(")")
            else:
                self.raise_syntax_error("(")
        return False

    def r_Scan(self):
        if self.t_lexeme("get"):
            self.Lexer.lexer()
            if self.t_lexeme("("):
                self.Lexer.lexer()
                self.r_Identifiers()
                if self.t_lexeme(")"):
                    self.Lexer.lexer()
                    if self.t_lexeme(";"):
                        self.Lexer.lexer()
                        return True
                    else:
                        self.raise_syntax_error(";")
                else:
                    self.raise_syntax_error(")")
            else:
                self.raise_syntax_error("(")
        return False

    def r_While(self):
        if self.t_lexeme("while"):
            self.Lexer.lexer()
            if self.t_lexeme("("):
                self.Lexer.lexer()
                self.r_Condition()
                if self.t_lexeme(")"):
                    self.Lexer.lexer()
                    if self.r_Statement():
                        if self.t_lexeme("whileend"):
                            self.Lexer.lexer()
                            return True
                        else:
                            self.raise_syntax_error("whileend")
                    else:
                        self.raise_syntax_error("appropriate statement following while loop.")
                else:
                    self.raise_syntax_error(")")
            else:
                self.raise_syntax_error("(")
        return False

    def r_Identifiers(self):
        if self.t_type(TokenIdentifier):
            self.Lexer.lexer()
            self.r_IdentifiersPrime()
        else:
            self.raise_syntax_error("Identifier")

    def r_IdentifiersPrime(self):
        if self.t_lexeme(","):
            self.Lexer.lexer()
            self.r_Identifiers()
        else:
            self.r_Empty()

    def r_Condition(self):
        self.r_Expression()
        self.r_RelationalOperator()
        self.r_Expression()

    def r_OptDeclarationList(self):
        if self.r_DeclarationList():
            return
        else:
            self.r_Empty()

    def r_DeclarationList(self):
        if self.r_Declarations():
            if self.t_lexeme(";"):
                self.Lexer.lexer()
                self.r_DeclarationListPrime()
                return True
            else:
                self.raise_syntax_error(";")
        return False


    def r_DeclarationListPrime(self):
        if self.r_DeclarationList():
            return
        else:
            self.r_Empty()

    def r_Declarations(self):
        if self.r_Qualifier("Doesn't need to pass"):
            self.r_Identifiers()
            return True
        else:
            return False

    def r_RelationalOperator(self):
        if self.t_lexeme("==") or self.t_lexeme("^=") or self.t_lexeme(">") or self.t_lexeme("<") or self.t_lexeme("=>") or self.t_lexeme("=<"):
            self.Lexer.lexer()
        else:
            self.raise_syntax_error("Relational Operator")

    def r_Expression(self):
        self.r_Term()
        self.r_ExpressionPrime()

    def r_ExpressionPrime(self):
        if self.t_lexeme("+") or self.t_lexeme("-"):
            self.Lexer.lexer()
            self.r_Term()
            self.r_ExpressionPrime()
        else:
            self.r_Empty()

    def r_Term(self):
        self.r_Factor()
        self.r_TermPrime()

    def r_TermPrime(self):
        if self.t_lexeme("*") or self.t_lexeme("/"):
            self.Lexer.lexer()
            self.r_Factor()
            self.r_TermPrime()
        else:
            self.r_Empty()

    def r_Factor(self):
        if self.t_lexeme("-"):
            self.Lexer.lexer()
        self.r_Primary()

    def r_Primary(self):
        if self.t_type(TokenInteger) or self.t_type(TokenReal) or self.t_lexeme("true") or self.t_lexeme("false"):
            self.Lexer.lexer()
            return
        elif self.t_type(TokenIdentifier):
            self.Lexer.lexer()
            if self.t_lexeme("("):
                self.Lexer.lexer()
                self.r_Identifiers()
                if self.t_lexeme(")"):
                    self.Lexer.lexer()
                else:
                    self.raise_syntax_error(")")
            else:
                return
        elif self.t_lexeme("("):
            self.Lexer.lexer()
            self.r_Expression()
            if self.t_lexeme(")"):
                self.Lexer.lexer()
                return
            else:
                self.raise_syntax_error(")")
        else:
            self.raise_syntax_error("acceptable Primary Expression [Identifier, Real, Integer, Bool...")

    def r_Empty(self):
        return