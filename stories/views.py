from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, status, serializers
from django.db import IntegrityError
from users.models import UserSetting
from stories.neo_models import StoryNode
from .models import Story, Like, Dislike, Bookmark, Category
from .serializers import StorySerializer, BookmarkSerializer, CategorySerializer
from utils.permissions import CustomIsAuthenticated
from utils.mixins import SoftDeleteMixin
from .serializers import (
    LikeSerializer,
    DislikeSerializer,
    CategorySerializer,
    TrendingStorySerializer,
)
from utils.pagination import CustomPageNumberPagination
from utils.permissions import IsOwner
from .mixins import StoryMixin
from django.db.models import F, Count, Q
import logging

logger = logging.getLogger(__name__)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]
    ordering = ["-created_at"]


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StoriesByCategoryView(generics.ListAPIView):
    queryset = Story.active_unflagged_objects.all()
    serializer_class = StorySerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        return self.queryset.filter(category__slug=category_slug)


class StoryListCreateView(generics.ListCreateAPIView):
    """View to list all stories or create a new story."""

    # permission_classes = [CustomIsAuthenticated]
    serializer_class = StorySerializer

    def get_queryset(self):
        stories = (
            Story.objects.all()
            .annotate(
                total_likes=Count("likes_set"), total_dislikes=Count("dislikes_set")
            )
            .prefetch_related("multimedia")
            .order_by("-created_at")
        )

        # Prefetch related StoryNode objects from Neo4j
        story_ids = [story.id for story in stories]
        story_nodes = StoryNode.nodes.filter(story_id__in=story_ids)
        # Create a dictionary to map story IDs to their corresponding StoryNode objects
        story_node_map = {node.story_id: node for node in story_nodes}
        for story in stories:
            story.story_node = story_node_map.get(story.id)

        return stories


class StoryRetrieveUpdateDestroyView(
    SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView
):
    """View to retrieve, update, or delete a story."""

    queryset = Story.objects.all()
    serializer_class = StorySerializer
    lookup_field = "slug"  # Use the slug for lookup
    lookup_url_kwarg = "story_slug"


class UserFeedView(generics.ListAPIView):
    serializer_class = StorySerializer
    # permission_classes = [CustomIsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        logger.debug(f"The logged user: {user}!")

        if not user.is_authenticated:
            logger.debug("User is not authenticated.")
            return Story.objects.none()

        try:
            user_settings = UserSetting.objects.get(user=user)
            preferred_categories = user_settings.personal_settings.get(
                "favorite_categories", []
            )
            logger.debug(f"The preferred_categories: {preferred_categories} found!")
        except UserSetting.DoesNotExist:
            logger.debug("User settings not found.")
            return Story.objects.none()

        if "__all__" in preferred_categories:
            return Story.objects.all().order_by("-created_at")
        elif preferred_categories:
            return Story.objects.filter(category__id__in=preferred_categories).order_by(
                "-created_at"
            )
        else:
            logger.debug("Favorite categories are empty.")
            return Story.objects.none()


class UserInverseFeedView(generics.ListAPIView):
    serializer_class = StorySerializer

    def get_queryset(self):
        user = self.request.user
        print(f"The logged user: {user}!")

        if not user.is_authenticated:
            print("User is not authenticated.")
            return Story.objects.none()

        try:
            user_settings = UserSetting.objects.get(user=user)
            preferred_categories = user_settings.personal_settings.get(
                "favorite_categories", []
            )
            print(f"The preferred_categories: {preferred_categories} found!")
        except UserSetting.DoesNotExist:
            print("User settings not found.")
            return Story.objects.none()

        if "__all__" in preferred_categories:
            # Return an empty queryset if user's favorite categories include all categories
            print("User's favorite categories include all categories.")
            return Story.objects.none()
        elif preferred_categories:
            # Exclude stories from preferred categories
            return Story.objects.exclude(
                category__id__in=preferred_categories
            ).order_by("-created_at")
        else:
            # Return all stories if favorite categories are empty
            return Story.objects.all().order_by("-created_at")


class TrendingStoriesView(generics.ListAPIView):
    serializer_class = TrendingStorySerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Story.objects.none()

        try:
            user_settings = UserSetting.objects.get(user=user)
            favorite_categories = user_settings.personal_settings.get(
                "favorite_categories", []
            )
        except UserSetting.DoesNotExist:
            return Story.objects.none()

        queryset = (
            Story.objects.filter(category__id__in=favorite_categories)
            .annotate(
                like_count=Count("likes_set", distinct=True),
                dislike_count=Count("dislikes_set", distinct=True),
                view_count=Count(
                    "interactions",
                    filter=Q(interactions__interaction_type="view"),
                    distinct=True,
                ),
            )
            .annotate(
                calculated_trending_score=F("like_count")
                - F("dislike_count")
                + F("view_count")
            )
            .order_by("-calculated_trending_score")
        )

        return queryset


class LikeCreateView(StoryMixin, generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [CustomIsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise serializers.ValidationError("You have already liked this story.")


class DislikeCreateView(StoryMixin, generics.CreateAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    permission_classes = [CustomIsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise serializers.ValidationError("You have already disliked this story.")


class LikeDestroyView(StoryMixin, generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [CustomIsAuthenticated]

    def get_queryset(self):
        story_id = self.kwargs.get("story_id")
        story_slug = self.kwargs.get("story_slug")

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
    permission_classes = [CustomIsAuthenticated]

    def get_queryset(self):
        story_id = self.kwargs.get("story_id")
        story_slug = self.kwargs.get("story_slug")

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
    permission_classes = [CustomIsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Bookmark.objects.filter(user=user)

        # Get the 'category' query parameter
        category = self.request.query_params.get("category", None)
        if category is not None:
            queryset = queryset.filter(bookmark_category=category)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        story_id = serializer.validated_data.get(
            "story_id"
        ).id  # Get the ID of the story instance

        # Check if the story has already been bookmarked by the user
        if Bookmark.objects.filter(story_id=story_id, user=user).exists():
            raise serializers.ValidationError(
                {"detail": "You have already bookmarked this story."}
            )

        # Update the validated_data with user and story_id
        validated_data = serializer.validated_data
        validated_data.update({"user": user, "story_id": story_id})

        # Save the bookmark with the updated validated_data
        serializer.save(**validated_data)

    def create(self, request, *args, **kwargs):
        response = super(BookmarkCreateListView, self).create(request, *args, **kwargs)

        # Check if creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            response.data = {"status": "success", "data": response.data}
        # Note: If there are other status codes you want to handle, you can add more conditions.
        return response


class BaseBookmarkView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [CustomIsAuthenticated, IsOwner]

    def get_user_bookmark(self, lookup_field, lookup_value):
        user = self.request.user
        filter_kwargs = {lookup_field: lookup_value, "user": user}
        return get_object_or_404(Bookmark, **filter_kwargs)


class BookmarkRetrieveUpdateDestroyView(BaseBookmarkView):
    def get_object(self):
        bookmark_id = self.kwargs.get("bookmark_id")
        return self.get_user_bookmark("pk", bookmark_id)


class BookmarkRetrieveUpdateDestroyViewByStoryId(BaseBookmarkView):
    def get_object(self):
        story_id = self.kwargs.get("story_id")
        return self.get_user_bookmark("story_id", story_id)


# stories/views.py
