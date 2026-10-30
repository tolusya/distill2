import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
}


def fetch_static(url, selector):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.select(selector)
    if not elements:
        raise ValueError(f"Селектор '{selector}' ничего не нашёл на {url}")

    return "\n\n".join(el.get_text("\n", strip=True) for el in elements)


def fetch_rendered(url, selector):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector(selector, timeout=30000)
        page.wait_for_load_state("networkidle")
        text = page.inner_text(selector)
        browser.close()
    return text


if __name__ == "__main__":
    rq = fetch_static(
        "https://rosenberg-quartier.de/apartments-wohnungen/student-apartments",
        'table[id^="reos-"]',
    )
    print("=== Rosenberg ===")
    print(rq[:500])

    hn = fetch_rendered(
        "https://www.apartments-hn.de/en/book-apartment/",
        "table.book-property__table",
    )
    print("=== HN ===")
    print(hn[:500])
