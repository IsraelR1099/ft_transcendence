# myapp/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/rooms', consumers.MyConsumer.as_asgi()),
    # Add more paths for different consumers if needed
]