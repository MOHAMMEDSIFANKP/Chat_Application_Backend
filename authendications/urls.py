from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView,)
from .views import *
urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_refresh'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', Registration.as_view(), name='Registration'),
    path('userdetils/<int:id>/', UserDetils.as_view(), name='UserDetils'),
]