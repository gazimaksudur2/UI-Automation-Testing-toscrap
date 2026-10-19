from playwright.sync_api import Page

from pages.quotes_home_page import QuotesHomePage
from pages.quotes_login_page import QuotesLoginPage


def test_quotes_login_and_logout_link(page: Page) -> None:
    """Verify login functionality and autheticated logout link."""

    home = QuotesHomePage(page)
    login = QuotesLoginPage(page)

    home.navigate()

    home.open_login_page()
    login.verify_login_page()

    login.login("User Name", "demopassword")
    home.verify_authenticated()
