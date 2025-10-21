"""
Browser Setup Script for IRD Semi-Automatic Login

This script will:
1. Start Chrome browser with persistent context
2. Navigate to login page
3. Automatically fill TIN and PIN credentials
4. Wait for user to complete CAPTCHA and click login
5. Allow user to navigate to form page manually
6. Keep session active until browser window is closed
7. Automatically logout when browser window is closed

Login URL: https://eservices.ird.gov.lk/Authentication/LoginPersonal
Form URL: https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling
Credentials: TIN: 103136962, PIN: Yogar950
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

# Constants
LOGIN_URL = "https://eservices.ird.gov.lk/Authentication/LoginPersonal"
TARGET_URL = "https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling"
USER_DATA_DIR = "C:\\chrome-automation"


async def logout_user(page):
    """Logout the user by clicking the logout button."""
    try:
        print("🔓 Logging out user...")
        # Look for the logout link using the provided HTML structure
        logout_selector = 'a.r-login.r-link-login[href="/Authentication/Logout"]'
        await page.wait_for_selector(logout_selector, state="visible", timeout=10000)
        await page.click(logout_selector)
        print("✓ Successfully logged out")
        await page.wait_for_timeout(2000)  # Wait for logout to complete
    except PWTimeoutError:
        print("✗ Could not find logout button or logout failed")
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
                await page.fill("#MyTaxReferNo", "106298408")
                print("✓ Tax Reference Number filled: 106298408")
            except PWTimeoutError:
                print("✗ Timeout waiting for Tax Reference Number field")
                raise
            
            # Fill IRD PIN
            try:
                await page.wait_for_selector("#MyIRDPIN", state="visible", timeout=20000)
                await page.fill("#MyIRDPIN", "Judet568")
                print("✓ IRD PIN filled: Judet568")
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
            
            # Set up event listeners for browser window close detection
            async def handle_browser_close():
                """Handle browser close event by logging out."""
                try:
                    print("🔓 Browser window closed - attempting logout...")
                    await logout_user(page)
                except Exception as e:
                    print(f"✗ Error during logout on browser close: {str(e)}")
            
            # Add event listener for page close
            page.on("close", lambda: asyncio.create_task(handle_browser_close()))
            
            # Add event listener for browser context close
            context.on("close", lambda: asyncio.create_task(handle_browser_close()))
            
            try:
                while True:
                    # Check if page is still open
                    if page.is_closed():
                        print("🔓 Browser window was closed - logging out...")
                        await logout_user(page)
                        break
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 Script terminated by user - keeping session active")
            
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
    
    asyncio.run(main())
