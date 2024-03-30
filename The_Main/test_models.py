from django.test import TestCase
from django.contrib.auth.models import User
from .models import DanbooruImage, Character, Comment
from django.utils import timezone
import time


class DanbooruImageModelTest(TestCase):
    def test_image_creation(self):
        image = DanbooruImage.objects.create(image_url="https://example.com/image.jpg", tags="test_tags")
        self.assertEqual(image.tags, "test_tags")


class CharacterModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="password")

    def test_character_creation(self):
        character = Character.objects.create(name="Test Character", category="anime")
        self.assertEqual(character.name, "Test Character")
        self.assertEqual(character.category, "anime")

    def test_character_with_trivia(self):
        character = Character.objects.create(name="Character with Trivia", category="game", trivia="Some trivia")
        self.assertEqual(character.trivia, "Some trivia")

    def test_character_age_optional(self):
        character = Character.objects.create(name="Character without Age", category="game")
        self.assertIsNone(character.age)

    def test_character_created_at(self):
        character = Character.objects.create(name="Character Created At", category="anime")
        self.assertIsNotNone(character.created_at)

    def test_character_updated_at(self):
        character = Character.objects.create(name="Character Updated At", category="anime")
        initial_updated_at = character.updated_at
        time.sleep(1)  # Introduce a slight delay to ensure a different update time
        character.name = "Updated Name"
        character.save()
        self.assertNotEqual(initial_updated_at, character.updated_at)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="password")
        self.character = Character.objects.create(name="Test Character", category="anime")

    def test_comment_creation(self):
        comment = Comment.objects.create(character=self.character, user=self.user, text="Test Comment")
        self.assertEqual(comment.text, "Test Comment")
        self.assertEqual(comment.character, self.character)
        self.assertEqual(comment.user, self.user)
