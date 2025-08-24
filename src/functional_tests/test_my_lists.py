# Django
from django.conf import settings # Access to Django project settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model # Tools for session-based authentication
from django.contrib.sessions.backends.db import SessionStore # Manages session data using the database backend

# Selenium
from selenium.webdriver.common.by import By  # Strategies for locating elements on a web page

# Local application
from .base import FunctionalTest # Base class for functional tests with custom setup/teardown
from .container_commands import create_session_on_server  # Utility to trigger remote session creation on staging server
from .management.commands.create_session import create_pre_authenticated_session  # Function to manually create a session locally

class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        # Create a session on the appropriate server (local or remote)
        if self.test_server:
            session_key = create_session_on_server(self.test_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        # Set session cookie by visiting a dummy page first (required by browser)
        self.browser.get(self.live_server_url + "/404_no_such_url")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path="/"
            )
        )
    
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session("edith@example.com")

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item("Reticulate splines")
        self.add_list_item("Immanentize eschaton")
        first_list_url = self.browser.current_url

        # She notices a "My lists" link, for the first time.
        self.browser.find_element(By.LINK_TEXT, "My lists").click()

        # She sees her email is there in the page heading
        self.wait_for(
            lambda: self.assertIn(
                "edith@example.com",
                self.browser.find_element(By.CSS_SELECTOR, "h1").text,
            )
        )

        # And she sees that her list is in there,
        # named according to its first list item
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, "Reticulate splines")
        )
        self.browser.find_element(By.LINK_TEXT, "Reticulate splines").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item("Click cows")
        second_list_url = self.browser.current_url

        # Under "my lists", her new list appears
        self.browser.find_element(By.LINK_TEXT, "My lists").click()
        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, "Click cows"))
        self.browser.find_element(By.LINK_TEXT, "Click cows").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out.  The "My lists" option disappears
        self.browser.find_element(By.CSS_SELECTOR, "#id_logout").click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements(By.LINK_TEXT, "My lists"),
                [],
            )
        )