from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView,)
from .views import *
urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_refresh'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', Registration.as_view(), name='Registration'),
    path('googeregister/', GoogleRegistration.as_view(), name='Googeregister'),
    path('logout/', LogoutView.as_view(), name ='logout'),
    path('userdetils/<int:id>/', UserDetils.as_view(), name='UserDetils'),
    path('profile-update/<int:id>/', ProfileimageUpdateView.as_view(), name='ProfileimageUpdateView'),
   
    path('changepassword/', ChangePassword.as_view(), name='ChangePassword'),
]

