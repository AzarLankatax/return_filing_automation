"""
Main Return Component for IRD Form Automation

This module handles the main return section of the IRD form including:
- Radio button selections
- Basic form setup
- Navigation to other components
"""

from .base_component import BaseComponent


class MainReturnComponent(BaseComponent):
    """Handles the main return section of the IRD form."""
    
    def __init__(self, page):
        """Initialize the Main Return Component."""
        super().__init__(page, "Main Return")
        self.selectors = {
            "resident_yes": "#Resident_Resident",
            "resident_no": "#Resident_NonResident", 
            "senior_citizen_yes": "#IsSeniorCitizen",
            "senior_citizen_no": "#IsSeniorCitizenNo",
            "schedule1_button": "#btnSchedule1",
            "schedule2_button": "#btnSchedule2"
        }
    
    async def setup_main_return(self):
        """
        Set up the main return section with radio button selections.
        
        Returns:
            bool: True if setup was successful
        """
        try:
            self.log_info("Starting main return setup...")
            
            # Step 1: Select Resident
            await self.select_resident()
            
            # Step 2: Select Senior citizen = No
            await self.select_senior_citizen()
            
            # Step 3: Navigate to Schedule 1
            await self.navigate_to_schedule1()
            
            self.log_success("Main return setup completed successfully")
            return True
            
        except Exception as e:
            self.log_error(f"Error in main return setup: {str(e)}")
            return False
    
    async def select_resident(self):
        """Select Resident radio button."""
        try:
            await self.select_radio_button(self.selectors["resident_yes"])
            self.log_success("Selected Resident: Resident")
        except Exception as e:
            self.log_error(f"Failed to select Resident: {str(e)}")
            raise
    
    async def select_senior_citizen(self):
        """Select Senior citizen = No."""
        try:
            await self.select_radio_button(self.selectors["senior_citizen_no"])
            self.log_success("Selected Senior citizen: No")
        except Exception as e:
            self.log_error(f"Failed to select Senior citizen: {str(e)}")
            raise
    
    async def navigate_to_schedule1(self):
        """Navigate to Schedule 1 component."""
        try:
            await self.click_element(self.selectors["schedule1_button"])
            self.log_success("Navigated to Schedule 1")
            
            # Wait for Schedule 1 to load
            await self.page.wait_for_load_state("networkidle")
            self.log_success("Schedule 1 component loaded")
            
        except Exception as e:
            self.log_error(f"Failed to navigate to Schedule 1: {str(e)}")
            raise
    
    async def navigate_to_schedule2(self):
        """Navigate to Schedule 2 component."""
        try:
            await self.click_element(self.selectors["schedule2_button"])
            self.log_success("Navigated to Schedule 2")
            
            # Wait for Schedule 2 to load
            await self.page.wait_for_load_state("networkidle")
            self.log_success("Schedule 2 component loaded")
            
        except Exception as e:
            self.log_error(f"Failed to navigate to Schedule 2: {str(e)}")
            raise
    
    async def is_main_return_visible(self):
        """
        Check if main return section is visible.
        
        Returns:
            bool: True if main return is visible
        """
        try:
            await self.wait_for_element(self.selectors["resident_yes"], timeout=5000)
            return True
        except:
            return False
    
    async def get_current_status(self):
        """
        Get the current status of main return selections.
        
        Returns:
            dict: Status of radio button selections
        """
        try:
            status = {}
            
            # Check Resident selection
            resident_checked = await self.page.is_checked(self.selectors["resident_yes"])
            status["resident"] = "Resident" if resident_checked else "Non-Resident"
            
            # Check Senior citizen selection
            senior_checked = await self.page.is_checked(self.selectors["senior_citizen_no"])
            status["senior_citizen"] = "No" if senior_checked else "Yes"
            
            return status
            
        except Exception as e:
            self.log_error(f"Error getting status: {str(e)}")
            return {}
    
    async def validate_setup(self):
        """
        Validate that the main return setup is correct.
        
        Returns:
            bool: True if setup is valid
        """
        try:
            status = await self.get_current_status()
            
            if status.get("resident") != "Resident":
                self.log_error("Resident selection is incorrect")
                return False
            
            if status.get("senior_citizen") != "No":
                self.log_error("Senior citizen selection is incorrect")
                return False
            
            self.log_success("Main return setup validation passed")
            return True
            
        except Exception as e:
            self.log_error(f"Error validating setup: {str(e)}")
            return False
