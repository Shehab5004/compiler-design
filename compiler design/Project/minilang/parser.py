from lexer import Lexer, TokenType
from ast import *
from errors import ParserError

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()
        self.errors = []
    
    def error(self, message):
        self.errors.append(ParserError(message, self.current_token.line, self.current_token.column))
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
        else:
            self.error(f"Expected {token_type.value}, got {self.current_token.type.value}")
    
    def parse(self):
        program = self.parse_program()
        if self.errors:
            for error in self.errors:
                print(error)
        return program
    
    def parse_program(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements)
    
    def parse_statement(self):
        if self.current_token.type == TokenType.LET:
            return self.parse_var_decl()
        elif self.current_token.type == TokenType.PRINT:
            return self.parse_print()
        elif self.current_token.type == TokenType.IF:
            return self.parse_if()
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while()
        elif self.current_token.type == TokenType.FOR:
            return self.parse_for()
        elif self.current_token.type == TokenType.LBRACE:
            return self.parse_block()
        elif self.current_token.type == TokenType.IDENT:
            # Could be assignment or expression
            ident_token = self.current_token
            self.eat(TokenType.IDENT)
            
            if self.current_token.type == TokenType.ASSIGN:
                return self.parse_assignment(ident_token)
            else:
                # Just an identifier expression
                ident_node = IdentNode(ident_token.lexeme, ident_token.line, ident_token.column)
                if self.current_token.type == TokenType.SEMICOLON:
                    self.eat(TokenType.SEMICOLON)
                return ExprStmtNode(ident_node, ident_token.line, ident_token.column)
        else:
            # Try to parse as expression statement
            expr = self.parse_expression()
            if expr:
                if self.current_token.type == TokenType.SEMICOLON:
                    self.eat(TokenType.SEMICOLON)
                return ExprStmtNode(expr, expr.line, expr.column)
        
        self.error("Expected statement")
        return None
    
    def parse_var_decl(self):
        let_token = self.current_token
        self.eat(TokenType.LET)
        
        ident_token = self.current_token
        self.eat(TokenType.IDENT)
        
        self.eat(TokenType.ASSIGN)
        
        value = self.parse_expression()
        if not value:
            self.error("Expected expression after '='")
            return None
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return VarDeclNode(ident_token.lexeme, value, let_token.line, let_token.column)
    
    def parse_assignment(self, ident_token):
        assign_token = self.current_token
        self.eat(TokenType.ASSIGN)
        
        value = self.parse_expression()
        if not value:
            self.error("Expected expression after '='")
            return None
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return AssignmentNode(ident_token.lexeme, value, assign_token.line, assign_token.column)
    
    def parse_print(self):
        print_token = self.current_token
        self.eat(TokenType.PRINT)
        
        self.eat(TokenType.LPAREN)
        
        value = self.parse_expression()
        if not value:
            self.error("Expected expression in print statement")
            return None
        
        self.eat(TokenType.RPAREN)
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return PrintNode(value, print_token.line, print_token.column)
    
    def parse_if(self):
        if_token = self.current_token
        self.eat(TokenType.IF)
        
        self.eat(TokenType.LPAREN)
        
        condition = self.parse_expression()
        if not condition:
            self.error("Expected condition in if statement")
            return None
        
        self.eat(TokenType.RPAREN)
        
        then_branch = self.parse_statement()
        if not then_branch:
            self.error("Expected statement after if condition")
            return None
        
        else_branch = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            else_branch = self.parse_statement()
            if not else_branch:
                self.error("Expected statement after else")
        
        return IfNode(condition, then_branch, else_branch, if_token.line, if_token.column)
    
    def parse_while(self):
        while_token = self.current_token
        self.eat(TokenType.WHILE)
        
        self.eat(TokenType.LPAREN)
        
        condition = self.parse_expression()
        if not condition:
            self.error("Expected condition in while statement")
            return None
        
        self.eat(TokenType.RPAREN)
        
        body = self.parse_statement()
        if not body:
            self.error("Expected statement after while condition")
            return None
        
        return WhileNode(condition, body, while_token.line, while_token.column)
    
    def parse_for(self):
        for_token = self.current_token
        self.eat(TokenType.FOR)
        
        self.eat(TokenType.LPAREN)
        
        # Parse initialization (optional)
        init = None
        if self.current_token.type != TokenType.SEMICOLON:
            if self.current_token.type == TokenType.LET:
                init = self.parse_var_decl()
            else:
                init = self.parse_expression()
                if init and self.current_token.type == TokenType.SEMICOLON:
                    self.eat(TokenType.SEMICOLON)
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        # Parse condition (optional)
        condition = None
        if self.current_token.type != TokenType.SEMICOLON:
            condition = self.parse_expression()
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        # Parse update (optional)
        update = None
        if self.current_token.type != TokenType.RPAREN:
            update = self.parse_expression()
        
        self.eat(TokenType.RPAREN)
        
        body = self.parse_statement()
        if not body:
            self.error("Expected statement after for loop")
            return None
        
        return ForNode(init, condition, update, body, for_token.line, for_token.column)
    
    def parse_block(self):
        brace_token = self.current_token
        self.eat(TokenType.LBRACE)
        
        statements = []
        while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        self.eat(TokenType.RBRACE)
        return BlockNode(statements, brace_token.line, brace_token.column)
    
    def parse_expression(self):
        return self.parse_comparison()
    
    def parse_comparison(self):
        left = self.parse_term()
        
        while self.current_token.type in [TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.GT, 
                                         TokenType.LE, TokenType.GE, TokenType.AND, TokenType.OR]:
            op_token = self.current_token
            
            if op_token.type == TokenType.EQ:
                op = BinOpType.EQ
            elif op_token.type == TokenType.NE:
                op = BinOpType.NE
            elif op_token.type == TokenType.LT:
                op = BinOpType.LT
            elif op_token.type == TokenType.GT:
                op = BinOpType.GT
            elif op_token.type == TokenType.LE:
                op = BinOpType.LE
            elif op_token.type == TokenType.GE:
                op = BinOpType.GE
            elif op_token.type == TokenType.AND:
                op = BinOpType.AND
            elif op_token.type == TokenType.OR:
                op = BinOpType.OR
            else:
                break
            
            self.eat(op_token.type)
            right = self.parse_term()
            left = BinOpNode(op, left, right, op_token.line, op_token.column)
        
        return left
    
    def parse_term(self):
        left = self.parse_factor()
        
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op_token = self.current_token
            op = BinOpType.ADD if op_token.type == TokenType.PLUS else BinOpType.SUB
            self.eat(op_token.type)
            right = self.parse_factor()
            left = BinOpNode(op, left, right, op_token.line, op_token.column)
        
        return left
    
    def parse_factor(self):
        left = self.parse_primary()
        
        while self.current_token.type in [TokenType.STAR, TokenType.SLASH, TokenType.PERCENT]:
            op_token = self.current_token
            
            if op_token.type == TokenType.STAR:
                op = BinOpType.MUL
            elif op_token.type == TokenType.SLASH:
                op = BinOpType.DIV
            elif op_token.type == TokenType.PERCENT:
                op = BinOpType.MOD
            else:
                break
            
            self.eat(op_token.type)
            right = self.parse_primary()
            left = BinOpNode(op, left, right, op_token.line, op_token.column)
        
        return left
    
    def parse_primary(self):
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberNode(token.value, token.line, token.column)
        
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return StringNode(token.value, token.line, token.column)
        
        elif token.type == TokenType.IDENT:
            self.eat(TokenType.IDENT)
            return IdentNode(token.lexeme, token.line, token.column)
        
        elif token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return BoolNode(True, token.line, token.column)
        
        elif token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return BoolNode(False, token.line, token.column)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
        
        elif token.type in [TokenType.MINUS, TokenType.NOT]:
            self.eat(token.type)
            op = UnaryOpType.NEG if token.type == TokenType.MINUS else UnaryOpType.NOT
            operand = self.parse_primary()
            return UnaryOpNode(op, operand, token.line, token.column)
        
        self.error("Expected primary expression")
        return None