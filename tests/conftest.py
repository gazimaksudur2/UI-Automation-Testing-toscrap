import os
import random
import secrets

import pytest
from playwright.sync_api import Browser

from pages.books_home_page import BooksHomePage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def five_random_books(
    browser: Browser,
    browser_context_args: dict,
) -> list[str]:
    context = browser.new_context(**browser_context_args)
    try:
        page = context.new_page()
        home = BooksHomePage(page)
        home.navigate()

        titles = list(dict.fromkeys(home.get_book_titles()))
        assert len(titles) >= 5, "Not enough books available"

        seed = int(
            os.getenv("BOOK_SAMPLE_SEED") or secrets.randbits(32)
        )

        print(f"\nRandom seed: {seed}")
        return random.Random(seed).sample(titles, 5)

    finally:
        context.close()
