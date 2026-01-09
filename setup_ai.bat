@echo off
echo ===============================================
echo CSI Crew Calculator - AI Setup
echo ===============================================
echo.
echo This script will set up the Google Gemini API key
echo for the AI Chat feature.
echo.
echo Step 1: Get your FREE API key from:
echo    https://aistudio.google.com/app/apikey
echo.
echo Step 2: Enter your API key below
echo.
set /p GEMINI_KEY="Enter your Gemini API Key: "
echo.
echo Setting environment variable...
setx GEMINI_API_KEY "%GEMINI_KEY%"
echo.
echo ===============================================
echo Done! API key saved.
echo.
echo Restart the server to apply changes:
echo    cd backend
echo    python app.py
echo ===============================================
pause
