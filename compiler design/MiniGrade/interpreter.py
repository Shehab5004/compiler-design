from ast_nodes import *
from typing import Dict, List, Any

class StudentResult:
    def __init__(self, name: str, marks: Dict[str, int], credits: Dict[str, int]):
        self.name = name
        self.marks = marks
        self.credits = credits
        self.total_marks = 0
        self.grade_points = {}
        self.letter_grades = {}
        self.sgpa = 0.0
        self.credit_total = 0
        self.weighted_gp_total = 0.0
    
    def get_grade_point(self, percentage: float) -> tuple:
        """UGC Grading Scale"""
        if percentage >= 80:
            return ("A+", 4.00)
        elif percentage >= 75:
            return ("A", 3.75)
        elif percentage >= 70:
            return ("A-", 3.50)
        elif percentage >= 65:
            return ("B+", 3.25)
        elif percentage >= 60:
            return ("B", 3.00)
        elif percentage >= 55:
            return ("B-", 2.75)
        elif percentage >= 50:
            return ("C+", 2.50)
        elif percentage >= 45:
            return ("C", 2.25)
        elif percentage >= 40:
            return ("D", 2.00)
        else:
            return ("F", 0.00)
    
    def compute(self):
        self.credit_total = sum(self.credits.values())
        self.weighted_gp_total = 0.0
        
        # Calculate grade points for each course
        for subject, mark in self.marks.items():
            credit = self.credits.get(subject, 1)
            percentage = mark  # Assuming marks are already in percentage
            
            letter_grade, gp = self.get_grade_point(percentage)
            self.letter_grades[subject] = letter_grade
            self.grade_points[subject] = gp
            
            # Calculate weighted grade points
            weighted_gp = credit * gp
            self.weighted_gp_total += weighted_gp
        
        # Calculate SGPA using UGC formula
        if self.credit_total > 0:
            self.sgpa = self.weighted_gp_total / self.credit_total
        else:
            self.sgpa = 0.0
        
        # Calculate total marks
        self.total_marks = sum(self.marks.values())
    
    def __str__(self):
        result = [
            f"Student: {self.name}",
            f"SGPA: {self.sgpa:.2f}",
            f"Total Credits: {self.credit_total}",
            "",
            "Course Details:"
        ]
        
        # Course-wise breakdown in the exact format requested
        for subject in self.marks.keys():
            credit = self.credits.get(subject, 1)
            letter_grade = self.letter_grades[subject]
            gp = self.grade_points[subject]
            
            # Exact format: "  Subject: Credit: X | Grade: Y | GP: Z"
            result.append(f"  {subject}: Credit: {credit} | Grade: {letter_grade} | GP: {gp:.2f}")
        
        return "\n".join(result)

class ClassSummary:
    def __init__(self):
        self.student_results = []
        self.class_sgpa = 0.0
        self.highest_sgpa = 0.0
        self.lowest_sgpa = 0.0
        self.cgpa = 0.0
    
    def add_student_result(self, result: StudentResult):
        self.student_results.append(result)
    
    def compute_class_summary(self):
        if not self.student_results:
            return
        
        sgpas = [result.sgpa for result in self.student_results]
        self.highest_sgpa = max(sgpas)
        self.lowest_sgpa = min(sgpas)
        self.class_sgpa = sum(sgpas) / len(sgpas)
        
        # Calculate overall CGPA (weighted by credits)
        total_credits = sum(result.credit_total for result in self.student_results)
        total_weighted_gp = sum(result.weighted_gp_total for result in self.student_results)
        
        if total_credits > 0:
            self.cgpa = total_weighted_gp / total_credits
        else:
            self.cgpa = 0.0

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.students = {}
        self.results = {}
        self.class_summary = ClassSummary()
    
    def interpret(self, node: ASTNode):
        return node.accept(self)
    
    def visit_program(self, node: Program):
        for stmt in node.statements:
            stmt.accept(self)
    
    def visit_student_declaration(self, node: StudentDeclaration):
        self.students[node.name] = StudentResult(node.name, node.marks, node.credits)
    
    def visit_compute_statement(self, node: ComputeStatement):
        if node.student_name in self.students:
            student = self.students[node.student_name]
            student.compute()
            self.results[node.student_name] = student
            self.class_summary.add_student_result(student)
            print(f"✓ Computed SGPA for {node.student_name}: {student.sgpa:.2f}")
        else:
            raise RuntimeError(f"Student {node.student_name} not found")
    
    def visit_print_report_statement(self, node: PrintReportStatement):
        if not self.results:
            print("No student results to display")
            return
        
        self.class_summary.compute_class_summary()
        
        print("\n" + "="*70)
        print("UGC GRADING SYSTEM - SEMESTER REPORT")
        print("="*70)
        
        # Display UGC grading scale
        print("\n📊 UGC Grading Scale:")
        print("Marks (%) | Grade | Grade Point")
        print("80–100    | A+    | 4.00")
        print("75–79     | A     | 3.75")
        print("70–74     | A-    | 3.50")
        print("65–69     | B+    | 3.25")
        print("60–64     | B     | 3.00")
        print("55–59     | B-    | 2.75")
        print("50–54     | C+    | 2.50")
        print("45–49     | C     | 2.25")
        print("40–44     | D     | 2.00")
        print("< 40      | F     | 0.00")
        
        # Individual student reports
        print("\n" + "="*70)
        print("INDIVIDUAL STUDENT REPORTS")
        print("="*70)
        
        for name, result in self.results.items():
            print(f"\n{result}")
            print("\n")
            print("-" * 50)
            
    
        # Class summary
        print("\n" + "="*70)
        print("CLASS SUMMARY")
        print("="*70)
        print(f"Class SGPA Average: {self.class_summary.class_sgpa:.2f}")
        print(f"Class CGPA: {self.class_summary.cgpa:.2f}")
        print(f"Highest SGPA: {self.class_summary.highest_sgpa:.2f}")
        print(f"Lowest SGPA: {self.class_summary.lowest_sgpa:.2f}")
        print(f"Total Students: {len(self.results)}")
    
    def visit_variable_declaration(self, node: VariableDeclaration):
        value = node.value.accept(self)
        self.variables[node.name] = value
    
    def visit_print_statement(self, node: PrintStatement):
        value = node.expression.accept(self)
        print(value)
    
    def visit_binary_op(self, node: BinaryOp):
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            return left / right if right != 0 else 0
        else:
            raise RuntimeError(f"Unknown operator: {node.operator}")
    
    def visit_identifier(self, node: Identifier):
        if node.name in self.variables:
            return self.variables[node.name]
        elif node.name in self.results:
            return self.results[node.name]
        else:
            raise RuntimeError(f"Undefined variable: {node.name}")
    
    def visit_number_literal(self, node: NumberLiteral):
        return node.value
    
    def visit_string_literal(self, node: StringLiteral):
        return node.value