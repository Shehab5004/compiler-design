#!/usr/bin/env python3
import sys
import os
from minilang.lexer import Lexer
from minilang.parser import Parser
from minilang.interpreter import Interpreter

def print_usage(program_name):
    print(f"Usage: {program_name} [options] <file.mlg>")
    print("Options:")
    print("  -t, --tokens    Print tokens")
    print("  -a, --ast       Print AST")
    print("  -h, --help      Show this help message")
    print("  -v, --version   Show version information")

def print_version():
    print("MiniLang Interpreter v2.0 (Python)")
    print("A sophisticated interpreted programming language")

def print_tokens(source, filename):
    lexer = Lexer(source, filename)
    print(f"=== Tokens from {filename} ===")
    try:
        while True:
            token = lexer.next_token()
            print(f"  {token}")
            if token.type.value == "EOF":
                break
    except Exception as e:
        print(f"Lexer error: {e}")
    print("=== End of tokens ===\n")

def print_ast(node, depth=0):
    indent = "  " * depth
    
    if isinstance(node, ProgramNode):
        print(f"{indent}PROGRAM")
        for stmt in node.statements:
            print_ast(stmt, depth + 1)
    
    elif isinstance(node, BlockNode):
        print(f"{indent}BLOCK")
        for stmt in node.statements:
            print_ast(stmt, depth + 1)
    
    elif isinstance(node, VarDeclNode):
        print(f"{indent}VAR_DECL({node.name})")
        print_ast(node.value, depth + 1)
    
    elif isinstance(node, AssignmentNode):
        print(f"{indent}ASSIGNMENT({node.name})")
        print_ast(node.value, depth + 1)
    
    elif isinstance(node, PrintNode):
        print(f"{indent}PRINT")
        print_ast(node.value, depth + 1)
    
    elif isinstance(node, IfNode):
        print(f"{indent}IF")
        print(f"{indent}  CONDITION:")
        print_ast(node.condition, depth + 2)
        print(f"{indent}  THEN:")
        print_ast(node.then_branch, depth + 2)
        if node.else_branch:
            print(f"{indent}  ELSE:")
            print_ast(node.else_branch, depth + 2)
    
    elif isinstance(node, WhileNode):
        print(f"{indent}WHILE")
        print(f"{indent}  CONDITION:")
        print_ast(node.condition, depth + 2)
        print(f"{indent}  BODY:")
        print_ast(node.body, depth + 2)
    
    elif isinstance(node, ForNode):
        print(f"{indent}FOR")
        if node.init:
            print(f"{indent}  INIT:")
            print_ast(node.init, depth + 2)
        if node.condition:
            print(f"{indent}  CONDITION:")
            print_ast(node.condition, depth + 2)
        if node.update:
            print(f"{indent}  UPDATE:")
            print_ast(node.update, depth + 2)
        print(f"{indent}  BODY:")
        print_ast(node.body, depth + 2)
    
    elif isinstance(node, BinOpNode):
        print(f"{indent}BINOP({node.op.value})")
        print_ast(node.left, depth + 1)
        print_ast(node.right, depth + 1)
    
    elif isinstance(node, UnaryOpNode):
        print(f"{indent}UNARYOP({node.op.value})")
        print_ast(node.operand, depth + 1)
    
    elif isinstance(node, IdentNode):
        print(f"{indent}IDENT({node.name})")
    
    elif isinstance(node, NumberNode):
        print(f"{indent}NUMBER({node.value})")
    
    elif isinstance(node, StringNode):
        print(f"{indent}STRING('{node.value}')")
    
    elif isinstance(node, BoolNode):
        print(f"{indent}BOOL({node.value})")
    
    elif isinstance(node, ExprStmtNode):
        print(f"{indent}EXPR_STMT")
        print_ast(node.expr, depth + 1)
    
    else:
        print(f"{indent}UNKNOWN({type(node).__name__})")

def run_file(filename, print_tokens_flag=False, print_ast_flag=False):
    try:
        with open(filename, 'r') as file:
            source = file.read()
    except FileNotFoundError:
        print(f"Error: Could not open file '{filename}'")
        return
    
    if print_tokens_flag:
        print_tokens(source, filename)
    
    lexer = Lexer(source, filename)
    parser = Parser(lexer)
    ast = parser.parse()
    
    if parser.errors:
        print(f"Parser completed with {len(parser.errors)} errors")
        return
    
    if print_ast_flag:
        print(f"=== AST for {filename} ===")
        print_ast(ast)
        print("=== End of AST ===\n")
    
    interpreter = Interpreter()
    interpreter.interpret(ast)
    
    if interpreter.had_error:
        print("Execution completed with errors")

def run_repl():
    print("MiniLang REPL v2.0 (Python)")
    print("Type 'exit' to quit, 'help' for help")
    print()
    
    interpreter = Interpreter()
    
    while True:
        try:
            line = input("ml> ").strip()
            
            if line in ['exit', 'quit']:
                break
            elif line == 'help':
                print("REPL commands:")
                print("  exit, quit - Exit the REPL")
                print("  help       - Show this help")
                print("  clear      - Clear the screen")
                continue
            elif line == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            elif not line:
                continue
            
            # Add semicolon if missing for single expressions
            if not line.endswith(';'):
                line += ';'
            
            lexer = Lexer(line, "repl")
            parser = Parser(lexer)
            ast = parser.parse()
            
            if not parser.errors and ast:
                result = interpreter.interpret(ast)
                # Print result if it's not null (for expressions)
                if result.type != "null":
                    print(f"=> {result}")
        
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except Exception as e:
            print(f"Error: {e}")
    
    print("Goodbye!")

def main():
    print_tokens_flag = False
    print_ast_flag = False
    filename = None
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ['-h', '--help']:
            print_usage(sys.argv[0])
            return
        elif arg in ['-v', '--version']:
            print_version()
            return
        elif arg in ['-t', '--tokens']:
            print_tokens_flag = True
        elif arg in ['-a', '--ast']:
            print_ast_flag = True
        elif not arg.startswith('-'):
            filename = arg
        else:
            print(f"Unknown option: {arg}")
            print_usage(sys.argv[0])
            return
        i += 1
    
    if filename:
        run_file(filename, print_tokens_flag, print_ast_flag)
    else:
        run_repl()

if __name__ == "__main__":
    main()