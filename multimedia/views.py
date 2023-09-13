from rest_framework import generics, status
from rest_framework.response import Response
from .models import Multimedia
from .serializers import MultimediaSerializer
from rest_framework.exceptions import ValidationError
from utils import permissions

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
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MultimediaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a multimedia.
    """
    queryset = Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.IsOwnerOrReadOnly]

    def handle_exception(self, exc):
        """Handle exceptions and return custom error response."""
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
