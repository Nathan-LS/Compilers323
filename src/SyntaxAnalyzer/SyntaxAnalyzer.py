from Tokens import *
from CompilerExceptions import *
import argparse
import Lexer
from colorama import Fore
import os


class SyntaxAnalyzer:
    def __init__(self, file_ptr, argp):
        self.Lexer = Lexer.Lexer(file_ptr, argp)
        self.print_out: bool = argp.syntax
        self.filename: str = argp.input

        self.state_strs_pending_print = []
        self.state_strs_pending_file = []
        self.productions_pending_write = []
        self.new_production = []

    def run_analyzer(self):
        try:  # entry point to the syntax analyzer
            self.r_Rat18F()  # call the first rule
        except CSyntaxError as ex:  # if a syntax error occurs we catch it here and print it to console and file using custom exceptions for lineno/ exepected, etc
            self.print_p(str(ex), color=Fore.RED, force_console=True)  # output buffer add with red text for error message
        finally:  # regardless of errors or success
            self.Lexer.finish_iterations()  # obtain remaining tokens within the file
            self.Lexer.write_tokens()  # write lexer tokens to their own file
            self.write_productions()  # write all productions to separate file

    def write_productions(self):
        fname = (os.path.join(os.path.dirname(self.filename), "syntax_{}".format(os.path.basename(self.filename))))  # prefix syntax to file name
        with open(fname, 'w') as f:  # open file for write
            for sa in self.productions_pending_write:  # iterate through list of productions used and output to the file
                text_block = ""
                for obj in sa:
                    text_block += str(obj) + '\n'
                text_block += "\n"
                if self.print_out:  # output production to console if the -s CLI arg is set
                    print(text_block)
                f.write(text_block)
            print("Wrote {} syntax analysis productions or messages to the file: "
                  "'{}'".format(len(self.productions_pending_write), fname))
            for p in self.state_strs_pending_file:  # output success or error messages to file and console
                f.write(p)
            for p in self.state_strs_pending_print:
                print(p)

    def print_p(self, production_rule: str, color="", force_console=False):
        """
        :param production_rule: A str production rule to output to console and add to pending file write buffer
        :param color: a colorama fore color for console output. Ex. Fore.Green, Fore.Red
        :param force_console: Force print to console regardless of the Syntax Analyzer print to console flag being set
        :return: None
        """
        if self.print_out or force_console:  # helper function for color output status messages. error or success
            self.state_strs_pending_print.append(color + production_rule)
        self.state_strs_pending_file.append(production_rule)

    def lexer(self):
        new_tok = self.Lexer.lexer()  # proxy lexer to obtain token for pretty printout to file.
        self.new_production = [new_tok] + self.new_production
        self.productions_pending_write.append(self.new_production)
        self.new_production = []

    def t_lexeme(self, lexeme):  # lexeme check. Peek the next token and check if the given lexeme str matches it.
        try:
            if self.Lexer.lexer_peek().is_lexeme(lexeme):
                return True
            return False
        except StopIteration:  # StopIteration is raised for an EOF by the lexer
            self.raise_syntax_error(lexeme)

    def t_type(self, t_type):  # token type check. Peek next token and check if it's an identifier, relop, etc.
        try:
            if self.Lexer.lexer_peek().is_type(t_type):
                return True
            return False
        except StopIteration:  # StopIteration is raised for an EOF by the lexer
            self.raise_syntax_error(t_type.type_name())

    def raise_syntax_error(self, expected):  # make the exception with the expected str and the peek token
        try:
            raise CSyntaxError(self.Lexer.lexer_peek(), expected)
        except StopIteration:
            raise CSyntaxErrorEOF(expected)

    def r_Rat18F(self):  # first rule using the RDP parsing technique
        self.new_production.append("<Rat18F>\t-->\t<Opt Function Definitions>  '$$'  <Opt Declaration List>  "
                                   "<Statement List>  '$$'")
        self.r_OptFunctionDefinitions()
        if self.t_lexeme("$$"):
            self.lexer()
            self.r_OptDeclarationList()
            self.r_StatementList("Must have statement list")
        else:
            self.raise_syntax_error("$$")
        if self.t_lexeme("$$"):
            self.lexer()
        else:
            self.raise_syntax_error("$$")
        try:
            self.Lexer.lexer_peek()  # check if there are remaining tokens after the last $$ marker
            self.print_p("Error. Expected end of file marker after $$ token.", color=Fore.RED, force_console=True)
            self.raise_syntax_error('$$')
        except StopIteration:  # eof indicating pass of the Rat18R rule with no tokens remaining
            self.print_p("Success! There are no syntax errors here! :)", color=Fore.GREEN, force_console=True)

    def r_OptFunctionDefinitions(self):
        self.new_production.append("<Opt Function Definitions>\t-->\t<Function Definitions>  '|'  <Empty>")
        if self.r_FunctionDefinitions():
            return
        else:
            self.r_Empty()

    def r_FunctionDefinitions(self):
        self.new_production.append("<Function Definitions>\t-->\t<Function>  <Function Definition Prime>")
        if self.r_Function():
            self.r_FunctionDefinitionsPrime()
            return True
        return False

    def r_FunctionDefinitionsPrime(self):
        self.new_production.append("<Function Definition Prime>\t-->\t<Function Definitions  '|'  <Empty>")
        if self.r_FunctionDefinitions():
            pass
        self.r_Empty()

    def r_Function(self):
        # print(self.Lexer.peek_token().return_token())
        self.new_production.append("<Function>\t-->\tfunction  IDENTIFIER  (  <Optional Parameter List>  )  <Optional"
                                   " Declaration List>  Body")
        if self.t_lexeme("function"):
            self.lexer()
            if self.t_type(TokenIdentifier):
                self.lexer()
                if self.t_lexeme("("):
                    self.lexer()
                    self.r_OptParameterList()
                    if self.t_lexeme(")"):
                        self.lexer()
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
        self.new_production.append("<Optional Parameter List>\t-->\t<Parameter List>  '|'  <Empty>")
        if self.r_ParameterList():
            return
        else:
            self.r_Empty()

    def r_ParameterList(self):
        self.new_production.append("<Parameter List>\t-->\t<Parameter>  <Parameter List Prime>")
        if self.r_Parameter(flag="Doesn't need to pass"):
            self.r_ParameterListPrime()
            return True
        return False

    def r_ParameterListPrime(self):
        self.new_production.append("<Parameter List Prime>\t-->\t,  <Parameter>  <Parameter List Prime>")
        if self.t_lexeme(","):
            self.lexer()
            self.r_Parameter()
            self.r_ParameterListPrime()
        else:
            self.r_Empty()

    def r_Parameter(self, flag="None"):
        self.new_production.append("<Parameter>\t-->\t<IDs>  :  <Qualifier>")
        if self.t_type(TokenIdentifier):
            self.lexer()
            if self.t_lexeme(":"):
                self.lexer()
                self.r_Qualifier()
                return True
            else:
                self.raise_syntax_error(":")
        elif flag == "None":
            self.raise_syntax_error("Identifier")
        else:
            return False

    def r_Qualifier(self, flag="None"):
        self.new_production.append("<Qualifier>\t-->\tint  '|'  bool  '|'  real")
        if self.t_lexeme("int") or self.t_lexeme("bool") or self.t_lexeme("real"):
            self.lexer()
            return True
        elif flag != "None":
            return False
        else:
            self.raise_syntax_error("Qualifier [int, bool, real]")

    def r_Body(self):
        self.new_production.append("<Body>\t-->\t{  <Statement List>  }")
        if self.t_lexeme("{"):
            self.lexer()
            self.r_StatementList("Must Pass")
            if self.t_lexeme("}"):
                self.lexer()
                return
            else:
                self.raise_syntax_error("}")
        else:
            self.raise_syntax_error("{")

    def r_StatementList(self, flag="None"):
        self.new_production.append("<Statement List>\t-->\t<Statement>  <Statement List Prime>")
        if self.r_Statement():
            self.r_StatementListPrime()
            return True
        elif flag == "None":
            return False
        else:
            self.raise_syntax_error("appropriate Statement preceding '{' token.")

    def r_StatementListPrime(self):
        self.new_production.append("<Statement List Prime>\t-->\t<Statement List>  '|'  <Empty>")
        if not self.r_StatementList():
            self.r_Empty()

    def r_Statement(self):
        self.new_production.append("<Statement>\t-->\t<Compound>  '|'  <Assign>  '|'  <If>  '|'  <Print>  '|'  <Scan>"
                                   "  '|'  <While>")
        if self.r_Compound() or self.r_Assign() or self.r_If() or self.r_Return() or self.r_Print() or self.r_Scan() or self.r_While():
            return True
        return False

    def r_Compound(self):
        self.new_production.append("<Compound>\t-->\t{  <Statement List>  }")
        if self.t_lexeme("{"):
            self.lexer()
            if not self.r_StatementList("Must Pass"):
                self.raise_syntax_error("appropriate Statement preceding '{' token.")
            if self.t_lexeme("}"):
                self.lexer()
                return True
            else:
                self.raise_syntax_error("}")
        else:
            return False

    def r_Assign(self):
        self.new_production.append("<Assign>\t-->\tIDENTIFIER  =  <Expression>  ;")
        if self.t_type(TokenIdentifier):
            self.lexer()
            if self.t_lexeme("="):
                self.lexer()
                self.r_Expression()
                if self.t_lexeme(";"):
                    self.lexer()
                    return True
                else:
                    self.raise_syntax_error(";")
            else:
                self.raise_syntax_error("=")
        else:
            return False

    def r_If(self):
        self.new_production.append("<If>\t-->\tif  (  <Condition>  )  <Statement>  <If Prime>")
        if self.t_lexeme("if"):
            self.lexer()
            if self.t_lexeme("("):
                self.lexer()
                self.r_Condition()
                if self.t_lexeme(")"):
                    self.lexer()
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
        self.new_production.append("<If Prime>\t-->\tifend  '|'  else  <Statement>  ifend")
        if self.t_lexeme("ifend"):
            self.lexer()
            return
        elif self.t_lexeme("else"):
            self.lexer()
            if self.r_Statement():
                if self.t_lexeme("ifend"):
                    self.lexer()
                    return
                else:
                    self.raise_syntax_error("ifend")
            else:
                self.raise_syntax_error("appropriate statement after if conditional.")
        else:
            self.raise_syntax_error("ifend or else statement.")

    def r_Return(self):
        self.new_production.append("<Return>\t-->\treturn  <Return Prime>")
        if self.t_lexeme("return"):
            self.lexer()
            self.r_ReturnPrime()
            return True
        return False

    def r_ReturnPrime(self):
        self.new_production.append("<Return Prime>\t-->\t;  '|'  <Expression>  ;")
        if self.t_lexeme(";"):
            self.lexer()
        else:
            self.r_Expression()
            if self.t_lexeme(";"):
                self.lexer()
            else:
                self.raise_syntax_error(";")

    def r_Print(self):
        self.new_production.append("<Print>\t-->\tput  (  <Expression>  )  ;")
        if self.t_lexeme("put"):
            self.lexer()
            if self.t_lexeme("("):
                self.lexer()
                self.r_Expression()
                if self.t_lexeme(")"):
                    self.lexer()
                    if self.t_lexeme(";"):
                        self.lexer()
                        return True
                    else:
                        self.raise_syntax_error(";")
                else:
                    self.raise_syntax_error(")")
            else:
                self.raise_syntax_error("(")
        return False

    def r_Scan(self):
        self.new_production.append("<Scan>\t-->\tget  (  <IDs>  )  ;")
        if self.t_lexeme("get"):
            self.lexer()
            if self.t_lexeme("("):
                self.lexer()
                self.r_Identifiers()
                if self.t_lexeme(")"):
                    self.lexer()
                    if self.t_lexeme(";"):
                        self.lexer()
                        return True
                    else:
                        self.raise_syntax_error(";")
                else:
                    self.raise_syntax_error(")")
            else:
                self.raise_syntax_error("(")
        return False

    def r_While(self):
        self.new_production.append("<While>\t-->\twhile  (  <Condition>  )  <Statement>  whileend")
        if self.t_lexeme("while"):
            self.lexer()
            if self.t_lexeme("("):
                self.lexer()
                self.r_Condition()
                if self.t_lexeme(")"):
                    self.lexer()
                    if self.r_Statement():
                        if self.t_lexeme("whileend"):
                            self.lexer()
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
        self.new_production.append("<IDs>\t-->\tIDENTIFIER  <IDs Prime>")
        if self.t_type(TokenIdentifier):
            self.lexer()
            self.r_IdentifiersPrime()
        else:
            self.raise_syntax_error("Identifier")

    def r_IdentifiersPrime(self):
        self.new_production.append("<IDs Prime>\t-->\t,  <IDs>  '|'  <Empty>")
        if self.t_lexeme(","):
            self.lexer()
            self.r_Identifiers()
        else:
            self.r_Empty()

    def r_Condition(self):
        self.new_production.append("<Condition>\t-->\t<Expression>  <Relational Operator>  <Expression>")
        self.r_Expression()
        self.r_RelationalOperator()
        self.r_Expression()

    def r_OptDeclarationList(self):
        self.new_production.append("<Optional Declaration List>\t-->\t<Declaration List>  '|'  <Empty>")
        if self.r_DeclarationList():
            return
        else:
            self.r_Empty()

    def r_DeclarationList(self):
        self.new_production.append("<Declaration List>\t-->\t<Declaration>  ;  <Declaration List Prime>")
        if self.r_Declarations():
            if self.t_lexeme(";"):
                self.lexer()
                self.r_DeclarationListPrime()
                return True
            else:
                self.raise_syntax_error(";")
        return False


    def r_DeclarationListPrime(self):
        self.new_production.append("<Declaration List Prime>\t-->\t<Declaration List>  '|'  <Empty>")
        if self.r_DeclarationList():
            return
        else:
            self.r_Empty()

    def r_Declarations(self):
        self.new_production.append("<Declaration>\t-->\t<Qualifier>  <IDs>")
        if self.r_Qualifier("Doesn't need to pass"):
            self.r_Identifiers()
            return True
        else:
            return False

    def r_RelationalOperator(self):
        self.new_production.append("<Relational Operator>\t-->\t==  '|'  ^=  '|'  >  '|'  <  '|'  =>  '|'  =<")
        if self.t_lexeme("==") or self.t_lexeme("^=") or self.t_lexeme(">") or self.t_lexeme("<") or self.t_lexeme("=>") or self.t_lexeme("=<"):
            self.lexer()
        else:
            self.raise_syntax_error("Relational Operator")

    def r_Expression(self):
        self.new_production.append("<Expression>\t-->\t<Term>  <Expression Prime>")
        self.r_Term()
        self.r_ExpressionPrime()

    def r_ExpressionPrime(self):
        self.new_production.append("<Expression Prime>\t-->\t+  <Term>  <Expression Prime>  '|'  -  <Term>  <Expression Prime>")
        if self.t_lexeme("+") or self.t_lexeme("-"):
            self.lexer()
            self.r_Term()
            self.r_ExpressionPrime()
        else:
            self.r_Empty()

    def r_Term(self):
        self.new_production.append("<Term>\t-->\t<Factor>  <Term Prime>")
        self.r_Factor()
        self.r_TermPrime()

    def r_TermPrime(self):
        self.new_production.append("<Term Prime>\t-->\t*  <Factor>  <Term Prime>  '|'  /  <Factor>  <Term Prime>")
        if self.t_lexeme("*") or self.t_lexeme("/"):
            self.lexer()
            self.r_Factor()
            self.r_TermPrime()
        else:
            self.r_Empty()

    def r_Factor(self):
        self.new_production.append("<Factor>\t-->\t-  <Primary>  '|'  <Primary>")
        if self.t_lexeme("-"):
            self.lexer()
        self.r_Primary()

    def r_Primary(self):
        self.new_production.append("<Primary>\t-->\tIDENTIFIER  '|'  INTEGER  '|'  REAL  '|'  Identifier  (  <IDs>  )"
                                   "  '|'  (  <Expression>  )  '|'  true  '|'  false")
        if self.t_type(TokenInteger) or self.t_type(TokenReal) or self.t_lexeme("true") or self.t_lexeme("false"):
            self.lexer()
            return
        elif self.t_type(TokenIdentifier):
            self.lexer()
            if self.t_lexeme("("):
                self.lexer()
                self.r_Identifiers()
                if self.t_lexeme(")"):
                    self.lexer()
                else:
                    self.raise_syntax_error(")")
            else:
                return
        elif self.t_lexeme("("):
            self.lexer()
            self.r_Expression()
            if self.t_lexeme(")"):
                self.lexer()
                return
            else:
                self.raise_syntax_error(")")
        else:
            self.raise_syntax_error("acceptable Primary Expression [Identifier, Real, Integer, Bool...")

    def r_Empty(self):
        self.new_production.append("<Empty>\t-->\te")
        return
