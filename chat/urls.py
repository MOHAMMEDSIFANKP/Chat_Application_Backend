from django.urls import path
from .views import *
urlpatterns = [    
    path('userlisting/<int:id>/', UserListing.as_view(), name='UserListing'),
    path("user-previous-chats/<int:user1>/<int:user2>/", PreviousMessagesView.as_view()),

    path('all-user-list/<int:id>/', AllUserList.as_view(), name='UserListing'),
    path('user-details/<int:id>/<int:user_id>', UserDetails.as_view(), name='UserListing'),

    path('connect/', ConnectionRequestView.as_view(), name='ConnectView'),
    path('accepted/', AcceptedRequestView.as_view(), name='AcceptedtView'),
    path('remove/', RemoveFriendsView.as_view(), name='RemoveView'),
   
    path('notification/<int:id>', NotificationListView.as_view(), name='NotificationView'),
    path('notification/count/<int:id>', NotificationCount.as_view(), name='NotificationView'),
    path('notification/is_read/<int:id>', IsReadView.as_view(), name='IsReadView'),


]
