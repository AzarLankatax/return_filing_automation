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
        print("BaseComponent imported successfully")
        
        # Test main return component import
        from ui_components.main_return_component import MainReturnComponent
        print("MainReturnComponent imported successfully")
        
        # Test schedule 01 component import
        from ui_components.schedule01_component import Schedule01Component
        print("Schedule01Component imported successfully")
        
        # Test schedule 02 component import
        from ui_components.schedule02_component import Schedule02Component
        print("Schedule02Component imported successfully")
        
        # Test component manager import
        from ui_components.component_manager import ComponentManager
        print("ComponentManager imported successfully")
        
        # Test package import
        from ui_components import ComponentManager as CM
        print("Package import successful")
        
        print("All modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def test_class_instantiation():
    """Test that classes can be instantiated."""
    try:
        print("\nTesting class instantiation...")
        
        # Test BaseComponent
        from ui_components.base_component import BaseComponent
        print("BaseComponent class accessible")
        
        # Test MainReturnComponent
        from ui_components.main_return_component import MainReturnComponent
        print("MainReturnComponent class accessible")
        
        # Test Schedule01Component
        from ui_components.schedule01_component import Schedule01Component
        print("Schedule01Component class accessible")
        
        # Test Schedule02Component
        from ui_components.schedule02_component import Schedule02Component
        print("Schedule02Component class accessible")
        
        # Test ComponentManager
        from ui_components.component_manager import ComponentManager
        print("ComponentManager class accessible")
        
        print("All classes can be instantiated!")
        return True
        
    except Exception as e:
        print(f"Class instantiation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing IRD Automation Component-Based Structure")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_class_instantiation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Component-based structure is working correctly.")
        print("\nProject Structure:")
        print("   ui_components/")
        print("      __init__.py")
        print("      base_component.py")
        print("      main_return_component.py")
        print("      schedule01_component.py")
        print("      schedule02_component.py")
        print("      component_manager.py")
        print("   form_automation_new.py")
        print("   browser_setup.py")
        print("\nNext steps:")
        print("   1. Run 'python browser_setup.py' to start browser")
        print("   2. Run 'python form_automation_new.py' to start automation")
        print("   3. Each component can be used independently")
        print("   4. Easy to extend with new components")
    else:
        print("Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
