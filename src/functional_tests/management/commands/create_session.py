# Django
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

# Get the custom or default User model
User = get_user_model()

# Define a Django management command
class Command(BaseCommand):
    # Allow the command to accept an email as an argument
    def add_arguments(self, parser):
        parser.add_argument("email")

    # Entry point for the command when run via `python manage.py <command>`
    def handle(self, *args, **options):
        # Create a session for the given email and print the session key
        session_key = create_pre_authenticated_session(options["email"])
        self.stdout.write(session_key)

# Helper function to create a logged-in session for a given email
def create_pre_authenticated_session(email):
    # Create a new user with the specified email
    user = User.objects.create(email=email)
    
    # Create a new session instance using the DB-backed session engine
    session = SessionStore()
    
    # Store the user ID and backend path in the session
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    
    # Save the session to the database
    session.save()
    
    # Return the session key so it can be used in a browser cookie
    return session.session_key
