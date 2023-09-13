from rest_framework import generics, permissions, viewsets
from .models import (
    StoryInteraction, DeviceData, LocationData, 
    ReferralData, UserSession, UserNotInterested, AccessibilityTool
)
from .serializers import (
    StoryInteractionSerializer, DeviceDataSerializer, LocationDataSerializer, 
    ReferralDataSerializer, AccessibilityToolSerializer, UserNotInterestedSerializer, UserSessionSerializer
)
from core import permissions
class StoryInteractionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing story interactions.
    """
    queryset = StoryInteraction.objects.all().select_related('user', 'story', 'session')
    serializer_class = StoryInteractionSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Save the user when creating a new story interaction.
        """
        serializer.save(user=self.request.user)


class DeviceDataViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing device data.
    """
    queryset = DeviceData.objects.all().select_related('interaction')
    serializer_class = DeviceDataSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class LocationDataViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing location data.
    """
    queryset = LocationData.objects.all().select_related('interaction')
    serializer_class = LocationDataSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class ReferralDataViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing referral data.
    """
    queryset = ReferralData.objects.all().select_related('interaction')
    serializer_class = ReferralDataSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class UserSessionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user sessions.
    """
    queryset = UserSession.objects.all().select_related('user').prefetch_related('device_data', 'location_data')
    serializer_class = UserSessionSerializer  # Assuming you have a serializer for UserSession
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class UserNotInterestedViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing stories users are not interested in.
    """
    queryset = UserNotInterested.objects.all().select_related('user', 'story')
    serializer_class = UserNotInterestedSerializer  # Assuming you have a serializer for UserNotInterested
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class AccessibilityToolViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing accessibility tools used by users.
    """
    queryset = AccessibilityTool.objects.all().select_related('user')
    serializer_class = AccessibilityToolSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Save the user when creating a new accessibility tool record.
        """
        serializer.save(user=self.request.user)

# analytics/views.py