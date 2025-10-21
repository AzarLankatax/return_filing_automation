# IRD Automation Project - Component-Based Architecture

A comprehensive, modular automation solution for IRD (Inland Revenue Department) form filling using Playwright with a clean component-based architecture.

## 🏗️ Project Structure

```
IRD-Automation/
├── ui_components/                    # UI Components Package
│   ├── __init__.py                  # Package initialization
│   ├── base_component.py            # Base component class
│   ├── main_return_component.py     # Main return section
│   ├── schedule01_component.py      # Schedule 1 section
│   ├── schedule02_component.py      # Schedule 2 section
│   └── component_manager.py         # Component orchestration
├── form_automation_new.py           # New component-based automation
├── form_automation.py               # Legacy automation (for reference)
├── browser_setup.py                 # Browser setup and login
├── test_components_simple.py        # Component structure tests
└── README.md                        # This file
```

## 🚀 Key Features

### **Modular Architecture**
- **Separation of Concerns**: Each UI component handles a specific form section
- **Reusable Components**: Components can be used independently or together
- **Easy Extension**: Add new components without affecting existing ones
- **Clean Interfaces**: Well-defined methods and error handling

### **Component-Based Design**
- **BaseComponent**: Shared functionality for all components
- **MainReturnComponent**: Handles main return section automation
- **Schedule01Component**: Handles Schedule 1 form automation
- **Schedule02Component**: Handles Schedule 2 form automation
- **ComponentManager**: Orchestrates all components

### **Robust Error Handling**
- **Graceful Degradation**: Components fail gracefully with clear error messages
- **Manual Fallback**: Instructions for manual completion when automation fails
- **Comprehensive Logging**: Detailed logs for debugging and monitoring

## 📋 Component Details

### **BaseComponent** (`base_component.py`)
Provides shared functionality for all UI components:
- Element waiting and interaction
- Form field filling (text, numeric, dropdown)
- Popup handling
- Error logging and status reporting

### **MainReturnComponent** (`main_return_component.py`)
Handles the main return section:
- Radio button selections (Resident, Senior citizen)
- Navigation to Schedule 1
- Status validation

### **Schedule01Component** (`schedule01_component.py`)
Handles Schedule 1 form automation:
- Form field filling (business details, financial data)
- Add button functionality
- Draft saving with confirmation handling
- Form validation

### **Schedule02Component** (`schedule02_component.py`)
Handles Schedule 2 form automation:
- Tab navigation and detection
- Form field filling (activity codes, business details)
- Draft saving
- New tab automation capability

### **ComponentManager** (`component_manager.py`)
Orchestrates all components:
- Complete automation workflow
- Individual component execution
- Validation and status checking
- Error handling and reporting

## 🛠️ Usage

### **Complete Automation**
```bash
# Start browser setup
python browser_setup.py

# Run complete automation (in another terminal)
python form_automation_new.py
```

### **Individual Components**
```python
from ui_components import ComponentManager

# Initialize component manager
component_manager = ComponentManager(page, context)

# Run specific components
await component_manager.run_main_return_only()
await component_manager.run_schedule01_only()
await component_manager.run_schedule02_only()
```

### **Custom Component Usage**
```python
from ui_components import MainReturnComponent, Schedule01Component

# Use components independently
main_return = MainReturnComponent(page)
await main_return.setup_main_return()

schedule01 = Schedule01Component(page)
await schedule01.setup_schedule01()
```

## 🔧 Configuration

### **Component Data Customization**
```python
# Update Schedule 1 data
schedule01_component = Schedule01Component(page)
schedule01_component.update_form_data({
    "101": "Your business description",
    "102": 200000,  # Your gains and profits
    "103": 3000000  # Your business turnover
})

# Update Schedule 2 data
schedule02_component = Schedule02Component(page)
schedule02_component.update_form_data({
    "201": "Your activity code",
    "202": "Your business nature",
    "203": 250000,  # Your gains
    "204A": 4000000  # Your turnover
})
```

## 🧪 Testing

### **Component Structure Test**
```bash
python test_components_simple.py
```

This test verifies:
- All components can be imported
- Classes can be instantiated
- Component structure is correct

### **Manual Testing**
1. Run `browser_setup.py` to start browser
2. Run `form_automation_new.py` to test automation
3. Monitor console output for component execution
4. Verify form completion manually

## 📊 Workflow

### **Complete Automation Flow**
1. **Browser Setup**: Start browser and login
2. **Main Return**: Set radio buttons and navigate
3. **Schedule 1**: Fill form fields and save draft
4. **Schedule 2**: Open new tab, fill form, save draft
5. **Completion**: Return to main workflow

### **Error Handling Flow**
1. **Component Failure**: Log error and provide manual instructions
2. **Graceful Degradation**: Continue with other components
3. **Manual Fallback**: User completes failed component manually
4. **Status Reporting**: Clear success/failure reporting

## 🔍 Benefits

### **For Developers**
- **Maintainable**: Clear separation of concerns
- **Extensible**: Easy to add new components
- **Testable**: Individual components can be tested
- **Debuggable**: Clear error messages and logging

### **For Users**
- **Reliable**: Robust error handling and fallbacks
- **Transparent**: Clear progress reporting
- **Flexible**: Components can be run independently
- **User-Friendly**: Manual completion instructions when needed

## 🚀 Future Enhancements

### **Planned Features**
- **Configuration File**: External configuration for form data
- **Database Integration**: Store and retrieve form data
- **Multi-User Support**: Handle multiple user sessions
- **Advanced Validation**: Enhanced form validation
- **Reporting**: Detailed automation reports

### **Extension Points**
- **New Components**: Add Schedule 3, 4, etc.
- **Custom Validators**: Add component-specific validation
- **Integration Hooks**: Connect with external systems
- **UI Enhancements**: Add progress bars, status indicators

## 📝 Development Guidelines

### **Adding New Components**
1. Inherit from `BaseComponent`
2. Implement required methods (`setup_*`, `validate_*`)
3. Add to `ComponentManager`
4. Update `__init__.py`
5. Add tests

### **Component Method Standards**
- **Setup Methods**: `setup_component_name()`
- **Validation Methods**: `validate_component_name()`
- **Status Methods**: `get_component_status()`
- **Reset Methods**: `reset_component()`

### **Error Handling Standards**
- **Log Errors**: Use component's log methods
- **Provide Fallbacks**: Give manual completion instructions
- **Return Status**: Return success/failure boolean
- **Graceful Degradation**: Don't crash entire automation

## 🤝 Contributing

1. **Fork Repository**: Create your own fork
2. **Create Branch**: Use feature branch naming
3. **Follow Standards**: Use existing patterns and conventions
4. **Add Tests**: Include tests for new components
5. **Document Changes**: Update README and docstrings
6. **Submit PR**: Create pull request with description

## 📄 License

This project is for educational and personal use only. Please ensure compliance with IRD terms of service.

---

**Note**: This component-based architecture provides a solid foundation for IRD form automation while maintaining flexibility and extensibility for future enhancements.
