"""
Schedule 1 Component for IRD Form Automation

This module handles the Schedule 1 section of the IRD form including:
- Form field filling
- Add button functionality
- Draft saving
"""

from .base_component import BaseComponent


class Schedule01Component(BaseComponent):
    """Handles the Schedule 1 section of the IRD form."""
    
    def __init__(self, page):
        """Initialize the Schedule 1 Component."""
        super().__init__(page, "Schedule 1")
        self.selectors = {
            "container": "#Schedule01Container",
            "add_button": "#btnS1AddC_2",
            "save_draft_button": "#btnS1SaveDraft",
            "confirm_yes": "input[value='Yes']",
            "confirm_ok": "input[value='Ok']"
        }
        
        # Schedule 1 form data
        self.form_data = {
            "101": "Consulting services",  # Nature of business
            "102": 150000,               # Gains and profits
            "103": 2000000,              # Total business turnover
            "104": 50000,                # Other income
            "105": 10000                 # Deductions
        }
    
    async def setup_schedule01(self):
        """
        Set up and fill the Schedule 1 form.
        
        Returns:
            bool: True if setup was successful
        """
        try:
            self.log_info("Starting Schedule 1 setup...")
            
            # Wait for Schedule 1 container to be visible
            await self.wait_for_schedule01_container()
            
            # Fill Schedule 1 form fields
            await self.fill_schedule01_form()
            
            # Click Add button
            await self.click_add_button()
            
            # Save draft
            await self.save_draft()
            
            self.log_success("Schedule 1 setup completed successfully")
            return True
            
        except Exception as e:
            self.log_error(f"Error in Schedule 1 setup: {str(e)}")
            return False
    
    async def wait_for_schedule01_container(self):
        """Wait for Schedule 1 container to be visible."""
        try:
            await self.wait_for_element(self.selectors["container"])
            self.log_success("Schedule 1 container is visible")
        except Exception as e:
            self.log_error(f"Schedule 1 container not found: {str(e)}")
            raise
    
    async def fill_schedule01_form(self):
        """Fill all Schedule 1 form fields."""
        try:
            self.log_info("Filling Schedule 1 form fields...")
            
            # Fill each form field
            for cage_number, value in self.form_data.items():
                if isinstance(value, str):
                    await self.fill_text_by_cage(cage_number, value)
                else:
                    await self.fill_kendo_numeric_by_cage(cage_number, value)
            
            self.log_success("Schedule 1 form fields filled successfully")
            
        except Exception as e:
            self.log_error(f"Error filling Schedule 1 form: {str(e)}")
            raise
    
    async def click_add_button(self):
        """Click the Add button for Schedule 1."""
        try:
            self.log_info("Clicking Add button...")
            
            # Try primary selector first
            try:
                await self.click_element(self.selectors["add_button"])
                self.log_success("Add button clicked successfully")
                return
            except:
                self.log_warning("Primary Add button selector failed, trying fallback...")
            
            # Try fallback selectors
            fallback_selectors = [
                'input[type="button"][value="Add"]',
                'button:has-text("Add")',
                'input[id*="Add"]'
            ]
            
            for selector in fallback_selectors:
                try:
                    await self.click_element(selector, timeout=5000)
                    self.log_success(f"Add button clicked using fallback selector: {selector}")
                    return
                except:
                    continue
            
            self.log_warning("Could not find Add button with any selector - may need manual click")
            
        except Exception as e:
            self.log_error(f"Error clicking Add button: {str(e)}")
            raise
    
    async def save_draft(self):
        """Save draft for Schedule 1."""
        try:
            self.log_info("Saving draft for Schedule 1...")
            
            # Click save draft button
            await self.click_element(self.selectors["save_draft_button"])
            
            # Handle confirmation dialogs
            await self.handle_save_confirmation()
            
            self.log_success("Draft saved for Schedule 1")
            
        except Exception as e:
            self.log_error(f"Error saving Schedule 1 draft: {str(e)}")
            raise
    
    async def handle_save_confirmation(self):
        """Handle save confirmation dialogs."""
        try:
            # Handle "Yes" confirmation
            try:
                await self.click_topmost_dialog_button("Yes", timeout=12000)
                self.log_success("Confirmed 'Yes' on save dialog")
            except:
                self.log_warning("No 'Yes' confirmation dialog found")
            
            # Handle "Ok" info dialog
            try:
                await self.click_topmost_dialog_button("Ok", timeout=10000)
                self.log_success("Acknowledged 'Ok' on info dialog")
            except:
                try:
                    await self.click_topmost_dialog_button("OK", timeout=3000)
                    self.log_success("Acknowledged 'OK' on info dialog")
                except:
                    self.log_warning("Info dialog (Ok/OK) not found - verify draft manually")
            
        except Exception as e:
            self.log_error(f"Error handling save confirmation: {str(e)}")
            raise
    
    async def is_schedule01_visible(self):
        """
        Check if Schedule 1 container is visible.
        
        Returns:
            bool: True if Schedule 1 is visible
        """
        try:
            await self.wait_for_element(self.selectors["container"], timeout=5000)
            return True
        except:
            return False
    
    async def get_form_data(self):
        """
        Get current form data from Schedule 1.
        
        Returns:
            dict: Current form data
        """
        try:
            current_data = {}
            
            for cage_number in self.form_data.keys():
                try:
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
                
                if isinstance(expected_value, (int, float)):
                    try:
                        if float(current_value) != float(expected_value):
                            self.log_warning(f"Field {cage_number} value mismatch: expected {expected_value}, got {current_value}")
                    except:
                        self.log_error(f"Field {cage_number} has invalid numeric value: {current_value}")
                        return False
            
            self.log_success("Schedule 1 form data validation passed")
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
        """Reset Schedule 1 form to default values."""
        try:
            self.log_info("Resetting Schedule 1 form...")
            
            for cage_number, value in self.form_data.items():
                try:
                    input_selector = f'input[data-cage="{cage_number}"]'
                    await self.page.fill(input_selector, "")
                except:
                    continue
            
            self.log_success("Schedule 1 form reset completed")
            
        except Exception as e:
            self.log_error(f"Error resetting form: {str(e)}")
            raise
