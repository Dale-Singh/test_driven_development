from django.db import models

# Inheriting from models.Model
class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default="")
    # Foreign key to the List model. If a List is deleted, 
    # all associated Items are deleted (cascading delete).
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
