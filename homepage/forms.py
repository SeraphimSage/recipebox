from django import forms
from homepage.models import Recipe, Author


class RecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    about = forms.CharField(widget=forms.Textarea)
    ingredients = forms.CharField(widget=forms.Textarea)
    equipment = forms.CharField(max_length=50)
    time_to_make = forms.CharField(max_length=50)
    steps = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(queryset=Author.objects.all())


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "bio"]
