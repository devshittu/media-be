from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView, SettingsListCreateView, CategoryListCreateView, CurrentUserView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('settings/', SettingsListCreateView.as_view(), name='settings-list-create'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
]
