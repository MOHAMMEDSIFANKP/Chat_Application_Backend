from django.urls import path
from .views import *
urlpatterns = [
    path('userlisting/<int:id>/', UserListing.as_view(), name='UserListing'),
    path("user-previous-chats/<int:user1>/<int:user2>/", PreviousMessagesView.as_view()),

]