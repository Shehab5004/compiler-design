from ast_nodes import *
from typing import Dict, Set

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = set()
        self.students = set()
        self.errors = []
    
    def analyze(self, node: ASTNode):
        node.accept(self)
    
    def visit_program(self, node: Program):
        for stmt in node.statements:
            stmt.accept(self)
    
    def visit_student_declaration(self, node: StudentDeclaration):
        if node.name in self.students:
            self.errors.append(f"Duplicate student declaration: {node.name}")
        self.students.add(node.name)
    
    def visit_compute_statement(self, node: ComputeStatement):
        if node.student_name not in self.students:
            self.errors.append(f"Unknown student: {node.student_name}")
    
    def visit_print_report_statement(self, node: PrintReportStatement):
        pass
    
    def visit_variable_declaration(self, node: VariableDeclaration):
        if node.name in self.symbols:
            self.errors.append(f"Duplicate variable declaration: {node.name}")
        self.symbols.add(node.name)
        node.value.accept(self)
    
    def visit_print_statement(self, node: PrintStatement):
        node.expression.accept(self)
    
    def visit_binary_op(self, node: BinaryOp):
        node.left.accept(self)
        node.right.accept(self)
    
    def visit_identifier(self, node: Identifier):
        if node.name not in self.symbols and node.name not in self.students:
            self.errors.append(f"Undefined identifier: {node.name}")
    
    def visit_number_literal(self, node: NumberLiteral):
        pass
    
    def visit_string_literal(self, node: StringLiteral):
        pass