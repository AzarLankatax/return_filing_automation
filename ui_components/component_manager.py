"""
Component Manager for IRD Form Automation

This module manages and orchestrates all UI components for the IRD form automation.
"""

from .main_return_component import MainReturnComponent
from .schedule01_component import Schedule01Component
from .schedule02_component import Schedule02Component


class ComponentManager:
    """Manages all UI components for IRD form automation."""
    
    def __init__(self, page, context=None):
        """
        Initialize the component manager.
        
        Args:
            page: Playwright page object
            context: Browser context (optional, for Schedule 2 automation)
        """
        self.page = page
        self.context = context
        
        # Initialize components
        self.main_return = MainReturnComponent(page)
        self.schedule01 = Schedule01Component(page)
        self.schedule02 = Schedule02Component(page)
        
        # Component execution order
        self.components = [
            ("main_return", self.main_return),
            ("schedule01", self.schedule01),
            ("schedule02", self.schedule02)
        ]
    
    async def run_complete_automation(self):
        """
        Run the complete IRD form automation.
        
        Returns:
            dict: Results of each component execution
        """
        results = {}
        
        try:
            print("🚀 Starting complete IRD form automation...")
            print("=" * 60)
            
            # Step 1: Main Return Component
            print("\n📋 Step 1: Main Return Component")
            print("-" * 40)
            results["main_return"] = await self.main_return.setup_main_return()
            
            if not results["main_return"]:
                print("❌ Main Return component failed - stopping automation")
                return results
            
            # Step 2: Schedule 1 Component
            print("\n📋 Step 2: Schedule 1 Component")
            print("-" * 40)
            results["schedule01"] = await self.schedule01.setup_schedule01()
            
            if not results["schedule01"]:
                print("❌ Schedule 1 component failed - stopping automation")
                return results
            
            # Step 3: Schedule 2 Component (in new tab)
            print("\n📋 Step 3: Schedule 2 Component")
            print("-" * 40)
            if self.context:
                results["schedule02"] = await self.schedule02.run_schedule02_automation(self.context)
            else:
                print("⚠️ No context provided - Schedule 2 automation skipped")
                results["schedule02"] = False
            
            # Summary
            print("\n" + "=" * 60)
            print("📊 AUTOMATION SUMMARY")
            print("=" * 60)
            
            for component_name, success in results.items():
                status = "✅ SUCCESS" if success else "❌ FAILED"
                print(f"{component_name.replace('_', ' ').title()}: {status}")
            
            overall_success = all(results.values())
            if overall_success:
                print("\n🎉 Complete automation completed successfully!")
            else:
                print("\n⚠️ Automation completed with some failures")
            
            return results
            
        except Exception as e:
            print(f"\n❌ Error during complete automation: {str(e)}")
            results["error"] = str(e)
            return results
    
    async def run_main_return_only(self):
        """
        Run only the Main Return component.
        
        Returns:
            bool: True if successful
        """
        try:
            print("🚀 Starting Main Return automation...")
            return await self.main_return.setup_main_return()
        except Exception as e:
            print(f"❌ Error in Main Return automation: {str(e)}")
            return False
    
    async def run_schedule01_only(self):
        """
        Run only the Schedule 1 component.
        
        Returns:
            bool: True if successful
        """
        try:
            print("🚀 Starting Schedule 1 automation...")
            return await self.schedule01.setup_schedule01()
        except Exception as e:
            print(f"❌ Error in Schedule 1 automation: {str(e)}")
            return False
    
    async def run_schedule02_only(self):
        """
        Run only the Schedule 2 component.
        
        Returns:
            bool: True if successful
        """
        try:
            if not self.context:
                print("❌ No context provided for Schedule 2 automation")
                return False
            
            print("🚀 Starting Schedule 2 automation...")
            return await self.schedule02.run_schedule02_automation(self.context)
        except Exception as e:
            print(f"❌ Error in Schedule 2 automation: {str(e)}")
            return False
    
    async def validate_all_components(self):
        """
        Validate all components are working correctly.
        
        Returns:
            dict: Validation results for each component
        """
        validation_results = {}
        
        try:
            print("🔍 Validating all components...")
            
            # Validate Main Return
            validation_results["main_return"] = await self.main_return.validate_setup()
            
            # Validate Schedule 1
            validation_results["schedule01"] = await self.schedule01.validate_form_data()
            
            # Validate Schedule 2
            validation_results["schedule02"] = await self.schedule02.validate_form_data()
            
            print("\n📊 VALIDATION SUMMARY")
            print("-" * 30)
            
            for component_name, valid in validation_results.items():
                status = "✅ VALID" if valid else "❌ INVALID"
                print(f"{component_name.replace('_', ' ').title()}: {status}")
            
            return validation_results
            
        except Exception as e:
            print(f"❌ Error during validation: {str(e)}")
            return {"error": str(e)}
    
    def get_component_status(self):
        """
        Get the current status of all components.
        
        Returns:
            dict: Status information for each component
        """
        status = {}
        
        try:
            # Get Main Return status
            status["main_return"] = asyncio.run(self.main_return.get_current_status())
            
            # Get Schedule 1 form data
            status["schedule01"] = asyncio.run(self.schedule01.get_form_data())
            
            # Get Schedule 2 form data
            status["schedule02"] = asyncio.run(self.schedule02.get_form_data())
            
        except Exception as e:
            status["error"] = str(e)
        
        return status
    
    def update_component_data(self, component_name, data):
        """
        Update data for a specific component.
        
        Args:
            component_name (str): Name of the component
            data (dict): Data to update
        
        Returns:
            bool: True if update was successful
        """
        try:
            if component_name == "schedule01":
                self.schedule01.update_form_data(data)
            elif component_name == "schedule02":
                self.schedule02.update_form_data(data)
            else:
                print(f"❌ Unknown component: {component_name}")
                return False
            
            print(f"✅ Updated {component_name} data successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error updating {component_name} data: {str(e)}")
            return False
    
    async def reset_all_components(self):
        """Reset all components to default state."""
        try:
            print("🔄 Resetting all components...")
            
            await self.schedule01.reset_form()
            await self.schedule02.reset_form()
            
            print("✅ All components reset successfully")
            
        except Exception as e:
            print(f"❌ Error resetting components: {str(e)}")
            raise
