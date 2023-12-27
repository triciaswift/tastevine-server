from django.db import models
from django.contrib.auth.models import User


class GroceryList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    items = models.ManyToManyField("Ingredient", through="GroceryListItem", related_name="grocery_lists")
