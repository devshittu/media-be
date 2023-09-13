from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom user model.
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'name', 'profile_picture', 'date_of_birth', 'bio', 'phone_number', 'last_activity', 'has_completed_setup', 'roles')
