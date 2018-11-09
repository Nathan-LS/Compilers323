import Lexer


class SyntaxAnalyzer:
    def __init__(self, file_ptr):
        self.file_ptr = file_ptr
        self.Lexer = Lexer.Lexer(file_ptr)

    def run_analyzer(self):
        self.r_Rat18F()

#   Add private method to tokenbase "is_lexeme(self, lexeme):
    def t_lexeme(self, lexeme):
        try:
            if self.Lexer.peek_token().return_token() == lexeme:
                return True
            return False
        except:
            self.print_error(lexeme)

#   change to isinstance(TokenIdentifier)
    def t_type(self, lex_type):
        try:
            if self.Lexer.peek_token().__class__.__name__ == lex_type:
                return True
            return False
        except:
            self.print_error(lex_type)

    def print_error(self, expected):
        try:
            print("Error occurred at line number: {}. Got \"{}\", but expected an {}".format(
                                                                                    self.Lexer.peek_token().get_line(),
                                                                                    self.Lexer.peek_token().return_token(),
                                                                                    expected))
        except:
            print("Error occurred at end of file. Reached end of file marker, but expected {} or \"$$\"".format(expected))
        exit(-1)

    def r_Rat18F(self):
        self.r_OptFunctionDefinitions()
        if self.t_lexeme("$$"):
            print(self.Lexer.lexer())
            self.r_OptDeclarationList()
            self.r_StatementList("Must have statement list")
        else:
            self.print_error("$$")
        if self.t_lexeme("$$"):
            print(self.Lexer.lexer())
        else:
            self.print_error("$$")
        if self.Lexer.check_eof():
            print("Success! There are no syntax errors here! :)")
        else:
            print("Error. Expected end of file marker after $$ token.")

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
            print(self.Lexer.lexer())
            if self.t_type("TokenIdentifier"):
                print(self.Lexer.lexer())
                if self.t_lexeme("("):
                    print(self.Lexer.lexer())
                    self.r_OptParameterList()
                    if self.t_lexeme(")"):
                        print(self.Lexer.lexer())
                        self.r_OptDeclarationList()
                        self.r_Body()
                        return True
                    else:
                        self.print_error("\")\"")
                else:
                    self.print_error("\"(\"")
            else:
                self.print_error("Identifier")
        return False

    def r_OptParameterList(self):
        self.r_ParameterList()
        self.r_Empty()

    def r_ParameterList(self):
        self.r_Parameter()
        self.r_ParameterListPrime()

    def r_ParameterListPrime(self):
        if self.t_lexeme(","):
            print(self.Lexer.lexer())
            self.r_Parameter()
        else:
            self.r_Empty()

    def r_Parameter(self):
        if self.t_type("TokenIdentifier"):
            print(self.Lexer.lexer())
            if self.t_lexeme(":"):
                print(self.Lexer.lexer())
                self.r_Qualifier()
            else:
                self.print_error(":")
        else:
            self.print_error("Identifier")

    def r_Qualifier(self, flag="None"):
        if self.t_lexeme("int") or self.t_lexeme("bool") or self.t_lexeme("real"):
            print(self.Lexer.lexer())
            return True
        elif flag != "None":
            return False
        else:
            self.print_error("Qualifier [int, bool, real]")

    def r_Body(self):
        if self.t_lexeme("{"):
            print(self.Lexer.lexer())
            self.r_StatementList("Must Pass")
            if self.t_lexeme("}"):
                print(self.Lexer.lexer())
                return
            else:
                self.print_error("}")
        else:
            self.print_error("{")

    def r_StatementList(self, flag="None"):
        if self.r_Statement():
            self.r_StatementListPrime()
            return True
        elif flag == "None":
            return False
        else:
            self.print_error("appropriate Statement preceding '{' token.")

    def r_StatementListPrime(self):
        if not self.r_StatementList():
            self.r_Empty()

    def r_Statement(self):
        if self.r_Compound() or self.r_Assign() or self.r_If() or self.r_Return() or self.r_Print() or self.r_Scan() or self.r_While():
            return True
        return False

    def r_Compound(self):
        if self.t_lexeme("{"):
            print(self.Lexer.lexer())
            if not self.r_StatementList("Must Pass"):
                self.print_error("appropriate Statement preceding '{' token.")
            if self.t_lexeme("}"):
                print(self.Lexer.lexer())
                return True
            else:
                self.print_error("}")
        else:
            return False

    def r_Assign(self):
        if self.t_type("TokenIdentifier"):
            print(self.Lexer.lexer())
            if self.t_lexeme("="):
                print(self.Lexer.lexer())
                self.r_Expression()
                if self.t_lexeme(";"):
                    print(self.Lexer.lexer())
                    return True
                else:
                    self.print_error(";")
            else:
                self.print_error("=")
        else:
            return False

    def r_If(self):
        if self.t_lexeme("if"):
            print(self.Lexer.lexer())
            if self.t_lexeme("("):
                print(self.Lexer.lexer())
                self.r_Condition()
                if self.t_lexeme(")"):
                    print(self.Lexer.lexer())
                    if self.r_Statement():
                        self.r_IfPrime()
                        return True
                    else:
                        self.print_error("appropriate statement after if conditional.")
                else:
                    self.print_error(")")
            else:
                self.print_error("(")
        else:
            return False

    def r_IfPrime(self):
        if self.t_lexeme("ifend"):
            print(self.Lexer.lexer())
            return
        elif self.t_lexeme("else"):
            print(self.Lexer.lexer())
            if self.r_Statement():
                if self.t_lexeme("ifend"):
                    print(self.Lexer.lexer())
                    return
                else:
                    self.print_error("ifend")
            else:
                self.print_error("appropriate statement after if conditional.")
        else:
            self.print_error("ifend or else statement.")

    def r_Return(self):
        if self.t_lexeme("return"):
            print(self.Lexer.lexer())
            self.r_ReturnPrime()
            return True
        return False

    def r_ReturnPrime(self):
        if self.t_lexeme(";"):
            print(self.Lexer.lexer())
        else:
            self.r_Expression()
            if self.t_lexeme(";"):
                print(self.Lexer.lexer())
            else:
                self.print_error(";")

    def r_Print(self):
        if self.t_lexeme("put"):
            print(self.Lexer.lexer())
            if self.t_lexeme("("):
                print(self.Lexer.lexer())
                self.r_Expression()
                if self.t_lexeme(")"):
                    print(self.Lexer.lexer())
                    if self.t_lexeme(";"):
                        print(self.Lexer.lexer())
                        return True
                    else:
                        self.print_error(";")
                else:
                    self.print_error(")")
            else:
                self.print_error("(")
        return False

    def r_Scan(self):
        if self.t_lexeme("get"):
            print(self.Lexer.lexer())
            if self.t_lexeme("("):
                print(self.Lexer.lexer())
                self.r_Identifiers()
                if self.t_lexeme(")"):
                    print(self.Lexer.lexer())
                    if self.t_lexeme(";"):
                        print(self.Lexer.lexer())
                        return True
                    else:
                        self.print_error(";")
                else:
                    self.print_error(")")
            else:
                self.print_error("(")
        return False

    def r_While(self):
        if self.t_lexeme("while"):
            print(self.Lexer.lexer())
            if self.t_lexeme("("):
                print(self.Lexer.lexer())
                self.r_Condition()
                if self.t_lexeme(")"):
                    print(self.Lexer.lexer())
                    if self.r_Statement():
                        if self.t_lexeme("whileend"):
                            print(self.Lexer.lexer())
                            return True
                        else:
                            self.print_error("whileend")
                    else:
                        self.print_error("appropriate statement following while loop.")
                else:
                    self.print_error(")")
            else:
                self.print_error("(")
        return False

    def r_Identifiers(self):
        if self.t_type("TokenIdentifier"):
            print(self.Lexer.lexer())
            self.r_IdentifiersPrime()
        else:
            self.print_error("Identifier")

    def r_IdentifiersPrime(self):
        if self.t_lexeme(","):
            print(self.Lexer.lexer())
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
                print(self.Lexer.lexer())
                self.r_DeclarationListPrime()
                return True
            else:
                self.print_error(";")
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
            print(self.Lexer.lexer())
        else:
            self.print_error("Relational Operator")

    def r_Expression(self):
        self.r_Term()
        self.r_ExpressionPrime()

    def r_ExpressionPrime(self):
        if self.t_lexeme("+") or self.t_lexeme("-"):
            print(self.Lexer.lexer())
            self.r_Term()
            self.r_ExpressionPrime()
        else:
            self.r_Empty()

    def r_Term(self):
        self.r_Factor()
        self.r_TermPrime()

    def r_TermPrime(self):
        if self.t_lexeme("*") or self.t_lexeme("/"):
            print(self.Lexer.lexer())
            self.r_Factor()
            self.r_TermPrime()
        else:
            self.r_Empty()

    def r_Factor(self):
        if self.t_lexeme("-"):
            print(self.Lexer.lexer())
        self.r_Primary()

    def r_Primary(self):
        if self.t_type("TokenInteger") or self.t_type("TokenReal") or self.t_lexeme("true") or self.t_lexeme("false"):
            print(self.Lexer.lexer())
            return
        elif self.t_type("TokenIdentifier"):
            print(self.Lexer.lexer())
            if self.t_lexeme("("):
                print(self.Lexer.lexer())
                self.r_Identifiers()
                if self.t_lexeme(")"):
                    print(self.Lexer.lexer())
                else:
                    self.print_error(")")
            else:
                return
        elif self.t_lexeme("("):
            print(self.Lexer.lexer())
            self.r_Expression()
            if self.t_lexeme(")"):
                print(self.Lexer.lexer())
                return
            else:
                self.print_error(")")
        else:
            self.print_error("acceptable Primary Expression [Identifier, Real, Integer, Bool...")

    def r_Empty(self):
        return