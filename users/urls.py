from django.urls import path
from .views import (UserListCreateView, UserRetrieveUpdateDestroyView, UserSettingListCreateView, 
                    FollowUserView, UnfollowUserView, UserFollowersListView, 
                    UpdateFeedPositionView, UnfollowedUsersView)

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),

    path('unfollowed/', UnfollowedUsersView.as_view(), name='unfollowed-users'),
    
    path('settings/', UserSettingListCreateView.as_view(), name='user-settings-list-create'),

    path('update-feed-position/', UpdateFeedPositionView.as_view(), name='update-feed-position'),

    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user-by-id'),
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow-user-by-username'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user-by-id'),
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow-user-by-username'),
    
    path('<int:user_id>/followers/', UserFollowersListView.as_view(), name='user-followers-list'),
    
]
