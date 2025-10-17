"""
Playwright automation script for IRD form filling.

This script will:
1. Start Chrome automatically
2. Navigate to login page for manual login
3. Wait for you to log in manually
4. Automatically proceed to form URL and complete automation

Login URL: https://eservices.ird.gov.lk/Authentication/LoginPersonal
Form URL: https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

# Constants
LOGIN_URL = "https://eservices.ird.gov.lk/Authentication/LoginPersonal"
TARGET_URL = "https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling"
USER_DATA_DIR = "C:\\chrome-automation"


async def wait_for_manual_login(page):
    """Wait for user to manually log in and navigate to the target page."""
    print("\n🔐 MANUAL LOGIN REQUIRED")
    print("=" * 50)
    print("📝 Please log in manually in the browser window")
    print("📝 After logging in, navigate to the form page")
    print("📝 The automation will continue automatically once you reach the form")
    print("=" * 50)
    
    # Wait for user to navigate to the target URL
    print("⏳ Waiting for you to navigate to the form page...")
    
    while True:
        current_url = page.url
        if TARGET_URL in current_url:
            print("✅ Detected navigation to form page!")
            break
        
        # Check if still on login page or other pages
        if "LoginPersonal" in current_url:
            print("⏳ Still on login page... please log in")
        else:
            print(f"📍 Current page: {current_url}")
            print("⏳ Please navigate to the form page...")
        
        await asyncio.sleep(2)  # Check every 2 seconds
    
    # Wait a bit more for page to fully load
    await page.wait_for_load_state("networkidle")
    print("✅ Form page loaded successfully!")


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


async def main():
    """Main automation function."""
    async with async_playwright() as p:
        try:
            print("🚀 Starting Chrome browser...")
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
            
            # Wait for manual login and navigation to form page
            await wait_for_manual_login(page)
            
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


            # Keep the tab open - don't close browser
            print("⏳ Keeping tab open... Press Ctrl+C to exit this script.")
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 Script terminated by user")
            
        except Exception as e:
            print(f"\n❌ Error during automation: {str(e)}")
            print("📄 Tab remains open for debugging.")
            raise
        finally:
            # Don't close browser - let user manage it
            pass


if __name__ == "__main__":
    print("🚀 Starting IRD form automation...")
    print("📝 This script will:")
    print("   1. Start Chrome automatically")
    print("   2. Navigate to login page")
    print("   3. Wait for you to log in manually")
    print("   4. Automatically proceed to form and complete automation")
    print("-" * 60)
    
    asyncio.run(main())
