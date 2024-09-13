import requests
import csv

CSV_URL = "https://alexwaygood.github.io/typeshed-stats/stats_as_csv.csv"

def download_typeshed_csv() -> Dict[str, Dict[str, Any]]:
    """Download and parse the typeshed CSV file into a dictionary."""
    response = requests.get(CSV_URL)
    response.raise_for_status()  # Ensure the download was successful

    typeshed_data = {}
    decoded_content = response.content.decode('utf-8').splitlines()
    csv_reader = csv.DictReader(decoded_content)

    for row in csv_reader:
        package_name = row['package_name'].strip()
        typeshed_data[package_name] = {
            "completeness_level": row['completeness_level'],
            "annotated_parameters": row['annotated_parameters'],
            "unannotated_parameters": row['unannotated_parameters'],
            "% param": row['% param'],
            "annotated_returns": row['annotated_returns'],
            "unannotated_returns": row['unannotated_returns'],
            "% return": row['% return'],
            "stubtest_strictness": row['stubtest_strictness'],
            "stubtest_platforms": row['stubtest_platforms'],
        }
    
    return typeshed_data