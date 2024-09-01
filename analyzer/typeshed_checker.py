# typeshed_checker.py

import os

TYPESHED_DIR = os.path.join(os.path.dirname(__file__), "typeshed")

def check_typeshed(package_name: str) -> bool:
    """Checks if the package has stubs available in the typeshed repository."""
    typeshed_path = os.path.join(TYPESHED_DIR, 'stubs', package_name)
    return os.path.exists(typeshed_path)
