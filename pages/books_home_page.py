from playwright.sync_api import Page
from config.settings import BOOKS_HOME_URL


class BooksHomePage:
    def __init__(self, page: Page):
        self.page = page
        self.book_cards = page.locator("article.product_pod")
        self.headings = page.locator("h1, h2, h3, h4, h5, h6")
        self.books_section = page.locator("section:has(article.product_pod)")

    def navigate(self) -> None:
        self.page.goto(BOOKS_HOME_URL)

    def get_book_count(self) -> int:
        return self.book_cards.count()
