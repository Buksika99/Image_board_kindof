from django.db import models


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
    name = models.CharField(max_length=100, unique=True)  # Ensure unique names
    default_image = models.URLField()  # URL for the default image
    trivia = models.TextField(blank=True)  # Allow trivia to be blank
    age = models.PositiveIntegerField(null=True, blank=True)  # Allow age to be optional
    created_at = models.DateTimeField(auto_now_add=True)  # Track creation time
    updated_at = models.DateTimeField(auto_now=True)  # Track last update time
    ability = models.TextField(blank=True)
    hair = models.TextField(blank=True)
    eye_color = models.CharField(max_length=100, blank=True)
    # You can add more fields such as description, abilities, etc. based on your needs

    def __str__(self):
        return self.name
