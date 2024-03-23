from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveUpdateAPIView
from rest_framework.filters import SearchFilter
from .serializers import *
from authendications.models import User
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .models import *

class UserListing(ListAPIView):
    serializer_class = UserListserializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name','last_name','email']
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        user_id = self.kwargs['id']
        queryset = User.objects.all().exclude(Q(id=user_id) | Q(is_superuser=True))
        return queryset

class PreviousMessagesView(ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = 'chat_'+thread_suffix
        queryset = Message.objects.filter(
            thread_name=thread_name
        )
        return queryset


class AllUserList(ListAPIView):
    serializer_class = AllUserListSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

    def get_queryset(self):
        user_id = int(self.kwargs['id'])
        return User.objects.all().exclude(Q(id=user_id) | Q(is_superuser=True) |Q(is_active=False))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = int(self.kwargs['id'])
        return context

class UserDetails(RetrieveUpdateAPIView):
    serializer_class = UserDetailSerialzer
    queryset = User.objects.all()
    lookup_field = 'id'
    # permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['id'] = int(self.kwargs['id'])
        context['user_id'] = int(self.kwargs['user_id'])
        return context