# How to Run the IRD Automation Project

This guide will walk you through running the IRD automation project step by step.

## 📋 Prerequisites

### **1. Python Installation**
- Python 3.7 or higher installed
- pip package manager available

### **2. Install Dependencies**
```bash
pip install playwright
playwright install
```

### **3. Project Files**
Make sure you have these files in your project directory:
- `browser_setup.py` - Browser setup and login
- `form_automation_new.py` - New component-based automation
- `ui_components/` folder with all component files

## 🚀 Running the Project

### **Method 1: Complete Automation (Recommended)**

#### **Step 1: Start Browser Setup**
Open **Terminal/Command Prompt** and run:
```bash
python browser_setup.py
```

**What happens:**
- Chrome browser opens automatically
- Navigates to IRD login page
- Fills your TIN and PIN credentials
- Waits for you to complete CAPTCHA manually
- Keeps browser open for automation

#### **Step 2: Complete Login Manually**
1. **Fill CAPTCHA** in the browser window
2. **Click Login** button
3. **Navigate to form page** if needed
4. **Keep browser open** - don't close it

#### **Step 3: Run Form Automation**
Open **another Terminal/Command Prompt** and run:
```bash
python form_automation_new.py
```

**What happens:**
- Connects to existing browser
- Runs Main Return component
- Runs Schedule 1 component
- Runs Schedule 2 component (in new tab)
- Automatically logs out when browser closes

### **Method 2: Individual Components**

#### **Run Only Main Return:**
```python
from ui_components import ComponentManager
from playwright.async_api import async_playwright

async def run_main_return_only():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    page = await context.new_page()
    
    component_manager = ComponentManager(page, context)
    await component_manager.run_main_return_only()

# Run it
import asyncio
asyncio.run(run_main_return_only())
```

#### **Run Only Schedule 1:**
```python
from ui_components import ComponentManager
# ... (similar setup as above)

component_manager = ComponentManager(page, context)
await component_manager.run_schedule01_only()
```

#### **Run Only Schedule 2:**
```python
from ui_components import ComponentManager
# ... (similar setup as above)

component_manager = ComponentManager(page, context)
await component_manager.run_schedule02_only()
```

## 🔧 Configuration

### **Update Your Credentials**
Edit `browser_setup.py` and change these lines:
```python
TAX_REFERENCE_NUMBER = "YOUR_TAX_REFERENCE_NUMBER"  # Change this
IRD_PIN = "YOUR_IRD_PIN"                            # Change this
```

### **Update Form Data**
Edit the component files to customize form data:

**Schedule 1 Data** (`ui_components/schedule01_component.py`):
```python
self.form_data = {
    "101": "Your business description",  # Nature of business
    "102": 200000,                       # Gains and profits
    "103": 3000000,                      # Total business turnover
    "104": 50000,                        # Other income
    "105": 10000                         # Deductions
}
```

**Schedule 2 Data** (`ui_components/schedule02_component.py`):
```python
self.form_data = {
    "201": "Your activity code",         # Activity code
    "202": "Your business nature",       # Nature of business
    "203": 250000,                       # Gains and profits
    "204A": 4000000                      # Total business turnover
}
```

## 📊 Expected Output

### **Browser Setup Output:**
```
Starting IRD Browser Setup...
This script will:
   1. Start Chrome browser automatically
   2. Navigate to login page
   3. Automatically fill TIN and PIN credentials
   4. Wait for you to complete CAPTCHA and login
   5. Allow you to navigate to form page manually
   6. Keep browser open for automation
   7. Automatically logout when browser window is closed
------------------------------------------------------------
Using Tax Reference Number: YOUR_NUMBER
Using IRD PIN: YOUR_PIN
To change these values, edit the variables at the top of this file
------------------------------------------------------------
Starting Chrome browser for manual login...
Opening new tab...
Navigating to login page: https://eservices.ird.gov.lk/Authentication/LoginPersonal
Login page loaded successfully
Filling login credentials automatically...
Tax Reference Number filled: YOUR_NUMBER
IRD PIN filled: YOUR_PIN
CAPTCHA REQUIRED
==================================================
Login credentials have been filled automatically
Please fill in the CAPTCHA manually
After filling CAPTCHA, click the login button
After logging in, navigate to the form page
The browser will stay open for automation
==================================================
Browser is ready for manual login and navigation...
The system will automatically logout when you close the browser window.
```

