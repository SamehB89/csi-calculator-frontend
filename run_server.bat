@echo off
title CSI Data Server
echo Starting CSI Data Manager Backend...
echo.

cd /d "%~dp0backend"

if not exist "app.py" (
    echo Error: app.py not found in backend folder
    pause
    exit /b
)

echo Installing requirements...
pip install -r "%~dp0requirements.txt" > nul 2>&1

echo.
echo Server is starting...
echo Keep this window OPEN while using the Excel tool.
echo.

python app.py

if %errorlevel% neq 0 (
    echo.
    echo Server crashed or failed to start.
    pause
)
