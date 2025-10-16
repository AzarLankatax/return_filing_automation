To run the automation script, follow these steps:

## Prerequisites

1. **Install Playwright** (if not already installed):
   ```bash
   pip install playwright
   playwright install chromium
   ```

## Step-by-Step Instructions

### 1. Start Chrome with CDP Support
Open Command Prompt or PowerShell and run:
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome-cdp"
```

This will open Chrome with remote debugging enabled. You should see Chrome open normally.

### 2. Manual Login Setup
- In the Chrome window that opened, navigate to: `https://eservices.ird.gov.lk/Authentication/LoginPersonal`
- **Log in manually** with your credentials
- Make sure you're on the form page and ready to proceed

### 3. Run the Automation Script
Open a new Command Prompt/PowerShell window and navigate to your project directory:
```bash
cd "C:\Users\Dell\Desktop\Projects Azar"
python automation.py
```

## What Happens Next

The script will:
1. Connect to your existing Chrome session
2. Open a new tab in the same Chrome window
3. Navigate to the form URL
4. Automate the form filling process
5. Keep the tab open for your review

## Troubleshooting

- **If Chrome doesn't start with CDP**: Make sure no other Chrome instances are running, or use a different port/user-data-dir
- **If connection fails**: Ensure Chrome is running with the exact command above
- **If elements aren't found**: The page might not be fully loaded - the script includes waiting mechanisms

The automation will run automatically once you execute `python automation.py` and will provide detailed logging of each step!