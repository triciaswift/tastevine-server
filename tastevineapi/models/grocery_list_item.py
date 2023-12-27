from django.db import models

class GroceryListItem(models.Model):
    grocery_list = models.ForeignKey("GroceryList", on_delete=models.CASCADE, related_name="groceries")
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
