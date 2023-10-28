from django.urls import path
from .views import *
urlpatterns = [
    path('userlisting/', UserListing.as_view(), name='UserListing'),
]