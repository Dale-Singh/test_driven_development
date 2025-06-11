# Django imports
from django.contrib.auth import get_user_model  # Retrieves the user model defined in settings (custom or default)
from django.http import HttpRequest  # Used to simulate an HTTP request in tests
from django.test import TestCase  # Base test case class for writing unit tests

# Local applications
from accounts.authentication import PasswordlessAuthenticationBackend  # Custom authentication backend for passwordless login
from accounts.models import Token, User  # Token model used for authentication

# Get the current user model class (defined in settings - AUTH_USER_MODEL)
User = get_user_model()

# Tests for the custom passwordless authentication backend
class AuthenticateTest(TestCase):

    def test_returns_none_if_no_such_token(self):
        # Returns None if no token matches the given UID
        result = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(), "no-such-token"
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        # Creates a token and authenticates using its UID, ensuring a new user is created with the correct email
        email = "edith@example.com"
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(), token.uid
        )

        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)
    
    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        # If a user with the token's email already exists, authenticating with that token should return the existing user
        email = "edith@example.com"
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(
            HttpRequest(), token.uid
        )
        self.assertEqual(user, existing_user)


# Tests for retrieving users by email using the custom authentication backend
class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        # Retrieves a user by email when the user exists
        User.objects.create(email="another@example.com")
        desired_user = User.objects.create(email="edith@example.com")
        found_user = PasswordlessAuthenticationBackend().get_user("edith@example.com")
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        # Returns None when no user with the given email exists
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user("edith@example.com")
        )