"""
Schedule 2 Component for IRD Form Automation

This module handles the Schedule 2 section of the IRD form including:
- Form field filling
- Draft saving
- Tab navigation
"""

from .base_component import BaseComponent


class Schedule02Component(BaseComponent):
    """Handles the Schedule 2 section of the IRD form."""
    
    def __init__(self, page):
        """Initialize the Schedule 2 Component."""
        super().__init__(page, "Schedule 2")
        self.selectors = {
            "container": "#Schedule02Container",
            "tab_link": 'a[href="javascript:void(0)"][onclick*="tabStrip.select(tabSchedule2)"]',
            "tab_link_alt": 'a:has-text("(Schedule 2)")',
            "save_draft_button": "#btnS2SaveDraft",
            "confirm_yes": "input[value='Yes']",
            "confirm_ok": "input[value='Ok']"
        }
        
        # Schedule 2 form data
        self.form_data = {
            "201": "702000-MANAGEMENT CONSULTANCY ACTIVITIES",  # Activity code
            "202": "Consulting services",                        # Nature of business
            "203": 150000,                                       # Gains and profits
            "204A": 2000000                                      # Total business turnover
        }
    
    async def setup_schedule02(self):
        """
        Set up and fill the Schedule 2 form.
        
        Returns:
            bool: True if setup was successful
        """
        try:
            self.log_info("Starting Schedule 2 setup...")
            
            # Navigate to Schedule 2 tab
            await self.navigate_to_schedule02_tab()
            
            # Wait for Schedule 2 container to be visible
            await self.wait_for_schedule02_container()
            
            # Fill Schedule 2 form fields
            await self.fill_schedule02_form()
            
            # Save draft
            await self.save_draft()
            
            self.log_success("Schedule 2 setup completed successfully")
            return True
            
        except Exception as e:
            self.log_error(f"Error in Schedule 2 setup: {str(e)}")
            return False
    
    async def navigate_to_schedule02_tab(self):
        """Navigate to Schedule 2 tab."""
        try:
            self.log_info("Looking for Schedule 2 tab...")
            
            # Try primary selector first
            try:
                await self.click_element(self.selectors["tab_link"], timeout=15000)
                self.log_success("Successfully clicked Schedule 2 tab")
                return
            except:
                self.log_warning("Primary Schedule 2 tab selector failed, trying alternative...")
            
            # Try alternative selector
            try:
                await self.click_element(self.selectors["tab_link_alt"], timeout=10000)
                self.log_success("Successfully clicked Schedule 2 tab using alternative selector")
                return
            except:
                self.log_warning("Alternative Schedule 2 tab selector failed")
            
            # If both fail, wait for manual click
            self.log_warning("Could not find Schedule 2 tab automatically")
            self.log_info("Please manually click on Schedule 2 tab")
            
            # Wait for user to manually click
            await self.wait_for_element(self.selectors["container"], timeout=30000)
            self.log_success("Schedule 2 container is now visible (manual click detected)")
            
        except Exception as e:
            self.log_error(f"Error navigating to Schedule 2 tab: {str(e)}")
            raise
    
    async def wait_for_schedule02_container(self):
        """Wait for Schedule 2 container to be visible."""
        try:
            await self.wait_for_element(self.selectors["container"])
            self.log_success("Schedule 2 container is visible")
            
            # Wait a moment for the form to load
            await self.page.wait_for_timeout(2000)
            
        except Exception as e:
            self.log_error(f"Schedule 2 container not found: {str(e)}")
            raise
    
    async def fill_schedule02_form(self):
        """Fill all Schedule 2 form fields."""
        try:
            self.log_info("Filling Schedule 2 form fields...")
            
            # Fill each form field
            for cage_number, value in self.form_data.items():
                try:
                    if cage_number == "201":  # Activity code dropdown
                        await self.select_kendo_dropdown_by_cage(cage_number, value)
                    elif isinstance(value, str):
                        await self.fill_text_by_cage(cage_number, value)
                    else:
                        await self.fill_kendo_numeric_by_cage(cage_number, value)
                    
                    self.log_success(f"Field {cage_number} filled successfully")
                    
                except Exception as e:
                    self.log_error(f"Error filling field {cage_number}: {str(e)}")
                    self.log_info(f"Please fill field {cage_number} manually")
            
            self.log_success("Schedule 2 form fields filled successfully")
            
        except Exception as e:
            self.log_error(f"Error filling Schedule 2 form: {str(e)}")
            raise
    
    async def save_draft(self):
        """Save draft for Schedule 2."""
        try:
            self.log_info("Saving draft for Schedule 2...")
            
            # Click save draft button
            await self.click_element(self.selectors["save_draft_button"])
            
            # Handle confirmation dialogs
            await self.handle_save_confirmation()
            
            self.log_success("Draft saved for Schedule 2")
            
        except Exception as e:
            self.log_error(f"Error saving Schedule 2 draft: {str(e)}")
            raise
    
    async def handle_save_confirmation(self):
        """Handle save confirmation dialogs."""
        try:
            # Handle "Yes" confirmation
            try:
                await self.click_topmost_dialog_button("Yes", timeout=12000)
                self.log_success("Confirmed 'Yes' on save dialog (S2)")
            except:
                self.log_warning("No confirmation dialog (S2); continuing...")
            
            # Handle "Ok" info dialog
            try:
                await self.click_topmost_dialog_button("Ok", timeout=10000)
                self.log_success("Acknowledged 'Ok' on info dialog (S2 draft saved)")
            except:
                try:
                    await self.click_topmost_dialog_button("OK", timeout=3000)
                    self.log_success("Acknowledged 'OK' on info dialog (S2 draft saved)")
                except:
                    self.log_warning("Info dialog (Ok/OK) not found for S2; verify draft manually")
            
        except Exception as e:
            self.log_error(f"Error handling save confirmation: {str(e)}")
            raise
    
    async def is_schedule02_visible(self):
        """
        Check if Schedule 2 container is visible.
        
        Returns:
            bool: True if Schedule 2 is visible
        """
        try:
            await self.wait_for_element(self.selectors["container"], timeout=5000)
            return True
        except:
            return False
    
    async def get_form_data(self):
        """
        Get current form data from Schedule 2.
        
        Returns:
            dict: Current form data
        """
        try:
            current_data = {}
            
            for cage_number in self.form_data.keys():
                try:
                    if cage_number == "201":  # Dropdown
                        select_selector = f'select[data-cage="{cage_number}"]'
                        value = await self.page.input_value(select_selector)
                    else:  # Input fields
                        input_selector = f'input[data-cage="{cage_number}"]'
                        value = await self.page.input_value(input_selector)
                    
                    current_data[cage_number] = value
                except:
                    current_data[cage_number] = None
            
            return current_data
            
        except Exception as e:
            self.log_error(f"Error getting form data: {str(e)}")
            return {}
    
    async def validate_form_data(self):
        """
        Validate that form data is correctly filled.
        
        Returns:
            bool: True if form data is valid
        """
        try:
            current_data = await self.get_form_data()
            
            for cage_number, expected_value in self.form_data.items():
                current_value = current_data.get(cage_number)
                
                if current_value is None or str(current_value).strip() == "":
                    self.log_error(f"Field {cage_number} is empty")
                    return False
                
                if cage_number == "201":  # Activity code
                    if expected_value not in str(current_value):
                        self.log_warning(f"Field {cage_number} value mismatch: expected {expected_value}, got {current_value}")
                elif isinstance(expected_value, (int, float)):
                    try:
                        if float(current_value) != float(expected_value):
                            self.log_warning(f"Field {cage_number} value mismatch: expected {expected_value}, got {current_value}")
                    except:
                        self.log_error(f"Field {cage_number} has invalid numeric value: {current_value}")
                        return False
            
            self.log_success("Schedule 2 form data validation passed")
            return True
            
        except Exception as e:
            self.log_error(f"Error validating form data: {str(e)}")
            return False
    
    def update_form_data(self, new_data):
        """
        Update form data with new values.
        
        Args:
            new_data (dict): New form data to use
        """
        self.form_data.update(new_data)
        self.log_info(f"Form data updated: {new_data}")
    
    async def reset_form(self):
        """Reset Schedule 2 form to default values."""
        try:
            self.log_info("Resetting Schedule 2 form...")
            
            for cage_number, value in self.form_data.items():
                try:
                    if cage_number == "201":  # Dropdown
                        select_selector = f'select[data-cage="{cage_number}"]'
                        await self.page.select_option(select_selector, "")
                    else:  # Input fields
                        input_selector = f'input[data-cage="{cage_number}"]'
                        await self.page.fill(input_selector, "")
                except:
                    continue
            
            self.log_success("Schedule 2 form reset completed")
            
        except Exception as e:
            self.log_error(f"Error resetting form: {str(e)}")
            raise
    
    async def run_schedule02_automation(self, context):
        """
        Run complete Schedule 2 automation in a new tab.
        
        Args:
            context: Browser context for creating new tabs
        
        Returns:
            bool: True if automation was successful
        """
        try:
            self.log_info("Starting Schedule 2 automation in new tab...")
            
            # Open new tab and navigate to the form URL
            schedule02_page = await context.new_page()
            
            # Navigate to the form URL
            form_url = "https://eservices.ird.gov.lk/Assessment/IIT2/ReturnFiling"
            await schedule02_page.goto(form_url)
            await schedule02_page.wait_for_load_state("networkidle")
            self.log_success("Form page loaded successfully")
            
            # Create Schedule 2 component for the new page
            schedule02_component = Schedule02Component(schedule02_page)
            
            # Run Schedule 2 automation
            success = await schedule02_component.setup_schedule02()
            
            # Close the tab
            await schedule02_page.close()
            self.log_success("Schedule 2 tab closed")
            
            return success
            
        except Exception as e:
            self.log_error(f"Error during Schedule 2 automation: {str(e)}")
            self.log_info("Please complete Schedule 2 manually if needed")
            
            # Try to close the tab if it exists
            try:
                if 'schedule02_page' in locals():
                    await schedule02_page.close()
            except:
                pass
            
            return False
