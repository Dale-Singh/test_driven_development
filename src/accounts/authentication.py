# Local applications
from accounts.models import Token, User

# Custom authentication backend for passwordless login using tokens
class PasswordlessAuthenticationBackend:
    def authenticate(self, request, uid):
        try:
            # Look up the token by its unique ID
            token = Token.objects.get(uid=uid)
            # Return the user associated with the token's email if they exist
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            # If no user exists, create a new one with the token's email
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            # If the token is invalid or missing, return None
            return None
    
    # Retrieves a user by email, or returns None if no such user exists
    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
