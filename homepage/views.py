from django.shortcuts import render, HttpResponseRedirect, reverse
from homepage.models import Recipe, Author, Favorite
from homepage.forms import RecipeForm, AuthorForm, LoginForm, SignupForm, EditRecipe
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def faving(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    Favorite.objects.create(author=request.user.author, recipe=recipe)
    return HttpResponseRedirect(reverse('homepage'))

def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipes": my_recipes, "welcome_name": "everyone"})


def recipe_detail(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_recipe})


def author_detail(request, author_id):
    an_author = Author.objects.filter(id=author_id).first()
    published_recipe = Recipe.objects.filter(author=an_author)
    favorites = Favorite.objects.filter(author=author_id)
    return render(request, "author_detail.html", {"author": an_author, "recipes": published_recipe, 'favorites': favorites})


@login_required
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
                author=request.user.author
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = RecipeForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def author_form_view(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AuthorForm()
    return render(request, "generic_form.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))

    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get(
                "username"), password=data.get("password"))
            Author.objects.create(name=data.get("username"), user=new_user)
            login(request, new_user)

            return HttpResponseRedirect(reverse("homepage"))

    form = SignupForm()
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))

@login_required
def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).first()
    if request.user.is_staff or request.user.author.id == recipe.author.id:
        if request.method == "POST":
            form = EditRecipe(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                recipe.title = data.get('title')
                recipe.about = data.get('about')
                recipe.ingredients = data.get('ingredients')
                recipe.equipment = data.get('equipment')
                recipe.time_to_make = data.get('time_to_make')
                recipe.steps = data.get('steps')
                recipe.save()
                return HttpResponseRedirect(reverse('homepage'))
    form = EditRecipe(initial={'title': recipe.title, 'about': recipe.about, 'ingredients': recipe.ingredients,
                               'equipment': recipe.equipment, 'time_to_make': recipe.time_to_make, 'steps': recipe.steps})
    return render(request, 'generic_form.html', {'form': form})
