from enum import Enum
from errors import LexerError

class TokenType(Enum):
    EOF = "EOF"
    IDENT = "IDENT"
    NUMBER = "NUMBER"
    STRING = "STRING"
    LET = "LET"
    PRINT = "PRINT"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    TRUE = "TRUE"
    FALSE = "FALSE"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    PERCENT = "PERCENT"
    ASSIGN = "ASSIGN"
    EQ = "EQ"
    NE = "NE"
    LT = "LT"
    GT = "GT"
    LE = "LE"
    GE = "GE"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"

class Token:
    def __init__(self, type, lexeme, line, column, value=None):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.column = column
        self.value = value
    
    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type.value}, '{self.lexeme}', {self.value})"
        return f"Token({self.type.value}, '{self.lexeme}')"

class Lexer:
    def __init__(self, source, filename="<unknown>"):
        self.source = source
        self.filename = filename
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if source else None
    
    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.position += 1
        if self.position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.position]
    
    def peek(self):
        if self.position + 1 >= len(self.source):
            return None
        return self.source[self.position + 1]
    
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        while self.current_char and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.advance()
    
    def make_token(self, type, lexeme=None):
        if lexeme is None:
            lexeme = self.current_char
        return Token(type, lexeme, self.line, self.column)
    
    def read_identifier(self):
        start_pos = self.position
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            self.advance()
        
        ident = self.source[start_pos:self.position]
        
        # Check for keywords
        keywords = {
            'let': TokenType.LET,
            'print': TokenType.PRINT,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT
        }
        
        token_type = keywords.get(ident, TokenType.IDENT)
        return Token(token_type, ident, self.line, self.column - len(ident))
    
    def read_number(self):
        start_pos = self.position
        while self.current_char and self.current_char.isdigit():
            self.advance()
        
        number_str = self.source[start_pos:self.position]
        return Token(TokenType.NUMBER, number_str, self.line, self.column - len(number_str), int(number_str))
    
    def read_string(self):
        self.advance()  # Skip opening quote
        start_pos = self.position
        
        while self.current_char and self.current_char != '"':
            self.advance()
        
        if not self.current_char:
            raise LexerError("Unterminated string", self.line, self.column)
        
        string_value = self.source[start_pos:self.position]
        self.advance()  # Skip closing quote
        
        return Token(TokenType.STRING, string_value, self.line, self.column - len(string_value) - 2, string_value)
    
    def next_token(self):
        while self.current_char:
            self.skip_whitespace()
            
            if not self.current_char:
                break
            
            if self.current_char == '#':
                self.skip_comment()
                continue
            
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
            
            if self.current_char.isdigit():
                return self.read_number()
            
            # Handle multi-character operators
            if self.current_char == '=' and self.peek() == '=':
                token = self.make_token(TokenType.EQ, "==")
                self.advance()
                self.advance()
                return token
            
            if self.current_char == '!' and self.peek() == '=':
                token = self.make_token(TokenType.NE, "!=")
                self.advance()
                self.advance()
                return token
            
            if self.current_char == '<' and self.peek() == '=':
                token = self.make_token(TokenType.LE, "<=")
                self.advance()
                self.advance()
                return token
            
            if self.current_char == '>' and self.peek() == '=':
                token = self.make_token(TokenType.GE, ">=")
                self.advance()
                self.advance()
                return token
            
            # Single character tokens
            if self.current_char == '"':
                return self.read_string()
            if self.current_char == '+':
                token = self.make_token(TokenType.PLUS)
                self.advance()
                return token
            if self.current_char == '-':
                token = self.make_token(TokenType.MINUS)
                self.advance()
                return token
            if self.current_char == '*':
                token = self.make_token(TokenType.STAR)
                self.advance()
                return token
            if self.current_char == '/':
                token = self.make_token(TokenType.SLASH)
                self.advance()
                return token
            if self.current_char == '%':
                token = self.make_token(TokenType.PERCENT)
                self.advance()
                return token
            if self.current_char == '=':
                token = self.make_token(TokenType.ASSIGN)
                self.advance()
                return token
            if self.current_char == '<':
                token = self.make_token(TokenType.LT)
                self.advance()
                return token
            if self.current_char == '>':
                token = self.make_token(TokenType.GT)
                self.advance()
                return token
            if self.current_char == '(':
                token = self.make_token(TokenType.LPAREN)
                self.advance()
                return token
            if self.current_char == ')':
                token = self.make_token(TokenType.RPAREN)
                self.advance()
                return token
            if self.current_char == '{':
                token = self.make_token(TokenType.LBRACE)
                self.advance()
                return token
            if self.current_char == '}':
                token = self.make_token(TokenType.RBRACE)
                self.advance()
                return token
            if self.current_char == ';':
                token = self.make_token(TokenType.SEMICOLON)
                self.advance()
                return token
            if self.current_char == ',':
                token = self.make_token(TokenType.COMMA)
                self.advance()
                return token
            
            # Unknown character
            raise LexerError(f"Unexpected character: '{self.current_char}'", self.line, self.column)
        
        return Token(TokenType.EOF, "", self.line, self.column)