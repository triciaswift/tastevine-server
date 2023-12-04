from django.db import models

class RecipeCategory(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
