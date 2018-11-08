from Tokens import *
from CompilerExceptions import *
import argparse
import Lexer
from colorama import Fore
from functools import partial


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

    def nt_call(self, production_str: str, *args):
        self.print_production(production_str)
        p = self.Lexer.bt_get()
        ex_syntax = None
        for prod_list in args:
            if not isinstance(prod_list, list):
                raise TypeError
            try:
                for function_ptr in prod_list:
                    function_ptr()
                return
            except CSyntaxError as ex:
                ex_syntax = ex
                self.Lexer.bt_set(p)
        raise ex_syntax

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
        p1 = [partial(self.r_OptFunctionDefinitions),
              partial(self.t_lexeme, '$$'),
              partial(self.r_OptDeclarationList),
              partial(self.r_StatementList),
              partial(self.t_lexeme, '$$')]
        self.nt_call("Rat18F -> OFD $$ ODL SL $$", p1)

    def r_OptFunctionDefinitions(self):
        p1 = [partial(self.r_FunctionDefinitions)]
        p2 = [partial(self.r_Empty)]
        self.nt_call("OptFunctionDefinition -> FunctionDefinitions | Empty", p1, p2)

    def r_FunctionDefinitions(self):
        p1 = [partial(self.r_Function),
              partial(self.r_FunctionDefinitions_prime)]
        self.nt_call("FunctionDefinitions -> Function FunctionDefinitions' ", p1)

    def r_FunctionDefinitions_prime(self):
        p1 = [partial(self.r_FunctionDefinitions)]
        p2 = [partial(self.r_Empty)]
        self.nt_call("FunctionDefinitions' -> FunctionDefinitions | Empty ", p1, p2)

    def r_Function(self):
        p1 = [partial(self.t_lexeme, "function"),
              partial(self.t_type, TokenIdentifier),
              partial(self.t_lexeme, "("),
              partial(self.r_OptParameterList),
              partial(self.t_lexeme, ")"),
              partial(self.r_OptDeclarationList),
              partial(self.r_Body)]
        self.nt_call("Function -> function Identifier ( OptParameterList ) OptDeclarationList Body", p1)

    def r_OptParameterList(self):
        p1 = [partial(self.r_ParameterList)]
        p2 = [partial(self.r_Empty)]
        self.nt_call("OptParameterList -> ParameterList | Empty", p1, p2)

    def r_ParameterList(self):
        p1 = [partial(self.r_Parameter),
              partial(self.r_ParameterList_prime)]
        self.nt_call("ParameterList -> Parameter ParameterList' ", p1)

    def r_ParameterList_prime(self):
        p1 = [partial(self.t_lexeme, ","),
              partial(self.r_Parameter)]
        p2 = [partial(self.r_Empty)]
        self.nt_call("ParameterList' -> , Parameter | Empty", p1, p2)

    def r_Parameter(self):
        p1 = [partial(self.r_IDs),
              partial(self.t_lexeme, ":"),
              partial(self.r_Qualifier)]
        self.nt_call("Parameter -> IDs : Qualifier", p1)

    def r_Qualifier(self):
        p1 = [partial(self.t_lexeme, "int")]
        p2 = [partial(self.t_lexeme, "bool")]
        p3 = [partial(self.t_lexeme, "real")]
        self.nt_call("Qualifier -> int | bool | real", p1, p2, p3)

    def r_Body(self):
        p1 = [partial(self.t_lexeme, "{"),
              partial(self.r_StatementList),
              partial(self.t_lexeme, "}")]
        self.nt_call("Body -> { StatementList }", p1)

    def r_OptDeclarationList(self):
        p1 = [partial(self.r_DeclarationList)]
        p2 = [partial(self.r_Empty)]
        self.nt_call("OptDeclarationList -> DeclarationList | Empty", p1, p2)

    def r_DeclarationList(self):
        p1 = [partial(self.r_Declaration),
              partial(self.t_lexeme, ";"),
              partial(self.r_DeclarationList_prime)]
        self.nt_call("DeclarationList -> Declaration ; DeclarationList' ", p1)

    def r_DeclarationList_prime(self):
        p1 = [partial(self.r_DeclarationList)]
        p2 = [partial(self.r_Empty)]
        self.nt_call("DeclarationList' -> DeclarationList | Empty ", p1, p2)

    def r_Declaration(self):
        p1 = [partial(self.r_Qualifier),
              partial(self.r_IDs)]
        self.nt_call("Declaration -> Qualifier IDs ", p1)

    def r_IDs(self):
        p1 = [partial(self.t_type, TokenIdentifier),
              partial(self.r_IDs_prime)]
        self.nt_call("IDs -> ID IDs' ", p1)

    def r_IDs_prime(self):
        p1 = [partial(self.t_lexeme, ","),
              partial(self.r_IDs)]
        p2 = [partial(self.r_Empty)]
        self.nt_call("IDs' -> , IDs | Empty ", p1, p2)

    def r_StatementList(self):
        p1 = [partial(self.r_Statement),
              partial(self.r_StatementList_prime)]
        self.nt_call("StatementList -> Statement StatementList' ", p1)

    def r_StatementList_prime(self):
        p1 = [partial(self.r_StatementList)]
        p2 = [partial(self.r_Empty)]
        self.nt_call("StatementList' -> StatementList | Empty ", p1, p2)

    def r_Statement(self):
        p1 = [partial(self.r_Compound)]
        p2 = [partial(self.r_Assign)]
        p3 = [partial(self.r_If)]
        p4 = [partial(self.r_Return)]
        p5 = [partial(self.r_Print)]
        p6 = [partial(self.r_Scan)]
        p7 = [partial(self.r_While)]
        self.nt_call("Statement -> Compound | Assign | If | Return | Print | Scan | While", p1, p2, p3, p4, p5, p6, p7)

    def r_Compound(self):
        p1 = [partial(self.t_lexeme, "{"),
              partial(self.r_StatementList),
              partial(self.t_lexeme, "}")]
        self.nt_call("Compound -> { StatementList }", p1)

    def r_Assign(self):
        p1 = [partial(self.t_type, TokenIdentifier),
              partial(self.t_lexeme, "="),
              partial(self.r_Expression),
              partial(self.t_lexeme, ";")]
        self.nt_call("Assign -> ID = Expression ;", p1)

    def r_If(self):
        p1 = [partial(self.t_lexeme, "if"),
              partial(self.t_lexeme, "("),
              partial(self.r_Condition),
              partial(self.t_lexeme, ")"),
              partial(self.r_Statement),
              partial(self.r_If_prime)]
        self.nt_call("If -> if ( Condition ) Statement If' ", p1)

    def r_If_prime(self):
        p1 = [partial(self.t_lexeme, "ifend")]
        p2 = [partial(self.t_lexeme, "else"),
              partial(self.r_Statement),
              partial(self.t_lexeme, "ifend")]
        self.nt_call("If' -> ifend | else Statement ifend ", p1, p2)

    def r_Return(self):
        p1 = [partial(self.t_lexeme, "return"),
              partial(self.t_lexeme, ";")]
        p2 = [partial(self.t_lexeme, "return"),
              partial(self.r_Expression),
              partial(self.t_lexeme, ";")]
        self.nt_call("Return -> return ; | return Expression ;", p1, p2)

    def r_Print(self):
        p1 = [partial(self.t_lexeme, "put"),
              partial(self.t_lexeme, "("),
              partial(self.r_Expression),
              partial(self.t_lexeme, ")"),
              partial(self.t_lexeme, ";")]
        self.nt_call("Print -> put ( Expression ) ;", p1)

    def r_Scan(self):
        p1 = [partial(self.t_lexeme, "get"),
              partial(self.t_lexeme, "("),
              partial(self.r_IDs),
              partial(self.t_lexeme, ")"),
              partial(self.t_lexeme, ";")]
        self.nt_call("Scan -> get ( IDs ) ;", p1)

    def r_While(self):
        p1 = [partial(self.t_lexeme, "while"),
              partial(self.t_lexeme, "("),
              partial(self.r_Condition),
              partial(self.t_lexeme, ")"),
              partial(self.r_Statement),
              partial(self.t_lexeme, "whilend")]
        self.nt_call("While -> while ( Condition ) Statement whileend", p1)

    def r_Condition(self):
        p1 = [partial(self.r_Expression),
              partial(self.r_Relop),
              partial(self.r_Expression)]
        self.nt_call("Condition -> Expression Relop Expression", p1)

    def r_Relop(self):
        p1 = [partial(self.t_lexeme, "==")]
        p2 = [partial(self.t_lexeme, "^=")]
        p3 = [partial(self.t_lexeme, ">")]
        p4 = [partial(self.t_lexeme, "<")]
        p5 = [partial(self.t_lexeme, "=>")]
        p6 = [partial(self.t_lexeme, "=<")]
        self.nt_call("Relop -> == | ^= | > | < | => | =<", p1, p2, p3, p4, p5, p6)

    def r_Expression(self):
        p1 = [partial(self.r_Term),
              partial(self.r_Expression_prime)]
        self.nt_call("Expression -> Term Expression' ", p1)

    def r_Expression_prime(self):
        p1 = [partial(self.t_lexeme, "+"),
              partial(self.r_Term),
              partial(self.r_Expression_prime)]
        p2 = [partial(self.t_lexeme, "-"),
              partial(self.r_Term),
              partial(self.r_Expression_prime)]
        p3 = [partial(self.r_Empty)]
        self.nt_call("Expression' -> + Term Expression’ | - Term Expression’ | Empty ", p1, p2, p3)

    def r_Term(self):
        p1 = [partial(self.r_Factor),
              partial(self.r_Term_prime)]
        self.nt_call("Term -> Factor Term' ", p1)

    def r_Term_prime(self):
        p1 = [partial(self.t_lexeme, "*"),
              partial(self.r_Factor),
              partial(self.r_Term_prime)]
        p2 = [partial(self.t_lexeme, "/"),
              partial(self.r_Factor),
              partial(self.r_Term_prime)]
        p3 = [partial(self.r_Empty)]
        self.nt_call("Term' -> * Factor Term' | / Factor Term' | Empty ", p1, p2, p3)

    def r_Factor(self):
        p1 = [partial(self.t_lexeme, "-"),
              partial(self.r_Primary)]
        p2 = [partial(self.r_Primary)]
        self.nt_call("Factor -> -Primary | Primary", p1, p2)

    def r_Primary(self):
        p1 = [partial(self.t_type, TokenIdentifier)]
        p2 = [partial(self.t_type, TokenInteger)]
        p3 = [partial(self.t_type, TokenIdentifier),
              partial(self.t_lexeme, "("),
              partial(self.r_IDs),
              partial(self.t_lexeme, ")")]
        p4 = [partial(self.t_lexeme, "("),
              partial(self.r_Expression),
              partial(self.t_lexeme, ")")]
        p5 = [partial(self.t_type, TokenReal)]
        p6 = [partial(self.t_lexeme, "true")]
        p7 = [partial(self.t_lexeme, "false")]
        self.nt_call("Primary -> ID | INT | ID ( IDs ) | ( Expression ) | Real | true | false", p1, p2, p3, p4, p5,
                     p6, p7)

    def r_Empty(self):
        return


