from playwright.sync_api import Page, expect

from config.settings import BOOKS_HOME_URL
from pages.books_home_page import BooksHomePage


def test_homepage_validation(page: Page):
    home = BooksHomePage(page)
    home.navigate()

    expect(page).to_have_url(BOOKS_HOME_URL)
    expect(page).to_have_title("All products | Books to Scrape - Sandbox")

    visible_headings = [
        heading for heading in home.headings.all()
        if heading.is_visible()
    ]

    assert visible_headings, "NO visible headings found"

    for heading in visible_headings:
        expect(heading).to_be_visible()
        assert heading.inner_text().strip(), "Empty heading found"

    expect(home.books_section).to_be_visible()
    assert home.get_book_count() > 0
