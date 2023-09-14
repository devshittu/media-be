from django.urls import path
from . import views

urlpatterns = [
    path('interactions/', views.StoryInteractionListCreateView.as_view(), name='storyinteraction-list'),
    path('interactions/<int:pk>/', views.StoryInteractionDetailView.as_view(), name='storyinteraction-detail'),

    path('devices/', views.DeviceDataListCreateView.as_view(), name='devicedata-list'),
    path('devices/<int:pk>/', views.DeviceDataDetailView.as_view(), name='devicedata-detail'),

    path('locations/', views.LocationDataListCreateView.as_view(), name='locationdata-list'),
    path('locations/<int:pk>/', views.LocationDataDetailView.as_view(), name='locationdata-detail'),

    path('referrals/', views.ReferralDataListCreateView.as_view(), name='referraldata-list'),
    path('referrals/<int:pk>/', views.ReferralDataDetailView.as_view(), name='referraldata-detail'),

    path('sessions/', views.UserSessionListCreateView.as_view(), name='usersession-list'),
    path('sessions/<int:pk>/', views.UserSessionDetailView.as_view(), name='usersession-detail'),

    path('not-interested/', views.UserNotInterestedListCreateView.as_view(), name='usernotinterested-list'),
    path('not-interested/<int:pk>/', views.UserNotInterestedDetailView.as_view(), name='usernotinterested-detail'),

    path('accessibility-tools/', views.AccessibilityToolListCreateView.as_view(), name='accessibilitytool-list'),
    path('accessibility-tools/<int:pk>/', views.AccessibilityToolDetailView.as_view(), name='accessibilitytool-detail'),
]

# analytics/urls.py