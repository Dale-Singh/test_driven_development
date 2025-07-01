# Django
from django.conf import settings # Access to Django project settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model # Tools for session-based authentication
from django.contrib.sessions.backends.db import SessionStore # Manages session data using the database backend

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

    def test_logged_in_user_lists_are_saved_as_my_lists(self):
        email = "edith@example.com"
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Simulate login
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
