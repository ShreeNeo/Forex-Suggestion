@echo off
REM Start the web UI for XAU/USD Forex Trading Assistant

echo ================================================================
echo      XAU/USD Forex Trading Assistant - Web Dashboard
echo ================================================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Error: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Starting web dashboard...
echo Dashboard will open in your browser
echo To stop, press Ctrl+C
echo.

REM Start streamlit
streamlit run web_ui.py --server.port 8501 --server.address localhost

echo.
echo Dashboard stopped.
pause
