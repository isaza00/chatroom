from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from .models import Message

ROOM_NAME = 'chat_room'

@login_required(login_url='/user/login')
def index(request):
    return render(request, 'chat/index.html')

@login_required(login_url='/user/login')
def room(request, room_name):
    messages = reversed(Message.objects.all().order_by('-date')[:50])
    user = request.user.username
    return render(request, 'chat/room.html', {
        'room_name': ROOM_NAME,
        'messages': serialize('json', messages),
        'user': user
    })
