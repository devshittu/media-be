import logging
from rest_framework import generics, status, permissions
from rest_framework.response import Response
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

# Set up the logger for this module
logger = logging.getLogger('app_logger')


# UserSession views
class UserSessionListCreateView(generics.ListCreateAPIView):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer

    def list(self, request, *args, **kwargs):
        logger.debug('Listing all user sessions')
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.debug('Creating a new user session')
        return super().create(request, *args, **kwargs)


class UserSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer

    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving user session with id {kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating user session with id {kwargs['pk']}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.debug(f"Partially updating user session with id {kwargs['pk']}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting user session with id {kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)


# StoryInteraction views
class StoryInteractionListCreateView(generics.ListCreateAPIView):
    queryset = StoryInteraction.objects.all()
    serializer_class = StoryInteractionSerializer

    def list(self, request, *args, **kwargs):
        logger.debug('Listing all story interactions')
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.debug('Creating a new story interaction')
        return super().create(request, *args, **kwargs)


class StoryInteractionBatchCreateView(generics.CreateAPIView):
    queryset = StoryInteraction.objects.all()
    serializer_class = StoryInteractionSerializer

    def create(self, request, *args, **kwargs):
        # Check if the incoming request is a list
        logger.debug('Batch creating story interactions')
        if not isinstance(request.data, list):
            logger.warning('Expected a list of items but got type "dict"')
            return Response(
                {"detail": 'Expected a list of items but got type "dict".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Serialize the data
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        # Bulk create
        self.perform_create(serializer)
        logger.info('Successfully batch created story interactions')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Check if the user is authenticated and add them to the serializer's save method
        user = self.request.user if self.request.user.is_authenticated else None
        logger.debug(f'Performing create with user: {user}')
        serializer.save(user=user)


class StoryInteractionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StoryInteraction.objects.all()
    serializer_class = StoryInteractionSerializer

    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving story interaction with id {kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating story interaction with id {kwargs['pk']}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.debug(
            f"Partially updating story interaction with id {kwargs['pk']}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting story interaction with id {kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)


# UserNotInterested views
class UserNotInterestedListCreateView(generics.ListCreateAPIView):
    queryset = UserNotInterested.objects.all()
    serializer_class = UserNotInterestedSerializer

    def list(self, request, *args, **kwargs):
        logger.debug('Listing all user not interested entries')
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.debug('Creating a new user not interested entry')
        return super().create(request, *args, **kwargs)


class UserNotInterestedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserNotInterested.objects.all()
    serializer_class = UserNotInterestedSerializer

    def retrieve(self, request, *args, **kwargs):
        logger.debug(
            f"Retrieving user not interested entry with id {kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug(
            f"Updating user not interested entry with id {kwargs['pk']}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.debug(
            f"Partially updating user not interested entry with id {kwargs['pk']}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug(
            f"Deleting user not interested entry with id {kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)


# AccessibilityTool views
class AccessibilityToolListCreateView(generics.ListCreateAPIView):
    queryset = AccessibilityTool.objects.all()
    serializer_class = AccessibilityToolSerializer

    def list(self, request, *args, **kwargs):
        logger.debug('Listing all accessibility tools')
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.debug('Creating a new accessibility tool')
        return super().create(request, *args, **kwargs)


class AccessibilityToolDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccessibilityTool.objects.all()
    serializer_class = AccessibilityToolSerializer

    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving accessibility tool with id {kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating accessibility tool with id {kwargs['pk']}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.debug(
            f"Partially updating accessibility tool with id {kwargs['pk']}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting accessibility tool with id {kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)


# analytics/views.py
