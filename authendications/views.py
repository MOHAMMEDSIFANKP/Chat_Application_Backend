from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView,UpdateAPIView
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
    refresh['is_google'] = user.is_google

   
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
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

from django.contrib.auth.hashers import check_password

class ChangePassword(APIView):
    def post(self,request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        user_id = request.data.get('user_id')
        print(old_password,new_password,user_id)
        if old_password and new_password and user_id:
            user = User.objects.get(id = user_id)
            if check_password(old_password, user.password):
                user.set_password(new_password)
                user.save()
                return Response({'message':"Password updated successfully"},status=status.HTTP_200_OK)
            else:
                return Response({'message':"Invalid old password"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message':"Fields are blank"},status=status.HTTP_404_NOT_FOUND)

class ProfileimageUpdateView(UpdateAPIView):
    serializer_class = ProfileimageupdateSerializer
    queryset = User.objects.all()
    lookup_field = 'id'