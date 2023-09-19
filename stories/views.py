from django.db.models import Count
from rest_framework import generics, filters
from .models import Story,  Like, Dislike, Bookmark, Category
from .serializers import StorySerializer, BookmarkSerializer, CategorySerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .pagination import CenteredPagination
from core.settings import ANCESTORS_PER_PAGE, DESCENDANTS_PER_PAGE
from utils.mixins import SoftDeleteMixin
from .serializers import LikeSerializer, DislikeSerializer, CategorySerializer
from users.models import UserSetting
from utils.pagination import CustomPageNumberPagination

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']
    ordering = ['-created_at']

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StoryListCreateView(generics.ListCreateAPIView):
    """View to list all stories or create a new story."""
    # queryset = Story.objects.all()
    serializer_class = StorySerializer

    def get_queryset(self):
        return Story.objects.all()\
            .annotate(
                total_likes=Count('likes_set'),
                total_dislikes=Count('dislikes_set')
            )\
            .prefetch_related('multimedia')

class StoryRetrieveUpdateDestroyView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a story."""
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    lookup_field = 'slug'  # Use the slug for lookup
    lookup_url_kwarg = 'story_slug'



# from django.db.models import Q

# class StorylineView(APIView):
#     pagination_class = CenteredPagination

#     def get(self, request, story_slug):
#         print("Received slug:", story_slug)
#         all_slugs = Story.objects.values_list('slug', flat=True)
#         print("All slugs in database:", all_slugs)
#         try:
#             leading_story = Story.objects.get(slug=story_slug)
#         except Story.DoesNotExist:
#             return Response({"error": "Story not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Fetch the leading story, its ancestors, and its descendants based on configuration
#         ancestors = leading_story.get_all_parents()[:ANCESTORS_PER_PAGE]
#         descendants = leading_story.get_all_children()[:DESCENDANTS_PER_PAGE]
#         timeline_ids = [story.id for story in ancestors + [leading_story] + descendants]

#         # Convert the list of stories back to a queryset
#         timeline_queryset = Story.objects.filter(id__in=timeline_ids)

#         # Paginate the timeline
#         page = self.pagination_class().paginate_queryset(timeline_queryset, request, view=self)
#         if page is not None:
#             serialized_timeline = StorySerializer(page, many=True, context={'leading_slug': story_slug}).data
#             return self.pagination_class().get_paginated_response(serialized_timeline)

class StorylineView(APIView):
    pagination_class = CenteredPagination

    def get(self, request, story_slug):
        print(f"Inside StorylineView.get with slug: {story_slug}")

        try:
            leading_story = Story.objects.get(slug=story_slug)
            print(f"Found story with title: {leading_story.title}")
        except Story.DoesNotExist:
            print("Error: Story not found in direct query.")
            return Response({"error": "Story not found."}, status=status.HTTP_404_NOT_FOUND)

        ancestors = leading_story.get_all_parents()[:ANCESTORS_PER_PAGE]
        descendants = leading_story.get_all_children()[:DESCENDANTS_PER_PAGE]
        timeline = ancestors + [leading_story] + descendants

        print(f"Ancestors count: {len(ancestors)}, Descendants count: {len(descendants)}, Total timeline count: {len(timeline)}")

        page = self.pagination_class().paginate_queryset(timeline, request, view=self)
        if page is not None:
            serialized_timeline = StorySerializer(page, many=True, context={'leading_slug': story_slug}).data
            return self.pagination_class().get_paginated_response(serialized_timeline)
        else:
            print("Error: Page is None after pagination.")
            return Response({"error": "Pagination error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserFeedView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        stories = Story.objects.for_user(request.user)
        
        # Create an instance of the pagination class
        paginator = self.pagination_class()

        # Apply pagination using the paginator instance
        page = paginator.paginate_queryset(stories, request)
        if page is not None:
            serializer = StorySerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)  # Use the same paginator instance

        serializer = StorySerializer(stories, many=True, context={'request': request})
        return Response(serializer.data)


class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

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