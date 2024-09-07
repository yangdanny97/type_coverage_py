import tempfile
import os
import shutil
import json
import sys
import argparse
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

def analyze_package(package_name, rank=None, download_count=None):
    """Analyze a single package and generate a report."""
    package_report = {
        "DownloadCount": download_count,
        "DownloadRanking": rank,
    }

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        print(f"Temporary directory created: {temp_dir} for {package_name}")
        print(f"Analyzing package: {package_name} rank {rank}")

        # Download and extract package files
        files = extract_files(package_name, temp_dir)

        # Check if typeshed exists
        typeshed_exists = check_typeshed(package_name)
        package_report["HasTypeShed"] = typeshed_exists

        # Calculate coverage
        coverage_data = calculate_overall_coverage(files)
        package_report["CoverageData"] = coverage_data

        if typeshed_exists:
            print(f"Typeshed exists for {package_name}. Including it in analysis.")
            typestub_files = find_stub_files(package_name)
            merged_files = merge_files_with_stubs(files, typestub_files)

            coverage_data_with_stubs = calculate_overall_coverage(merged_files)
            package_report["CoverageData"]["parameter_coverage_with_stubs"] = coverage_data_with_stubs["parameter_coverage"]
            package_report["CoverageData"]["return_type_coverage_with_stubs"] = coverage_data_with_stubs["return_type_coverage"]
        else:
            package_report["CoverageData"]["parameter_coverage_with_stubs"] = coverage_data["parameter_coverage"]
            package_report["CoverageData"]["return_type_coverage_with_stubs"] = coverage_data["return_type_coverage"]

        # Generate report
        generate_report(package_report, package_name)

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)
        print(f"Temporary directory {temp_dir} has been deleted.")

    return package_report

def main(top_n=None, package_name=None, write_json=False, write_html=False):
    package_report = {}

    if package_name:
        # Analyze a specific package
        print(f"Analyzing specific package: {package_name}")
        package_report[package_name] = analyze_package(package_name)
    else:
        # Analyze top N packages
        sorted_packages = load_and_sort_top_packages(TOP_PYPI_PACKAGES)
        top_packages = sorted_packages[:top_n]

        for rank, package_data in enumerate(top_packages, start=1):
            package_name = package_data['project']
            download_count = package_data['download_count']

            package_report[package_name] = analyze_package(package_name, rank=rank, download_count=download_count)

    # Conditionally write the JSON report
    if write_json:
        with open(JSON_REPORT_FILE, "w") as json_file:
            json.dump(package_report, json_file, indent=4)
        print("package_report.json file generated.")

    # Conditionally generate the HTML report
    if write_html:
        generate_report_html(package_report)
        print("HTML report generated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Python package type coverage.")
    parser.add_argument('top_n', type=int, nargs='?', help="Analyze the top N PyPI packages.")
    parser.add_argument('--package-name', type=str, help="Analyze a specific package by name.")
    parser.add_argument('--write-json', action='store_true', help="Write the output to a JSON report.")
    parser.add_argument('--write-html', action='store_true', help="Generate an HTML report.")

    args = parser.parse_args()

    if args.package_name:
        main(package_name=args.package_name, write_json=args.write_json, write_html=args.write_html)
    elif args.top_n:
        if not (1 <= args.top_n <= 8000):
            print("Error: <top_n> must be an integer between 1 and 8000.")
            sys.exit(1)
        main(top_n=args.top_n, write_json=args.write_json, write_html=args.write_html)
    else:
        print("Error: Either provide a top N number or a package name.")
        sys.exit(1)
