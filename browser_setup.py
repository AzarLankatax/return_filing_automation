"""
Browser Setup Script for IRD Semi-Automatic Login

This script will:
1. Start Chrome browser with persistent context
2. Navigate to login page
3. Automatically fill TIN and PIN credentials (configurable)
4. Wait for user to complete CAPTCHA and click login
5. Allow user to navigate to form page manually
6. Keep session active until browser window is closed
7. Automatically logout when browser window is closed

Login URL: https://eservices.ird.gov.lk/Authentication/LoginPersonal
Form URL: https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling

CONFIGURATION:
- Change TAX_REFERENCE_NUMBER and IRD_PIN variables at the top of the file
- These values will be automatically filled in the login form
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

# Constants
LOGIN_URL = "https://eservices.ird.gov.lk/Authentication/LoginPersonal"
TARGET_URL = "https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling"
USER_DATA_DIR = "C:\\chrome-automation"

# =============================================================================
# USER CREDENTIALS - CHANGE THESE VALUES AS NEEDED
# =============================================================================
TAX_REFERENCE_NUMBER = "106298408"  # Change this to your Tax Reference Number
IRD_PIN = "Judet568"                # Change this to your IRD PIN
# =============================================================================


async def cleanup_and_logout(context, page=None):
    """Cleanup function to ensure proper logout and cleanup."""
    try:
        print("🧹 Starting cleanup process...")
        logout_successful = False
        
        # Try to logout if we have a valid page
        if page and not page.is_closed():
            print("🔓 Attempting logout from main page...")
            await logout_user(page)
            logout_successful = True
        
        # Try to logout using any remaining pages in the context
        if context and not context.is_closed():
            pages = context.pages
            for remaining_page in pages:
                if not remaining_page.is_closed():
                    try:
                        print("🔓 Attempting logout from remaining page...")
                        await logout_user(remaining_page)
                        logout_successful = True
                    except Exception as e:
                        print(f"✗ Error logging out from remaining page: {str(e)}")
        
        # If no pages available, try to create a new page for logout
        if not logout_successful and context and not context.is_closed():
            try:
                print("🔓 Creating new page for logout...")
                new_page = await context.new_page()
                await new_page.goto(LOGIN_URL)
                await logout_user(new_page)
                await new_page.close()
                logout_successful = True
            except Exception as e:
                print(f"✗ Error creating new page for logout: {str(e)}")
        
        if logout_successful:
            print("✅ Logout completed successfully")
        else:
            print("⚠️ Could not complete logout - session may still be active")
        
        print("✓ Cleanup process completed")
        
    except Exception as e:
        print(f"✗ Error during cleanup: {str(e)}")
        print("⚠️ Script terminating without proper logout")


async def logout_user(page):
    """Logout the user by clicking the logout button."""
    try:
        print("🔓 Logging out user...")
        
        # Try multiple logout selectors in case the page structure changes
        logout_selectors = [
            'a.r-login.r-link-login[href="/Authentication/Logout"]',
            'a[href="/Authentication/Logout"]',
            'a:has-text("Logout")',
            'a:has-text("Sign Out")',
            'button:has-text("Logout")',
            'button:has-text("Sign Out")'
        ]
        
        logout_successful = False
        
        for selector in logout_selectors:
            try:
                # Check if the logout element exists
                element = await page.query_selector(selector)
                if element:
                    await element.click()
                    print("✓ Successfully clicked logout button")
                    logout_successful = True
                    break
            except Exception as e:
                print(f"✗ Failed to click logout with selector '{selector}': {str(e)}")
                continue
        
        if not logout_successful:
            # Try to navigate to logout URL directly
            try:
                print("📝 Attempting direct logout URL...")
                await page.goto("https://eservices.ird.gov.lk/Authentication/Logout")
                print("✓ Successfully navigated to logout URL")
                logout_successful = True
            except Exception as e:
                print(f"✗ Failed to navigate to logout URL: {str(e)}")
        
        if logout_successful:
            print("✓ Successfully logged out")
            await page.wait_for_timeout(2000)  # Wait for logout to complete
        else:
            print("✗ Could not find logout button or logout failed")
            
    except PWTimeoutError:
        print("✗ Timeout waiting for logout elements")
    except Exception as e:
        print(f"✗ Error during logout: {str(e)}")


async def main():
    """Main browser setup function."""
    async with async_playwright() as p:
        try:
            print("🚀 Starting Chrome browser for manual login...")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=False,  # Show browser window
                args=[
                    "--remote-debugging-port=9222",
                    "--disable-web-security",
                    "--disable-features=VizDisplayCompositor",
                    "--no-first-run",
                    "--disable-default-apps"
                ]
            )
            
            print("📄 Opening new tab...")
            page = await context.new_page()
            
            print(f"🌐 Navigating to login page: {LOGIN_URL}")
            await page.goto(LOGIN_URL)
            
            # Wait for login page to load
            await page.wait_for_load_state("networkidle")
            print("✅ Login page loaded successfully")
            
            # Automatic login credentials filling
            print("\n🔐 Filling login credentials automatically...")
            
            # Fill Tax Reference Number
            try:
                await page.wait_for_selector("#MyTaxReferNo", state="visible", timeout=20000)
                await page.fill("#MyTaxReferNo", TAX_REFERENCE_NUMBER)
                print(f"✓ Tax Reference Number filled: {TAX_REFERENCE_NUMBER}")
            except PWTimeoutError:
                print("✗ Timeout waiting for Tax Reference Number field")
                raise
            
            # Fill IRD PIN
            try:
                await page.wait_for_selector("#MyIRDPIN", state="visible", timeout=20000)
                await page.fill("#MyIRDPIN", IRD_PIN)
                print(f"✓ IRD PIN filled: {IRD_PIN}")
            except PWTimeoutError:
                print("✗ Timeout waiting for IRD PIN field")
                raise
            
            print("\n🔐 CAPTCHA REQUIRED")
            print("=" * 50)
            print("📝 Login credentials have been filled automatically")
            print("📝 Please fill in the CAPTCHA manually")
            print("📝 After filling CAPTCHA, click the login button")
            print("📝 After logging in, navigate to the form page:")
            print(f"📝 {TARGET_URL}")
            print("📝 The browser will stay open for automation")
            print("=" * 50)
            
            # Set up logout functionality for browser window close
            print("⏳ Browser is ready for manual login and navigation...")
            print("📝 The system will automatically logout when you close the browser window.")
            
            # Flag to track if logout has been attempted
            logout_attempted = False
            logout_completed = False
            
            async def handle_browser_close():
                """Handle browser close event by logging out."""
                nonlocal logout_attempted, logout_completed
                if not logout_attempted:
                    logout_attempted = True
                    try:
                        print("🔓 Browser window closed - attempting logout...")
                        await cleanup_and_logout(context, page)
                        logout_completed = True
                        print("✅ Logout process completed - script will now terminate")
                    except Exception as e:
                        print(f"✗ Error during logout on browser close: {str(e)}")
                        print("⚠️ Script terminating without proper logout")
                        logout_completed = True
            
            # Set up event listeners for browser window close detection
            def on_page_close():
                """Handle page close event."""
                asyncio.create_task(handle_browser_close())
            
            def on_context_close():
                """Handle context close event."""
                asyncio.create_task(handle_browser_close())
            
            # Add event listeners
            page.on("close", on_page_close)
            context.on("close", on_context_close)
            
            try:
                # Monitor browser state and handle close events
                while not logout_completed:
                    # Check if page is still open
                    if page.is_closed():
                        print("🔓 Browser window was closed - logging out...")
                        await handle_browser_close()
                        break
                    
                    # Check if context is still open
                    if context.pages == []:
                        print("🔓 All browser windows closed - logging out...")
                        await handle_browser_close()
                        break
                    
                    await asyncio.sleep(1)
                
                # Wait a moment to ensure logout process is complete
                if logout_completed:
                    print("⏳ Waiting for logout to complete...")
                    await asyncio.sleep(3)
                    print("🏁 Script terminated after successful logout")
                    
            except KeyboardInterrupt:
                print("\n👋 Script terminated by user - attempting logout...")
                await cleanup_and_logout(context, page)
                print("⏳ Waiting for logout to complete...")
                await asyncio.sleep(3)
                print("🏁 Script terminated after logout attempt")
            
        except Exception as e:
            print(f"\n❌ Error during browser setup: {str(e)}")
            print("📄 Browser remains open for debugging.")
            raise
        finally:
            # Don't close browser - let user manage it
            pass


if __name__ == "__main__":
    print("🚀 Starting IRD Browser Setup...")
    print("📝 This script will:")
    print("   1. Start Chrome browser automatically")
    print("   2. Navigate to login page")
    print("   3. Automatically fill TIN and PIN credentials")
    print("   4. Wait for you to complete CAPTCHA and login")
    print("   5. Allow you to navigate to form page manually")
    print("   6. Keep browser open for automation")
    print("   7. Automatically logout when browser window is closed")
    print("-" * 60)
    print(f"🔐 Using Tax Reference Number: {TAX_REFERENCE_NUMBER}")
    print(f"🔐 Using IRD PIN: {IRD_PIN}")
    print("💡 To change these values, edit the variables at the top of this file")
    print("-" * 60)
    
    asyncio.run(main())
