import pytest
from io import BytesIO
import tarfile
import tempfile
import os
import sys
import json

# Add the directory containing main.py to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import main, load_and_sort_top_packages

def create_mock_tar_gz():
    # Create a mock tar.gz file in memory
    tar_bytes = BytesIO()
    with tarfile.open(fileobj=tar_bytes, mode='w:gz') as tar:
        # Add a dummy file to the tar.gz
        info = tarfile.TarInfo(name="test.py")
        info.size = len(b"print('Hello, world!')")
        tar.addfile(info, BytesIO(b"print('Hello, world!')"))
    tar_bytes.seek(0)
    return tar_bytes.read()

def mock_get(*args, **kwargs):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "urls": [{"packagetype": "sdist", "url": "https://example.com/fake_package.tar.gz"}]
            }

        @property
        def content(self):
            # Return a valid tar.gz file content
            return create_mock_tar_gz()

    return MockResponse()

def test_main(monkeypatch):
    def mock_load_and_sort_top_packages(json_file):
        return [
            {"download_count": 1000, "project": "package_a"},
            {"download_count": 500, "project": "package_b"},
        ]

    def mock_generate_report(*args, **kwargs):
        print("generate_report called with args:", args, "and kwargs:", kwargs)
    
    def mock_generate_report_html(*args, **kwargs):
        print("generate_report_html called with args:", args, "and kwargs:", kwargs)

    monkeypatch.setattr("main.load_and_sort_top_packages", mock_load_and_sort_top_packages)
    monkeypatch.setattr("main.generate_report", mock_generate_report)
    monkeypatch.setattr("main.generate_report_html", mock_generate_report_html)
    monkeypatch.setattr("requests.get", mock_get)

    with tempfile.TemporaryDirectory() as temp_dir:
        json_file = os.path.join(temp_dir, 'package_report.json')
        monkeypatch.setattr("main.JSON_REPORT_FILE", json_file)

        main(2)
        assert os.path.exists(json_file)