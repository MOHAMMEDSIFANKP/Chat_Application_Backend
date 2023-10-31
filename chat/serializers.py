from rest_framework.serializers import ModelSerializer
from .models import Message
from authendications.models import *
from rest_framework import serializers

class UserListserializer(ModelSerializer):
   class Meta:
        model = User
        fields = ['id', 'email', 'first_name','last_name', 'profile_image']

class MessageSerializer(ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')

    class Meta:
        model = Message
        fields = ['message', 'sender_email']
