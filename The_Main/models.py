from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

# Create your models here.
class To_Do_List(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    todolist = models.ForeignKey(To_Do_List, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text

class DanbooruImage(models.Model):
    image_url = models.URLField()
    tags = models.CharField(max_length=255)

    def __str__(self):
        return self.tags


class Character(models.Model):
    CATEGORY_CHOICES = [
        ('anime', 'Anime'),
        ('game', 'Game'),
        ('v-tuber', 'V-Tuber'),
    ]
    name = models.CharField(max_length=100, unique=True)  # Ensure unique names
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    trivia = models.TextField(blank=True)  # Allow trivia to be blank
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]  # Ensure age is positive
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Track creation time
    updated_at = models.DateTimeField(auto_now=True)  # Track last update time
    ability = models.TextField(blank=True)
    hair = models.TextField(blank=True)
    eye_color = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID field

    # You can add more fields such as description, abilities, etc. based on your needs

    def __str__(self):
        return self.name



class Comment(models.Model):
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)  # Add a field to store the username
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

