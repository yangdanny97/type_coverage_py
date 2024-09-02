# typeshed_checker.py

import os

# Get the absolute path to the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Construct the path to the typeshed directory
TYPESHED_DIR = os.path.join(PROJECT_ROOT, "typeshed")

def check_typeshed(package_name: str) -> bool:
    """Checks if the package has stubs available in the typeshed repository."""
    
    # Check in the third-party stubs directory
    stubs_path = os.path.join(TYPESHED_DIR, 'stubs', package_name)
    
    return os.path.exists(stubs_path)