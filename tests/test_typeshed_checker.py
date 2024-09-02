import os
import pytest
import sys
from analyzer.typeshed_checker import check_typeshed

def test_check_typeshed(monkeypatch, tmpdir):
    print("sys.path:", sys.path)  # Print sys.path to see where Python is looking

    # Create a mock typeshed directory structure in the temporary directory
    typeshed_dir = tmpdir.mkdir("typeshed")
    stubs_dir = typeshed_dir.mkdir("stubs")
    
    # Create a mock stub package
    mock_package = stubs_dir.mkdir("mock_package")
    mock_package.join("__init__.pyi").write("# mock init file for mock_package")

    # Monkeypatch the TYPESHED_DIR to point to the temporary typeshed directory
    monkeypatch.setattr("analyzer.typeshed_checker.TYPESHED_DIR", str(typeshed_dir))

    # Test that check_typeshed correctly identifies the existence of mock_package
    assert check_typeshed("mock_package") == True
    
    # Test that check_typeshed correctly identifies a non-existing package
    assert check_typeshed("nonexistent_package") == False