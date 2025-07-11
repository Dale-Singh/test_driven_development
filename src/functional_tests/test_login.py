# Standard library
import re  # For regex-based pattern matching

# Django
from django.core import mail  # Access Django's test email outbox

# Third-party (Selenium)
from selenium.webdriver.common.by import By  # Strategies for locating page elements
from selenium.webdriver.common.keys import Keys  # Simulate keyboard input (e.g., Enter, Backspace)

# Local application
from .base import FunctionalTest  # Base class for shared functional test setup

TEST_EMAIL = "edith@example.com"
SUBJECT = "Your login link for Superlists"

class LoginTest(FunctionalTest):
    def test_login_using_magic_link(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(
            TEST_EMAIL, Keys.ENTER
        )

        # A message appears telling her an email has been sent
        self.wait_for(
            lambda: self.assertIn(
                "Check your email",
                self.browser.find_element(By.CSS_SELECTOR, "body").text,
            )
        )

        if self.test_server:
            # Testing real email sending from the server is not worth it.
            return

        # She checks her email and finds a message
        email = mail.outbox.pop()
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a URL link in it
        self.assertIn("Use this link to log in", email.body)
        url_search = re.search(r"http://.+/.+$", email.body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # she clicks it
        self.browser.get(url)

        # she is logged in!
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # Now she logs out
        self.browser.find_element(By.CSS_SELECTOR, "#id_logout").click()

        # She is logged out
        self.wait_to_be_logged_out(email=TEST_EMAIL)
