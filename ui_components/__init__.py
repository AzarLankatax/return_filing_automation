"""
UI Components Package for IRD Form Automation

This package contains all UI components for the IRD form automation system.
Each component handles a specific section of the form.
"""

from .base_component import BaseComponent
from .main_return_component import MainReturnComponent
from .schedule01_component import Schedule01Component
from .schedule02_component import Schedule02Component
from .component_manager import ComponentManager

__all__ = [
    'BaseComponent',
    'MainReturnComponent', 
    'Schedule01Component',
    'Schedule02Component',
    'ComponentManager'
]

__version__ = "1.0.0"
