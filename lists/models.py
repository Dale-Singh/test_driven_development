from django.db import models

# Inheriting from models.Model
class Item(models.Model):
    text = models.TextField(default="")

