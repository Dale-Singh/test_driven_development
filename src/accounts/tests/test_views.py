# Standard library
from unittest import mock  # Tools for creating mock objects to isolate and test behavior in controlled scenarios

# Django
from django.test import TestCase  # Base test case class for writing unit tests with Django test utilities
from django.contrib import auth # Django's authentication system (e.g., login, logout, authenticate)

# Local applications
import accounts.views  # Import the accounts.views module so we can mock the send_mail function defined there
from accounts.models import Token # Import the Token model used to create and retrieve login tokens


# Tests for the send_login_email view in accounts/views.py
class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        # Simulates a POST request to send a login email and checks that the user is redirected to the homepage
        response = self.client.post(
            "/accounts/send_login_email",  # URL for submitting login email
            data={"email": "edith@example.com"}  # Simulated POST form data
        )
        # The view should respond with a redirect to the home page after processing
        self.assertRedirects(response, "/")

    @mock.patch("accounts.views.send_mail")  # Replaces send_mail with a mock object for the duration of the test - mock_send_email
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        # This test verifies that an email is sent to the correct address with the expected content

        # Simulate submitting the login email form
        self.client.post(
            "/accounts/send_login_email", 
            data={"email": "edith@example.com"}
        )

        # Check that the mocked send_mail function was actually called
        self.assertEqual(mock_send_mail.called, True)

        # Extract the arguments the mocked send_mail was called with
        # mock_send_mail.call_args is a tuple: ((args...), {kwargs...})
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args

        # Assert the subject line is correct
        self.assertEqual(subject, "Your login link for Superlists")

        # Assert the from address is the expected "noreply" sender
        self.assertEqual(from_email, "superlistsdalesingh@gmail.com")

        # Assert the recipient list includes the submitted email
        self.assertEqual(to_list, ["edith@example.com"])
    
    def test_adds_success_message(self):
        # Verifies that a success message is displayed after sending a login email
        response = self.client.post(
            "/accounts/send_login_email",
            data={"email": "edith@example.com"},
            follow=True,
        )

        # Extract the first message from the response context's messages framework
        message = list(response.context["messages"])[0]

        # Check that the correct success message was added
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in."
        )

        # Check that the message has the 'success' tag for styling purposes
        self.assertEqual(message.tags, "success")
    
    def test_creates_token_associated_with_email(self):
        # This test verifies that submitting an email via POST creates a Token associated with that email
        self.client.post(
            "/accounts/send_login_email", data={"email": "edith@example.com"}
        )

        # Retrieves the token that should have been created for the given email
        token = Token.objects.get()
        # Asserts that the token's email matches the submitted email
        self.assertEqual(token.email, "edith@example.com")

    @mock.patch("accounts.views.send_mail") # Replaces send_mail with a mock object for the duration of the test - mock_send_mail
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        # Verifies that the email body includes a login URL containing the correct token UID
        self.client.post(
            "/accounts/send_login_email", data={"email": "edith@example.com"}
        )

        # Retrieves the token created during the request
        token = Token.objects.get()

        # Constructs the expected login URL with the token UID
        expected_url = f"http://testserver/accounts/login?token={token.uid}"

        # Retrieves the arguments with which send_mail was called
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args

        # Asserts that the body of the email includes the login URL with the token
        self.assertIn(expected_url, body)

# Tests for the login view in accounts/views.py
class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self):
        # Simulates a GET request with a token in the URL and checks redirection to the homepage
        response = self.client.get("/accounts/login?token=abcd123")
        self.assertRedirects(response, "/")

    def test_logs_in_if_given_valid_token(self):
        # Verifies that a user is logged in when a valid token is provided in the URL

        # Before login: ensure the client is anonymous
        anon_user = auth.get_user(self.client)
        self.assertEqual(anon_user.is_authenticated, False)

        # Create a token for a specific email
        token = Token.objects.create(email="edith@example.com")

        # Simulate a login request using the token
        self.client.get(f"/accounts/login?token={token.uid}")

        # After login: retrieve the user and check that they are authenticated
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.email, "edith@example.com")
    
    def test_shows_login_error_if_token_invalid(self):
        # Verifies that an invalid token results in no login and an appropriate error message is displayed
        response = self.client.get("/accounts/login?token=invalid-token", follow=True)

        # Verifies that no user is logged in
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)

        # Checks that an error message is displayed to the user
        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Invalid login link, please request a new one",
        )
        self.assertEqual(message.tags, "error")
    
    @mock.patch("accounts.views.auth")  # Replaces the 'auth' module in accounts.views with a mock object during the test
    def test_calls_django_auth_authenticate(self, mock_auth):
        # Verifies that the login view extracts the token from the URL and passes it to the authentication system
        self.client.get("/accounts/login?token=abcd123")

        # Verifies that auth.authenticate() was called with the correct UID
        self.assertEqual(
            mock_auth.authenticate.call_args,  # Captures the arguments passed to mock_auth.authenticate
            mock.call(uid="abcd123"),          # Asserts it was called with uid="abcd123"
        )



