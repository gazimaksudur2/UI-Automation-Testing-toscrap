from playwright.sync_api import Page, expect


def test_browser_environment(page: Page):
    response = page.goto(
        "https://books.toscrape.com/index.html"
    )

    assert response is not None
    assert response.status == 200

    expect(
        page.locator("article.product_pod").first
    ).to_be_visible()
