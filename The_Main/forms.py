from django import forms
from .models import Character, Comment

class SearchForm(forms.Form):
    searchText = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'searchbar', 'placeholder': 'airplane'}))


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'trivia', 'age', 'ability', 'hair', 'eye_color']


# Customize the TextArea inside the comment box.
class CustomTextarea(forms.Textarea):
    def __init__(self, attrs=None):
        # Customize textarea attributes here
        default_attrs = {'class': 'custom-textarea-class', 'rows': '6', 'cols': '40'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    # Override render method to set width and height
    def render(self, name, value, attrs=None, renderer=None):
        # Set height to 150px
        attrs['style'] = 'height: 150px;'
        return super().render(name, value, attrs, renderer)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        # Set width to 100% of its container
        attrs['style'] = 'width: 100%;' + attrs.get('style', '')
        return attrs

# Define your form
class CommentForm(forms.ModelForm):
    # Associate custom widget with the 'text' field
    text = forms.CharField(widget=CustomTextarea, label='')

    class Meta:
        model = Comment
        fields = ['text']