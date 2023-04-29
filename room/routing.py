from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/users/user_activity/', consumers.UserActivityConsumer.as_asgi()),
    path('ws/chat/<slug:slug>/', consumers.ChatConsumer.as_asgi()),
]
