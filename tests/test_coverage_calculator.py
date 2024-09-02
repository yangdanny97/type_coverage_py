import pytest
from analyzer.coverage_calculator import (
    calculate_parameter_coverage,
    calculate_return_type_coverage,
    calculate_overall_coverage,
)

def test_calculate_parameter_coverage():
    # Test with a basic example
    files = ["tests/test_files/annotated_function.py"]  # Example file with annotated parameters
    param_coverage, skipped_files = calculate_parameter_coverage(files)
    assert param_coverage == 100.0
    assert skipped_files == 0

    # Test with a file that has no annotations
    files = ["tests/test_files/non_annotated_function.py"]
    param_coverage, skipped_files = calculate_parameter_coverage(files)
    assert param_coverage == 0.0
    assert skipped_files == 0

def test_calculate_return_type_coverage():
    # Test with a basic example
    files = ["tests/test_files/annotated_function.py"]  # Example file with return type annotations
    return_coverage, skipped_files = calculate_return_type_coverage(files)
    assert return_coverage == 100.0
    assert skipped_files == 0

    # Test with a file that has no annotations
    files = ["tests/test_files/non_annotated_function.py"]
    return_coverage, skipped_files = calculate_return_type_coverage(files)
    assert return_coverage == 0.0
    assert skipped_files == 0

def test_calculate_overall_coverage():
    # Test with a mix of files
    files = ["tests/test_files/annotated_function.py", "tests/test_files/non_annotated_function.py"]
    coverage_data = calculate_overall_coverage(files)
    assert coverage_data["parameter_coverage"] == 50.0  # Assuming 1 file with 100% and 1 with 0%
    assert coverage_data["return_type_coverage"] == 50.0
    assert coverage_data["skipped_files"] == 0

def test_calculate_overall_coverage_with_skipped_files():
    # Test with files that can't be parsed
    files = ["tests/test_files/syntax_error.py"]
    coverage_data = calculate_overall_coverage(files)
    assert coverage_data["parameter_coverage"] == 100.0  # No parameters to cover
    assert coverage_data["return_type_coverage"] == 100.0  # No returns to cover
    assert coverage_data["skipped_files"] == 1

def test_fully_annotated():
    files = ["tests/test_files/fully_annotated.py"]
    param_coverage, skipped_files = calculate_parameter_coverage(files)
    return_coverage, _ = calculate_return_type_coverage(files)
    assert param_coverage == 100.0
    assert return_coverage == 100.0
    assert skipped_files == 0

def test_partially_annotated():
    files = ["tests/test_files/partially_annotated.py"]
    param_coverage, skipped_files = calculate_parameter_coverage(files)
    return_coverage, _ = calculate_return_type_coverage(files)
    assert param_coverage == pytest.approx(33.33, rel=1e-2)  # Using pytest.approx for floating-point comparison
    assert skipped_files == 0

def test_complex_types():
    files = ["tests/test_files/complex_types.py"]
    param_coverage, skipped_files = calculate_parameter_coverage(files)
    return_coverage, _ = calculate_return_type_coverage(files)
    assert param_coverage == 100.0
    assert return_coverage == 100.0
    assert skipped_files == 0

def test_nested_functions():
    files = ["tests/test_files/nested_functions.py"]
    param_coverage, skipped_files = calculate_parameter_coverage(files)
    return_coverage, _ = calculate_return_type_coverage(files)
    assert param_coverage == 100.0
    assert return_coverage == 100.0
    assert skipped_files == 0

def test_embedded_pyi():
    files = ["tests/test_files/embedded_pyi.py", "tests/test_files/embedded_pyi.pyi"]
    param_coverage, skipped_files = calculate_parameter_coverage(files)
    return_coverage, _ = calculate_return_type_coverage(files)
    assert param_coverage == 100.0  # Since .pyi provides annotations
    assert return_coverage == 100.0  # Since .pyi provides annotations
    assert skipped_files == 0

def test_class_methods():
    files = ["tests/test_files/class_methods.py"]
    param_coverage, skipped_files = calculate_parameter_coverage(files)
    return_coverage, _ = calculate_return_type_coverage(files)
    assert param_coverage == 100.0  # All parameters annotated
    assert return_coverage == pytest.approx(66.67, rel=1e-2)  # 2 out of 3 methods annotated with return type
    assert skipped_files == 0

def test_order_independence_for_pyi_and_py():
    # Define the file paths for the .py and .pyi files
    py_file = "tests/test_files/embedded_pyi.py"
    pyi_file = "tests/test_files/embedded_pyi.pyi"
    
    # Test with .py first, then .pyi
    files_py_first = [py_file, pyi_file]
    param_coverage_py_first, skipped_files_py_first = calculate_parameter_coverage(files_py_first)
    return_coverage_py_first, _ = calculate_return_type_coverage(files_py_first)
    
    # Test with .pyi first, then .py
    files_pyi_first = [pyi_file, py_file]
    param_coverage_pyi_first, skipped_files_pyi_first = calculate_parameter_coverage(files_pyi_first)
    return_coverage_pyi_first, _ = calculate_return_type_coverage(files_pyi_first)
    
    # Assert that both orders produce the same results
    assert param_coverage_py_first == param_coverage_pyi_first, "Parameter coverage should be the same regardless of file order"
    assert return_coverage_py_first == return_coverage_pyi_first, "Return type coverage should be the same regardless of file order"
    assert skipped_files_py_first == skipped_files_pyi_first, "Skipped files should be the same regardless of file order"
