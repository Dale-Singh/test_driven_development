# Django
from django.db import models  # Provides Django's base classes for defining database models
from django.urls import reverse  # Utility to get URL paths by view name and arguments

# Django automatically creates a table for each model and defines an ID field
class List(models.Model):
    # Returns the URL for this list instance by reversing the URL pattern named 'view_list'.
    # The pattern maps to a view function, but 'reverse' finds the actual URL path (e.g., '/lists/5/').
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

class Item(models.Model):
    text = models.TextField(default="")
    # Foreign key to the List model. If a List is deleted, 
    # all associated Items are deleted (cascading delete).
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ("id",)
        unique_together = ("list", "text")
    
    # Return the item's text as its string representation for readability in admin, logs, and templates
    def __str__(self):
        return self.text
