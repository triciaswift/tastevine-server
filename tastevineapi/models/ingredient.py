from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=250)
    grocery_category = models.ForeignKey('GroceryCategory', on_delete=models.CASCADE)
