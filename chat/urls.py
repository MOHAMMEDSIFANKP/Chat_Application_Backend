from django.urls import path
from .views import *
urlpatterns = [
    path('userlisting/<int:id>/', UserListing.as_view(), name='UserListing'),
    path("user-previous-chats/<int:user1>/<int:user2>/", PreviousMessagesView.as_view()),

    path('all-user-list/<int:id>/', AllUserList.as_view(), name='UserListing'),
    path('user-details/<int:id>/<int:user_id>', UserDetails.as_view(), name='UserListing'),


]