from django.urls import path
from . import views

urlpatterns = [
    path('interactions/', views.StoryInteractionListCreateView.as_view(), name='storyinteraction-list'),
    path('interactions/<int:pk>/', views.StoryInteractionDetailView.as_view(), name='storyinteraction-detail'),
    path('interactions/batch/', views.StoryInteractionBatchCreateView.as_view(), name='storyinteractions-batch-create'),
    
    path('sessions/', views.UserSessionListCreateView.as_view(), name='usersession-list'),
    path('sessions/<int:pk>/', views.UserSessionDetailView.as_view(), name='usersession-detail'),

    path('not-interested/', views.UserNotInterestedListCreateView.as_view(), name='usernotinterested-list'),
    path('not-interested/<int:pk>/', views.UserNotInterestedDetailView.as_view(), name='usernotinterested-detail'),

    path('accessibility-tools/', views.AccessibilityToolListCreateView.as_view(), name='accessibilitytool-list'),
    path('accessibility-tools/<int:pk>/', views.AccessibilityToolDetailView.as_view(), name='accessibilitytool-detail'),
]

# analytics/urls.py