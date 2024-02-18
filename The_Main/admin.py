from django.contrib import admin
from .models import Character


# Register your models here.
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'trivia', 'age', 'eye_color', 'created_at', 'updated_at')  # Customize the fields displayed in the list view
    search_fields = ('name', 'trivia')  # Add fields to search
    list_filter = ('age', 'eye_color')  # Add filters for specific fields

admin.site.register(Character, CharacterAdmin)

