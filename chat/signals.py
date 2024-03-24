from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FriendsList
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# @receiver(post_save, sender=FriendsList)
# def makefriends(sender, instance, **kwargs):
#     if instance.is_accept:
#         FriendsList.objects.create(user_id=int(instance.friends_id),friends_id=int(instance.user_id),is_request=True,is_accept=True)