#!/bin/bash

# Local Data Engineering Environment Setup Script for Linux/Mac
# This script automates the setup of the virtual environment and dependencies

set -e  # Exit on any error

echo "======================================"
echo "Local Data Engineering Environment Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "ERROR: Python $REQUIRED_VERSION or higher is required. You have Python $PYTHON_VERSION."
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "env" ]; then
    echo "Warning: Virtual environment already exists. Removing old environment..."
    rm -rf env
fi

python3 -m venv env
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source env/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded to latest version"
echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt --quiet
echo "✓ All dependencies installed successfully"
echo ""

# Install Jupyter kernel
echo "Installing Jupyter kernel for this environment..."
python -m ipykernel install --user --name=local-de-env --display-name="Local DE Environment"
echo "✓ Jupyter kernel installed"
echo ""

echo "======================================"
echo "Setup completed successfully!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source env/bin/activate"
echo ""
echo "2. Verify the installation:"
echo "   python test_setup.py"
echo ""
echo "3. Start Jupyter Notebook:"
echo "   jupyter notebook"
echo ""
echo "4. Open notebooks/data_workflow.ipynb to begin!"
echo ""
