from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RoomUser(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='room_user')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # username = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    # username = models.CharField(max_length=255)
    # Use ForeignKey instead of OneToOneField due to one-to-many relationship between User and Message
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_user')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)

    def __str__(self):
        return self.content


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# We will now define signals so our Profile model will be automatically created/updated 
# when we create/update User instances with default settings.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
