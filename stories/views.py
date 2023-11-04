from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, status, serializers
from django.db import IntegrityError

from stories.neo_models import StoryNode
from .models import Story,  Like, Dislike, Bookmark, Category
from .serializers import StorySerializer, BookmarkSerializer, CategorySerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.mixins import SoftDeleteMixin
from .serializers import LikeSerializer, DislikeSerializer, CategorySerializer
from utils.pagination import CustomPageNumberPagination
from .mixins import StoryMixin
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
        stories = Story.objects.all()\
            .annotate(
                total_likes=Count('likes_set'),
                total_dislikes=Count('dislikes_set')
            )\
            .prefetch_related('multimedia')\
            .order_by('-created_at')
        
        # Prefetch related StoryNode objects from Neo4j
        story_ids = [story.id for story in stories]
        story_nodes = StoryNode.nodes.filter(story_id__in=story_ids)
        # Create a dictionary to map story IDs to their corresponding StoryNode objects
        story_node_map = {node.story_id: node for node in story_nodes}
        for story in stories:
            story.story_node = story_node_map.get(story.id)

        return stories


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


class LikeCreateView(StoryMixin, generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise serializers.ValidationError("You have already liked this story.")



class DislikeCreateView(StoryMixin, generics.CreateAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise serializers.ValidationError("You have already disliked this story.")



class LikeDestroyView(StoryMixin, generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        story_id = self.kwargs.get('story_id')
        story_slug = self.kwargs.get('story_slug')
        
        if story_id:
            return self.queryset.filter(user=self.request.user, story__id=story_id)
        elif story_slug:
            return self.queryset.filter(user=self.request.user, story__slug=story_slug)

    def get_object(self):
        story = self.get_story()
        obj = get_object_or_404(Like, user=self.request.user, story=story)
        self.check_object_permissions(self.request, obj)
        return obj

class DislikeDestroyView(StoryMixin, generics.DestroyAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        story_id = self.kwargs.get('story_id')
        story_slug = self.kwargs.get('story_slug')
        
        if story_id:
            return self.queryset.filter(user=self.request.user, story__id=story_id)
        elif story_slug:
            return self.queryset.filter(user=self.request.user, story__slug=story_slug)

    def get_object(self):
        story = self.get_story()
        obj = get_object_or_404(Like, user=self.request.user, story=story)
        self.check_object_permissions(self.request, obj)
        return obj

class BookmarkCreateListView(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    # permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        user = self.request.user
        story_id = serializer.validated_data.get('story_id').id  # Get the ID of the story instance
        
        # Check if the story has already been bookmarked by the user
        if Bookmark.objects.filter(story_id=story_id, user=user).exists():
            raise serializers.ValidationError({"detail": "You have already bookmarked this story."})
        
        # Update the validated_data with user and story_id
        validated_data = serializer.validated_data
        validated_data.update({
            'user': user,
            'story_id': story_id
        })
        
        # Save the bookmark with the updated validated_data
        serializer.save(**validated_data)


    def create(self, request, *args, **kwargs):
        response = super(BookmarkCreateListView, self).create(request, *args, **kwargs)
        
        # Check if creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            response.data = {
                "status": "success",
                "data": response.data
            }
        # Note: If there are other status codes you want to handle, you can add more conditions.
        return response


class BookmarkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the story ID from the URL
        story_id = self.kwargs.get('story_id')
        # Get the authenticated user
        user = self.request.user
        # Try to get the bookmark based on the story ID and user
        bookmark = get_object_or_404(Bookmark, story_id=story_id, user=user)
        return bookmark

# stories/views.py