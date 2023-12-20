from rest_framework import serializers
from .models import Multimedia


class MultimediaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Multimedia model.
    """

    # user = serializers.ReadOnlyField(source="user.email")  # Display the user's email
    # user = serializers. (source="user.email", write_only=True)  # Display the user's email

    class Meta:
        model = Multimedia
        fields = [
            "file",
            "media_url",
            "caption",
            "thumbnail",
            "media_type",
            "id",
            "user",
            "story",
        ]


# multimedia/serializers.py
