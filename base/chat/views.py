from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

ROOM_NAME = 'chat_room'

@login_required(login_url='/user/login')
def room(request, room_name):
    data_messages = Message.objects.all()
    return render(request, 'chat/room.html', {
        'room_name': ROOM_NAME,
        'data_messages': data_messages
    })
