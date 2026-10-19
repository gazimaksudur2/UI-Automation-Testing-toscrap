from playwright.sync_api import Page, expect


class QuotesLoginPage:
    """Page object for the Quotes to Scrape login form"""

    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.submit_button = page.locator("input[value='Login']")

    def verify_login_page(self) -> None:
        expect(self.page).to_have_url(
            "https://quotes.toscrape.com/login"
        )
        expect(self.username).to_be_visible()
        expect(self.password).to_be_visible()
        expect(self.submit_button).to_be_enabled()

    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)

        expect(self.username).to_have_value(username)
        expect(self.password).to_have_value(password)

        self.submit_button.click()
