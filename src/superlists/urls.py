"""
URL configuration for superlists project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Import the path function to define URL patterns,
# and include to reference other URL configurations
from django.urls import include, path
# Import view function from the lists app
from lists import views as list_views

urlpatterns = [
    # The root URL "/" becomes "" as Django removes the leading "/" from all URLs
    # The root URL is mapped to the home_page view and the pattern is called "home"
    path("", list_views.home_page, name="home"),
    # Any URL pattern matching lists/ is handled by lists.urls
    path("lists/", include("lists.urls")),
]
