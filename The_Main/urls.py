from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("characters/", views.characters, name="characters"),
    path('create/', views.create_character, name='create_character'),
    path('delete_comment/<path:current_path>/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path("characters/anime", views.characters, name="anime_characters"),
    path("characters/game", views.characters, name="game_characters"),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),
    path('named_characters/<str:character>', views.named_character_site, name='named_character'),
    path('get_default_secluded_box_images/', views.get_default_secluded_box_images, name='get_default_secluded_box_images'),
    path('proxy-image/<path:image_url>/', views.proxy_image, name='proxy_image'),
    path('proxy_for_static_image/<path:image_url>/', views.proxy_for_static_image, name='proxy_for_static_image'),

]
