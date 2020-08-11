from django.db import models
from django.utils import timezone

# Create your models here.
"""
Author
- Name - str - 80
- Bio - textfield


Recipe
- title - str - 50
- about - textfield
- ingredients str - 50
- equipment - str - 50
- time to make - str - 50
- steps - str - 50
- post date -datetime
- author - foreignkey
"""


class Author(models.Model):
    name = models.CharField(max_length=80)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    about = models.TextField()
    ingredients = models.TextField()
    equipment = models.CharField(max_length=50)
    time_to_make = models.CharField(max_length=50)
    steps = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.author.name}"
