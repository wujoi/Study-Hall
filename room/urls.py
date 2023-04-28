from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('users/active_users/', views.active_users, name='active_users'),
    path('<slug:slug>/', views.room, name='room'),
]
