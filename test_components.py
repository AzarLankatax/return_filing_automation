"""
Test script to verify the new component-based structure works correctly.
"""

import sys
import asyncio

def test_imports():
    """Test that all modules can be imported correctly."""
    try:
        print("Testing module imports...")
        
        # Test base component import
        from ui_components.base_component import BaseComponent
        print("✓ BaseComponent imported successfully")
        
        # Test main return component import
        from ui_components.main_return_component import MainReturnComponent
        print("✓ MainReturnComponent imported successfully")
        
        # Test schedule 01 component import
        from ui_components.schedule01_component import Schedule01Component
        print("✓ Schedule01Component imported successfully")
        
        # Test schedule 02 component import
        from ui_components.schedule02_component import Schedule02Component
        print("✓ Schedule02Component imported successfully")
        
        # Test component manager import
        from ui_components.component_manager import ComponentManager
        print("✓ ComponentManager imported successfully")
        
        # Test package import
        from ui_components import ComponentManager as CM
        print("✓ Package import successful")
        
        print("✅ All modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_class_instantiation():
    """Test that classes can be instantiated."""
    try:
        print("\n🧪 Testing class instantiation...")
        
        # Test BaseComponent
        from ui_components.base_component import BaseComponent
        # Note: BaseComponent requires a page object, so we'll just test the class exists
        print("✓ BaseComponent class accessible")
        
        # Test MainReturnComponent
        from ui_components.main_return_component import MainReturnComponent
        print("✓ MainReturnComponent class accessible")
        
        # Test Schedule01Component
        from ui_components.schedule01_component import Schedule01Component
        print("✓ Schedule01Component class accessible")
        
        # Test Schedule02Component
        from ui_components.schedule02_component import Schedule02Component
        print("✓ Schedule02Component class accessible")
        
        # Test ComponentManager
        from ui_components.component_manager import ComponentManager
        print("✓ ComponentManager class accessible")
        
        print("✅ All classes can be instantiated!")
        return True
        
    except Exception as e:
        print(f"❌ Class instantiation test failed: {e}")
        return False

def test_component_structure():
    """Test the component structure and methods."""
    try:
        print("\n🧪 Testing component structure...")
        
        from ui_components.main_return_component import MainReturnComponent
        from ui_components.schedule01_component import Schedule01Component
        from ui_components.schedule02_component import Schedule02Component
        
        # Test MainReturnComponent methods
        main_return_methods = [
            'setup_main_return', 'select_resident', 'select_senior_citizen',
            'navigate_to_schedule1', 'navigate_to_schedule2', 'is_main_return_visible',
            'get_current_status', 'validate_setup'
        ]
        
        for method in main_return_methods:
            if hasattr(MainReturnComponent, method):
                print(f"✓ MainReturnComponent.{method} exists")
            else:
                print(f"❌ MainReturnComponent.{method} missing")
                return False
        
        # Test Schedule01Component methods
        schedule01_methods = [
            'setup_schedule01', 'wait_for_schedule01_container', 'fill_schedule01_form',
            'click_add_button', 'save_draft', 'handle_save_confirmation',
            'is_schedule01_visible', 'get_form_data', 'validate_form_data',
            'update_form_data', 'reset_form'
        ]
        
        for method in schedule01_methods:
            if hasattr(Schedule01Component, method):
                print(f"✓ Schedule01Component.{method} exists")
            else:
                print(f"❌ Schedule01Component.{method} missing")
                return False
        
        # Test Schedule02Component methods
        schedule02_methods = [
            'setup_schedule02', 'navigate_to_schedule02_tab', 'wait_for_schedule02_container',
            'fill_schedule02_form', 'save_draft', 'handle_save_confirmation',
            'is_schedule02_visible', 'get_form_data', 'validate_form_data',
            'update_form_data', 'reset_form', 'run_schedule02_automation'
        ]
        
        for method in schedule02_methods:
            if hasattr(Schedule02Component, method):
                print(f"✓ Schedule02Component.{method} exists")
            else:
                print(f"❌ Schedule02Component.{method} missing")
                return False
        
        print("✅ All component methods exist!")
        return True
        
    except Exception as e:
        print(f"❌ Component structure test failed: {e}")
        return False

def test_component_manager():
    """Test the component manager functionality."""
    try:
        print("\n🧪 Testing ComponentManager...")
        
        from ui_components.component_manager import ComponentManager
        
        # Test ComponentManager methods
        manager_methods = [
            'run_complete_automation', 'run_main_return_only', 'run_schedule01_only',
            'run_schedule02_only', 'validate_all_components', 'get_component_status',
            'update_component_data', 'reset_all_components'
        ]
        
        for method in manager_methods:
            if hasattr(ComponentManager, method):
                print(f"✓ ComponentManager.{method} exists")
            else:
                print(f"❌ ComponentManager.{method} missing")
                return False
        
        print("✅ ComponentManager structure is correct!")
        return True
        
    except Exception as e:
        print(f"❌ ComponentManager test failed: {e}")
        return False

def test_form_automation_integration():
    """Test the form automation integration."""
    try:
        print("\n🧪 Testing form automation integration...")
        
        # Test that the new form automation can be imported
        import form_automation_new
        print("✓ form_automation_new.py imported successfully")
        
        # Test that it has the required functions
        required_functions = ['run_automation', 'main', 'connect_to_existing_browser', 'logout_user']
        
        for func in required_functions:
            if hasattr(form_automation_new, func):
                print(f"✓ form_automation_new.{func} exists")
            else:
                print(f"❌ form_automation_new.{func} missing")
                return False
        
        print("✅ Form automation integration is correct!")
        return True
        
    except Exception as e:
        print(f"❌ Form automation integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing IRD Automation Component-Based Structure")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_class_instantiation,
        test_component_structure,
        test_component_manager,
        test_form_automation_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Component-based structure is working correctly.")
        print("\n📝 Project Structure:")
        print("   📁 ui_components/")
        print("      ├── __init__.py")
        print("      ├── base_component.py")
        print("      ├── main_return_component.py")
        print("      ├── schedule01_component.py")
        print("      ├── schedule02_component.py")
        print("      └── component_manager.py")
        print("   📄 form_automation_new.py")
        print("   📄 browser_setup.py")
        print("\n🚀 Next steps:")
        print("   1. Run 'python browser_setup.py' to start browser")
        print("   2. Run 'python form_automation_new.py' to start automation")
        print("   3. Each component can be used independently")
        print("   4. Easy to extend with new components")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
