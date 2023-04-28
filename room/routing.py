from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/users/active_users/', consumers.ActiveUsersConsumer.as_asgi()),
    path('ws/users/away_users/', consumers.AwayUsersConsumer.as_asgi()),
    path('ws/users/inactive_users/', consumers.InactiveUsersConsumer.as_asgi()),
    path('ws/<slug:slug>/', consumers.ChatConsumer.as_asgi()),
]
