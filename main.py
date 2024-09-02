import tempfile
import os
import shutil
import json
import sys
from analyzer.package_analyzer import download_package, extract_files
from analyzer.typeshed_checker import check_typeshed, find_stub_files, merge_files_with_stubs
from analyzer.coverage_calculator import calculate_overall_coverage
from analyzer.report_generator import generate_report, generate_report_html

JSON_REPORT_FILE = 'package_report.json'
TOP_PYPI_PACKAGES = 'top-pypi-packages-30-days.min.json'

def load_and_sort_top_packages(json_file):
    """Load the JSON file and sort it by download_count."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    sorted_rows = sorted(data['rows'], key=lambda x: x['download_count'], reverse=True)
    return sorted_rows

def main(top_n):
    sorted_packages = load_and_sort_top_packages(TOP_PYPI_PACKAGES)

    # Process only the top N packages
    top_packages = sorted_packages[:top_n]

    package_report = {}
    for rank, package_data in enumerate(top_packages, start=1):
        package_name = package_data['project']
        download_count = package_data['download_count']

        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        package_report[package_name] = {
            "DownloadCount": download_count,
            "DownloadRanking": rank,
        }

        try:
            print(f"Temporary directory created: {temp_dir} for {package_name}")
            print(f"Analyzing package: {package_name} rank {rank}")
            
            # Download and extract package files
            files = extract_files(package_name, temp_dir)
            
            # Check if typeshed exists
            typeshed_exists = check_typeshed(package_name)
            package_report[package_name]["HasTypeShed"] = typeshed_exists

            # Calculate coverage
            coverage_data = calculate_overall_coverage(files)
            package_report[package_name]["CoverageData"] = coverage_data
            
            if typeshed_exists:
                print(f"Typeshed exists for {package_name}. Including it in analysis.")
                # prefer inline .pyi over typestubs
                typestub_files = find_stub_files(package_name)
                merged_files = merge_files_with_stubs(files, typestub_files)
                files # contains all file for package
                find_stub_files(package_name) # stubs from typeshed

                coverage_data_with_stubs = calculate_overall_coverage(merged_files)
                package_report[package_name]["CoverageData"]["parameter_coverage_with_stubs"] = coverage_data_with_stubs["parameter_coverage"]
                package_report[package_name]["CoverageData"]["return_type_coverage_with_stubs"] = coverage_data_with_stubs["return_type_coverage"]
            else:
                package_report[package_name]["CoverageData"]["parameter_coverage_with_stubs"] = coverage_data["parameter_coverage"]
                package_report[package_name]["CoverageData"]["return_type_coverage_with_stubs"] = coverage_data["return_type_coverage"]
            

            
            # Generate report
            generate_report(package_report[package_name], package_name)

        finally:
            # Clean up the temporary directory
            shutil.rmtree(temp_dir)
            print(f"Temporary directory {temp_dir} has been deleted.")

    # Write package_report to a JSON file before generating the HTML report
    with open(JSON_REPORT_FILE, "w") as json_file:
        json.dump(package_report, json_file, indent=4)
    print("package_report.json file generated.")

    # Generate the HTML report for all processed packages
    generate_report_html(package_report)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <top_n>")
        sys.exit(1)

    try:
        top_n = int(sys.argv[1])
        if not (1 <= top_n <= 8000):
            raise ValueError
    except ValueError:
        print("Error: <top_n> must be an integer between 1 and 8000.")
        sys.exit(1)

    main(top_n)
