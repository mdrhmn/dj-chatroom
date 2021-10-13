from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *


@login_required(login_url='login')
def index(request):
    return render(request, 'chat/index.html')


@login_required(login_url='login')
def room(request, room_name):
    # Get username from GET url
    username = request.GET.get('username', 'Anonymous')

    # Get Room object (use first() to get first instance from QuerySet)
    room = Room.objects.filter(name=room_name).first()

    # Get messages in Room
    messages = Message.objects.filter(
        room=room)

    # Get username of all room users
    # room_users = RoomUser.objects.filter(
    #     room=room).order_by().values('username').distinct()
    room_users = RoomUser.objects.filter(
        room=room).order_by().values('user__username')
    print(room_users)

    return render(request, 'chat/room.html', {'room_name': room_name,
                                              'username': username,
                                              'messages': messages,
                                              'room_users': room_users
                                              })


@login_required(login_url='login')
def check_room(request):
    # Get room name
    room = request.POST['room']

    # If room already exists, redirect to existing room
    if Room.objects.filter(name=room).exists():

        if not RoomUser.objects.filter(user=User.objects.get(id=request.user.id)).exists():
            # Create new user in room if first-time user
            new_room_user = RoomUser.objects.create(
                room=Room.objects.filter(name=room).first(),
                user=User.objects.get(id=request.user.id))
            new_room_user.save()

        # Redirect to room
        return redirect('/chat/' + room + '/?username=' + request.user.username)

    else:
        # Create new room if does not exist
        new_room = Room.objects.create(name=room)
        new_room.save()

        # Create new user in room
        new_room_user = RoomUser.objects.create(
            room=Room.objects.filter(name=room).first(),
            user=User.objects.get(id=request.user.id))
        new_room_user.save()

        # Redirect to room
        return redirect('/chat/' + room + '/?username=' + request.user.username)
