from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import *
from decouple import config

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_active'] = user.is_active
        token['is_google'] = user.is_google
        return token
    
class RegistrationSerialzer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name','last_name', 'password', 'profile_image']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class GoogleAuthSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name','last_name', 'password', 'profile_image']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserProfileSerializer(ModelSerializer):
    friends_count = SerializerMethodField()
    friends_list = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name','last_name', 'profile_image','place','district','state','bio','is_google','friends_count','friends_list']
    def get_friends_count(self,obj):
        friends_count = obj.friends_list.all().count()
        return friends_count
    def get_friends_list(self,obj):
        baseUrl = config('backend_url')
        friends_list = obj.friends_list.all()
        list = []
        for i in friends_list:
            data = {
                "id" : i.id,
                "email" : i.email,
                "first_name" : i.first_name,
                "last_name" : i.last_name,
                "profile_image" : f"{baseUrl}/media/{str(i.profile_image)}" or None,
            }
            list.append(data)
        return list