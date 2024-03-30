from django.test import TestCase
from .forms import SearchForm, CharacterForm, CommentForm
from .models import Character

class FormsTestCase(TestCase):
    def test_search_form_valid(self):
        form_data = {'searchText': 'airplane'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_invalid(self):
        # Test case where searchText is empty
        form_data = {'searchText': ''}
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_character_form_valid(self):
        form_data = {
            'name': 'John Doe',
            'trivia': 'Some trivia',
            'age': 25,
            'ability': 'Flying',
            'hair': 'Brown',
            'eye_color': 'Blue'
        }
        form = CharacterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_character_form_invalid(self):
        # Test case where name is empty
        form_data = {
            'name': '',  # Empty name
            'trivia': 'Some trivia',
            'age': 25,
            'ability': 'Flying',
            'hair': 'Brown',
            'eye_color': 'Blue'
        }
        form = CharacterForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Test case where age is negative
        form_data['name'] = 'John Doe'
        form_data['age'] = -25  # Negative age
        form = CharacterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_comment_form_valid(self):
        form_data = {'text': 'This is a comment.'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        # Test case where text field is empty
        form_data = {'text': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_character_form_duplicate_name(self):
        # Create a character with the same name as in the form data
        Character.objects.create(name='John Doe', trivia='Some trivia', age=25,
                                  ability='Flying', hair='Brown', eye_color='Blue')
        form_data = {
            'name': 'John Doe',  # Duplicate name
            'trivia': 'Some other trivia',
            'age': 30,
            'ability': 'Teleportation',
            'hair': 'Black',
            'eye_color': 'Green'
        }
        form = CharacterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_character_form_blank_name(self):
        form_data = {
            'name': '',  # Blank name
            'trivia': 'Some trivia',
            'age': 25,
            'ability': 'Flying',
            'hair': 'Brown',
            'eye_color': 'Blue'
        }
        form = CharacterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_character_form_non_positive_age(self):
        form_data = {
            'name': 'John Doe',
            'trivia': 'Some trivia',
            'age': 0,  # Zero age
            'ability': 'Flying',
            'hair': 'Brown',
            'eye_color': 'Blue'
        }
        form = CharacterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_character_form_exceed_field_lengths(self):
        form_data = {
            'name': 'A' * 101,  # Exceeds max_length of 100
            'trivia': 'A' * 1001,  # Exceeds max_length of TextField
            'age': 25,
            'ability': 'A' * 1001,  # Exceeds max_length of TextField
            'hair': 'A' * 1001,  # Exceeds max_length of TextField
            'eye_color': 'A' * 101  # Exceeds max_length of 100
        }
        form = CharacterForm(data=form_data)
        self.assertFalse(form.is_valid())