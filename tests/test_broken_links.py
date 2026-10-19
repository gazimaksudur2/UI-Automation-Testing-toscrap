from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, Playwright

from pages.books_home_page import BooksHomePage
from utils.url_utils import get_unique_urls


def test_homepage_links(
        page: Page,
        playwright: Playwright,
        browser_context_args: dict,
):
    home = BooksHomePage(page)
    home.navigate()

    hrefs = home.get_all_hrefs()
    urls = get_unique_urls(page.url, hrefs)

    assert urls, "No HTTP links found"
    api = playwright.request.new_context(
        ignore_https_errors=browser_context_args.get(
            "ignore_http_errors", False
        )
    )

    failures = []
    try:
        for url in urls:
            try:
                response = api.get(url, timeout=2000)
                if response.status != 200:
                    failures.append(f"{response.status}: {url}")
            except PlaywrightError as exc:
                failures.append(f"{url}: {exc}")
    finally:
        api.dispose()

    assert not failures, (
        "Broken Links Found:\n" + "\n".join(failures)
    )
