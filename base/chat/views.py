from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from .models import Message

ROOM_NAME = 'chat_room'

@login_required(login_url='/user/login')
def room(request, room_name):
    messages = Message.objects.all()[:49]
    user = request.user.username
    return render(request, 'chat/room.html', {
        'room_name': ROOM_NAME,
        'messages': serialize('json', messages),
        'user': user
    })
