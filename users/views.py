from rest_framework import generics
from .models import User, Settings, Category
from .serializers import UserSerializer, SettingsSerializer, CategorySerializer
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

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
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SettingsListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of settings or create new settings.
    """
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of categories or create a new category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
