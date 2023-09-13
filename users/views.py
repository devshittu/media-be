from rest_framework import generics, filters
from .models import UserSetting, Follow
from .serializers import UserSerializer, UserSettingSerializer, FollowSerializer   
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.models import CustomUser

class CurrentUserView(APIView):
    """
    View to retrieve the authenticated user's profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return the authenticated user's profile.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of users or create a new user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

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