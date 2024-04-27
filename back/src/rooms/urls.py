from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
import logging

urlpatterns = [
        path("rooms", views.rooms_view),
        path("rooms/<int:room_id>", views.rooms_view),
        # path("rooms/history/<int:user_id>", views.history_view)
        ]
