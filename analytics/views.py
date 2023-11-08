from rest_framework import generics, status, permissions
from .models import (
    StoryInteraction,
    UserSession,
    UserNotInterested,
    AccessibilityTool,
    StoryInteractionMetadataSchema,
)
from .serializers import (
    StoryInteractionSerializer,
    AccessibilityToolSerializer,
    UserNotInterestedSerializer,
    UserSessionSerializer,
)
from rest_framework.response import Response


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


class StoryInteractionBatchCreateView(generics.CreateAPIView):
    queryset = StoryInteraction.objects.all()
    serializer_class = StoryInteractionSerializer

    def create(self, request, *args, **kwargs):
        # Check if the incoming request is a list
        if not isinstance(request.data, list):
            return Response(
                {"detail": 'Expected a list of items but got type "dict".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Serialize the data
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        # Bulk create
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Check if the user is authenticated and add them to the serializer's save method
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


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
