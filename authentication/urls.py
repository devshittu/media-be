from django.urls import path
from . import views
from users.views import UserSettingView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    # Custom user views
    # path('users/', views.UserListView.as_view(), name='user-list'),
    # path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('complete_setup/', views.CompleteSetupView.as_view(), name='complete-setup'),
    path('me/', views.MeView.as_view(), name='me'),
    path('me/settings/', UserSettingView.as_view(), name='user-settings'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# authentication/urls.py