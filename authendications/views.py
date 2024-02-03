from django.shortcuts import render
from django.contrib.auth import authenticate
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

class GoogleRegistration(CreateAPIView):
    serializer_class = GoogleAuthSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        return super().get_serializer_class()
    def post(self, request):
        email = request.data.get('email')

        if not User.objects.filter(email=email).exists():
            serializer = GoogleAuthSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
        user = User.objects.filter(email=email).first()
        if user is not None:
            token=create_jwt_pair_tokens(user)
            response_data = {
                'status': 'success',
                'msg': 'Registratin Successfully',
                'token': token,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'msg': serializer.errors})

def create_jwt_pair_tokens(user): 
    refresh = RefreshToken.for_user(user)
    refresh['email'] = user.email
    refresh['is_active'] = user.is_active

   
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    
    return {
        "access": access_token,
        "refresh": refresh_token,
    }

    

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetils(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RegistrationSerialzer
    queryset = User.objects.all()
    lookup_field = 'id'