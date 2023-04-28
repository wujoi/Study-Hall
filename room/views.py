from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q

from .models import Room, Message

@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def active_users(request):
    ############ update to check activity rather than login ############
    # users that have logged in within the last 30 minutes excluding admins
    users = User.objects.filter(last_login__gt=timezone.now()-timezone.timedelta(minutes=30)).exclude(is_superuser=True)
    usernames = [user.username for user in users]
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'active_users',
        {
            'type': 'active_users_update',
            'data': usernames,
        }
    )
    return JsonResponse({'active_users': usernames})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25] # all messages for room, show first 25
    return render(request, 'room/room.html', {'room': room, 'messages': messages})





