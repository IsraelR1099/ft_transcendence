from django.urls import path

from .consumers import WSConsumer

ws_urlpatterns = [
        path('ws/chat/', WSConsumer.as_asgi()),
]
