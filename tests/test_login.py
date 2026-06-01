import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage
from utils.logger import LogGen

@pytest.mark.login
class TestLogin:
    @pytest.mark.smoke
    def test_successful_login(self, login_page, page):
        """Verifies that a user can successfully authenticate with valid credentials."""
        ip = InventoryPage(page)
        # Execute actions via the Page Object
        login_page.login("standard_user", "secret_sauce")
        # Assert conditions using Playwright's web-first 'expect' assertions
        expect(login_page.flash_message).to_be_hidden()
        ip.assert_product_section()

    @pytest.mark.regression
    @pytest.mark.skip_browser("webkit")
    # @pytest.mark.only_browser("chromium")
    def test_invalid_login(self, login_page, page):
        """Verifies that clear error messaging is displayed for invalid credentials."""
        login_page.login("invalid_user", "invalid_password")
        expect(login_page.flash_message).to_be_visible()
        # page.pause()
        expect(login_page.flash_message).to_contain_text("Username and password do not match any user in this service")
        # To hit single keystroke
        # modification shortcuts are also supported: Shift, Control, Alt, Meta
        login_page.password_input.press("Enter")
        login_page.password_input.press("Control+ArrowRight")
        login_page.login_button.focus()
        # Drag the source element towards the target element and drop it
        login_page.login_button.drag_to(login_page.password_input)
        # Returns the element.innerHTML
        self.logger.warning(f"Inner html = {login_page.login_logo.inner_html()}")
        # To upload a file
        # login_page.login_button.set_input_files('files/log3.pdf')
        # login_page.login_button.set_input_files(['files/log1.txt', 'files/log2.txt'])
        # login_page.login_button.set_input_files('files')
        # login_page.login_button.set_input_files([])