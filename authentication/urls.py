from django.urls import path
from . import views

urlpatterns = [
    # Custom user views
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('complete_setup/', views.CompleteSetupView.as_view(), name='complete-setup'),
    
    # Default dj-rest-auth views can be included here
]
