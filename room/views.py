from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .models import Room, Message

@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25] # all messages for room, show first 25
    return render(request, 'room/room.html', {'room': room, 'messages': messages})


@receiver(user_logged_in)
def on_user_logged_in(sender, **kwargs):
    active_users = User.objects.filter(last_login__gt=timezone.now()-timezone.timedelta(minutes=30)).exclude(is_superuser=True)
    away_users = User.objects.filter(last_login__gte=timezone.now()-timezone.timedelta(minutes=30), last_login__lte=timezone.now()-timezone.timedelta(minutes=60)).exclude(is_superuser=True)
    inactive_users = User.objects.exclude(username__in=list(active_users.values_list('username', flat=True))).exclude(username__in=list(away_users.values_list('username', flat=True))).exclude(is_superuser=True)
    
    active_usernames = [user.username for user in active_users]
    away_usernames = [user.username for user in away_users]
    inactive_usernames = [user.username for user in inactive_users]

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'user_activity',
        {
            'type': 'user_activity_update',
            'active_users': active_usernames,
            'away_users': away_usernames,
            'inactive_users': inactive_usernames
        }
    )

    response_data = {
        'active_users': active_usernames,
        'away_users': away_usernames,
        'inactive_users': inactive_usernames
    }

    return JsonResponse(response_data)


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    if request.user.is_authenticated:
        request.user.last_login = timezone.now() - timezone.timedelta(minutes=61)
        request.user.save()
        
    active_users = User.objects.filter(last_login__gt=timezone.now()-timezone.timedelta(minutes=30)).exclude(is_superuser=True)
    away_users = User.objects.filter(last_login__gte=timezone.now()-timezone.timedelta(minutes=30), last_login__lte=timezone.now()-timezone.timedelta(minutes=60)).exclude(is_superuser=True)
    inactive_users = User.objects.exclude(username__in=list(active_users.values_list('username', flat=True))).exclude(username__in=list(away_users.values_list('username', flat=True))).exclude(is_superuser=True)
    
    active_usernames = [user.username for user in active_users]
    away_usernames = [user.username for user in away_users]
    inactive_usernames = [user.username for user in inactive_users]

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'user_activity',
        {
            'type': 'user_activity_update',
            'active_users': active_usernames,
            'away_users': away_usernames,
            'inactive_users': inactive_usernames
        }
    )

    response_data = {
        'active_users': active_usernames,
        'away_users': away_usernames,
        'inactive_users': inactive_usernames
    }

    return JsonResponse(response_data)

@login_required
def user_activity(request):
    active_users = User.objects.filter(last_login__gt=timezone.now()-timezone.timedelta(minutes=30)).exclude(is_superuser=True)
    away_users = User.objects.filter(last_login__gte=timezone.now()-timezone.timedelta(minutes=30), last_login__lte=timezone.now()-timezone.timedelta(minutes=60)).exclude(is_superuser=True)
    inactive_users = User.objects.exclude(username__in=list(active_users.values_list('username', flat=True))).exclude(username__in=list(away_users.values_list('username', flat=True))).exclude(is_superuser=True)
    
    active_usernames = [user.username for user in active_users]
    away_usernames = [user.username for user in away_users]
    inactive_usernames = [user.username for user in inactive_users]

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'user_activity',
        {
            'type': 'user_activity_update',
            'active_users': active_usernames,
            'away_users': away_usernames,
            'inactive_users': inactive_usernames
        }
    )

    response_data = {
        'active_users': active_usernames,
        'away_users': away_usernames,
        'inactive_users': inactive_usernames
    }

    return JsonResponse(response_data)