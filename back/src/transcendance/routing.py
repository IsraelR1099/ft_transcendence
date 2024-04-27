from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.consumers import ChatConsumer
from tictac.consumers import GameRoom

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/chat/", ChatConsumer.as_asgi()),
        path("ws/game/", GameRoom.as_asgi()),
    ]),
})
