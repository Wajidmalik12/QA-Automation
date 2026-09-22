from playwright.sync_api import sync_playwright


def inspect_website(url):

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(url, wait_until="domcontentloaded")

    print("\n--- WEBSITE INFORMATION ---")
    print("URL:", page.url)
    print("TITLE:", page.title())

    page_text = page.locator("body").inner_text()

    print("\n--- PAGE TEXT ---")
    print(page_text[:3000])

    links = []

    for i in range(page.locator("a").count()):
        link = page.locator("a").nth(i)

        text = link.inner_text().strip()
        href = link.get_attribute("href")

        if text and href:
            links.append({
                "text": text,
                "href": href
            })

    print("\n--- LINKS ---")

    for i, link in enumerate(links, start=1):
        print(f"{i}. {link['text']} -> {link['href']}")

    return playwright, browser, page, page_text, links

def detect_login(page):

    login_keywords = [
        "login",
        "log in",
        "sign in",
        "signin"
    ]

    page_text = page.locator("body").inner_text().lower()

    for keyword in login_keywords:
        if keyword in page_text:
            return True

    # Also check common login links/buttons
    elements = page.locator("a, button")

    for i in range(elements.count()):
        text = elements.nth(i).inner_text().strip().lower()

        for keyword in login_keywords:
            if keyword in text:
                return True

    return False