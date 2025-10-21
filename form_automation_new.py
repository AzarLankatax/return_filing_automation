"""
Automation Script for IRD Form Filling

This script uses the new component-based architecture for IRD form automation.
It orchestrates all UI components to complete the form filling process.

Form URL: https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError
from ui_components import ComponentManager

# Constants
TARGET_URL = "https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling"
DEBUG_PORT = 9222


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


async def connect_to_existing_browser():
    """Connect to existing Chrome browser instance."""
    try:
        print("🔗 Connecting to existing Chrome browser...")
        playwright = await async_playwright().start()
        
        # Connect to existing browser via debug port
        browser = await playwright.chromium.connect_over_cdp(f"http://localhost:{DEBUG_PORT}")
        
        # Get the default context
        contexts = browser.contexts
        if not contexts:
            raise Exception("No browser contexts found. Make sure browser_setup.py is running.")
        
        context = contexts[0]
        print("✓ Connected to existing browser successfully")
        
        return playwright, browser, context
        
    except Exception as e:
        print(f"✗ Failed to connect to existing browser: {str(e)}")
        print("📝 Make sure browser_setup.py is running first!")
        raise


async def run_automation(page, context):
    """Run the form filling automation using component-based architecture."""
    try:
        print(f"🌐 Navigating to form page: {TARGET_URL}")
        await page.goto(TARGET_URL)
        
        # Wait for page to load
        await page.wait_for_load_state("networkidle")
        print("✅ Form page loaded successfully!")
        
        # Initialize component manager
        component_manager = ComponentManager(page, context)
        
        # Run complete automation
        results = await component_manager.run_complete_automation()
        
        # Check results
        if all(results.values()):
            print("🎉 All components completed successfully!")
        else:
            print("⚠️ Some components failed - check results above")
        
        return results
        
    except Exception as e:
        print(f"❌ Error during automation: {str(e)}")
        raise


async def main():
    """Main automation function."""
    playwright = None
    browser = None
    
    try:
        # Connect to existing browser
        playwright, browser, context = await connect_to_existing_browser()
        
        # Create new tab for automation
        print("📄 Opening new tab for automation...")
        page = await context.new_page()
        
        # Run the automation
        await run_automation(page, context)
        
        # Keep the browser open and set up logout on browser close
        print("\n⏳ Automation completed! Browser will stay open.")
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
                    await handle_browser_close()
                    break
                
                # Check if context is still open
                if context.pages == []:
                    print("🔓 All browser windows closed - logging out...")
                    await handle_browser_close()
                    break
                
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\n👋 Script terminated by user - attempting logout...")
            await logout_user(page)
        
    except Exception as e:
        print(f"\n❌ Error during automation: {str(e)}")
        raise
    finally:
        # Don't close browser - let user manage it
        pass


if __name__ == "__main__":
    print("🚀 Starting IRD Form Automation with Component Architecture...")
    print("📝 This script will:")
    print("   1. Connect to existing Chrome browser")
    print("   2. Navigate to form page")
    print("   3. Run Main Return component")
    print("   4. Run Schedule 1 component")
    print("   5. Run Schedule 2 component (in new tab)")
    print("   6. Keep browser open after completion")
    print("   7. Automatically logout when browser window is closed")
    print("-" * 60)
    
    asyncio.run(main())
