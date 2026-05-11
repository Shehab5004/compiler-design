import re
from typing import List, Optional

class Token:
    def __init__(self, type: str, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.line}:{self.column})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        self.keywords = {
            'student', 'compute', 'print_report', 'if', 'else', 'let', 'print'
        }
        
        self.token_specs = [
            ('COMMENT', r'#.*'),
            ('STRING', r'"[^"]*"'),
            ('NUMBER', r'\d+'),
            ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),
            ('OPERATOR', r'[+\-*/=]'),
            ('PUNCTUATION', r'[{}();,]'),
            ('WHITESPACE', r'\s+'),
            ('MISMATCH', r'.')
        ]
        
        self.regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specs)
    
    def tokenize(self) -> List[Token]:
        for match in re.finditer(self.regex, self.source):
            kind = match.lastgroup
            value = match.group()
            
            if kind == 'WHITESPACE':
                self._update_position(value)
                continue
            elif kind == 'COMMENT':
                self._update_position(value)
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f"Unexpected character '{value}' at {self.line}:{self.column}")
            
            # Handle string literals (remove quotes)
            if kind == 'STRING':
                value = value[1:-1]
            
            # Check if identifier is a keyword
            if kind == 'IDENTIFIER' and value in self.keywords:
                kind = 'KEYWORD'
            
            token = Token(kind, value, self.line, self.column)
            self.tokens.append(token)
            self._update_position(match.group())
        
        return self.tokens
    
    def _update_position(self, text: str):
        lines = text.split('\n')
        if len(lines) > 1:
            self.line += len(lines) - 1
            self.column = len(lines[-1]) + 1
        else:
            self.column += len(text)