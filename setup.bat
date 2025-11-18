@echo off
REM Setup script for XAU/USD Forex Trading Assistant (Windows)

echo ================================================================
echo      XAU/USD Forex Trading Assistant - Setup Script
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create data directory
echo Creating data directory...
if not exist data mkdir data

echo.
echo ================================================================
echo                    Setup Complete!
echo ================================================================
echo.
echo To start the application:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate.bat
echo.
echo   2. Run the application:
echo      python forex_trader.py
echo.
echo   3. (Optional) Configure API keys in config.json
echo.
echo For more information, see README.md
echo.
pause
