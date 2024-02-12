from django.urls import path
from . import views

urlpatterns = [
    path("alt_site/", views.An_Alt_Site, name='Alt_Site'),
    path('', views.index, name='index'),
    path('default_images/', views.default_images, name='default_images'),
    path('proxy-image/<path:image_url>/', views.proxy_image, name='proxy_image'),
    path('proxy_for_static_image/<path:image_url>/', views.proxy_for_static_image, name='proxy_for_static_image'),
]
