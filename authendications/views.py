from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView
from .serializer import *


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class Registration(CreateAPIView):
    serializer_class = RegistrationSerialzer
    queryset = User.objects.all()

class UserDetils(RetrieveUpdateDestroyAPIView):
    serializer_class = RegistrationSerialzer
    queryset = User.objects.all()
    lookup_field = 'id'