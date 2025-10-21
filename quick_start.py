"""
Quick Start Script for IRD Automation Project

This script provides an easy way to run the IRD automation project.
"""

import subprocess
import sys
import time
import os

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import playwright
        print("✓ Playwright is installed")
        return True
    except ImportError:
        print("✗ Playwright is not installed")
        print("Please run: pip install playwright")
        print("Then run: playwright install")
        return False

def check_files():
    """Check if required files exist."""
    required_files = [
        "browser_setup.py",
        "form_automation_new.py",
        "ui_components/__init__.py",
        "ui_components/base_component.py",
        "ui_components/main_return_component.py",
        "ui_components/schedule01_component.py",
        "ui_components/schedule02_component.py",
        "ui_components/component_manager.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("✗ Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✓ All required files exist")
        return True

def run_browser_setup():
    """Run browser setup."""
    print("\n🚀 Starting browser setup...")
    print("=" * 50)
    try:
        subprocess.run([sys.executable, "browser_setup.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"✗ Browser setup failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Browser setup interrupted by user")
        return False
    return True

def run_form_automation():
    """Run form automation."""
    print("\n🤖 Starting form automation...")
    print("=" * 50)
    try:
        subprocess.run([sys.executable, "form_automation_new.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"✗ Form automation failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Form automation interrupted by user")
        return False
    return True

def main():
    """Main function to run the automation."""
    print("IRD Automation Project - Quick Start")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check files
    if not check_files():
        return
    
    print("\n📋 Instructions:")
    print("1. Browser setup will start automatically")
    print("2. Complete CAPTCHA and login manually in the browser")
    print("3. Form automation will start automatically")
    print("4. Monitor console output for progress")
    print("\nPress Ctrl+C to stop at any time")
    
    input("\nPress Enter to start...")
    
    # Step 1: Browser Setup
    print("\n" + "=" * 50)
    print("STEP 1: BROWSER SETUP")
    print("=" * 50)
    print("This will:")
    print("- Open Chrome browser")
    print("- Navigate to IRD login page")
    print("- Fill your credentials automatically")
    print("- Wait for you to complete CAPTCHA")
    
    if not run_browser_setup():
        return
    
    # Step 2: Wait for user to complete login
    print("\n" + "=" * 50)
    print("STEP 2: MANUAL LOGIN")
    print("=" * 50)
    print("Please complete the following in the browser:")
    print("1. Fill CAPTCHA")
    print("2. Click Login button")
    print("3. Navigate to form page if needed")
    print("4. Keep browser open")
    
    input("\nPress Enter when login is complete...")
    
    # Step 3: Form Automation
    print("\n" + "=" * 50)
    print("STEP 3: FORM AUTOMATION")
    print("=" * 50)
    print("This will:")
    print("- Connect to existing browser")
    print("- Run Main Return component")
    print("- Run Schedule 1 component")
    print("- Run Schedule 2 component")
    print("- Save drafts automatically")
    
    if not run_form_automation():
        return
    
    print("\n🎉 Automation completed successfully!")
    print("Browser will remain open for manual review")
    print("Close browser window to logout automatically")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Quick start interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check the error and try again")
