from django.db import models

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=250, blank=True)
