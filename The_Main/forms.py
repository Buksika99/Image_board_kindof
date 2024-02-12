from django import forms

class SearchForm(forms.Form):
    searchText = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'searchbar', 'placeholder': 'airplane'}))

