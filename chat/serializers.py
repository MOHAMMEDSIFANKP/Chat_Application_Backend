from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import *
from authendications.models import *
from rest_framework import serializers

class UserListserializer(ModelSerializer):
   class Meta:
        model = User
        fields = ['id', 'email', 'first_name','last_name','place','state','district', 'bio','profile_image']

class UserChatListserializer(ModelSerializer):
    last_message = SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name','last_name','place','state','district', 'profile_image','last_message']
    def get_last_message(self,obj):
        user_id = self.context['user_id']
        thread_suffix = f"{user_id}_{obj.id}" if user_id > obj.id else f"{obj.id}_{user_id}"
        thread_name = 'chat_'+thread_suffix
        last_message = Message.objects.filter(thread_name=thread_name).values('message').last()

        return last_message

class MessageSerializer(ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')

    class Meta:
        model = Message
        fields = ['message', 'sender_email']

class ConnectSerializer(ModelSerializer):
    class Meta:
        model = FriendsList
        fields = ['user_id', 'friends_id','is_request']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message','url_path','type_list', 'is_read', 'created_at']

class is_readNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read']