from playwright.sync_api import Page, expect

from pages.books_home_page import BooksHomePage


def test_product_images_and_pagination(page: Page) -> None:
    home = BooksHomePage(page)
    home.navigate()

    max_pages = 5
    total_images = 0

    for page_number in range(1, max_pages + 1):
        images = home.get_product_images()

        assert images, f"No product images found on page {page_number}"
        for index, image in enumerate(images, start=1):
            expect(image).to_be_visible()
            src = image.get_attribute("src")
            alt = image.get_attribute("alt")
            classes = (image.get_attribute("class") or "").split()

            assert src and src.strip(), (
                f"Image {index} has an empty src on page {page_number}"
            )

            assert alt and alt.strip(), (
                f"Image {index} has an empty alt on page {page_number}"
            )
            assert "thumbnail" in classes, (
                f"Image {index} is missing thumbnail class "
                f"on page {page_number}"
            )

            total_images += 1

        print(
            f"Page {page_number}: "
            f"{len(images)} product images validated"
        )
        if page_number == max_pages or not home.has_next_page():
            break

        previous_url = page.url
        home.go_to_next_page()
        expect(page).not_to_have_url(previous_url)

    print(f"Total validated images: {total_images}")
