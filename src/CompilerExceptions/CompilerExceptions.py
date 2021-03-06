import Tokens


class CompilerExceptions(Exception):
    def __init__(self, message="Compiler base exception. Probably should not be raising this."):
        self.message = message
        super().__init__(self.get_message())

    def get_message(self):
        return self.message


class CSyntaxError(CompilerExceptions):
    def __init__(self, token_obj=None, expect=None):
        self.token = token_obj
        self.expect = expect
        super().__init__(self.get_message())

    def get_message(self):
        line_no = self.token.line if self.token else "Unknown"
        lexeme = self.token.lexeme if self.token else "Unknown Lexeme"
        t_type = self.token.type_name() if self.token else "Unknown token type"
        exp = self.expect if self.expect else "Unknown"
        msg = "Error occurred at line number: {}. Got '{}', but expected an '{}'.".format(line_no, lexeme, exp)
        return msg


class InvalidDeclareReal(CSyntaxError):
    def get_message(self):
        return "Error on line {}. Unable to declare real.".format(self.token.line)


class InvalidBoolUsage(CSyntaxError):
    def get_message(self):
        return "Error on line {}. Unable to assign value to bool other than true (1) or false (0). Unable to do arithmetic operations on bool values." \
               "".format(self.token.line)


class UndeclaredVariable(CSyntaxError):
    def get_message(self):
        return "Error on line {}. Use of an undeclared variable: '{}'.".format(self.token.line, self.token.lexeme)


class RedeclaredVariable(CSyntaxError):
    def get_message(self):
        return "Error on line {}. Attempting to redeclare an already declared variable: '{}'." \
               "".format(self.token.line, self.token.lexeme)


class CSyntaxErrorEOF(CSyntaxError):
    def __init__(self, expect=None):
        self.expect = expect
        super().__init__(token_obj=None, expect=self.expect)

    def get_message(self):
        exp = self.expect if self.expect else "Unknown"
        msg = "Error occurred at end of file. Reached end of file marker, but expected '{}' or '$$'.".format(exp)
        return msg


class BackTrackerInvalidIndex(CompilerExceptions):
    def get_message(self):
        return "Invalid backtracking index."


class SymbolExists(CompilerExceptions):
    def get_message(self):
        return "Symbol already exits in the symbol table."
