from urllib.parse import urljoin
def run_content_test(page, test):
    target = test["target"]

    try:
        locator = page.get_by_text(target, exact=False)

        if locator.count() > 0:
            return {
                "name": test["name"],
                "status": "PASS",
                "message": f"Found: {target}"
            }

        return {
            "name": test["name"],
            "status": "FAIL",
            "message": f"Could not find: {target}"
        }

    except Exception as e:
        return {
            "name": test["name"],
            "status": "FAIL",
            "message": str(e)
        }


def run_link_test(page, test):
    target = test["target"]

    try:
        link = page.get_by_role("link", name=target).first

        if link.count() == 0:
            return {
                "name": test["name"],
                "status": "FAIL",
                "message": f"Link not found: {target}"
            }

        actual_href = link.get_attribute("href")
        expected_href = test.get("href")

        if not actual_href:
            return {
                "name": test["name"],
                "status": "FAIL",
                "message": f"Link has no href: {target}"
            }

        if expected_href and actual_href != expected_href:
            return {
                "name": test["name"],
                "status": "FAIL",
                "message": (
                    f"Expected href: {expected_href} | "
                    f"Actual href: {actual_href}"
                )
            }

        return {
            "name": test["name"],
            "status": "PASS",
            "message": f"{target} -> {actual_href}"
        }

    except Exception as e:
        return {
            "name": test["name"],
            "status": "FAIL",
            "message": str(e)
        }


def run_navigation_test(page, test, base_url):
    target = test["target"]

    try:
        # Always start navigation tests from the original website
        page.goto(base_url, wait_until="domcontentloaded")

        link = page.get_by_role("link", name=target).first

        if link.count() == 0:
            return {
                "name": test["name"],
                "status": "FAIL",
                "message": f"Navigation link not found: {target}"
            }

        href = link.get_attribute("href")

        if not href:
            return {
                "name": test["name"],
                "status": "FAIL",
                "message": f"Navigation link has no href: {target}"
            }

        expected_url = urljoin(base_url, href)

        with page.expect_navigation(wait_until="domcontentloaded"):
            link.click()

        actual_url = page.url

        if actual_url == expected_url:
            return {
                "name": test["name"],
                "status": "PASS",
                "message": f"Navigated successfully to {actual_url}"
            }

        return {
            "name": test["name"],
            "status": "FAIL",
            "message": (
                f"Expected URL: {expected_url} | "
                f"Actual URL: {actual_url}"
            )
        }

    except Exception as e:
        return {
            "name": test["name"],
            "status": "FAIL",
            "message": str(e)
        }


def run_tests(page, tests, base_url):

    results = []

    for test in tests:

        if test["type"] == "content":
            result = run_content_test(page, test)

        elif test["type"] == "link":
            result = run_link_test(page, test)

        elif test["type"] == "navigation":
            result = run_navigation_test(page, test, base_url)

        else:
            continue

        result["type"] = test["type"]

        results.append(result)

    return results