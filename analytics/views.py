from rest_framework import generics, permissions, viewsets
from .models import (
    StoryInteraction, DeviceData, LocationData, 
    ReferralData, UserSession, UserNotInterested, AccessibilityTool
)
from .serializers import (
    StoryInteractionSerializer, DeviceDataSerializer, LocationDataSerializer, 
    ReferralDataSerializer, AccessibilityToolSerializer, UserNotInterestedSerializer, UserSessionSerializer
)

# DeviceData views
class DeviceDataListCreateView(generics.ListCreateAPIView):
    queryset = DeviceData.objects.all()
    serializer_class = DeviceDataSerializer

class DeviceDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeviceData.objects.all()
    serializer_class = DeviceDataSerializer

# LocationData views
class LocationDataListCreateView(generics.ListCreateAPIView):
    queryset = LocationData.objects.all()
    serializer_class = LocationDataSerializer

class LocationDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocationData.objects.all()
    serializer_class = LocationDataSerializer

# ReferralData views
class ReferralDataListCreateView(generics.ListCreateAPIView):
    queryset = ReferralData.objects.all()
    serializer_class = ReferralDataSerializer

class ReferralDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReferralData.objects.all()
    serializer_class = ReferralDataSerializer

# UserSession views
class UserSessionListCreateView(generics.ListCreateAPIView):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer

class UserSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer

# StoryInteraction views
class StoryInteractionListCreateView(generics.ListCreateAPIView):
    queryset = StoryInteraction.objects.all()
    serializer_class = StoryInteractionSerializer

class StoryInteractionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StoryInteraction.objects.all()
    serializer_class = StoryInteractionSerializer

# UserNotInterested views
class UserNotInterestedListCreateView(generics.ListCreateAPIView):
    queryset = UserNotInterested.objects.all()
    serializer_class = UserNotInterestedSerializer

class UserNotInterestedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserNotInterested.objects.all()
    serializer_class = UserNotInterestedSerializer

# AccessibilityTool views
class AccessibilityToolListCreateView(generics.ListCreateAPIView):
    queryset = AccessibilityTool.objects.all()
    serializer_class = AccessibilityToolSerializer

class AccessibilityToolDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccessibilityTool.objects.all()
    serializer_class = AccessibilityToolSerializer

# analytics/views.py