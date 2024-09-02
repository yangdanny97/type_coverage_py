import ast
from typing import List, Tuple

def calculate_parameter_coverage(files: List[str]) -> Tuple[float, int]:
    total_params = 0
    annotated_params = 0
    skipped_files = 0

    # To track functions analyzed in .pyi files
    functions_covered_by_pyi = set()

    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read(), filename=file)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name

                        # If this function is already covered by a .pyi file, skip it
                        if file.endswith(".py") and func_name in functions_covered_by_pyi:
                            continue

                        # Exclude 'self' and 'cls' from parameters
                        params = [arg for arg in node.args.args if arg.arg not in ('self', 'cls')]
                        total_params += len(params)
                        annotated_params += sum(1 for arg in params if arg.annotation is not None)

                        # Mark the function as covered by .pyi if applicable
                        if file.endswith(".pyi"):
                            functions_covered_by_pyi.add(func_name)

        except (SyntaxError, UnicodeDecodeError):
            print(f"Error: Skipping file {file} (couldn't be parsed)")
            skipped_files += 1

    if total_params == 0:
        return 100.0, skipped_files

    return (annotated_params / total_params) * 100.0, skipped_files

def calculate_return_type_coverage(files: List[str]) -> Tuple[float, int]:
    total_functions = 0
    annotated_functions = 0
    skipped_files = 0

    # To track functions analyzed in .pyi files
    functions_covered_by_pyi = set()

    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read(), filename=file)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name

                        # If this function is already covered by a .pyi file, skip it
                        if file.endswith(".py") and func_name in functions_covered_by_pyi:
                            continue

                        total_functions += 1
                        if node.returns is not None:
                            annotated_functions += 1

                        # Mark the function as covered by .pyi if applicable
                        if file.endswith(".pyi"):
                            functions_covered_by_pyi.add(func_name)

        except (SyntaxError, UnicodeDecodeError):
            print(f"Error: Skipping file {file} (couldn't be parsed)")
            skipped_files += 1

    if total_functions == 0:
        return 100.0, skipped_files

    return (annotated_functions / total_functions) * 100.0, skipped_files

def calculate_overall_coverage(files: List[str]) -> dict:
    param_coverage, param_skipped = calculate_parameter_coverage(files)
    return_type_coverage, return_skipped = calculate_return_type_coverage(files)

    total_skipped = max(param_skipped, return_skipped)

    return {
        "parameter_coverage": param_coverage,
        "return_type_coverage": return_type_coverage,
        "skipped_files": total_skipped
    }
