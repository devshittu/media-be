from rest_framework import generics, status
from rest_framework.response import Response
from .models import Multimedia
from .serializers import MultimediaSerializer
from rest_framework.exceptions import ValidationError
from utils import permissions
from utils.mixins import SoftDeleteMixin
import json

class MultimediaListCreateView(generics.ListCreateAPIView):
    """
    API view to list all multimedia or create a new multimedia.
    """

    queryset = Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    permission_classes = [
        # permissions.IsAuthenticatedOrReadOnly,
        permissions.IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        """Save the post data when creating a new multimedia."""
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            # Before creating, validate incoming JSON data if necessary
            # This could be done in the serializer or here before saving
            response = super().create(request, *args, **kwargs)

            # Get the created object from the response data
            created_object = response.data

            # Generate the media URL using the created object's filename
            media_url = self.request.build_absolute_uri(created_object["file"])

            # Add the media URL to the response data
            created_object["media_url"] = media_url

            return Response(created_object, status=response.status_code)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError as e:  # Catch JSON decode errors explicitly
            return Response(
                {"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST
            )


class MultimediaRetrieveUpdateDestroyView(
    SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    API view to retrieve, update, or delete a multimedia.
    """

    queryset = Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    permission_classes = [
        # permissions.IsAuthenticatedOrReadOnly,
        permissions.IsOwnerOrReadOnly,
    ]

    def handle_exception(self, exc):
        """Handle exceptions and return custom error response."""
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        hard_delete = request.query_params.get("hard", "false").lower() == "true"
        instance = self.get_object()

        if hard_delete:
            instance.hard_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return super().destroy(request, *args, **kwargs)


# multimedia/views.py
