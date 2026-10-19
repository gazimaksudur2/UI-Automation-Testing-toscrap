import re

import pytest
from playwright.sync_api import Page, expect

from config.settings import BOOKS_HOME_URL
from pages.book_details_page import BookDetailsPage
from pages.books_home_page import BooksHomePage


@pytest.mark.parametrize("book_index", range(5))
def test_random_book_navigation(
    page: Page,
    five_random_books: list[str],
    book_index: int
):
    book_title = five_random_books[book_index]
    home = BooksHomePage(page)
    details = BookDetailsPage(page)

    home.navigate()
    home.open_book_by_title(book_title)

    expect(page).to_have_url(
        re.compile(r"/catalogue/[^/]+/index\.html$")
    )
    expect(details.title).to_have_text(book_title)
    expect(details.product_info).to_be_visible()

    assert details.product_info.locator("tr").count() > 0

    page.go_back()
    expect(page).to_have_url(BOOKS_HOME_URL)
