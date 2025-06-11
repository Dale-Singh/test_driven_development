# Standard library
import uuid # For generating unique token identifiers

# Django imports
from django.db import models  # Provides Django's base classes for defining database models

class User(models.Model):
    # Unique identifier for the user
    email = models.EmailField(primary_key=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    is_anonymous = False
    is_authenticated = True

class Token(models.Model):
    email = models.EmailField()
    # Generates a unique ID using uuid4; stored as a string with a max length of 40
    uid = models.CharField(default=uuid.uuid4, max_length=40)
