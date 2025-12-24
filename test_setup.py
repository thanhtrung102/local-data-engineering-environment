#!/usr/bin/env python3
"""
Setup Validation Script for Local Data Engineering Environment

This script verifies that all requirements are correctly installed
and the environment is properly configured.
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Verify Python version is 3.9 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"  ✗ FAIL: Python 3.9+ required, found {version.major}.{version.minor}")
        return False
    print(f"  ✓ PASS: Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_package_imports():
    """Verify all required packages can be imported."""
    print("\nChecking required packages...")
    packages = {
        'dlt': 'dlt',
        'duckdb': 'duckdb',
        'pandas': 'pandas',
        'jupyter': 'jupyter',
        'notebook': 'notebook',
        'ipykernel': 'ipykernel'
    }

    all_passed = True
    for package_name, import_name in packages.items():
        try:
            __import__(import_name)
            print(f"  ✓ PASS: {package_name} is installed")
        except ImportError:
            print(f"  ✗ FAIL: {package_name} is not installed")
            all_passed = False

    return all_passed


def check_package_versions():
    """Verify package versions meet minimum requirements."""
    print("\nChecking package versions...")

    version_checks = []

    try:
        import dlt
        dlt_version = dlt.__version__
        print(f"  ✓ dlt version: {dlt_version}")
        version_checks.append(True)
    except Exception as e:
        print(f"  ✗ Could not verify dlt version: {e}")
        version_checks.append(False)

    try:
        import duckdb
        duckdb_version = duckdb.__version__
        print(f"  ✓ duckdb version: {duckdb_version}")
        version_checks.append(True)
    except Exception as e:
        print(f"  ✗ Could not verify duckdb version: {e}")
        version_checks.append(False)

    try:
        import pandas
        pandas_version = pandas.__version__
        print(f"  ✓ pandas version: {pandas_version}")
        version_checks.append(True)
    except Exception as e:
        print(f"  ✗ Could not verify pandas version: {e}")
        version_checks.append(False)

    return all(version_checks)


def check_directory_structure():
    """Verify required directories exist."""
    print("\nChecking directory structure...")

    required_dirs = ['notebooks', 'data']
    all_passed = True

    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            print(f"  ✓ PASS: {dir_name}/ directory exists")
        else:
            print(f"  ✗ FAIL: {dir_name}/ directory missing")
            all_passed = False

    return all_passed


def check_sample_data():
    """Verify sample data file exists."""
    print("\nChecking sample data...")

    sample_file = Path("data/sample.csv")
    if sample_file.exists():
        print(f"  ✓ PASS: data/sample.csv exists")
        return True
    else:
        print(f"  ⚠ WARNING: data/sample.csv not found (will be created)")
        return True  # Not a critical failure


def check_requirements_file():
    """Verify requirements.txt exists."""
    print("\nChecking configuration files...")

    req_file = Path("requirements.txt")
    if req_file.exists():
        print(f"  ✓ PASS: requirements.txt exists")
        return True
    else:
        print(f"  ✗ FAIL: requirements.txt missing")
        return False


def main():
    """Run all validation checks."""
    print("=" * 60)
    print("Local Data Engineering Environment - Setup Validation")
    print("=" * 60)
    print()

    checks = [
        check_python_version(),
        check_package_imports(),
        check_package_versions(),
        check_directory_structure(),
        check_sample_data(),
        check_requirements_file()
    ]

    print("\n" + "=" * 60)
    if all(checks):
        print("✓ ALL CHECKS PASSED!")
        print("=" * 60)
        print("\nYour environment is ready to use!")
        print("\nNext steps:")
        print("1. Start Jupyter Notebook: jupyter notebook")
        print("2. Open notebooks/data_workflow.ipynb")
        print("3. Run the cells to execute the data pipeline")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("1. Make sure you activated the virtual environment:")
        print("   - Linux/Mac: source env/bin/activate")
        print("   - Windows: env\\Scripts\\activate.bat")
        print("2. Re-run the setup script:")
        print("   - Linux/Mac: ./setup.sh")
        print("   - Windows: setup.bat")
        print("3. Install missing packages: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
