import pytest
from playwright.sync_api import Page, expect

from config.settings import BOOKS_HOME_URL
from pages.book_details_page import BookDetailsPage
from pages.books_home_page import BooksHomePage


@pytest.mark.parametrize("book_index", range(5))
def test_book_data_consistency(
    page: Page,
    five_random_books: list[str],
    book_index: int,
):
    selected_title = five_random_books[book_index]
    home = BooksHomePage(page)
    details = BookDetailsPage(page)

    home.navigate()
    home_title, home_price = home.get_book_data(selected_title)
    home.open_book_by_title(selected_title)

    expect(details.title).to_have_text(home_title)
    expect(details.price).to_have_text(home_price)

    page.go_back()
    expect(page).to_have_url(BOOKS_HOME_URL)