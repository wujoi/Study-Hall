from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Room, Message

@login_required
def rooms(request):
    rooms = Room.objects.all()
    active_users = User.objects.filter(last_login__lt=timezone.now()-timezone.timedelta(minutes=10)).exclude(is_superuser=True) # users that have logged in within the last 10 minutes
    return render(request, 'room/rooms.html', {'rooms': rooms, 'active_users': active_users})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25] # all messages for room, show first 25
    return render(request, 'room/room.html', {'room': room, 'messages': messages})





