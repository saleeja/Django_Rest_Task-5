from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('profiles/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='profile-detail'),
    path('profiles/<int:pk>/update/', ProfileUpdateAPIView.as_view(), name='profile-update'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('users/delete_all/', UserDeleteAllAPIView.as_view(), name='user-delete-all'),
    path('users/bulk-delete/', UserBulkDeleteAPIView.as_view(), name='user-bulk-delete'),


]