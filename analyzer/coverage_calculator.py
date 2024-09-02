import ast
from typing import List, Tuple

def calculate_parameter_coverage(files: List[str]) -> Tuple[float, int]:
    total_params = 0
    annotated_params = 0
    skipped_files = 0

    # To track annotations and parameters per function
    function_param_counts = {}
    functions_covered_by_pyi = set()
    
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read(), filename=file)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name
                        
                        # Exclude 'self' and 'cls' from parameters
                        params = [arg for arg in node.args.args if arg.arg not in ('self', 'cls')]
                        param_count = len(params)
                        annotation_count = sum(1 for arg in params if arg.annotation is not None)

                        # If this function is covered by a .pyi file, overwrite counts
                        if file.endswith(".pyi"):
                            functions_covered_by_pyi.add(func_name)
                            function_param_counts[func_name] = (param_count, annotation_count)
                        elif func_name not in functions_covered_by_pyi:
                            # Only add counts from .py if not already covered by .pyi
                            if func_name in function_param_counts:
                                continue
                            function_param_counts[func_name] = (
                                param_count,
                                annotation_count
                            )

        except (SyntaxError, UnicodeDecodeError):
            skipped_files += 1

    # Sum up the final counts
    total_params = sum(counts[0] for counts in function_param_counts.values())
    annotated_params = sum(counts[1] for counts in function_param_counts.values())
    
    if total_params == 0:
        return 100.0, skipped_files

    coverage = (annotated_params / total_params) * 100.0

    return coverage, skipped_files

def calculate_return_type_coverage(files: List[str]) -> Tuple[float, int]:
    total_functions = 0
    annotated_functions = 0
    skipped_files = 0

    # To track return type annotations per function
    function_return_counts = {}
    functions_covered_by_pyi = set()

    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read(), filename=file)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name

                        # If this function is covered by a .pyi file, overwrite counts
                        if file.endswith(".pyi"):
                            functions_covered_by_pyi.add(func_name)
                            function_return_counts[func_name] = (1, 1 if node.returns is not None else 0)
                        elif func_name not in functions_covered_by_pyi:
                            # Only add counts from .py if not already covered by .pyi
                            if func_name in function_return_counts:
                                continue
                            function_return_counts[func_name] = (
                                1,
                                1 if node.returns is not None else 0
                            )

        except (SyntaxError, UnicodeDecodeError):
            skipped_files += 1

    # Sum up the final counts
    total_functions = sum(counts[0] for counts in function_return_counts.values())
    annotated_functions = sum(counts[1] for counts in function_return_counts.values())

    if total_functions == 0:
        return 100.0, skipped_files

    coverage = (annotated_functions / total_functions) * 100.0

    return coverage, skipped_files

def calculate_overall_coverage(files: List[str]) -> dict:
    param_coverage, param_skipped = calculate_parameter_coverage(files)
    return_type_coverage, return_skipped = calculate_return_type_coverage(files)

    total_skipped = max(param_skipped, return_skipped)

    return {
        "parameter_coverage": param_coverage,
        "return_type_coverage": return_type_coverage,
        "skipped_files": total_skipped
    }
