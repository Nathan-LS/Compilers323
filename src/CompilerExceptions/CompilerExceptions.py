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
