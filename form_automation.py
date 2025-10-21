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



from playwright.async_api import TimeoutError as PWTimeoutError

# ---------- helpers ----------
async def click_topmost_dialog_button(page, label: str, timeout=12000) -> None:
    """
    Clicks a button (e.g., 'Yes', 'Ok') inside the topmost visible Kendo dialog.
    """
    # If site ever uses native confirm(), accept it
    page.once("dialog", lambda d: d.accept())

    dlg = page.locator(".k-window:visible, .k-animation-container:has(.k-window:visible), div[role='dialog']:visible").last
    await dlg.wait_for(state="visible", timeout=timeout)

    # Try common button patterns
    btn = dlg.locator(
        f"input[type='button'][value='{label}'].r-btn-pop, "
        f"input[type='button'][value='{label}'], "
        f"button:has-text('{label}'), "
        f"[role='button']:has-text('{label}')"
    ).last

    await btn.scroll_into_view_if_needed()
    await btn.click()

async def save_draft_schedule01(page) -> None:
    """
    In Schedule 01: click 'Save draft' → confirm 'Yes' → Info 'Ok'.
    """
    # Scope to Schedule 01 container so we never hit other pages’ buttons
    container = page.locator("#Schedule01Container")
    await container.wait_for(state="visible", timeout=20000)

    # Click the Save draft button inside Schedule 01
    save_btn = container.locator(
        "input[type='button'][value='Save draft'], button:has-text('Save draft')"
    ).first
    await save_btn.scroll_into_view_if_needed()
    await save_btn.click()
    print("✓ Clicked 'Save draft' (Schedule 01)")

    # Confirmation: "Do you want to save the changes?" → Yes
    try:
        await click_topmost_dialog_button(page, "Yes", timeout=12000)
        print("✓ Confirmed 'Yes' on save dialog")
    except PWTimeoutError:
        print("⏳ No confirmation dialog appeared; continuing...")

    # The server may take a moment before showing the Info dialog
    # Wait for Info dialog with 'Ok' and click it
    try:
        # Wait up to ~10s for the info modal to render
        info_dlg = page.locator(
            ".k-window:has-text('Info'), div[role='dialog']:has-text('Info'), .k-window:has(input[value='Ok'], button:has-text('Ok'))"
        ).last
        await info_dlg.wait_for(state="visible", timeout=10000)

        await click_topmost_dialog_button(page, "Ok", timeout=5000)
        print("✓ Acknowledged 'Ok' on info dialog (draft saved)")
    except PWTimeoutError:
        # Some environments show 'OK' uppercase—try it once
        try:
            await click_topmost_dialog_button(page, "OK", timeout=3000)
            print("✓ Acknowledged 'OK' on info dialog (draft saved)")
        except PWTimeoutError:
            print("⚠ Info dialog with Ok/OK not found; verify draft state manually")



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

        
        print("\n📋 Saving draft for Schedule 01...")
        await save_draft_schedule01(page)
        print("✓ Draft saved for Schedule 01")



        
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
