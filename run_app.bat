@echo off
echo Starting CSI Data Manager...
echo.
echo 1. Starting Backend Server...
start "CSI Backend" cmd /k "cd backend && python app.py"
echo.
echo 2. Opening Frontend...
timeout /t 2 >nul
start frontend/index.html
echo.
echo Application started!
echo Backend running at: http://localhost:5000
echo Frontend opened in your default browser.
echo.
pause
