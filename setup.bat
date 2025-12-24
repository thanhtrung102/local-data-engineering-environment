@echo off
REM Local Data Engineering Environment Setup Script for Windows
REM This script automates the setup of the virtual environment and dependencies

echo ======================================
echo Local Data Engineering Environment Setup
echo ======================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.9 or higher from https://www.python.org/
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo * Python %PYTHON_VERSION% detected
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist env (
    echo Warning: Virtual environment already exists. Removing old environment...
    rmdir /s /q env
)

python -m venv env
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    exit /b 1
)
echo * Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call env\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    exit /b 1
)
echo * Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo * pip upgraded to latest version
echo.

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    exit /b 1
)
echo * All dependencies installed successfully
echo.

REM Install Jupyter kernel
echo Installing Jupyter kernel for this environment...
python -m ipykernel install --user --name=local-de-env --display-name="Local DE Environment"
echo * Jupyter kernel installed
echo.

echo ======================================
echo Setup completed successfully!
echo ======================================
echo.
echo Next steps:
echo 1. Activate the virtual environment:
echo    env\Scripts\activate.bat
echo.
echo 2. Verify the installation:
echo    python test_setup.py
echo.
echo 3. Start Jupyter Notebook:
echo    jupyter notebook
echo.
echo 4. Open notebooks/data_workflow.ipynb to begin!
echo.

pause
