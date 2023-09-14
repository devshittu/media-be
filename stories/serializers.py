from rest_framework import serializers
from .models import Story, Category, Like, Dislike, Bookmark
from multimedia.serializers import MultimediaSerializer



class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    class Meta:
        model = Category
        fields = '__all__'

class StorySerializer(serializers.ModelSerializer):
    """Serializer for the Story model."""
    media = MultimediaSerializer(many=True, read_only=True)
    lineage = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    bookmarked = serializers.SerializerMethodField()


    class Meta:
        model = Story
        # fields = '__all__'
        fields = ['id', 'title', 'slug', 'body', 'has_liked', 'likes_count', 'dislikes_count', 'bookmarked', 'category', 'parents', 'children', 'source_link', 'event_occurred_at', 'event_reported_at', 'created_at', 'updated_at'  ]  # other fields

    def get_has_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Like.objects.filter(story=obj, user=user).exists()
        return None
    
    def get_bookmarked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Bookmark.objects.filter(story=obj, user=user).exists()
        return None


# class UserInterestSerializer(serializers.ModelSerializer):
#     """Serializer for the UserInterest model."""
#     class Meta:
#         model = UserInterest
#         fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'story', 'created_at']

class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['user', 'story', 'created_at']

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'story', 'created_at']

# stories/serializers.py