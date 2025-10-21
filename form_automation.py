"""
Automation Script for IRD Form Filling

This script will:
1. Connect to existing Chrome browser (must be running from browser_setup.py)
2. Open new tab and navigate to form URL
3. Automatically fill the IRD form
4. Keep browser open after completion
5. Only logout when browser window is manually closed

Form URL: https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

# Constants
TARGET_URL = "https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling"
DEBUG_PORT = 9222


async def click_popup_button_by_value(page, button_value):
    """Helper function to click popup buttons by their value."""
    try:
        button_selector = f'input[type="button"][value="{button_value}"].r-btn-pop'
        await page.wait_for_selector(button_selector, state="visible", timeout=10000)
        await page.click(button_selector)
        print(f"✓ Clicked popup button: {button_value}")
        # Wait a moment for popup to close
        await page.wait_for_timeout(1000)
    except PWTimeoutError:
        print(f"✗ Timeout waiting for popup button: {button_value}")
        raise


async def fill_numeric_input(page, selector, value):
    """Helper function to fill numeric Kendo input fields."""
    try:
        element = await page.wait_for_selector(selector, state="visible", timeout=10000)
        await element.focus()
        await page.keyboard.press("Control+a")  # Select all existing text
        await page.keyboard.type(str(value))
        print(f"✓ Filled numeric input {selector} with value: {value}")
    except PWTimeoutError:
        print(f"✗ Timeout waiting for numeric input: {selector}")
        raise


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


async def run_automation(page):
    """Run the form filling automation."""
    try:
        print(f"🌐 Navigating to form page: {TARGET_URL}")
        await page.goto(TARGET_URL)
        
        # Wait for page to load
        await page.wait_for_load_state("networkidle")
        print("✅ Form page loaded successfully!")
        
        # Step 1: Set radio buttons
        print("\n📋 Step 1: Setting radio buttons...")
        
        # Select Resident
        try:
            await page.wait_for_selector("#Resident_Resident", state="visible", timeout=20000)
            await page.check("#Resident_Resident")
            print("✓ Selected Resident: Resident")
        except PWTimeoutError:
            print("✗ Timeout waiting for Resident radio button")
            raise
        
        # Select Senior citizen = No
        try:
            await page.wait_for_selector("#IsSeniorCitizen", state="visible", timeout=20000)
            await page.check("#IsSeniorCitizen")
            print("✓ Selected Senior citizen: No")
        except PWTimeoutError:
            print("✗ Timeout waiting for Senior citizen radio button")
            raise
        
        # Step 2: Scroll to bottom and click Next
        print("\n📋 Step 2: Clicking Next button...")
        try:
            await page.wait_for_selector("#btnNext", state="visible", timeout=20000)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)  # Wait for scroll
            await page.click("#btnNext")
            print("✓ Clicked Next button")
        except PWTimeoutError:
            print("✗ Timeout waiting for Next button")
            raise
        
        # Step 3: Handle confirmation popup
        print("\n📋 Step 3: Handling confirmation popup...")
        await click_popup_button_by_value(page, "Yes")
        
        # Step 4: Handle info popup
        print("\n📋 Step 4: Handling info popup...")
        try:
            await click_popup_button_by_value(page, "Ok")
        except PWTimeoutError:
            # Try alternative spelling
            try:
                await click_popup_button_by_value(page, "OK")
            except PWTimeoutError:
                print("✗ Could not find Ok/OK popup button")
                raise
        
        # Wait for Schedule 1 to load
        await page.wait_for_load_state("networkidle")
        print("✓ Schedule 1 component loaded")
        
        # Step 5: Fill Schedule 1 form
        print("\n📋 Step 5: Filling Schedule 1 form...")

        # Part 1: Details of Employment income (S1)
        print("\n📋 Part 1: Details of Employment income (S1)...")
        
        # Employer/company name	
        try:
            await page.wait_for_selector('input[name="Schedule1AModel.Sch1_Cage102"]', state="visible", timeout=20000)
            await page.fill('input[name="Schedule1AModel.Sch1_Cage102"]', "Mahesh")
            print("✓ Employer/company name field: Mahesh")
        except PWTimeoutError:
            print("✗ Timeout waiting for Employer/company name field")
            raise
        
        # TIN of the employer	
        try:
            await page.wait_for_selector('input[name="Schedule1AModel.Sch1_2021Cage103"]', state="visible", timeout=20000)
            await page.fill('input[name="Schedule1AModel.Sch1_2021Cage103"]', "103136962")
            print("✓ TIN of the employer ID field: 103136962")
        except PWTimeoutError:
            print("✗ Timeout waiting for TIN of the employer ID field")
            raise
        
        # Remuneration (Rs.) field (Cage 104)
        try:
            # Wait for the Kendo widget that contains cage="104"
            container = await page.wait_for_selector('span.k-numerictextbox:has(input[cage="104"])', timeout=20000)

            # Find the visible input *inside that same widget*
            remuneration_field = await container.query_selector('input.k-formatted-value')

            # Focus, clear, and type
            await remuneration_field.click()
            await remuneration_field.press("Control+A")
            await remuneration_field.press("Backspace")
            await remuneration_field.type("50000", delay=100)
            await remuneration_field.press("Tab")

            print("✓ Remuneration (Rs.) field (Cage 104) filled successfully: 50000")

        except Exception as e:
            print(f"✗ Failed to fill Remuneration (Rs.) field: {e}")
            raise

        # click Add button (S1 Add A)
        try:
            await page.wait_for_selector('#btnS1AddA_2', state="visible", timeout=20000)
            await page.click('#btnS1AddA_2')
            print("✓ Clicked Add button")
        except PWTimeoutError:
            print("✗ Timeout waiting for Add button")
            raise

        # Part 2: Employment Income (S1)
        print("\n📋 Part 2: Employment Income (S1)...")

        # TIN of the employer	
        try:
            await page.wait_for_selector('input[name="Schedule1CModel.Sch1_2021Cage113"]', state="visible", timeout=20000)
            await page.fill('input[name="Schedule1CModel.Sch1_2021Cage113"]', "103136962")
            print("✓ TIN of the employer ID field: 103136962")
        except PWTimeoutError:
            print("✗ Timeout waiting for TIN of the employer ID field")
            raise
        
        # Amount (Rs.) field (Cage 114) - Kendo UI Numeric Textbox
        try:
            # Wait for the Kendo widget that contains cage="114"
            container = await page.wait_for_selector('span.k-numerictextbox:has(input[cage="114"])', timeout=20000)

            # Find the visible input *inside that same widget*
            amount_field = await container.query_selector('input.k-formatted-value')

            # Focus, clear, and type
            await amount_field.click()
            await amount_field.press("Control+A")
            await amount_field.press("Backspace")
            await amount_field.type("50000", delay=100)
            await amount_field.press("Tab")

            print("✓ Amount (Rs.) field (Cage 114) filled successfully: 50000")

        except Exception as e:
            print(f"✗ Failed to fill Amount (Rs.) field: {e}")
            # Try alternative approach
            try:
                print("🔄 Trying alternative approach for Amount field...")
                # Try direct input with cage attribute
                await page.wait_for_selector('input[cage="114"]', state="visible", timeout=10000)
                await page.fill('input[cage="114"]', "50000")
                print("✓ Amount (Rs.) field filled using alternative method: 50000")
            except Exception as e2:
                print(f"✗ Alternative approach also failed: {e2}")
                raise

        # Click Add button
        try:
            # Use the specific button ID provided
            await page.wait_for_selector('#btnS1AddC_2', state="visible", timeout=20000)
            await page.click('#btnS1AddC_2')
            print("✓ Clicked Add button (btnS1AddC_2)")
        except PWTimeoutError:
            print("✗ Timeout waiting for Add button (btnS1AddC_2)")
            # Try fallback selectors
            try:
                print("🔄 Trying fallback selectors...")
                fallback_selectors = [
                    'input[type="button"][value="Add"]',
                    'button:has-text("Add")',
                    'input[id*="Add"]'
                ]
                
                add_button_clicked = False
                for selector in fallback_selectors:
                    try:
                        await page.wait_for_selector(selector, state="visible", timeout=5000)
                        await page.click(selector)
                        print(f"✓ Clicked Add button using fallback selector: {selector}")
                        add_button_clicked = True
                        break
                    except PWTimeoutError:
                        continue
                
                if not add_button_clicked:
                    print("⚠ Could not find Add button with any selector - may need manual click")
                    
            except Exception as e:
                print(f"⚠ Error with fallback selectors: {e}")
                print("📝 Please click Add button manually if needed")
        except Exception as e:
            print(f"⚠ Error clicking Add button: {e}")
            print("📝 Please click Add button manually if needed")

        # Step 6: Click Next button (inside Schedule01Container)
        print("\n📋 Step 6: Clicking Next button...")
        try:
            # First, ensure we're in the Schedule01Container context
            print("🔍 Looking for Schedule01Container...")
            await page.wait_for_selector("#Schedule01Container", state="visible", timeout=20000)
            print("✓ Found Schedule01Container")
            
            # Wait for Next button within the container
            await page.wait_for_selector("#Schedule01Container #btnNext", state="visible", timeout=20000)
            print("✓ Found Next button within Schedule01Container")
            
            # Scroll to bottom to ensure button is visible
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)  # Wait for scroll
            
            # Try JavaScript execution approach for container-specific button
            print("🔄 Trying JavaScript execution for Next button in container...")
            result = await page.evaluate("""
                () => {
                    // Find the Schedule01Container first
                    const container = document.getElementById('Schedule01Container');
                    if (!container) {
                        console.log('Schedule01Container not found');
                        return 'container_not_found';
                    }
                    
                    // Look for Next button within the container
                    const btnNext = container.querySelector('#btnNext');
                    if (btnNext && btnNext.offsetParent !== null) {
                        console.log('Found btnNext within Schedule01Container');
                        btnNext.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        setTimeout(() => btnNext.click(), 500);
                        return 'clicked_by_id';
                    }
                    
                    // Try by value within container
                    const nextByValue = container.querySelector('input[type="button"][value="Next"]');
                    if (nextByValue && nextByValue.offsetParent !== null) {
                        console.log('Found Next button by value within container');
                        nextByValue.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        setTimeout(() => nextByValue.click(), 500);
                        return 'clicked_by_value';
                    }
                    
                    return 'not_found';
                }
            """)
            
            if result == 'container_not_found':
                print("✗ Schedule01Container not found")
                raise Exception("Schedule01Container not found")
            elif result != 'not_found':
                print(f"✓ Clicked Next button using JavaScript: {result}")
                await page.wait_for_timeout(3000)  # Wait for page to respond
            else:
                print("⚠ JavaScript approach didn't find Next button in container")
                # Fallback to direct click
                await page.click("#Schedule01Container #btnNext")
                print("✓ Clicked Next button using direct selector")
                await page.wait_for_timeout(2000)
                
        except Exception as js_error:
            print(f"⚠ JavaScript approach failed: {js_error}")
            
            # Fallback to Playwright approach
            print("🔄 Trying Playwright approach for Next button in container...")
            try:
                # Try clicking the button within the container
                await page.click("#Schedule01Container #btnNext")
                print("✓ Clicked Next button using Playwright container selector")
                await page.wait_for_timeout(2000)
                
            except Exception as pw_error:
                print(f"⚠ Playwright container approach failed: {pw_error}")
                
                # Last resort: try without container specificity
                try:
                    await page.click("#btnNext")
                    print("✓ Clicked Next button using fallback selector")
                    await page.wait_for_timeout(2000)
                except Exception as fallback_error:
                    print(f"✗ All approaches failed: {fallback_error}")
                    print("📝 Please click Next button manually")
        
        # Step 3: Handle confirmation popup
        print("\n📋 Step 3: Handling confirmation popup...")
        await click_popup_button_by_value(page, "Yes")
        
        # Step 4: Handle info popup
        print("\n📋 Step 4: Handling info popup...")
        try:
            await click_popup_button_by_value(page, "Ok")
        except PWTimeoutError:
            # Try alternative spelling
            try:
                await click_popup_button_by_value(page, "OK")
            except PWTimeoutError:
                print("✗ Could not find Ok/OK popup button")
                raise
        
        
        # Wait for Schedule 1 to load
        await page.wait_for_load_state("networkidle")
        print("✓ Schedule 1 component loaded")
        
        # Fill Schedule 2 form
        print("\n📋 Filling Schedule 2 form...")

        print("✅ Automation completed successfully!")
        
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
        await run_automation(page)
        
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
                    await logout_user(page)
                    break
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Script terminated by user - keeping session active")
        
    except Exception as e:
        print(f"\n❌ Error during automation: {str(e)}")
        print("📄 Browser remains open for debugging.")
        raise
    finally:
        # Don't close browser - let user manage it
        if playwright:
            await playwright.stop()


if __name__ == "__main__":
    print("🚀 Starting IRD Form Automation...")
    print("📝 This script will:")
    print("   1. Connect to existing Chrome browser")
    print("   2. Open new tab and navigate to form page")
    print("   3. Automatically fill the IRD form")
    print("   4. Keep browser open after completion")
    print("   5. Automatically logout when browser window is closed")
    print("📝 Make sure browser_setup.py is running first!")
    print("-" * 60)
    
    asyncio.run(main())