### **Form Automation Output:**
```
Starting IRD Form Automation with Component Architecture...
This script will:
   1. Connect to existing Chrome browser
   2. Navigate to form page
   3. Run Main Return component
   4. Run Schedule 1 component
   5. Run Schedule 2 component (in new tab)
   6. Keep browser open after completion
   7. Automatically logout when browser window is closed
------------------------------------------------------------
Connecting to existing Chrome browser...
Connected to existing browser successfully
Opening new tab for automation...
Navigating to form page: https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling
Form page loaded successfully!
Starting complete IRD form automation...
============================================================

Step 1: Main Return Component
----------------------------------------
[Main Return] Starting main return setup...
[Main Return] Selected Resident: Resident
[Main Return] Selected Senior citizen: No
[Main Return] Navigated to Schedule 1
[Main Return] Schedule 1 component loaded
[Main Return] Main return setup completed successfully

Step 2: Schedule 1 Component
----------------------------------------
[Schedule 1] Starting Schedule 1 setup...
[Schedule 1] Schedule 1 container is visible
[Schedule 1] Filling Schedule 1 form fields...
[Schedule 1] Field 101 filled successfully
[Schedule 1] Field 102 filled successfully
[Schedule 1] Field 103 filled successfully
[Schedule 1] Field 104 filled successfully
[Schedule 1] Field 105 filled successfully
[Schedule 1] Schedule 1 form fields filled successfully
[Schedule 1] Clicking Add button...
[Schedule 1] Add button clicked successfully
[Schedule 1] Saving draft for Schedule 1...
[Schedule 1] Draft saved for Schedule 1
[Schedule 1] Schedule 1 setup completed successfully

Step 3: Schedule 2 Component
----------------------------------------
[Schedule 2] Starting Schedule 2 automation in new tab...
[Schedule 2] Form page loaded successfully
[Schedule 2] Looking for Schedule 2 tab...
[Schedule 2] Successfully clicked Schedule 2 tab
[Schedule 2] Schedule 2 container is visible
[Schedule 2] Filling Schedule 2 form fields...
[Schedule 2] Field 201 filled successfully
[Schedule 2] Field 202 filled successfully
[Schedule 2] Field 203 filled successfully
[Schedule 2] Field 204A filled successfully
[Schedule 2] Schedule 2 form fields filled successfully
[Schedule 2] Saving draft for Schedule 2...
[Schedule 2] Draft saved for Schedule 2
[Schedule 2] Schedule 2 tab closed
[Schedule 2] Schedule 2 automation completed successfully!

============================================================
AUTOMATION SUMMARY
============================================================
Main Return: SUCCESS
Schedule 1: SUCCESS
Schedule 2: SUCCESS

Complete automation completed successfully!
Automation completed! Browser will stay open.
The system will automatically logout when you close the browser window.
```

## 🛠️ Troubleshooting

### **Common Issues:**

#### **1. Browser Connection Failed**
```
Failed to connect to existing browser: [error]
Make sure browser_setup.py is running first!
```
**Solution:** Run `browser_setup.py` first, then `form_automation_new.py`

#### **2. Login Form Not Found**
```
Timeout waiting for Tax Reference Number field
```
**Solution:** Check if the page has loaded completely, refresh if needed

#### **3. Schedule 2 Tab Not Found**
```
Could not find Schedule 2 tab automatically
Please manually click on Schedule 2 tab
```
**Solution:** Click on Schedule 2 tab manually in the browser

#### **4. Form Fields Not Found**
```
Timeout waiting for element: [selector]
```
**Solution:** Check if the form has loaded, refresh if needed

### **Debug Mode:**
Set `HEADLESS_MODE = False` in `browser_setup.py` to see browser actions:
```python
HEADLESS_MODE = False  # Set to True to run browser in headless mode
```

## 📝 Manual Steps Required

### **Always Required:**
1. **CAPTCHA**: Fill CAPTCHA manually in browser
2. **Login**: Click login button after CAPTCHA
3. **Navigation**: Navigate to form page if needed

### **Sometimes Required:**
1. **Schedule 2 Tab**: Click Schedule 2 tab if automatic detection fails
2. **Form Fields**: Fill fields manually if automation fails
3. **Save Draft**: Click save buttons if automation fails

## 🔄 Workflow Summary

1. **Start**: `python browser_setup.py`
2. **Login**: Complete CAPTCHA and login manually
3. **Automate**: `python form_automation_new.py`
4. **Monitor**: Watch console output for progress
5. **Complete**: Automation finishes automatically
6. **Cleanup**: Browser logs out when closed

## 📞 Support

If you encounter issues:
1. Check console output for error messages
2. Verify all files are in the correct location
3. Ensure Python and Playwright are installed
4. Try running components individually
5. Check browser console for JavaScript errors

---

**Note**: This automation handles most of the form filling automatically, but some manual steps (like CAPTCHA) are always required due to security measures.
