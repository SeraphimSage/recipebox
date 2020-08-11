from django.shortcuts import render
from homepage.models import Recipe, Author
# Create your views here.


def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipes": my_recipes, "welcome_name": "everyone"})


def recipe_detail(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_recipe})


def author_detail(request, author_id):
    an_author = Author.objects.filter(id=author_id).first()
    published_recipe = Recipe.objects.filter(author=an_author)
    return render(request, "author_detail.html", {"author": an_author, "recipes": published_recipe})
