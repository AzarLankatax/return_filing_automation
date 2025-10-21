@echo off
echo IRD Automation Project - Quick Start
echo ====================================
echo.
echo This will run the IRD automation project step by step.
echo.
echo Step 1: Browser Setup
echo - Opens Chrome browser
echo - Fills login credentials
echo - Waits for CAPTCHA completion
echo.
echo Step 2: Manual Login (you need to do this)
echo - Complete CAPTCHA in browser
echo - Click Login button
echo - Navigate to form page
echo.
echo Step 3: Form Automation
echo - Runs all components automatically
echo - Saves drafts
echo - Completes the process
echo.
pause
echo.
echo Starting browser setup...
python browser_setup.py
echo.
echo Browser setup completed. Please complete login in the browser.
echo Press any key when login is complete...
pause
echo.
echo Starting form automation...
python form_automation_new.py
echo.
echo Automation completed!
pause
