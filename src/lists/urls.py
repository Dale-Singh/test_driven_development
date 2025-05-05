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
# Import the path function to define URL patterns
from django.urls import path
# Import view function from the lists app
from lists import views

urlpatterns = [
    path("new", views.new_list, name="new_list"),
    # URL pattern that captures an integer stored in the variable (list_id) from the URL
    # Example: Visiting "/lists/1/" will call view_list(request, list_id=1)
    path("<int:list_id>/", views.view_list, name="view_list"),

]