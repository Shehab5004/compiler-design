from typing import List, Dict, Any, Optional

class ASTNode:
    def accept(self, visitor):
        pass

class Program(ASTNode):
    def __init__(self, statements: List['ASTNode']):
        self.statements = statements
    
    def accept(self, visitor):
        return visitor.visit_program(self)

class StudentDeclaration(ASTNode):
    def __init__(self, name: str, marks: Dict[str, int], credits: Dict[str, int] = None):
        self.name = name
        self.marks = marks
        self.credits = credits or {}
    
    def accept(self, visitor):
        return visitor.visit_student_declaration(self)

class ComputeStatement(ASTNode):
    def __init__(self, student_name: str):
        self.student_name = student_name
    
    def accept(self, visitor):
        return visitor.visit_compute_statement(self)

class PrintReportStatement(ASTNode):
    def accept(self, visitor):
        return visitor.visit_print_report_statement(self)

class VariableDeclaration(ASTNode):
    def __init__(self, name: str, value):
        self.name = name
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)

class PrintStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_print_statement(self)

class BinaryOp(ASTNode):
    def __init__(self, left, operator: str, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)

class Identifier(ASTNode):
    def __init__(self, name: str):
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)

class NumberLiteral(ASTNode):
    def __init__(self, value: int):
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_number_literal(self)

class StringLiteral(ASTNode):
    def __init__(self, value: str):
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_string_literal(self)