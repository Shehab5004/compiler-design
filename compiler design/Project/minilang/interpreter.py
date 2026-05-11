from ast import *
from errors import RuntimeError

class Value:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
    
    def __str__(self):
        if self.value is None:
            return "null"
        return str(self.value)
    
    def is_truthy(self):
        if self.type == "number":
            return self.value != 0
        elif self.type == "string":
            return bool(self.value)
        elif self.type == "bool":
            return self.value
        elif self.type == "null":
            return False
        return False

class SymbolTable:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent
    
    def define(self, name, value):
        if name in self.variables:
            return False
        self.variables[name] = value
        return True
    
    def assign(self, name, value):
        if name in self.variables:
            self.variables[name] = value
            return True
        if self.parent:
            return self.parent.assign(name, value)
        return False
    
    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        return None

class Interpreter:
    def __init__(self):
        self.global_table = SymbolTable()
        self.current_table = self.global_table
        self.had_error = False
    
    def error(self, message, line, column):
        self.had_error = True
        raise RuntimeError(message, line, column)
    
    def interpret(self, node):
        try:
            if isinstance(node, ProgramNode):
                return self.interpret_program(node)
            elif isinstance(node, BlockNode):
                return self.interpret_block(node)
            elif isinstance(node, VarDeclNode):
                return self.interpret_var_decl(node)
            elif isinstance(node, AssignmentNode):
                return self.interpret_assignment(node)
            elif isinstance(node, PrintNode):
                return self.interpret_print(node)
            elif isinstance(node, IfNode):
                return self.interpret_if(node)
            elif isinstance(node, WhileNode):
                return self.interpret_while(node)
            elif isinstance(node, ForNode):
                return self.interpret_for(node)
            elif isinstance(node, BinOpNode):
                return self.interpret_binop(node)
            elif isinstance(node, UnaryOpNode):
                return self.interpret_unaryop(node)
            elif isinstance(node, IdentNode):
                return self.interpret_ident(node)
            elif isinstance(node, NumberNode):
                return Value("number", node.value)
            elif isinstance(node, StringNode):
                return Value("string", node.value)
            elif isinstance(node, BoolNode):
                return Value("bool", node.value)
            elif isinstance(node, ExprStmtNode):
                return self.interpret(node.expr)
            else:
                self.error(f"Unknown node type: {type(node)}", getattr(node, 'line', 1), getattr(node, 'column', 1))
        except RuntimeError as e:
            print(e)
            return Value("null")
    
    def interpret_program(self, node):
        result = Value("null")
        for stmt in node.statements:
            result = self.interpret(stmt)
            if self.had_error:
                break
        return result
    
    def interpret_block(self, node):
        # Create new scope
        previous_table = self.current_table
        self.current_table = SymbolTable(previous_table)
        
        result = Value("null")
        for stmt in node.statements:
            result = self.interpret(stmt)
            if self.had_error:
                break
        
        # Restore previous scope
        self.current_table = previous_table
        return result
    
    def interpret_var_decl(self, node):
        value = self.interpret(node.value)
        if self.had_error:
            return value
        
        if not self.current_table.define(node.name, value):
            self.error(f"Variable '{node.name}' already defined", node.line, node.column)
        
        return value
    
    def interpret_assignment(self, node):
        value = self.interpret(node.value)
        if self.had_error:
            return value
        
        if not self.current_table.assign(node.name, value):
            # If assignment fails, define the variable (like Python)
            if not self.current_table.define(node.name, value):
                self.error(f"Undefined variable '{node.name}'", node.line, node.column)
        
        return value
    
    def interpret_print(self, node):
        value = self.interpret(node.value)
        if self.had_error:
            return Value("null")
        
        print(value)
        return Value("null")
    
    def interpret_if(self, node):
        condition = self.interpret(node.condition)
        if self.had_error:
            return Value("null")
        
        if condition.is_truthy():
            return self.interpret(node.then_branch)
        elif node.else_branch:
            return self.interpret(node.else_branch)
        
        return Value("null")
    
    def interpret_while(self, node):
        result = Value("null")
        
        while True:
            condition = self.interpret(node.condition)
            if self.had_error:
                break
            
            if not condition.is_truthy():
                break
            
            result = self.interpret(node.body)
            if self.had_error:
                break
        
        return result
    
    def interpret_for(self, node):
        # Create new scope for the for loop
        previous_table = self.current_table
        self.current_table = SymbolTable(previous_table)
        
        result = Value("null")
        
        # Execute initialization
        if node.init:
            self.interpret(node.init)
            if self.had_error:
                self.current_table = previous_table
                return Value("null")
        
        # Loop
        while True:
            # Check condition
            if node.condition:
                condition = self.interpret(node.condition)
                if self.had_error:
                    break
                if not condition.is_truthy():
                    break
            
            # Execute body
            result = self.interpret(node.body)
            if self.had_error:
                break
            
            # Execute update
            if node.update:
                self.interpret(node.update)
                if self.had_error:
                    break
        
        # Restore previous scope
        self.current_table = previous_table
        return result
    
    def interpret_binop(self, node):
        left = self.interpret(node.left)
        if self.had_error:
            return Value("null")
        
        right = self.interpret(node.right)
        if self.had_error:
            return Value("null")
        
        # Number operations
        if left.type == "number" and right.type == "number":
            if node.op == BinOpType.ADD:
                return Value("number", left.value + right.value)
            elif node.op == BinOpType.SUB:
                return Value("number", left.value - right.value)
            elif node.op == BinOpType.MUL:
                return Value("number", left.value * right.value)
            elif node.op == BinOpType.DIV:
                if right.value == 0:
                    self.error("Division by zero", node.line, node.column)
                    return Value("null")
                return Value("number", left.value // right.value)
            elif node.op == BinOpType.MOD:
                if right.value == 0:
                    self.error("Modulo by zero", node.line, node.column)
                    return Value("null")
                return Value("number", left.value % right.value)
            elif node.op == BinOpType.EQ:
                return Value("bool", left.value == right.value)
            elif node.op == BinOpType.NE:
                return Value("bool", left.value != right.value)
            elif node.op == BinOpType.LT:
                return Value("bool", left.value < right.value)
            elif node.op == BinOpType.GT:
                return Value("bool", left.value > right.value)
            elif node.op == BinOpType.LE:
                return Value("bool", left.value <= right.value)
            elif node.op == BinOpType.GE:
                return Value("bool", left.value >= right.value)
        
        # Boolean operations
        if node.op == BinOpType.AND:
            return Value("bool", left.is_truthy() and right.is_truthy())
        elif node.op == BinOpType.OR:
            return Value("bool", left.is_truthy() or right.is_truthy())
        
        # String concatenation
        if node.op == BinOpType.ADD and left.type == "string" and right.type == "string":
            return Value("string", left.value + right.value)
        
        self.error(f"Invalid operation {node.op.value} for types {left.type} and {right.type}", node.line, node.column)
        return Value("null")
    
    def interpret_unaryop(self, node):
        operand = self.interpret(node.operand)
        if self.had_error:
            return Value("null")
        
        if node.op == UnaryOpType.NEG:
            if operand.type == "number":
                return Value("number", -operand.value)
        elif node.op == UnaryOpType.NOT:
            return Value("bool", not operand.is_truthy())
        
        self.error(f"Invalid unary operation {node.op.value} for type {operand.type}", node.line, node.column)
        return Value("null")
    
    def interpret_ident(self, node):
        value = self.current_table.get(node.name)
        if value is None:
            self.error(f"Undefined variable '{node.name}'", node.line, node.column)
            return Value("null")
        return value