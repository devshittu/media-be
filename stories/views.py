from rest_framework import generics
from .models import Story, Media, Category, UserInterest
from .serializers import StorySerializer, MediaSerializer, CategorySerializer, UserInterestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .pagination import CenteredPagination
from core.settings import ANCESTORS_PER_PAGE, DESCENDANTS_PER_PAGE

class StoryListCreateView(generics.ListCreateAPIView):
    """View to list all stories or create a new story."""
    queryset = Story.objects.all()
    serializer_class = StorySerializer

class StoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a story."""
    queryset = Story.objects.all()
    serializer_class = StorySerializer


class StorylineView(APIView):
    pagination_class = CenteredPagination

    def get(self, request, story_slug):
        try:
            leading_story = Story.objects.get(slug=story_slug)
        except Story.DoesNotExist:
            return Response({"error": "Story not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the leading story, its ancestors, and its descendants based on configuration
        ancestors = leading_story.get_all_parents()[:ANCESTORS_PER_PAGE]
        descendants = leading_story.get_all_children()[:DESCENDANTS_PER_PAGE]
        timeline = ancestors + [leading_story] + descendants

        # Paginate the timeline
        page = self.pagination_class().paginate_queryset(timeline, request, self)
        if page is not None:
            serialized_timeline = StorySerializer(page, many=True, context={'leading_slug': story_slug}).data
            return self.pagination_class().get_paginated_response(serialized_timeline)

# stories/views.py