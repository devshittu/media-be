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
from utils.permissions import CustomIsAuthenticated
from utils.error_codes import ErrorCode
from rest_framework import serializers
from rest_framework.exceptions import APIException
from .utils import create_default_settings
import logging

logger = logging.getLogger('app_logger')


class UserListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of users or create a new user.
    """
    # Must be admin to create a new user
    # permission_classes = [CustomIsAuthenticated, IsStaffUser]
    queryset = CustomUser.objects.all().order_by("-id")
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        """
        Exclude the authenticated user from the queryset if they are authenticated.
        Otherwise, return all users.
        """
        user = self.request.user
        if user.is_authenticated:
            logger.debug(
                f'Authenticated user: {user.id}, excluding them from the list')
            queryset = CustomUser.objects.exclude(id=user.id).order_by("-id")
        else:
            logger.debug('User is not authenticated, returning all users')
            queryset = CustomUser.objects.all().order_by("-id")
        return queryset


class UserRetrieveUpdateDestroyView(
    SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    API view to retrieve, update, or delete a user.
    """

    # Must be authenticated to update user information.
    permission_classes = [CustomIsAuthenticated]
    queryset = CustomUser.objects.all().order_by("-id")
    serializer_class = CustomUserSerializer


# class UserSettingView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserSettingSerializer
#     permission_classes = [CustomIsAuthenticated]

#     def get_object(self):
#         try:
#             return UserSetting.objects.get(user=self.request.user)
#         except UserSetting.DoesNotExist:
#             raise APIException(
#                 {
#                     "code": ErrorCode.SETTINGS_NOT_FOUND,
#                     "detail": "User settings not found.",
#                 }
#             )

#     def update(self, request, *args, **kwargs):
#         try:
#             return super().update(request, *args, **kwargs)
#         except Exception as e:
#             raise APIException(
#                 {"code": ErrorCode.SETTINGS_UPDATE_FAILED, "detail": str(e)}
#             )


class UserSettingView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve or update the authenticated user's settings.
    """
    serializer_class = UserSettingSerializer
    permission_classes = [CustomIsAuthenticated]

    def get_object(self):
        try:
            # Fetch the existing UserSetting object
            return UserSetting.objects.get(user=self.request.user)
        except UserSetting.DoesNotExist:
            # In the unlikely event this happens, create default settings
            return create_default_settings(self.request.user)

    def update(self, request, *args, **kwargs):
        # Remove fields that should not be updated
        restricted_fields = ['email', 'user_id',
                             'username', 'id', 'created_at', 'updated_at']
        for field in restricted_fields:
            request.data.pop(field, None)
            request.data.get('account_settings', {}).pop(field, None)

        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            raise APIException(
                {"code": ErrorCode.SETTINGS_UPDATE_FAILED, "detail": str(e)}
            )


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
    permission_classes = [CustomIsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["follower__username", "timestamp"]
    ordering = ["-timestamp"]  # Default ordering: recent followers

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Follow.objects.filter(followed__id=user_id)


class FollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [CustomIsAuthenticated]

    def perform_create(self, serializer):
        try:
            followed_user = CustomUser.objects.get(
                pk=self.kwargs.get("user_id", None))
        except (CustomUser.DoesNotExist, ValueError):
            followed_user = get_object_or_404(
                CustomUser, username=self.kwargs.get("username", "")
            )

        # Prevent user from following themselves
        if self.request.user == followed_user:
            raise serializers.ValidationError(
                {"detail": "You cannot follow yourself."})

        try:
            serializer.save(follower=self.request.user, followed=followed_user)
        except IntegrityError:
            raise serializers.ValidationError(
                {"detail": "You are already following this user."}
            )

    def create(self, request, *args, **kwargs):
        response = super(FollowUserView, self).create(request, *args, **kwargs)

        # Check if creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            response.data = {"status": "success", "data": response.data}
        # Note: If there are other status codes you want to handle, you can add more conditions.
        return response


class UnfollowUserView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    permission_classes = [CustomIsAuthenticated]

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
