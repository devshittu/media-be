from rest_framework import serializers
from .models import Story, Media, Category, UserInterest

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    class Meta:
        model = Category
        fields = '__all__'

class MediaSerializer(serializers.ModelSerializer):
    """Serializer for the Media model."""
    class Meta:
        model = Media
        fields = '__all__'

class StorySerializer(serializers.ModelSerializer):
    """Serializer for the Story model."""
    media = MediaSerializer(many=True, read_only=True)
    lineage = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = '__all__'

class UserInterestSerializer(serializers.ModelSerializer):
    """Serializer for the UserInterest model."""
    class Meta:
        model = UserInterest
        fields = '__all__'

# stories/serializers.py