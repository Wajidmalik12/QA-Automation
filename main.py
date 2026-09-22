from browser import inspect_website, detect_login
from auth import get_test_credentials,login
from LLm import analyze_website
from test import run_tests
from report import generate_csv_report


url = input("Enter website URL: ")

playwright, browser, page, page_text, links = inspect_website(url)

login_exists = detect_login(page)
if login_exists:
    print("\n🔐 LOGIN SYSTEM DETECTED")
    username, password = get_test_credentials()
    login_success, login_message = login(
        page,
        username,
        password
    )

    if login_success:

        print(f"\n[PASS] LOGIN - {login_message}")
        print("\n--- AUTHENTICATED WEBSITE ---")

    else:

        print(f"\n[FAIL] LOGIN - {login_message}")
        print("\nLOGIN SYSTEM / CREDENTIAL CHECK FAILED")
        print("Normal QA tests stopped.")

        browser.close()
        playwright.stop()
        exit()
else:

    print("\nNo login system detected")

page_text = page.locator("body").inner_text()

print("\n--- WEBSITE READY FOR QA ---")

print("\n--- AI QA ANALYSIS ---")

tests = analyze_website(page_text, links)


if tests:

    for i, test in enumerate(tests["tests"], start=1):

        print(f"\nTEST {i}")
        print("Name:", test["name"])
        print("Type:", test["type"])
        print("Target:", test["target"])
        print("Expected:", test["expected"])


    print("\n--- RUNNING TESTS ---")

    results = run_tests(
        page,
        tests["tests"],
        url
    )
    for result in results:

        print(
            f"[{result['status']}] "
            f"{result['name']} - "
            f"{result['message']}"
        )

    generate_csv_report(
        tests["tests"],
        results
    )


browser.close()
playwright.stop()