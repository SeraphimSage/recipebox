from django.shortcuts import render, HttpResponseRedirect, reverse
from homepage.models import Recipe, Author
from homepage.forms import RecipeForm, AuthorForm
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


def recipe_form_view(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                about=data.get('about'),
                ingredients=data.get('ingredients'),
                equipment=data.get('equipment'),
                time_to_make=data.get('time_to_make'),
                steps=data.get('steps'),
                author=data.get('author')
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = RecipeForm()
    return render(request, "generic_form.html", {"form": form})


def author_form_view(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AuthorForm()
    return render(request, "generic_form.html", {"form": form})
