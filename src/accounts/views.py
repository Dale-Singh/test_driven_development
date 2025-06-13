# Django
from django.shortcuts import redirect, render # Utilities for rendering templates and handling redirects
from django.core.mail import send_mail # Send email using Django's email backend
from django.contrib import auth, messages  # Auth system and flash message framework
from django.urls import reverse # Utility to get URL paths by view name and arguments

# Local applications
from accounts.models import Token

# Handles login email requests
def send_login_email(request):
    # Get the email address submitted via POST
    email = request.POST["email"]

    # Generate a token using the submitted email address
    token = Token.objects.create(email=email)

    # Construct a fully qualified url using the token
    url = request.build_absolute_uri(
        reverse("login") + "?token=" + str(token.uid)
    )

    # Construct a message
    message_body = f"Use this link to log in: \n\n{url}"

    # Send an email containing a login link
    send_mail(
        "Your login link for Superlists",      # Email subject
        message_body,                          # Email body (placeholder)
        "superlistsdalesingh@gmail.com",       # Sender address
        [email]                                # Recipient list
    )

    # Add a success message to display on the redirected page
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )

    # Redirect the user to the home page
    return redirect("/")

def login(request):
    # Attempts to authenticate the user using the token from the query string
    if user := auth.authenticate(uid=request.GET["token"]):  # The walrus operator assigns the result to 'user'
        # If authentication succeeds, logs the user in by starting a session
        auth.login(request, user)
    else:
        # If authentication fails (user is None), adds an error message to be displayed to the user
        messages.error(request, "Invalid login link, please request a new one")
    
    # Redirects the user to the homepage regardless of the outcome
    return redirect("/")
