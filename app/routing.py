from django.urls import path

from app.consumers import *

websocket_urlpatterns = [
    path('ws/ac/<int:id>/', MyAsyncJsonWebSocketConsumer.as_asgi()),
    path('ws/ac/online/', onlineStatusAsyncJonWebsocketConsumer.as_asgi()),
]