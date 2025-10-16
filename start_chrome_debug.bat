@echo off
echo Starting Chrome with debugging enabled...
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"
echo Chrome started! You can now login to IRD website manually.
echo After logging in, run your Python automation script.
pause
