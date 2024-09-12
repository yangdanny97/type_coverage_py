import ast
import os
from typing import List, Tuple, Dict, Set, Optional

def is_test_file(file_path: str) -> bool:
    """Determine if the file is in a test directory or part of a test suite."""
    # Normalize path and split into components
    parts = os.path.normpath(file_path).split(os.sep)
    
    # Check if 'test' or 'tests' is a directory and not just part of the file name
    return "test" in parts or "tests" in parts


def calculate_parameter_coverage(files: List[str]) -> Tuple[float, float, int]:
    total_params: int = 0
    annotated_params: int = 0
    total_params_with_tests: int = 0
    annotated_params_with_tests: int = 0
    skipped_files: int = 0

    # To track annotations and parameters per function
    function_param_counts: Dict[str, Tuple[int, int]] = {}
    functions_covered_by_pyi: Set[str] = set()

    for file in files:
        # Skip __init__.py files
        if file.endswith("__init__.py"):
            continue

        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read(), filename=file)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name: str = node.name
                        
                        # Exclude 'self', 'metacls', 'mcls' and 'cls' from parameters
                        params = [arg for arg in node.args.args if arg.arg not in ('self', 'cls', 'metacls', 'mcls')]
                        param_count: int = len(params)
                        annotation_count: int = sum(1 for arg in params if arg.annotation is not None)

                        # Track counts with and without test files
                        if is_test_file(file):
                            total_params_with_tests += param_count
                            annotated_params_with_tests += annotation_count
                        else:
                            total_params += param_count
                            total_params_with_tests += param_count
                            annotated_params += annotation_count

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

    # Sum up the final counts
    if total_params_with_tests == 0:
        return -1.0, -1.0, skipped_files

    # Calculate coverage with and without tests
    annotated_params_with_tests += annotated_params
    param_coverage_with_tests = (annotated_params_with_tests / total_params_with_tests) * 100.0

    if total_params == 0:
        return -1.0, param_coverage_with_tests, skipped_files

    param_coverage = (annotated_params / total_params) * 100.0

    return param_coverage, param_coverage_with_tests, skipped_files


def calculate_return_type_coverage(files: List[str]) -> Tuple[float, float, int]:
    total_functions: int = 0
    annotated_functions: int = 0
    total_functions_with_tests: int = 0
    annotated_functions_with_tests: int = 0
    skipped_files: int = 0

    # To track return type annotations per function
    function_return_counts: Dict[str, Tuple[int, int]] = {}
    functions_covered_by_pyi: Set[str] = set()

    for file in files:
        # Skip __init__.py files
        if file.endswith("__init__.py"):
            continue

        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read(), filename=file)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name: str = node.name

                        # Track counts with and without test files
                        if is_test_file(file):
                            total_functions_with_tests += 1
                            if node.returns is not None:
                                annotated_functions_with_tests += 1
                        else:
                            total_functions_with_tests += 1
                            total_functions += 1
                            if node.returns is not None:
                                annotated_functions += 1

        except (SyntaxError, UnicodeDecodeError):
            skipped_files += 1

    # Sum up the final counts
    total_functions = sum(counts[0] for counts in function_return_counts.values())
    annotated_functions = sum(counts[1] for counts in function_return_counts.values())

    # Sum up the final counts
    if total_functions_with_tests == 0:
        return -1.0, -1.0, skipped_files

    annotated_functions_with_tests += annotated_functions
    return_coverage_with_tests = (annotated_functions_with_tests / total_functions_with_tests) * 100.0
    
    if total_functions == 0:
        return -1.0, return_coverage_with_tests, skipped_files

    return_coverage = (annotated_functions / total_functions) * 100.0   

    return return_coverage, return_coverage_with_tests, skipped_files


def calculate_overall_coverage(files: List[str]) -> Dict[str, float]:
    param_coverage, param_coverage_with_tests, param_skipped = calculate_parameter_coverage(files)
    return_type_coverage, return_coverage_with_tests, return_skipped = calculate_return_type_coverage(files)

    total_skipped: int = max(param_skipped, return_skipped)

    return {
        "parameter_coverage": param_coverage,
        "param_coverage_with_tests": param_coverage_with_tests,
        "return_type_coverage": return_type_coverage,
        "return_coverage_with_tests": return_coverage_with_tests,
        "skipped_files": total_skipped
    }
