from django.contrib import admin
from .models import Character


# Register your models here.
class AnimeCharacter(Character):
    class Meta:
        proxy = True

class GameCharacter(Character):
    class Meta:
        proxy = True

class AnimeCharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'trivia', 'age', 'eye_color', 'created_at', 'updated_at', 'order')
    search_fields = ('name', 'trivia')
    list_filter = ('age', 'eye_color')
    list_editable = ('order',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category='anime')

class GameCharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'trivia', 'age', 'eye_color', 'created_at', 'updated_at', 'order')
    search_fields = ('name', 'trivia')
    list_filter = ('age', 'eye_color')
    list_editable = ('order',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category='game')

admin.site.register(AnimeCharacter, AnimeCharacterAdmin)
admin.site.register(GameCharacter, GameCharacterAdmin)