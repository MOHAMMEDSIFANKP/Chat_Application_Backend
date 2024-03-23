# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

# User = get_user_model()
# @receiver(post_save, sender=User)
# def update_users_list(sender, instance, **kwargs):
#     channel_layer = get_channel_layer()

#     async_to_sync(channel_layer.group_send)(
#         'users_group',  
#         {
#             'type': 'update_users_list',
#         }
#     )
