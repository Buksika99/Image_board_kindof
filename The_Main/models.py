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
