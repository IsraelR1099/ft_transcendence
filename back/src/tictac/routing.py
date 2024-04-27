from django.urls import path

from .consumers import GameRoom

tictac_ws_urlpatterns = [
        path("ws/game/<int:room_code>/", GameRoom.as_asgi()),
]
