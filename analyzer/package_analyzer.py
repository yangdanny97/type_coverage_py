import os
import requests
import zipfile
import tarfile
from typing import List
from urllib.parse import urljoin

def download_package(package_name: str, temp_dir) -> str:
    """Downloads the specified package from PyPI and extracts it to a temporary directory."""
    # Fetch the package metadata from PyPI
    pypi_url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(pypi_url)
    response.raise_for_status()
    data = response.json()
    
    # Get the URL for the source distribution
    urls = data.get('urls', [])
    sdist_url = None
    for url_info in urls:
        if url_info.get('packagetype') == 'sdist':
            sdist_url = url_info.get('url')
            break
    
    if not sdist_url:
        raise ValueError(f"Source distribution for package '{package_name}' not found on PyPI.")
    
    # Download the source distribution
    sdist_response = requests.get(sdist_url)
    sdist_response.raise_for_status()
    
    
    # Determine the archive type and extract
    if sdist_url.endswith('.zip'):
        archive_path = os.path.join(temp_dir, f"{package_name}.zip")
        with open(archive_path, 'wb') as archive_file:
            archive_file.write(sdist_response.content)
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
    elif sdist_url.endswith(('.tar.gz', '.tgz')):
        archive_path = os.path.join(temp_dir, f"{package_name}.tar.gz")
        with open(archive_path, 'wb') as archive_file:
            archive_file.write(sdist_response.content)
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            tar_ref.extractall(temp_dir)
    else:
        raise ValueError(f"Unsupported archive format for {sdist_url}.")
    
    # Return the path to the extracted package
    return temp_dir

def extract_files(package_name: str, temp_dir) -> List[str]:
    """Extracts Python files from the downloaded package directory."""
    package_dir = download_package(package_name, temp_dir)
    python_files = []
    
    for root, _, files in os.walk(package_dir):
        for file in files:
            if file.endswith('.py') or file.endswith('.pyi'):
                python_files.append(os.path.join(root, file))
    
    return python_files
