from playwright.sync_api import Locator, Page

from config.settings import BOOKS_HOME_URL


class BooksHomePage:
    def __init__(self, page: Page):
        self.page = page
        self.book_cards = page.locator("article.product_pod")
        self.headings = page.locator("h1, h2, h3, h4, h5, h6")
        self.books_section = page.locator("section:has(article.product_pod)")
        self.product_images = page.locator("article.product_pod img")
        self.next_button = page.locator("li.next a")

    def navigate(self) -> None:
        self.page.goto(BOOKS_HOME_URL)

    def get_book_count(self) -> int:
        return self.book_cards.count()

    def get_book_titles(self) -> list[str]:
        links = self.book_cards.locator("h3 a")
        titles = [link.get_attribute("title") for link in links.all()]
        return [title for title in titles if title]

    def open_book_by_title(self, title: str) -> None:
        card = self.get_book_card(title)
        card.locator("h3 a").click()

    def get_book_card(self, title: str) -> Locator:
        for card in self.book_cards.all():
            if card.locator("h3 a").get_attribute("title") == title:
                return card
        raise ValueError(f"Book not found: {title}")

    def get_book_data(self, title: str) -> tuple[str, str]:
        card = self.get_book_card(title)
        book_title = card.locator("h3 a").get_attribute("title")
        book_price = card.locator(".price_color").inner_text().strip()

        if not book_title:
            raise ValueError("Book title is empty")
        return book_title, book_price

    def get_all_hrefs(self) -> list[str]:
        return self.page.locator("a[href]").evaluate_all(
            "(elements) => elements.map(el => el.getAttribute('href'))"
        )

    def get_product_images(self):
        return self.product_images.all()

    def has_next_page(self) -> bool:
        return self.next_button.count() > 0

    def go_to_next_page(self) -> None:
        self.next_button.click()
