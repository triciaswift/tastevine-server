from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    posted_on = models.DateField(auto_now_add=True)
