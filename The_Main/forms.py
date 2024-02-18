from django import forms
from .models import Character

class SearchForm(forms.Form):
    searchText = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'searchbar', 'placeholder': 'airplane'}))


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'default_image', 'trivia', 'age', 'ability', 'hair', 'eye_color']
