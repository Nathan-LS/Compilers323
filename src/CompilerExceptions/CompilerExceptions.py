import Tokens


class CompilerExceptions(Exception):
    def __init__(self, token_obj=None, expect=None):
        self.token: Tokens.TokenBase = token_obj
        self.expect = expect
        super().__init__(self.get_message())

    def get_message(self):
        return "Compiler base exception. Probably should not be raising this."


class CSyntaxError(CompilerExceptions):
    def __init__(self, token_obj=None, expect=None):
        super().__init__(token_obj, expect)

    def get_message(self):
        line_no = self.token.line if self.token else "Unknown"
        lexeme = self.token.lexeme if self.token else "Unknown Lexeme"
        t_type = self.token.type_name() if self.token else "Unknown token type"
        exp = self.expect if self.expect else "Unknown"
        msg = "Syntax error on line {}. Got '{}' of type {} but was expecting '{}'.".format(line_no, lexeme, t_type, exp)
        return msg


class BackTrackerInvalidIndex(CompilerExceptions):
    def __init__(self, token_obj=None, expect=None):
        super().__init__(token_obj, expect)

    def get_message(self):
        return "Invalid backtracking index."
