from rest_framework import generics, filters
from .models import UserSetting, Follow
from .serializers import UserSettingSerializer, FollowSerializer
from authentication.serializers import CustomUserSerializer
from rest_framework import permissions
from authentication.models import CustomUser
from utils.mixins import SoftDeleteMixin

class UserListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of users or create a new user.
    """
    # TODO: Must be admin to create a new user
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UserRetrieveUpdateDestroyView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a user.
    """
    # TODO: Must be authenticated to update user information.
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserSettingView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve or update the authenticated user's settings.
    """
    serializer_class = UserSettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserSetting.objects.get(user=self.request.user)
    

class UserSettingListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of settings or create new settings.
    """
    queryset = UserSetting.objects.all()
    serializer_class = UserSettingSerializer

class UserFollowersListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['follower__username', 'timestamp']
    ordering = ['-timestamp']  # Default ordering: recent followers

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Follow.objects.filter(followed__id=user_id)
    

class FollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        followed_user = CustomUser.objects.get(pk=self.kwargs['user_id'])
        serializer.save(follower=self.request.user, followed=followed_user)

class UnfollowUserView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Fetch only the relevant record
        return Follow.objects.get(follower=self.request.user, followed__pk=self.kwargs['user_id'])