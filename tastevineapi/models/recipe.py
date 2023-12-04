from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = models.CharField(max_length=250)
    instructions = models.CharField(max_length=300)
    image = models.ImageField(upload_to='tastevineimages', height_field=None, width_field=None, max_length=None, null=True)
    publication_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    ingredients = models.ManyToManyField('Ingredient', through ='RecipeIngredient', related_name='recipes')
    categories = models.ManyToManyField('Category', through='RecipeCategory', related_name='recipes')
