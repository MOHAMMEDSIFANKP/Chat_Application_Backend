from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/chat/<int:id>/', ChatConsumer.as_asgi()),
    # path('ws/users/<int:id>', UsersListConsumer.as_asgi()),

]