# Calculating staleness from stub packages

from typing import Any, Dict
import json

import requests

from datetime import datetime
format_str = "%Y-%m-%dT%H:%M:%S"

def get_latest_release_time_for_package(package_name: str) -> datetime:
    # Fetch the package metadata from PyPI
    pypi_url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(pypi_url)
    response.raise_for_status()

    # The API returns a JSON response, so 'data' is a dictionary
    data: Dict[str, Any] = response.json()
    latest_version = data['info']['version']
    release_info = data['releases'][latest_version]
    latest_upload = max(release_info, key=lambda x: datetime.strptime(x['upload_time'], format_str))
    return datetime.strptime(latest_upload['upload_time'], format_str)

with open("stub_packages.json", "r") as f:
    data = json.load(f)
    for d in data:
        package_release_time = get_latest_release_time_for_package(d)
        stub_release_time = get_latest_release_time_for_package(d + "-stubs")
        time_difference = package_release_time - stub_release_time
        print(f"{d}: {time_difference.days} days stale")
