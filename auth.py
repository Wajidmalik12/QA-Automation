from getpass import getpass


def get_test_credentials():

    print("\n--- LOGIN CREDENTIALS ---")

    username = input("Test username/email: ")
    password = getpass("Test password: ")

    return username, password


def login(page, username, password):

    print("\n--- TESTING LOGIN ---")

    try:
        # Find username/email field
        username_field = page.locator(
            "input[type='email'], "
            "input[type='text'], "
            "input[name*='user'], "
            "input[name*='email']"
        ).first

        # Find password field
        password_field = page.locator(
            "input[type='password']"
        ).first

        if username_field.count() == 0:
            return False, "Username/email field not found"

        if password_field.count() == 0:
            return False, "Password field not found"

        username_field.fill(username)
        password_field.fill(password)

        # Find login button
        login_button = page.get_by_role(
            "button",
            name=lambda text: any(
                word in text.lower()
                for word in ["login", "log in", "sign in", "signin"]
            )
        ).first

        # Some websites use an input instead of a button
        if login_button.count() == 0:

            login_button = page.locator(
                "input[type='submit'], "
                "button[type='submit']"
            ).first

        if login_button.count() == 0:
            return False, "Login button not found"

        old_url = page.url

        login_button.click()

        page.wait_for_load_state("domcontentloaded")

        # Basic success checks
        if page.url != old_url:
            return True, f"Login successful. New URL: {page.url}"

        # If login form disappeared, consider authentication successful
        if password_field.count() == 0:
            return True, "Login successful. Login form disappeared"

        return False, "Login was not successful. Please check credentials"

    except Exception as e:

        return False, f"Login test error: {str(e)}"