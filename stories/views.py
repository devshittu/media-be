from rest_framework import generics
from .models import Story,  Like, Dislike, Bookmark
from .serializers import StorySerializer, BookmarkSerializer, CategorySerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .pagination import CenteredPagination
from core.settings import ANCESTORS_PER_PAGE, DESCENDANTS_PER_PAGE
from utils.mixins import SoftDeleteMixin
from .serializers import LikeSerializer, DislikeSerializer

class StoryListCreateView(generics.ListCreateAPIView):
    """View to list all stories or create a new story."""
    queryset = Story.objects.all()
    serializer_class = StorySerializer

class StoryRetrieveUpdateDestroyView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a story."""
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    lookup_field = 'slug'  # Use the slug for lookup
    lookup_url_kwarg = 'story_slug'


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


class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DislikeCreateView(generics.CreateAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeDestroyView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = 'story'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class DislikeDestroyView(generics.DestroyAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    lookup_field = 'story'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
class BookmarkCreateListView(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def perform_create(self, serializer):
        serializer.save()

class BookmarkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer


# stories/views.py