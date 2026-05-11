from enum import Enum
from typing import List, Optional

class NodeType(Enum):
    PROGRAM = "PROGRAM"
    VAR_DECL = "VAR_DECL"
    ASSIGNMENT = "ASSIGNMENT"
    PRINT = "PRINT"
    IF = "IF"
    WHILE = "WHILE"
    FOR = "FOR"
    BLOCK = "BLOCK"
    BINOP = "BINOP"
    UNARYOP = "UNARYOP"
    IDENT = "IDENT"
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOL = "BOOL"
    EXPR_STMT = "EXPR_STMT"

class BinOpType(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    EQ = "=="
    NE = "!="
    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="
    AND = "and"
    OR = "or"

class UnaryOpType(Enum):
    NEG = "-"
    NOT = "not"

class ASTNode:
    def __init__(self, type: NodeType, line: int = 1, column: int = 1):
        self.type = type
        self.line = line
        self.column = column

class ProgramNode(ASTNode):
    def __init__(self, statements: List[ASTNode] = None):
        super().__init__(NodeType.PROGRAM)
        self.statements = statements or []

class VarDeclNode(ASTNode):
    def __init__(self, name: str, value: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.VAR_DECL, line, column)
        self.name = name
        self.value = value

class AssignmentNode(ASTNode):
    def __init__(self, name: str, value: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.ASSIGNMENT, line, column)
        self.name = name
        self.value = value

class PrintNode(ASTNode):
    def __init__(self, value: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.PRINT, line, column)
        self.value = value

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: ASTNode, else_branch: ASTNode = None, line: int = 1, column: int = 1):
        super().__init__(NodeType.IF, line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.WHILE, line, column)
        self.condition = condition
        self.body = body

class ForNode(ASTNode):
    def __init__(self, init: ASTNode, condition: ASTNode, update: ASTNode, body: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.FOR, line, column)
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class BlockNode(ASTNode):
    def __init__(self, statements: List[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(NodeType.BLOCK, line, column)
        self.statements = statements or []

class BinOpNode(ASTNode):
    def __init__(self, op: BinOpType, left: ASTNode, right: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.BINOP, line, column)
        self.op = op
        self.left = left
        self.right = right

class UnaryOpNode(ASTNode):
    def __init__(self, op: UnaryOpType, operand: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.UNARYOP, line, column)
        self.op = op
        self.operand = operand

class IdentNode(ASTNode):
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__(NodeType.IDENT, line, column)
        self.name = name

class NumberNode(ASTNode):
    def __init__(self, value: int, line: int = 1, column: int = 1):
        super().__init__(NodeType.NUMBER, line, column)
        self.value = value

class StringNode(ASTNode):
    def __init__(self, value: str, line: int = 1, column: int = 1):
        super().__init__(NodeType.STRING, line, column)
        self.value = value

class BoolNode(ASTNode):
    def __init__(self, value: bool, line: int = 1, column: int = 1):
        super().__init__(NodeType.BOOL, line, column)
        self.value = value

class ExprStmtNode(ASTNode):
    def __init__(self, expr: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.EXPR_STMT, line, column)
        self.expr = expr