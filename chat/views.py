from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from .serializer import *
from authendications.models import User

class UserListing(ListAPIView):
    serializer_class = UserListserializer
    queryset = User.objects.all().exclude(is_superuser=True)
    filter_backends = [SearchFilter]
    search_fields = ['first_name','last_name','email']
