# Django
from django.urls import include, path # Tools for declaring URL patterns and including other URLconfs

# Local applications
from lists import views as list_views

# The root URL "/" becomes "" as Django removes the leading "/" from all URLs
urlpatterns = [
    # The root URL is mapped to the home_page view and the pattern is called "home"
    path("", list_views.home_page, name="home"),
    # Any URL pattern matching lists/ is handled by lists.urls
    path("lists/", include("lists.urls")),
    # Any URL pattern matching accounts/ is handled by accounts.urls
    path("accounts/", include("accounts.urls"))
]
