from rest_framework import serializers
from .models import Multimedia

class MultimediaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Multimedia model.
    """
    user = serializers.ReadOnlyField(source='user.email')  # Display the user's email

    class Meta:
        model = Multimedia
        fields = '__all__'

# multimedia/serializers.py