@echo off
echo Starting IRD Form Automation...
echo.
echo Make sure you have:
echo 1. Chrome running with debugging enabled (port 9222)
echo 2. Already logged into IRD website
echo 3. Navigated to the form page
echo.
echo Starting automation in 3 seconds...
timeout /t 3 /nobreak >nul
echo.
python ird_automation.py
echo.
echo Automation completed!
pause
