from django.contrib.auth import get_user_model
from .models import CustomUser
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer, CustomUserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

class UserListView(generics.ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or created.
    """
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single user to be viewed, edited, or deleted.
    """
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer



class CompleteSetupView(generics.UpdateAPIView):
    """
    API endpoint to mark the user's setup as complete.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        user.has_completed_setup = True
        user.save()
        return Response({"status": "Account setup marked as complete."})

class MeView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve or update the authenticated user's information.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
# authentication/views.py