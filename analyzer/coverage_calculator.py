from typing import List, Dict
import ast

def calculate_parameter_coverage(files: List[str]) -> (float, int):
    total_params = 0
    annotated_params = 0
    skipped_files = 0

    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read(), filename=file)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        total_params += len(node.args.args)
                        annotated_params += sum(1 for arg in node.args.args if arg.annotation is not None)
        except (SyntaxError, UnicodeDecodeError):
            print(f"Error: Skipping file {file} (couldn't be parsed)")
            skipped_files += 1

    if total_params == 0:
        return 100.0, skipped_files

    return (annotated_params / total_params) * 100.0, skipped_files

def calculate_return_type_coverage(files: List[str]) -> (float, int):
    total_functions = 0
    annotated_functions = 0
    skipped_files = 0

    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read(), filename=file)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        total_functions += 1
                        if node.returns is not None:
                            annotated_functions += 1
        except (SyntaxError, UnicodeDecodeError):
            print(f"Error: Skipping file {file} (couldn't be parsed)")
            skipped_files += 1

    if total_functions == 0:
        return 100.0, skipped_files

    return (annotated_functions / total_functions) * 100.0, skipped_files

def calculate_overall_coverage(files: List[str]) -> Dict[str, float]:
    param_coverage, param_skipped = calculate_parameter_coverage(files)
    return_type_coverage, return_skipped = calculate_return_type_coverage(files)

    # Ensure we do not double count skipped files
    total_skipped = max(param_skipped, return_skipped)

    return {
        "parameter_coverage": param_coverage,
        "return_type_coverage": return_type_coverage,
        "skipped_files": total_skipped
    }
