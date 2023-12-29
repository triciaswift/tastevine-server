from django.db import models

class GroceryCategory(models.Model):
    category = models.CharField(max_length=250)