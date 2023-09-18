from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView, UserSettingListCreateView, FollowUserView, UnfollowUserView, UserFollowersListView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('settings/', UserSettingListCreateView.as_view(), name='user-settings-list-create'),

    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),

    path('<int:user_id>/followers/', UserFollowersListView.as_view(), name='user-followers-list'),
    
]
