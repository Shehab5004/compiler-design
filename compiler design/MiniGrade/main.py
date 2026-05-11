import sys
import os
import pandas as pd
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from interpreter import Interpreter

def csv_to_minigrade(csv_file):
    """Convert CSV file to MiniGrade language code"""
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        print(f"📊 Loaded CSV with {len(df)} records")
        print(f"📝 Students: {df['student_name'].nunique()}")
        print(f"📚 Subjects: {df['subject'].nunique()}")
        
        # Check required columns
        if 'student_name' not in df.columns:
            raise ValueError("CSV must have 'student_name' column")
        if 'subject' not in df.columns:
            raise ValueError("CSV must have 'subject' column")
        if 'marks' not in df.columns:
            raise ValueError("CSV must have 'marks' column")
        
        # Use credits if available, otherwise default to 1
        has_credits = 'credits' in df.columns
        if has_credits:
            print("✅ Credits column found")
        else:
            print("ℹ️  No credits column - using default credit=1")
        
        minigrade_code = ["# Auto-generated from CSV file"]
        
        # Group by student
        for student_name, group in df.groupby('student_name'):
            minigrade_code.append(f'student {{')
            minigrade_code.append(f'    "{student_name}"')
            
            for _, row in group.iterrows():
                # Convert subject names with spaces to use underscores
                subject = row["subject"].replace(" ", "_")
                if has_credits:
                    minigrade_code.append(f'    {subject} = {row["marks"]} credit = {row["credits"]}')
                else:
                    minigrade_code.append(f'    {subject} = {row["marks"]}')
            
            minigrade_code.append(f'}}')
            minigrade_code.append('')
        
        # Add compute statements for all students
        student_names = df['student_name'].unique()
        for name in student_names:
            minigrade_code.append(f'compute "{name}";')
        
        minigrade_code.append('')
        minigrade_code.append('print_report();')
        
        return '\n'.join(minigrade_code)
        
    except Exception as e:
        raise RuntimeError(f"Error reading CSV file: {e}")

def run_minigrade(source_code):
    """Run MiniGrade interpreter"""
    try:
        # Lexical Analysis
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        print("✅ Tokenization completed")
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        print("✅ AST built successfully")
        
        # Semantic Analysis
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        if analyzer.errors:
            print("❌ Semantic errors:")
            for error in analyzer.errors:
                print(f"   {error}")
            return
        
        print("✅ Semantic analysis passed")
        
        # Interpretation
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    if len(sys.argv) != 2:
        print("🎓 MiniGrade - UGC Grading System")
        print("=" * 50)
        print("Usage: python main.py <students.csv>")
        print("\nCSV Format Required Columns:")
        print("  • student_name - Student's name")
        print("  • subject - Course name")
        print("  • marks - Marks (percentage)")
        print("  • credits - Optional: Credit hours")
        print("\nExample CSV:")
        print("student_name,subject,marks,credits")
        print('"Alice","math",85,3')
        print('"Alice","physics",78,4')
        print('"Bob","math",65,3')
        print(f"\nCurrent directory: {os.getcwd()}")
        
        # Show available CSV files
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        if csv_files:
            print(f"\nAvailable CSV files: {', '.join(csv_files)}")
        else:
            print("\nNo CSV files found in current directory")
        return
    
    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        print(f"Current directory: {os.getcwd()}")
        
        # Show available files
        files = os.listdir('.')
        csv_files = [f for f in files if f.endswith('.csv')]
        if csv_files:
            print(f"Available CSV files: {', '.join(csv_files)}")
        return
    
    if not csv_file.lower().endswith('.csv'):
        print("❌ Please provide a .csv file")
        return
    
    try:
        print(f"📁 Loading: {csv_file}")
        source_code = csv_to_minigrade(csv_file)
        
        print("\n🚀 Processing...")
        run_minigrade(source_code)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()