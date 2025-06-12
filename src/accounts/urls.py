# Django
from django.urls import path # Tools for declaring URL patterns
from django.contrib.auth import views as auth_views # Imports built-in Django auth views

# Local applications
from accounts import views

# Define urls
urlpatterns = [
    path("send_login_email", views.send_login_email, name="send_login_email"),
    path("login", views.login, name="login"),
    # Defines a URL route for logging out users using Django's built-in LogoutView.
    # When accessed, it logs the user out and then redirects them to the homepage ("/").    
    path("logout", auth_views.LogoutView.as_view(next_page="/"), name="logout"),

]