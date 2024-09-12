import pytest
from unittest.mock import Mock
from io import BytesIO
import tarfile
import tempfile
import os
import sys
from typing import Any, Dict

# Add the directory containing main.py to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import main

def create_mock_tar_gz() -> bytes:
    # Create a mock tar.gz file in memory
    tar_bytes = BytesIO()
    with tarfile.open(fileobj=tar_bytes, mode='w:gz') as tar:
        # Add a dummy file to the tar.gz
        info = tarfile.TarInfo(name="test.py")
        info.size = len(b"print('Hello, world!')")
        tar.addfile(info, BytesIO(b"print('Hello, world!')"))
    tar_bytes.seek(0)
    return tar_bytes.read()

def mock_get(*args: Any, **kwargs: Any) -> Any:
    class MockResponse:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> Dict[str, Any]:
            return {
                "urls": [{"packagetype": "sdist", "url": "https://example.com/fake_package.tar.gz"}]
            }

        @property
        def content(self) -> bytes:
            # Return a valid tar.gz file content
            return create_mock_tar_gz()

    return MockResponse()

def test_main_with_write_json_and_write_html(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_load_and_sort_top_packages(json_file: str) -> list[Dict[str, Any]]:
        return [
            {"download_count": 1000, "project": "package_a"},
            {"download_count": 500, "project": "package_b"},
        ]
    
    mock_generate_report = Mock()
    mock_generate_report_html = Mock()

    monkeypatch.setattr("main.load_and_sort_top_packages", mock_load_and_sort_top_packages)
    monkeypatch.setattr("main.generate_report", mock_generate_report)
    monkeypatch.setattr("main.generate_report_html", mock_generate_report_html)
    monkeypatch.setattr("requests.get", mock_get)

    with tempfile.TemporaryDirectory() as temp_dir:
        json_file = os.path.join(temp_dir, 'package_report.json')
        monkeypatch.setattr("main.JSON_REPORT_FILE", json_file)

        # Test when --write-json and --write-html flags are passed
        main(top_n=2, write_json=True, write_html=True)

        # Check that the JSON file was created
        assert os.path.exists(json_file)

        # Check that the HTML report was generated
        mock_generate_report_html.assert_called_once()

def test_main_without_write_json_and_write_html(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_load_and_sort_top_packages(json_file: str) -> list[Dict[str, Any]]:
        return [
            {"download_count": 1000, "project": "package_a"},
            {"download_count": 500, "project": "package_b"},
        ]
    
    mock_generate_report = Mock()
    mock_generate_report_html = Mock()

    monkeypatch.setattr("main.load_and_sort_top_packages", mock_load_and_sort_top_packages)
    monkeypatch.setattr("main.generate_report", mock_generate_report)
    monkeypatch.setattr("main.generate_report_html", mock_generate_report_html)
    monkeypatch.setattr("requests.get", mock_get)

    with tempfile.TemporaryDirectory() as temp_dir:
        json_file = os.path.join(temp_dir, 'package_report.json')
        monkeypatch.setattr("main.JSON_REPORT_FILE", json_file)

        # Test when --write-json and --write-html flags are not passed
        main(top_n=2, write_json=False, write_html=False)

        # Check that the JSON file was NOT created
        assert not os.path.exists(json_file)

        # Check that the HTML report generation was NOT called
        mock_generate_report_html.assert_not_called()
