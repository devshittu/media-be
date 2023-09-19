from django.urls import path
from .views import (CategoryListCreateView, CategoryRetrieveUpdateDestroyView, 
                    StoryListCreateView, StoryRetrieveUpdateDestroyView, StorylineView, 
                    UserFeedView, 
                    LikeCreateView, DislikeCreateView, LikeDestroyView, 
                    DislikeDestroyView, BookmarkCreateListView, BookmarkRetrieveUpdateDestroyView,
                    )



urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),
    path('stories/', StoryListCreateView.as_view(), name='story-list-create'),
    path('user-feed/', UserFeedView.as_view(), name='user-feed'),
    path('stories/<slug:story_slug>/', StoryRetrieveUpdateDestroyView.as_view(), name='story-retrieve-update-destroy'),
    path('stories/<slug:story_slug>/timeline/', StorylineView.as_view(), name='story-timeline'),
    path('stories/<int:story_id>/like/', LikeCreateView.as_view(), name='like-story'),
    path('stories/<int:story_id>/dislike/', DislikeCreateView.as_view(), name='dislike-story'),
    path('stories/<int:story_id>/unlike/', LikeDestroyView.as_view(), name='unlike-story'),
    path('stories/<int:story_id>/undislike/', DislikeDestroyView.as_view(), name='undislike-story'),

    # Add URLs for Media, Category, and UserInterest views.
    path('bookmarks/', BookmarkCreateListView.as_view(), name='bookmark-list-create'),
    path('bookmarks/<int:pk>/', BookmarkRetrieveUpdateDestroyView.as_view(), name='bookmark-retrieve-update-destroy'),
    
]

# stories/urls.py