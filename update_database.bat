@echo off
echo ============================================================
echo CSI Database Auto-Updater
echo ============================================================
echo.
echo This will update the database from CSI.xlsm
echo.
echo Steps:
echo   1. Read data from CSI.xlsm
echo   2. Clean and validate the data
echo   3. Update database/csi_data.db
echo.
echo ============================================================
echo.
pause

python update_database_from_excel.py

echo.
echo ============================================================
echo Update Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Restart the Flask server (run_server.bat)
echo   2. Refresh the web application
echo.
pause
