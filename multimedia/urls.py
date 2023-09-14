from django.urls import path
from . import views

urlpatterns = [
    path('multimedia/', views.MultimediaListCreateView.as_view(), name='multimedia-list-create'),
    path('multimedia/<int:pk>/', views.MultimediaRetrieveUpdateDestroyView.as_view(), name='multimedia-detail'),
]
