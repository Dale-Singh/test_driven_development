# Django
from django.urls import path # Tools for declaring URL patterns

# Local applications
from lists import views

# Define urls
urlpatterns = [
    path("new", views.new_list, name="new_list"),
    # URL pattern that captures an integer stored in the variable (list_id) from the URL
    # Example: Visiting "/lists/1/" will call view_list(request, list_id=1)
    path("<int:list_id>/", views.view_list, name="view_list"),

]