from typing import Dict

HTML_REPORT_FILE = "index.html"

def generate_report(package_data: Dict[str, Dict[str, float]], package_name: str) -> None:
    """Generates a report of the coverage data."""
    coverage_data = package_data["CoverageData"]
    print(f"Coverage Report for {package_name}:")
    print(f"Has typeshed stubs: {package_data['HasTypeShed']}")
    print(f"Parameter Type Coverage: {coverage_data['parameter_coverage']:.2f}%")
    print(f"Return Type Coverage: {coverage_data['return_type_coverage']:.2f}%")
    print(f"Parameter Type Coverage With Stubs: {coverage_data['parameter_coverage_with_stubs']:.2f}%")
    print(f"Return Type Coverage With Stubs: {coverage_data['return_type_coverage_with_stubs']:.2f}%")
    print("-" * 40)

def get_color(percentage: float) -> str:
    """Calculate a subtle but noticeable color gradient from light red (0%) to light green (100%)."""
    if percentage < 50:
        # Transition from light red to light yellow for 0% to 50%
        red = 255
        green = int(255 * (percentage / 50))
    else:
        # Transition from light yellow to light green for 50% to 100%
        red = int(255 * ((100 - percentage) / 50))
        green = 255
    
    blue = 200  # A small amount of blue for a softer, more pleasant color
    return f"rgb({red},{green},{blue})"

def generate_report_html(package_report: Dict[str, Dict[str, Dict[str, float]]]) -> None:
    """Generates an HTML report of the package coverage data."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Package Type Coverage Report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f4f4f4;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 18px;
                text-align: left;
            }
            table th, table td {
                padding: 12px;
                border: 1px solid #ddd;
            }
            table th {
                background-color: #f2f2f2;
                color: #333;
            }
            table tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            table tr:hover {
                background-color: #f1f1f1;
            }
            .coverage-cell {
                text-align: right;
                padding-right: 10px;
                color: #333;  /* Darker text color for better readability */
            }
            .skipped-cell {
                text-align: center;
                color: #d9534f; /* Red color for skipped text */
            }
            .github-link {
                text-align: center;
                margin-top: 20px;
                font-size: 16px;
            }
            .github-link a {
                color: #0066cc;
                text-decoration: none;
            }
            .github-link a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Package Type Coverage Report</h1>
        <p class="github-link">See code and methodology here: 
            <a href="https://github.com/lolpack/type_coverage_py" target="_blank">
                https://github.com/lolpack/type_coverage_py
            </a>
        </p>
        <table>
            <tr>
                <th>Ranking</th>
                <th>Package Name</th>
                <th>Download Count</th>
                <th>Has Typeshed</th>
                <th>Parameter Type Coverage</th>
                <th>Return Type Coverage</th>
                <th>Parameter Coverage with Typeshed</th>
                <th>Return Type Coverage with Typeshed</th>
                <th>Skipped Files</th>
            </tr>
    """

    for package_name, details in package_report.items():
        coverage_data = details['CoverageData']
        parameter_coverage = round(coverage_data['parameter_coverage'], 2)
        return_coverage = round(coverage_data['return_type_coverage'], 2)
        parameter_coverage_with_stubs = round(coverage_data.get('parameter_coverage_with_stubs', 0), 2)
        return_coverage_with_stubs = round(coverage_data.get('return_type_coverage_with_stubs', 0), 2)
        
        param_color = get_color(parameter_coverage)
        return_color = get_color(return_coverage)
        param_stub_color = get_color(parameter_coverage_with_stubs)
        return_stub_color = get_color(return_coverage_with_stubs)
        skipped_files = f"{coverage_data['skipped_files']}"

        html_content += f"""
            <tr>
                <td>{details['DownloadRanking']}</td>
                <td>{package_name}</td>
                <td>{details['DownloadCount']}</td>
                <td>{'Yes' if details['HasTypeShed'] else 'No'}</td>
                <td class="coverage-cell" style="background-color: {param_color};">{parameter_coverage:.2f}%</td>
                <td class="coverage-cell" style="background-color: {return_color};">{return_coverage:.2f}%</td>
                <td class="coverage-cell" style="background-color: {param_stub_color};">{parameter_coverage_with_stubs:.2f}%</td>
                <td class="coverage-cell" style="background-color: {return_stub_color};">{return_coverage_with_stubs:.2f}%</td>
                <td class="skipped-cell">{skipped_files}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    # Output the HTML to a file
    with open(HTML_REPORT_FILE, "w") as file:
        file.write(html_content)

    print(f"HTML report generated: {HTML_REPORT_FILE}")
