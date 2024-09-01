# type_coverage_py

Calculate the Type Coverage for top Python packages.

Take the top pypi packages pulled from this project [https://github.com/hugovk/top-pypi-packages](https://github.com/hugovk/top-pypi-packages)

## Methodology

This section outlines how the script analyzes Python packages, checks for typeshed availability, and calculates type coverage. The process involves three key steps: package extraction, typeshed check, and type coverage calculation.

### **Package Extraction**

- **Downloading**: The script downloads the source distribution of each selected package from PyPI and extracts it into a temporary directory.
- **File Extraction**: It identifies and extracts all Python files (`.py`) and type stub files (`.pyi`) from the package for analysis.

### **Typeshed Check**

- **Typeshed Directory**: The script checks if a corresponding stub exists in the `typeshed` repository, which contains type stubs for standard library modules and popular third-party packages.
- **Existence Check**: If a typeshed stub exists, it is recorded as `HasTypeShed: Yes`; otherwise, it is marked as `HasTypeShed: No`.

### **Type Coverage Calculation**

- **Parameter Coverage**: 
  - The script analyzes function definitions in the extracted files and calculates the percentage of function parameters that have type annotations.
  - The formula used:
  \[
  \text{Parameter Coverage} = \left( \frac{\text{Number of Parameters with Type Annotations}}{\text{Total Number of Parameters}} \right) \times 100
  \]

- **Return Type Coverage**:
  - Similarly, the script calculates the percentage of functions that have return type annotations.
  - The formula used:
  \[
  \text{Return Type Coverage} = \left( \frac{\text{Number of Functions with Return Type Annotations}}{\text{Total Number of Functions}} \right) \times 100
  \]

- **Skipped Files**:
  - Files that cannot be processed due to syntax or encoding errors are skipped, and the number of skipped files is recorded.

This methodology ensures accurate and detailed analysis of type coverage for popular Python packages.

## Usage

Call the main function with the top number of packages to analyze, the max is 8,000.

`python3 main.py 100`

