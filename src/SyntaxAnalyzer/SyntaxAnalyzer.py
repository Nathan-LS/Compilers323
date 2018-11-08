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

    def exception_helper(self, bt_pos: int, expect: str):
        """
        Raises an exception after reaching the end of a NT. Catches EOF files and returns the appropriate CSyntaxError
        :param bt_pos: lexer error position
        :param expect: expected str/token
        :return: None
        """
        try:
            raise CSyntaxError(self.Lexer.lexer_peek(bt_pos), expect)
        except StopIteration:
            raise CSyntaxErrorEOF(expect=expect)

    def r_Rat18F(self):
        self.print_production("Rat18F -> OFD $$ ODL SL $$")
        p = self.Lexer.bt_get()
        try:
            self.r_OptFunctionDefinitions()
            self.t_lexeme('$$')
            self.r_OptDeclarationList()
            self.r_StatementList()
            self.t_lexeme('$$')
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_OptFunctionDefinitions(self):
        self.print_production("OptFunctionDefinition -> FunctionDefinitions | Empty")
        p = self.Lexer.bt_get()
        try:
            self.r_FunctionDefinitions()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Empty()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "OptFunctionDefinitions")

    def r_FunctionDefinitions(self):
        self.print_production("FunctionDefinitions -> Function FunctionDefinitions' ")
        p = self.Lexer.bt_get()
        try:
            self.r_Function()
            self.r_FunctionDefinitions_prime()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "FunctionDefinitions")

    def r_FunctionDefinitions_prime(self):
        self.print_production("FunctionDefinitions' -> FunctionDefinitions | Empty ")
        p = self.Lexer.bt_get()
        try:
            self.r_FunctionDefinitions()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Empty()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "FunctionDefinitions_prime")

    def r_Function(self):
        self.print_production("Function -> function Identifier ( OptParameterList ) OptDeclarationList Body")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("function")
            self.t_type(TokenIdentifier)
            self.t_lexeme("(")
            self.r_OptParameterList()
            self.t_lexeme(")")
            self.r_OptDeclarationList()
            self.r_Body()
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_OptParameterList(self):
        self.print_production("OptParameterList -> ParameterList | Empty")
        p = self.Lexer.bt_get()
        try:
            self.r_ParameterList()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Empty()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "OptParameterList")

    def r_ParameterList(self):
        self.print_production("ParameterList -> Parameter ParameterList' ")
        p = self.Lexer.bt_get()
        try:
            self.r_Parameter()
            self.r_ParameterList_prime()
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_ParameterList_prime(self):
        self.print_production("ParameterList' -> , Parameter | Empty")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme(",")
            self.r_Parameter()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Empty()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "ParameterList'")

    def r_Parameter(self):
        self.print_production("Parameter -> IDs : Qualifier")
        p = self.Lexer.bt_get()
        try:
            self.r_IDs()
            self.t_lexeme(":")
            self.r_Qualifier()
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_Qualifier(self):
        self.print_production("Qualifier -> int | bool | real")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("int")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("bool")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("real")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "Qualifier")

    def r_Body(self):
        self.print_production("Body -> { StatementList }")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("{")
            self.r_StatementList()
            self.t_lexeme("}")
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_OptDeclarationList(self):
        self.print_production("OptDeclarationList -> DeclarationList | Empty")
        p = self.Lexer.bt_get()
        try:
            self.r_DeclarationList()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Empty()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "OptDeclarationList")

    def r_DeclarationList(self):
        self.print_production("DeclarationList -> Declaration ; DeclarationList' ")
        p = self.Lexer.bt_get()
        try:
            self.r_Declaration()
            self.t_lexeme(";")
            self.r_DeclarationList_prime()
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_DeclarationList_prime(self):
        self.print_production("DeclarationList' -> DeclarationList | Empty ")
        p = self.Lexer.bt_get()
        try:
            self.r_DeclarationList()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Empty()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "DeclarationList_prime")

    def r_Declaration(self):
        self.print_production("Declaration -> Qualifier IDs ")
        p = self.Lexer.bt_get()
        try:
            self.r_Qualifier()
            self.r_IDs()
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_IDs(self):
        self.print_production("IDs -> ID IDs' ")
        p = self.Lexer.bt_get()
        try:
            self.t_type(TokenIdentifier)
            self.r_IDs_prime()
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_IDs_prime(self):
        self.print_production("IDs' -> , IDs | Empty ")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme(",")
            self.r_IDs()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Empty()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "IDs")

    def r_StatementList(self):
        self.print_production("StatementList -> Statement StatementList' ")
        p = self.Lexer.bt_get()
        try:
            self.r_Statement()
            self.r_StatementList_prime()
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_StatementList_prime(self):
        self.print_production("StatementList' -> StatementList | Empty ")
        p = self.Lexer.bt_get()
        try:
            self.r_StatementList()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Empty()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "StatementList_prime")

    def r_Statement(self):
        self.print_production("Statement -> Compound | Assign | If | Return | Print | Scan | While")
        p = self.Lexer.bt_get()
        try:
            self.r_Compound()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Assign()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_If()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Return()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Print()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Scan()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_While()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "Statement")

    def r_Compound(self):
        self.print_production("Compound -> { StatementList }")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("{")
            self.r_StatementList()
            self.t_lexeme("}")
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_Assign(self):
        self.print_production("Assign -> ID = Expression ;")
        p = self.Lexer.bt_get()
        try:
            self.t_type(TokenIdentifier)
            self.t_lexeme("=")
            self.r_Expression()
            self.t_lexeme(";")
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_If(self):
        self.print_production("If -> if ( Condition ) Statement If' ")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("if")
            self.t_lexeme("(")
            self.r_Condition()
            self.t_lexeme(")")
            self.r_Statement()
            self.r_If_prime()
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_If_prime(self):
        self.print_production("If' -> ifend | else Statement ifend ")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("ifend")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("else")
            self.r_Statement()
            self.t_lexeme("ifend")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "If'")

    def r_Return(self):
        self.print_production("Return -> return ; | return Expression ;")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("return")
            self.t_lexeme(";")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("return")
            self.r_Expression()
            self.t_lexeme(";")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "Return")

    def r_Print(self):
        self.print_production("Print -> put ( Expression ) ;")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("put")
            self.t_lexeme("(")
            self.r_Expression()
            self.t_lexeme(")")
            self.t_lexeme(";")
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_Scan(self):
        self.print_production("Scan -> get ( IDs ) ;")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("get")
            self.t_lexeme("(")
            self.r_IDs()
            self.t_lexeme(")")
            self.t_lexeme(";")
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_While(self):
        self.print_production("While -> while ( Condition ) Statement whileend")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("while")
            self.t_lexeme("(")
            self.r_Condition()
            self.t_lexeme(")")
            self.r_Statement()
            self.t_lexeme("whileend")
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_Condition(self):
        self.print_production("Condition -> Expression Relop Expression")
        p = self.Lexer.bt_get()
        try:
            self.r_Expression()
            self.r_Relop()
            self.r_Expression()
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_Relop(self):
        self.print_production("Relop -> == | ^= | > | < | => | =<")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("==")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("^=")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme(">")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("<")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("=>")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("=<")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "Relop")

    def r_Expression(self):
        self.print_production("Expression -> Term Expression' ")
        p = self.Lexer.bt_get()
        try:
            self.r_Term()
            self.r_Expression_prime()
            return
        except CSyntaxErrorEOF as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_Expression_prime(self):
        self.print_production("Expression' -> + Term Expression’ | - Term Expression’ | Empty ")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("+")
            self.r_Term()
            self.r_Expression_prime()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("-")
            self.r_Term()
            self.r_Expression_prime()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Empty()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "Expression'")

    def r_Term(self):
        self.print_production("Term -> Factor Term' ")
        p = self.Lexer.bt_get()
        try:
            self.r_Factor()
            self.r_Term_prime()
            return
        except CSyntaxError as ex:
            self.Lexer.bt_set(p)
            raise ex

    def r_Term_prime(self):
        self.print_production("Term' -> * Factor Term' | / Factor Term' | Empty ")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("*")
            self.r_Factor()
            self.r_Term_prime()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("/")
            self.r_Factor()
            self.r_Term_prime()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Empty()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "Term'")

    def r_Factor(self):
        self.print_production("Factor -> -Primary | Primary")
        p = self.Lexer.bt_get()
        try:
            self.t_lexeme("-")
            self.r_Primary()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.r_Primary()
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "Factor")

    def r_Primary(self):
        self.print_production("Primary -> ID | INT | ID ( IDs ) | ( Expression ) | Real | true | false")
        p = self.Lexer.bt_get()
        try:
            self.t_type(TokenIdentifier)
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_type(TokenInteger)
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_type(TokenIdentifier)
            self.t_lexeme("(")
            self.r_IDs()
            self.t_lexeme(")")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("(")
            self.r_Expression()
            self.t_lexeme(")")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_type(TokenReal)
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("true")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        try:
            self.t_lexeme("false")
            return
        except CSyntaxError:
            self.Lexer.bt_set(p)
        self.exception_helper(p, "Primary")

    def r_Empty(self):
        return


