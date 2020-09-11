from django.shortcuts import render, HttpResponseRedirect, reverse
from homepage.models import Recipe, Author
from homepage.forms import RecipeForm, AuthorForm, LoginForm, SignupForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

# New function to edit recipes
@login_required
def recipe_edit_view(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.user.is_staff or recipe.author == request.user.username:
        if request.method == "POST":
            form = RecipeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                recipe.title = data["title"]
                recipe.about = data["about"]
                recipe.ingredients = data["ingredients"]
                recipe.equipment = data["equiptment"]
                recipe.time_to_make = data["time_to_make"]
                recipe.steps = data["steps"]
                recipe.save()
                return HttpResponseRedirect(reverse("recipedetail", args=[recipe.id]))
        data = {
            "title": recipe.title,
            "about": recipe.about,
            "ingredients": recipe.ingredients,
            "equiptment": recipe.equipment,
            "time_to_make": recipe.time_to_make,
            "steps": recipe.steps,
        }
        form = RecipeForm(initial=data)
        return render(request, "generic_form.html", {"form": form})
    else:
        return HttpResponseRedirect(reverse('error'))


@login_required
def author_form_view(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
            Author.objects.create(name=data.get("username"), bio=data.get("bio"), user=new_user)
            return HttpResponseRedirect(reverse('homepage'))
    form = AuthorForm()
    return render(request, 'generic_form.html', {"form": form})
    

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

def error_view(request):
    return render(request, 'error.html')
