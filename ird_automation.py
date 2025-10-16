import asyncio
from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

CDP_ENDPOINT = "http://localhost:9222"  # Chrome started with --remote-debugging-port=9222
TARGET_URL = "https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling"

async def run():
    async with async_playwright() as p:
        # Attach to the *existing* Chrome you started with the debugging port
        browser = await p.chromium.connect_over_cdp(CDP_ENDPOINT)

        # Use the default context (actual Chrome profile). Open a **new tab**.
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()

        # Go to the page (same session cookies are reused)
        await page.goto(TARGET_URL, wait_until="domcontentloaded")

        # --- Main Return: select radios ---
        # 1) Resident radio
        try:
            resident_radio = page.locator("#Resident_Resident")
            await resident_radio.wait_for(state="visible", timeout=15000)
            await resident_radio.set_checked(True)
        except PWTimeoutError:
            print("Resident radio not found (maybe already selected). Continuing.")

        # 2) Senior citizen = No (the provided element shows id=IsSeniorCitizen with value=No and checked)
        try:
            senior_no = page.locator("#IsSeniorCitizen")
            await senior_no.wait_for(state="visible", timeout=15000)
            # If this is the "No" radio, ensure it's checked
            await senior_no.set_checked(True)
        except PWTimeoutError:
            print("Senior citizen 'No' radio not found (maybe already selected). Continuing.")

        # Scroll to bottom and click Next
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.locator("#btnNext").click()

        # --- Confirmation popup: click Yes ---
        # The popup renders an <input type="button" class="r-btn r-btn-pop" value="Yes">
        yes_btn = page.locator("input.r-btn.r-btn-pop[value='Yes']")
        await yes_btn.wait_for(state="visible", timeout=20000)
        await yes_btn.click()

        # --- Info popup: click Ok ---
        ok_btn = page.locator("input.r-btn.r-btn-pop[value='Ok'], input.r-btn.r-btn-pop[value='OK']")
        await ok_btn.wait_for(state="visible", timeout=20000)
        await ok_btn.click()

        # After Ok, the same URL shows Schedule 1 component. Fill the fields.

        # 102: name="Schedule1AModel.Sch1_Cage102" -> "Mahesh"
        fld_102 = page.locator("input[name='Schedule1AModel.Sch1_Cage102']")
        await fld_102.wait_for(state="visible", timeout=20000)
        await fld_102.fill("Mahesh")

        # 103: name="Schedule1AModel.Sch1_2021Cage103" -> "103136962"
        fld_103 = page.locator("input[name='Schedule1AModel.Sch1_2021Cage103']")
        await fld_103.wait_for(state="visible", timeout=20000)
        await fld_103.fill("103136962")

        # 104 (numeric Kendo): first input with class "k-formatted-value r-numerictextbox k-input" -> 500000
        # If there are multiple numeric inputs, adjust .nth(0/1/2) as needed.
        num_104 = page.locator("input.k-formatted-value.r-numerictextbox.k-input").first
        await num_104.wait_for(state="visible", timeout=20000)
        await num_104.click()
        # Clear any existing formatted content and type fresh value
        await num_104.press("Control+A")
        await num_104.type("500000")

        print("Filled Schedule 1 fields successfully.")

        # Keep the tab open so you can review
        # await context.close()  # <- uncomment to auto-close when done

if __name__ == "__main__":
    asyncio.run(run())
