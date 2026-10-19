from urllib.parse import urldefrag, urljoin, urlsplit


def get_unique_urls(base_url: str, hrefs: list[str]) -> list[str]:
    urls = {
        urldefrag(urljoin(base_url, href.strip())).url
        for href in hrefs
        if href is not None
    }
    return sorted(
        url for url in urls
        if urlsplit(url).scheme in ("http", "https")
    )
