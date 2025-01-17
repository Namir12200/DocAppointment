from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from .views import UserListView, ProfileListView, ProfileDetailView, UserDetailView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserListView.as_view(), name='register'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', ProfileListView.as_view(), name="profile"),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
]