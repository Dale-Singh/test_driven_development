# Django
from django.contrib.auth import get_user_model  # Retrieves the user model defined in settings (custom or default)
from django.test import TestCase  # Base test case class for writing unit tests

# Local applications
from accounts.models import Token

# Get the current user model class (defined in settings - AUTH_USER_MODEL)
User = get_user_model()

# Tests for the custom user model
class UserModelTest(TestCase):
    def test_user_is_valid_with_email_only(self):
        # Creates a user instance with only an email address
        user = User(email="a@b.com")
        user.full_clean()
    
    def test_email_is_primary_key(self):
        # Creates a user and checks that the primary key is the email address
        user = User(email="a@b.com")
        self.assertEqual(user.pk, "a@b.com")

# Tests for the Token model
class TokenModelTest(TestCase):
    # Creates two tokens for the same email and ensures each has a unique ID
    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email="a@b.com")
        token2 = Token.objects.create(email="a@b.com")
        self.assertNotEqual(token1.uid, token2.uid)

