import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Multimedia
from .serializers import MultimediaSerializer
from utils import permissions
from utils.mixins import SoftDeleteMixin

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class MultimediaListCreateView(generics.ListCreateAPIView):
    """
    API view to list all multimedia or create a new multimedia.
    """
    queryset = Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Save the post data when creating a new multimedia."""
        try:
            logger.debug('Attempting to save new multimedia')
            serializer.save(user=self.request.user)
            logger.info(f"Multimedia created by user {self.request.user}")
        except Exception as e:
            logger.error(f"Error creating multimedia: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            logger.debug('Creating new multimedia via API')
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MultimediaRetrieveUpdateDestroyView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a multimedia.
    """
    queryset = Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, permissions.IsOwnerOrReadOnly]

    def handle_exception(self, exc):
        """Handle exceptions and return custom error response."""
        logger.error(f"Exception handled: {exc}")
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        hard_delete = request.query_params.get(
            'hard', 'false').lower() == 'true'
        instance = self.get_object()

        if hard_delete:
            logger.debug('Performing hard delete on multimedia')
            instance.hard_delete()
            logger.info(f"Hard deleted multimedia {instance.id}")
            return Response(status=status.HTTP_204_NO_CONTENT)

        logger.debug('Performing soft delete on multimedia')
        return super().destroy(request, *args, **kwargs)

# multimedia/views.py
