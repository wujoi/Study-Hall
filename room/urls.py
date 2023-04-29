from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('users/user_activity/', views.user_activity, name="user_activity"),
    path('chat/<slug:slug>/', views.room, name='room'),
]
