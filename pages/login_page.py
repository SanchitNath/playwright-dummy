import re

from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        # Define locators using Playwright's recommended locator strategies
        self.login_logo = page.locator(".login_logo")
        self.username_input = page.locator("id=user-name")
        self.password_input = page.locator("#password, [name='password']")
        self.login_button = page.locator("[type='submit']")
        self.flash_message = page.locator("[data-test='error']")

    def assert_navigation(self):
        """Assert the navigation flow to the application website."""
        expect(self.page).to_have_url('https://www.saucedemo.com/')
        expect(self.page).to_have_title(re.compile("Swag Labs"))

    def login(self, username, password):
        """Executes the login workflow sequential steps."""
        expect(self.login_logo).to_have_text("Swag Labs")
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.username_input).to_be_enabled()
        expect(self.password_input).to_be_enabled()
        expect(self.username_input).to_have_count(1)
        expect(self.password_input).to_have_count(1)
        self.username_input.fill(username)
        self.password_input.fill(password)
        expect(self.username_input).to_have_value(username)
        expect(self.password_input).to_have_value(password)
        self.login_button.click()
