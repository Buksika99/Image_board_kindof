from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("alt_site/", views.An_Alt_Site, name='Alt_Site'),
    path("characters/", views.characters, name="characters"),
    path('create/', views.create_character, name='create_character'),
    path("characters/anime", views.characters, name="anime_characters"),
    path("characters/game", views.characters, name="game_characters"),
    path('', views.index, name='index'),
    path('named_characters/<str:character>', views.named_character_site, name='named_character'),
    path('get_default_secluded_box_images/', views.get_default_secluded_box_images, name='get_default_secluded_box_images'),
    path('proxy-image/<path:image_url>/', views.proxy_image, name='proxy_image'),
    path('proxy_for_static_image/<path:image_url>/', views.proxy_for_static_image, name='proxy_for_static_image'),
    path('<str:tag_name>', views.index, name='random_page'),
]
