import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_successful_login(login_page):
    """Verifies that a user can successfully authenticate with valid credentials."""
    # Execute actions via the Page Object
    login_page.login("standard_user", "secret_sauce")
    # Assert conditions using Playwright's web-first 'expect' assertions
    expect(login_page.flash_message).to_be_hidden()


@pytest.mark.regression
def test_invalid_login(login_page):
    """Verifies that clear error messaging is displayed for invalid credentials."""
    login_page.login("invalid_user", "invalid_password")
    expect(login_page.flash_message).to_be_visible()
    expect(login_page.flash_message).to_contain_text("Username and password do not match any user in this service")
