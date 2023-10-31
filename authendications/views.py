from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView
from .serializer import *


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class Registration(CreateAPIView):
    serializer_class = RegistrationSerialzer
    queryset = User.objects.all()


class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetils(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RegistrationSerialzer
    queryset = User.objects.all()
    lookup_field = 'id'