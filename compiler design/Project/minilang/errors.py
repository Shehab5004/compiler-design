class Error:
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
    
    def __str__(self):
        if self.line is not None and self.column is not None:
            return f"Error at {self.line}:{self.column}: {self.message}"
        return f"Error: {self.message}"

class LexerError(Error):
    pass

class ParserError(Error):
    pass

class RuntimeError(Error):
    pass