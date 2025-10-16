Write-Host "Starting IRD Form Automation..." -ForegroundColor Green
Write-Host ""
Write-Host "Make sure you have:" -ForegroundColor Yellow
Write-Host "1. Chrome running with debugging enabled (port 9222)" -ForegroundColor Yellow
Write-Host "2. Already logged into IRD website" -ForegroundColor Yellow
Write-Host "3. Navigated to the form page" -ForegroundColor Yellow
Write-Host ""
Write-Host "Starting automation in 3 seconds..." -ForegroundColor Cyan
Start-Sleep -Seconds 3
Write-Host ""
python ird_automation.py
Write-Host ""
Write-Host "Automation completed!" -ForegroundColor Green
Read-Host "Press Enter to exit"
