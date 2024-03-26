from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, **kwargs):
    user_id = instance.user_id
    count = Notification.objects.filter(user=user_id, is_read=False).count()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user_id}',
        {
            'type': 'notification_count',
            'count': count
        }
    )