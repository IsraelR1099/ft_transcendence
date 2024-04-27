from django.urls import re_path
from . import rooms

websocket_urlpatterns = [
    re_path(r"ws/<game>/", rooms.Rooms.as_asgi()),
]
