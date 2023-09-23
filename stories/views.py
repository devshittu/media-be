from django.db.models import Count
from rest_framework import generics, filters
from .models import Story,  Like, Dislike, Bookmark, Category
from .serializers import StorySerializer, BookmarkSerializer, CategorySerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.mixins import SoftDeleteMixin
from .serializers import LikeSerializer, DislikeSerializer, CategorySerializer
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


class StoriesByCategoryView(generics.ListAPIView):
    queryset = Story.active_unflagged_objects.all()
    serializer_class = StorySerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        return self.queryset.filter(category__slug=category_slug)


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


#             return Response({"error": "Pagination error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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