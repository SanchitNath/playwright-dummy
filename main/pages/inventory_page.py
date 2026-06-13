from playwright.sync_api import Page, expect

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        # Define locators using Playwright's recommended locator strategies
        self.title = page.locator(".app_logo")
        self.shopping_cart_icon = page.locator(".shopping_cart_link")
        self.products = page.locator(".title")
        self.filter = page.locator("//option[@value='az']")
        self.footer = page.locator(".social")
        self.list_to_add = ['Sauce Labs Backpack', 'Sauce Labs Bike Light', 'Sauce Labs Onesie']

    def assert_product_section(self):
        """Assert the product page"""
        self.title.click(force=True)
        expect(self.shopping_cart_icon).to_be_enabled()
        expect(self.products).to_be_visible()
        expect(self.filter).to_have_text("Name (A to Z)")
        expect(self.filter).to_contain_text("Name")
        self.footer.scroll_into_view_if_needed()

