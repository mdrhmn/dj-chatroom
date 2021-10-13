from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Room)
# admin.site.register(RoomUser)
# admin.site.register(Message)

@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'date_added',
                    'content')
    list_filter = ('user', 'room', 'date_added')
    ordering = ("id",)

    def get_name(self, obj):
        return obj.user

@admin.register(RoomUser)
class RoomUser(admin.ModelAdmin):
    list_display = ('id', 'room', 'user')
    list_filter = ('user', 'room')
    ordering = ("id",)

    def get_name(self, obj):
        return obj.user

admin.site.register(Profile)
