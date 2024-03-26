from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from authendications.models import User
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .models import *
from decouple import config

class UserListing(ListAPIView):
    serializer_class = UserChatListserializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name','last_name','email']
    # permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        user_id = self.kwargs['id']
        user_instance = User.objects.filter(id=user_id).first()
        queryset = user_instance.friends_list.all()
        return queryset
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = int(self.kwargs['id'])
        return context
    

class PreviousMessagesView(ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = None
    # permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = 'chat_'+thread_suffix
        queryset = Message.objects.filter(
            thread_name=thread_name
        )
        return queryset


class AllUserList(APIView):
    def get(self, request, id):
        backend_url = str(config('backend_url'))
        selectoption = request.query_params.get('selectoption')
        try:
            data = []
            if selectoption == 'People':
               
                friends_ids = FriendsList.objects.filter(friends_id=id).values_list('user_id', flat=True)
                user_instance = User.objects.filter(
                    ~Q(id=id) & ~Q(id__in=friends_ids) & ~Q(friends_list=id) & Q(is_active=True) & Q(is_superuser=False)
                ).order_by('-id')
                serializer = UserListserializer(user_instance, many=True)
                data = serializer.data

                friends_pending_list = FriendsList.objects.filter(user_id=id).values_list('friends_id', flat=True)
                
                # Mark all users as not friends
                for user in data:
                    user['is_connect'] = 'not_friends'
                    user['profile_image'] = f"{backend_url}{user['profile_image']}" if user['profile_image'] else None

                
                for friend_id in friends_pending_list:
                    for user in data:
                        if user['id'] == friend_id:
                            user['is_connect'] = 'pending'
            
            elif selectoption == 'Requests':
                friends_ids = FriendsList.objects.filter(friends_id=id).values_list('user_id', flat=True)
                requests_users = User.objects.filter(id__in=friends_ids).order_by('-id')
                serializer = UserListserializer(requests_users, many=True)
                data = serializer.data

                # Modify profile image URLs to include the backend URL
                for user in data:
                    user['profile_image'] = f"{backend_url}{user['profile_image']}" if user['profile_image'] else None
                    user['is_connect'] = "accept"

            elif selectoption == 'MyFriends':
                user_instance = User.objects.get(id=id)
                myfriends_instance = user_instance.friends_list.all().order_by('-id')

                serializer = UserListserializer(myfriends_instance, many=True)
                data = serializer.data
            
                for user in data:
                    user['is_connect'] = 'remove'
                    user['profile_image'] = f"{backend_url}{user['profile_image']}" if user['profile_image'] else None
            return Response({'data': data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': f'User with ID {id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
    
class UserDetails(APIView):
    def get(self,request,id,user_id):
            backend_url = str(config('backend_url'))
            try:
                user_instance = User.objects.filter(id=id).first()
                friends_instance = User.objects.filter(id=user_id).first()
                serializers = UserListserializer(user_instance)
                data = serializers.data
                data['is_connect'] = 'not_friends'
                if user_instance.friends_list.filter(id=user_id).exists():
                    data['is_connect'] = 'remove'
                if FriendsList.objects.filter(user_id=user_id,friends_id=id,is_request=True):
                    data['is_connect'] = 'pending'
                if FriendsList.objects.filter(user_id=id,friends_id=user_id,is_request=True):
                    data['is_connect'] = 'accept'
                
                data['profile_image'] =f"{backend_url}{data['profile_image']}" if data['profile_image'] else None
                friends_list = user_instance.friends_list.all()
                friends_serializer = UserListserializer(friends_list, many=True)
                data['friends_list'] = friends_serializer.data
                data['friends_count'] = friends_list.count()
                for friends in data['friends_list']:
                    friends['profile_image'] = f"{backend_url}{friends['profile_image']}" if friends['profile_image'] else None
                    friends['is_connect'] = 'not_friends'
                    if friends_instance.friends_list.filter(id=friends['id']).exists():
                        friends['is_connect'] = 'remove'
                    if FriendsList.objects.filter(user_id=user_id,friends_id=friends['id'],is_request=True):
                        friends['is_connect'] = 'pending'
                    if FriendsList.objects.filter(friends_id=user_id,user_id=friends['id'],is_request=True):
                        friends['is_connect'] = 'accept'

                return Response({'data':data},status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': f'User with ID {id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class ConnectionRequestView(CreateAPIView):
    serializer_class = ConnectSerializer
    queryset = FriendsList.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        user_id = validated_data.get('user_id')
        friends_id = validated_data.get('friends_id')

        if user_id == friends_id:
            return Response({'message': 'User id and friends id cannot be the same'}, status=status.HTTP_400_BAD_REQUEST)


        if FriendsList.objects.filter(user_id=user_id, friends_id=friends_id).exists():
            return Response({'message': 'This connection already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)

        full_name = user_id.get_full_name().upper()
        message = f'{full_name} sent a connection request'
        Notification.objects.create(user=friends_id, message=message, url_path='/users', type_list='Requests')
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class AcceptedRequestView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        friends_id = request.data.get('friends_id')
        if user_id == friends_id:
            return Response({'message': 'User id and friends id cannot be the same'}, status=status.HTTP_400_BAD_REQUEST)
        
        friends_instance = FriendsList.objects.filter(user_id=user_id, friends_id=friends_id)
        friends_instance.delete()
        
        user_instance = User.objects.get(id=user_id)
        user_instance.friends_list.add(friends_id)
        user_instance = User.objects.filter(id=user_id).first()
        friends_instance = User.objects.filter(id=friends_id).first()
        full_name = friends_instance.get_full_name().upper()
        message = f'{full_name} accepted your connection request'
        Notification.objects.create(user=user_instance, message=message, url_path='/users', type_list='MyFriends')
        
        
        return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)

class RemoveFriendsView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        friends_id = request.data.get('friends_id')
        
        user_instance = User.objects.get(id=user_id)
        user_instance.friends_list.remove(friends_id)
        
        friend_instance = User.objects.get(id=friends_id)
        friend_instance.friends_list.remove(user_id)
        
        return Response({'message': 'Friend removed successfully'}, status=status.HTTP_200_OK)

class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer

    def get(self, request, id):
        try:
            queryset = Notification.objects.filter(user=id).order_by('-created_at')
            serializer = NotificationSerializer(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'message': f'User with ID {id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
class NotificationCount(APIView):
    def get(self,request,id):
        count = Notification.objects.filter(user=id,is_read=False).count()
        return Response({"un_read_count":count},status=status.HTTP_200_OK)
class IsReadView(UpdateAPIView):
    serializer_class = is_readNotificationSerializer
    queryset  =Notification.objects.all()
    lookup_field = 'id'