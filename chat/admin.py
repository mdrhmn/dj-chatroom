from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Room)
# admin.site.register(RoomUser)

@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = ('id', 'username', 'room', 'date_added',
                    'content')
    list_filter = ('username', 'room__name', 'date_added')
    ordering = ("id",)

    def get_name(self, obj):
        return obj.user

@admin.register(RoomUser)
class Message(admin.ModelAdmin):
    list_display = ('id', 'room', 'username')
    list_filter = ('username', 'room__name')
    ordering = ("id",)

    def get_name(self, obj):
        return obj.user