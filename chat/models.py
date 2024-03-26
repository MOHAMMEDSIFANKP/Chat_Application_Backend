from django.db import models
from authendications.models import User
# Create your models here.



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="sender_message_set")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="reciever_message_set")
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.sender.first_name}-{self.sender.last_name}'


class FriendsList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_id")
    friends_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="friends_id")
    is_request = models.BooleanField(default=False)
    is_accept = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    url_path = models.CharField(max_length=100,blank=True,null=True)
    type_list = models.CharField(max_length=100,blank=True,null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)