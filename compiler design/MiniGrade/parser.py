from typing import List, Optional
from ast_nodes import *

# Import Token class
try:
    from lexer import Token
except ImportError:
    # Define Token here if import fails
    class Token:
        def __init__(self, type: str, value: str, line: int, column: int):
            self.type = type
            self.value = value
            self.line = line
            self.column = column
        
        def __repr__(self):
            return f"Token({self.type}, '{self.value}', {self.line}:{self.column})"

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def current_token(self) -> Optional[Token]:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    
    def peek(self, offset=1) -> Optional[Token]:
        if self.position + offset < len(self.tokens):
            return self.tokens[self.position + offset]
        return None
    
    def consume(self, expected_type: str = None, expected_value: str = None) -> Token:
        token = self.current_token()
        if not token:
            raise RuntimeError("Unexpected end of input")
        
        if expected_type and token.type != expected_type:
            raise RuntimeError(f"Expected {expected_type}, got {token.type} at {token.line}:{token.column}")
        
        if expected_value and token.value != expected_value:
            raise RuntimeError(f"Expected '{expected_value}', got '{token.value}' at {token.line}:{token.column}")
        
        self.position += 1
        return token
    
    def parse(self) -> Program:
        statements = []
        while self.current_token():
            if self.current_token().type == 'KEYWORD' and self.current_token().value == 'student':
                statements.append(self.parse_student_declaration())
            elif self.current_token().type == 'KEYWORD' and self.current_token().value == 'compute':
                statements.append(self.parse_compute_statement())
            elif self.current_token().type == 'KEYWORD' and self.current_token().value == 'print_report':
                statements.append(self.parse_print_report_statement())
            elif self.current_token().type == 'KEYWORD' and self.current_token().value == 'let':
                statements.append(self.parse_variable_declaration())
            elif self.current_token().type == 'KEYWORD' and self.current_token().value == 'print':
                statements.append(self.parse_print_statement())
            else:
                raise RuntimeError(f"Unexpected token {self.current_token()} at {self.current_token().line}:{self.current_token().column}")
        
        return Program(statements)
    
    def parse_student_declaration(self) -> StudentDeclaration:
        self.consume('KEYWORD', 'student')
        self.consume('PUNCTUATION', '{')
        
        name_token = self.consume('STRING')
        name = name_token.value
        
        marks = {}
        credits = {}
        
        while self.current_token() and self.current_token().type != 'PUNCTUATION':
            # Handle subject names - can be IDENTIFIER (with underscores)
            subject = self.consume('IDENTIFIER').value
        
            self.consume('OPERATOR', '=')
            mark = int(self.consume('NUMBER').value)
            marks[subject] = mark
            
            # Check if credit is specified
            if self.current_token() and self.current_token().value == 'credit':
                self.consume('IDENTIFIER', 'credit')
                self.consume('OPERATOR', '=')
                credit = int(self.consume('NUMBER').value)
                credits[subject] = credit
    
        self.consume('PUNCTUATION', '}')
        
        return StudentDeclaration(name, marks, credits)
    
    def parse_compute_statement(self) -> ComputeStatement:
        self.consume('KEYWORD', 'compute')
        student_name = self.consume('STRING').value
        self.consume('PUNCTUATION', ';')
        return ComputeStatement(student_name)
    
    def parse_print_report_statement(self) -> PrintReportStatement:
        self.consume('KEYWORD', 'print_report')
        self.consume('PUNCTUATION', '(')
        self.consume('PUNCTUATION', ')')
        self.consume('PUNCTUATION', ';')
        return PrintReportStatement()
    
    def parse_variable_declaration(self) -> VariableDeclaration:
        self.consume('KEYWORD', 'let')
        name = self.consume('IDENTIFIER').value
        self.consume('OPERATOR', '=')
        value = self.parse_expression()
        self.consume('PUNCTUATION', ';')
        return VariableDeclaration(name, value)
    
    def parse_print_statement(self) -> PrintStatement:
        self.consume('KEYWORD', 'print')
        expr = self.parse_expression()
        self.consume('PUNCTUATION', ';')
        return PrintStatement(expr)
    
    def parse_expression(self):
        return self.parse_additive()
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.current_token() and self.current_token().type == 'OPERATOR' and self.current_token().value in ['+', '-']:
            op = self.consume().value
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self):
        left = self.parse_primary()
        
        while self.current_token() and self.current_token().type == 'OPERATOR' and self.current_token().value in ['*', '/']:
            op = self.consume().value
            right = self.parse_primary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_primary(self):
        token = self.current_token()
        if not token:
            raise RuntimeError("Unexpected end of input")
        
        if token.type == 'NUMBER':
            self.consume()
            return NumberLiteral(int(token.value))
        elif token.type == 'STRING':
            self.consume()
            return StringLiteral(token.value)
        elif token.type == 'IDENTIFIER':
            self.consume()
            return Identifier(token.value)
        elif token.type == 'PUNCTUATION' and token.value == '(':
            self.consume('PUNCTUATION', '(')
            expr = self.parse_expression()
            self.consume('PUNCTUATION', ')')
            return expr
        else:
            raise RuntimeError(f"Unexpected token {token} at {token.line}:{token.column}")