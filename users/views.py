from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework import generics, filters, status
from .models import UserSetting, Follow, UserFeedPosition
from .serializers import UserSettingSerializer, FollowSerializer
from common.serializers import CustomUserSerializer
from authentication.models import CustomUser
from utils.mixins import SoftDeleteMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from stories.models import Story
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsActiveUser, IsStaffUser, HasRoleReader
from rest_framework import serializers


class UserListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of users or create a new user.
    """

    # Must be admin to create a new user
    # permission_classes = [IsAuthenticated, IsStaffUser]
    queryset = CustomUser.objects.all().order_by("-id")
    serializer_class = CustomUserSerializer


class UserRetrieveUpdateDestroyView(
    SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    API view to retrieve, update, or delete a user.
    """

    # Must be authenticated to update user information.
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all().order_by("-id")
    serializer_class = CustomUserSerializer


class UserSettingView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve or update the authenticated user's settings.
    """

    serializer_class = UserSettingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserSetting.objects.get(user=self.request.user)


class UserSettingListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of settings or create new settings.
    """

    queryset = UserSetting.objects.all()
    serializer_class = UserSettingSerializer


class UpdateFeedPositionView(APIView):
    def patch(self, request, *args, **kwargs):
        story_id = request.data.get("story_id")
        story = get_object_or_404(Story, id=story_id)

        feed_position, created = UserFeedPosition.objects.get_or_create(
            user=request.user
        )
        feed_position.update_position(story)

        return Response(
            {"message": "Position updated successfully."}, status=status.HTTP_200_OK
        )


class UserFollowersListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["follower__username", "timestamp"]
    ordering = ["-timestamp"]  # Default ordering: recent followers

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Follow.objects.filter(followed__id=user_id)


class FollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            followed_user = CustomUser.objects.get(pk=self.kwargs.get("user_id", None))
        except (CustomUser.DoesNotExist, ValueError):
            followed_user = get_object_or_404(
                CustomUser, username=self.kwargs.get("username", "")
            )
        
        # Prevent user from following themselves
        if self.request.user == followed_user:
            raise serializers.ValidationError({"detail": "You cannot follow yourself."})

        try:
            serializer.save(follower=self.request.user, followed=followed_user)
        except IntegrityError:
            raise serializers.ValidationError({"detail": "You are already following this user."})

    def create(self, request, *args, **kwargs):
        response = super(FollowUserView, self).create(request, *args, **kwargs)
        
        # Check if creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            response.data = {
                "status": "success",
                "data": response.data
            }
        # Note: If there are other status codes you want to handle, you can add more conditions.
        return response

class UnfollowUserView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Follow.objects.get(
                follower=self.request.user,
                followed__pk=self.kwargs.get("user_id", None),
            )
        except (Follow.DoesNotExist, ValueError):
            followed_user = get_object_or_404(
                CustomUser, username=self.kwargs.get("username", "")
            )
            return get_object_or_404(
                Follow, follower=self.request.user, followed=followed_user
            )


class UnfollowedUsersView(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.not_followed_by(user).order_by("id")


# users/views.py
