from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import *
from authendications.models import *
from rest_framework import serializers

class UserListserializer(ModelSerializer):
   class Meta:
        model = User
        fields = ['id', 'email', 'first_name','last_name','place','state','district', 'profile_image']

class MessageSerializer(ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')

    class Meta:
        model = Message
        fields = ['message', 'sender_email']
class ConnectSerializer(ModelSerializer):
    class Meta:
        model = FriendsList
        fields = ['user_id', 'friends_id','is_request']

