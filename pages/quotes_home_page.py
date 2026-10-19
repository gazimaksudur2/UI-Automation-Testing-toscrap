from playwright.sync_api import Page, expect

from config.settings import QUOTES_HOME_URL


class QuotesHomePage:
    """Page object for the Quotes to Scrape homepage"""

    def __init__(self, page: Page):
        self.page = page
        self.login_link = page.get_by_role("link", name="Login")
        self.logout_link = page.get_by_role("link", name="Logout")

    def navigate(self) -> None:
        """Navigate to the Quotes to Scrape hompage and verify it loads."""
        response = self.page.goto(QUOTES_HOME_URL)
        assert response is not None and response.ok, "Failed to load Quotes homepage"
        expect(self.page).to_have_url(QUOTES_HOME_URL)

    def open_login_page(self) -> None:
        expect(self.login_link).to_be_visible()
        expect(self.login_link).to_be_enabled()
        self.login_link.click()

    def verify_authenticated(self) -> None:
        expect(self.page).to_have_url(QUOTES_HOME_URL)
        expect(self.logout_link).to_be_visible()
        expect(self.logout_link).to_be_enabled()
