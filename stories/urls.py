from django.urls import path
from . import views

urlpatterns = [
    path('stories/', views.StoryListCreateView.as_view(), name='story-list-create'),
    path('stories/<int:pk>/', views.StoryRetrieveUpdateDestroyView.as_view(), name='story-retrieve-update-destroy'),
    path('stories/timeline/<slug:story_slug>/', views.StorylineView.as_view(), name='story-timeline'),
    
    # Add URLs for Media, Category, and UserInterest views.
]

# stories/urls.py