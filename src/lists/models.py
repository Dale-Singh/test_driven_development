from django.db import models
from django.urls import reverse

# Django automatically creates a table for each model and defines an ID field
class List(models.Model):
    # Special Django-recognised method that defines the URL for this object.
    # Enables automatic URL resolution for redirects, templates, and admin links.
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

class Item(models.Model):
    text = models.TextField(default="")
    # Foreign key to the List model. If a List is deleted, 
    # all associated Items are deleted (cascading delete).
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
