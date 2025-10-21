"""
Base Component Class for IRD UI Components

This module provides the base class and shared functionality for all UI components.
"""

import asyncio
from playwright.async_api import TimeoutError as PWTimeoutError


class BaseComponent:
    """Base class for all UI components."""
    
    def __init__(self, page, component_name):
        """
        Initialize the base component.
        
        Args:
            page: Playwright page object
            component_name (str): Name of the component
        """
        self.page = page
        self.component_name = component_name
        self.timeout = 20000  # Default timeout in milliseconds
    
    async def wait_for_element(self, selector, timeout=None):
        """
        Wait for an element to be visible.
        
        Args:
            selector (str): CSS selector for the element
            timeout (int): Timeout in milliseconds (optional)
        
        Returns:
            ElementHandle: The element handle
        """
        timeout = timeout or self.timeout
        try:
            element = await self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return element
        except PWTimeoutError:
            print(f"✗ Timeout waiting for element: {selector}")
            raise
    
    async def click_element(self, selector, timeout=None):
        """
        Click an element by selector.
        
        Args:
            selector (str): CSS selector for the element
            timeout (int): Timeout in milliseconds (optional)
        """
        timeout = timeout or self.timeout
        try:
            await self.wait_for_element(selector, timeout)
            await self.page.click(selector)
            print(f"✓ Clicked element: {selector}")
        except PWTimeoutError:
            print(f"✗ Timeout waiting to click element: {selector}")
            raise
    
    async def fill_input(self, selector, value, timeout=None):
        """
        Fill an input field.
        
        Args:
            selector (str): CSS selector for the input
            value (str): Value to fill
            timeout (int): Timeout in milliseconds (optional)
        """
        timeout = timeout or self.timeout
        try:
            await self.wait_for_element(selector, timeout)
            await self.page.fill(selector, str(value))
            print(f"✓ Filled input {selector} with value: {value}")
        except PWTimeoutError:
            print(f"✗ Timeout waiting to fill input: {selector}")
            raise
    
    async def select_radio_button(self, selector, timeout=None):
        """
        Select a radio button.
        
        Args:
            selector (str): CSS selector for the radio button
            timeout (int): Timeout in milliseconds (optional)
        """
        timeout = timeout or self.timeout
        try:
            await self.wait_for_element(selector, timeout)
            await self.page.check(selector)
            print(f"✓ Selected radio button: {selector}")
        except PWTimeoutError:
            print(f"✗ Timeout waiting to select radio button: {selector}")
            raise
    
    async def click_popup_button_by_value(self, button_value, timeout=10000):
        """
        Click popup buttons by their value.
        
        Args:
            button_value (str): Value of the button to click
            timeout (int): Timeout in milliseconds
        """
        try:
            button_selector = f'input[type="button"][value="{button_value}"].r-btn-pop'
            await self.page.wait_for_selector(button_selector, state="visible", timeout=timeout)
            await self.page.click(button_selector)
            print(f"✓ Clicked popup button: {button_value}")
            # Wait a moment for popup to close
            await self.page.wait_for_timeout(1000)
        except PWTimeoutError:
            print(f"✗ Timeout waiting for popup button: {button_value}")
            raise
    
    async def fill_numeric_input(self, selector, value, timeout=None):
        """
        Fill numeric Kendo input fields.
        
        Args:
            selector (str): CSS selector for the input
            value (int/float): Numeric value to fill
            timeout (int): Timeout in milliseconds (optional)
        """
        timeout = timeout or self.timeout
        try:
            element = await self.wait_for_element(selector, timeout)
            await element.focus()
            await self.page.keyboard.press("Control+a")  # Select all existing text
            await self.page.keyboard.type(str(value))
            print(f"✓ Filled numeric input {selector} with value: {value}")
        except PWTimeoutError:
            print(f"✗ Timeout waiting for numeric input: {selector}")
            raise
    
    async def select_kendo_dropdown_by_cage(self, cage_number, option_text):
        """
        Select option from Kendo dropdown by cage number.
        
        Args:
            cage_number (str): Cage number for the dropdown
            option_text (str): Text of the option to select
        """
        try:
            # Find the dropdown by cage number
            dropdown_selector = f'select[data-cage="{cage_number}"]'
            await self.wait_for_element(dropdown_selector)
            
            # Select the option
            option_selector = f'{dropdown_selector} option:has-text("{option_text}")'
            await self.page.select_option(dropdown_selector, option_text)
            print(f"✓ Selected dropdown option for cage {cage_number}: {option_text}")
        except Exception as e:
            print(f"✗ Error selecting dropdown for cage {cage_number}: {e}")
            raise
    
    async def fill_text_by_cage(self, cage_number, text_value):
        """
        Fill text input by cage number.
        
        Args:
            cage_number (str): Cage number for the input
            text_value (str): Text value to fill
        """
        try:
            # Find the input by cage number
            input_selector = f'input[data-cage="{cage_number}"]'
            await self.fill_input(input_selector, text_value)
            print(f"✓ Filled text input for cage {cage_number}: {text_value}")
        except Exception as e:
            print(f"✗ Error filling text for cage {cage_number}: {e}")
            raise
    
    async def fill_kendo_numeric_by_cage(self, cage_number, numeric_value):
        """
        Fill Kendo numeric input by cage number.
        
        Args:
            cage_number (str): Cage number for the input
            numeric_value (int/float): Numeric value to fill
        """
        try:
            # Find the input by cage number
            input_selector = f'input[data-cage="{cage_number}"]'
            await self.fill_numeric_input(input_selector, numeric_value)
            print(f"✓ Filled numeric input for cage {cage_number}: {numeric_value}")
        except Exception as e:
            print(f"✗ Error filling numeric for cage {cage_number}: {e}")
            raise
    
    async def click_topmost_dialog_button(self, label, timeout=12000):
        """
        Click a button in the topmost visible Kendo dialog.
        
        Args:
            label (str): Label of the button to click
            timeout (int): Timeout in milliseconds
        """
        try:
            # Handle native confirm dialogs
            self.page.once("dialog", lambda d: d.accept())
            
            # Find the topmost dialog
            dialog_selector = ".k-window:visible, div[role='dialog']:visible"
            dialog = self.page.locator(dialog_selector).last
            
            # Wait for dialog to be visible
            await dialog.wait_for(state="visible", timeout=timeout)
            
            # Click the button
            button_selector = f"input[value='{label}'], button:has-text('{label}')"
            await dialog.locator(button_selector).click()
            
            print(f"✓ Clicked dialog button: {label}")
            
        except PWTimeoutError:
            print(f"✗ Timeout waiting for dialog button: {label}")
            raise
    
    async def wait_for_page_load(self):
        """Wait for page to load completely."""
        try:
            await self.page.wait_for_load_state("networkidle")
            print(f"✓ {self.component_name} page loaded successfully")
        except Exception as e:
            print(f"✗ Error waiting for page load: {e}")
            raise
    
    def log_info(self, message):
        """Log information message."""
        print(f"📝 [{self.component_name}] {message}")
    
    def log_success(self, message):
        """Log success message."""
        print(f"✅ [{self.component_name}] {message}")
    
    def log_error(self, message):
        """Log error message."""
        print(f"❌ [{self.component_name}] {message}")
    
    def log_warning(self, message):
        """Log warning message."""
        print(f"⚠️ [{self.component_name}] {message}")
