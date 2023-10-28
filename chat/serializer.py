from rest_framework.serializers import ModelSerializer
from authendications.models import *
class UserListserializer(ModelSerializer):
   class Meta:
        model = User
        fields = ['id', 'email', 'first_name','last_name', 'profile_image']