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

    def get_book_titles(self) -> list[str]:
        links = self.book_cards.locator("h3 a")
        titles = [link.get_attribute("title") for link in links.all()]
        return [title for title in titles if title]

    def open_book_by_title(self, title: str) -> None:
        links = self.book_cards.locator("h3 a")

        for link in links.all():
            if link.get_attribute("title") == title:
                link.click()
                return

        raise ValueError(f"Book not found: {title}")
