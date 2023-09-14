from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.ReportCreateView.as_view(), name='report-create'),
]
