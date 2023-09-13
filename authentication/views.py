from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import CustomUser
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def set_online_status(request):
#     """
#     API endpoint to set the user's status to online.
#     """
#     request.user.set_online()
#     return Response({"status": "User is now online."})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def set_offline_status(request):
#     """
#     API endpoint to set the user's status to offline.
#     """
#     request.user.set_offline()
#     return Response({"status": "User is now offline."})

class UserListView(generics.ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or created.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single user to be viewed, edited, or deleted.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer



class CompleteSetupView(generics.UpdateAPIView):
    """
    API endpoint to mark the user's setup as complete.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        user.has_completed_setup = True
        user.save()
        return Response({"status": "Account setup marked as complete."})