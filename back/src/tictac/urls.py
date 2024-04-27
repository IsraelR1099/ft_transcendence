from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
        path("create_join/", views.home, name="home"),
        path("play/<int:room_code>/", views.play, name="play"),
]
