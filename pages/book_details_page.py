from playwright.sync_api import Page


class BookDetailsPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator(".product_main h1")
        self.product_info = page.locator("table.table-striped")