from django.shortcuts import render, redirect
from .models import *


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    # Get username from GET url
    username = request.GET.get('username', 'Anonymous')

    # Get Room object (use first() to get first instance from QuerySet)
    room = Room.objects.filter(name=room_name).first()

    # Take only first 25 messages from Room
    # messages = Message.objects.filter(
    #     room=room)[0:25]
    messages = Message.objects.filter(
        room=room)
    room_users = RoomUser.objects.filter(
        room=room).order_by().values('username').distinct()

    return render(request, 'chat/room.html', {'room_name': room_name,
                                              'username': username,
                                              'messages': messages,
                                              'room_users': room_users})


def check_room(request):
    room = request.POST['room']
    username = request.POST['username']

    # If room already exists, redirect to existing room
    if Room.objects.filter(name=room).exists():

        if not RoomUser.objects.filter(username=username).exists():
            # Create new user in room if first-time user
            new_room_user = RoomUser.objects.create(
                room=Room.objects.filter(name=room).first(), username=username)
            new_room_user.save()

        # Redirect to room
        return redirect('/'+room+'/?username='+username)

    else:
        # Create new room if does not exist
        new_room = Room.objects.create(name=room)
        new_room.save()

        # Create new user in room
        new_room_user = RoomUser.objects.create(
            room=Room.objects.filter(name=room).first(), username=username)
        new_room_user.save()

        # Redirect to room
        return redirect('/'+room+'/?username='+username)
