from rest_framework import serializers
from .models import Story, Category, Like, Dislike, Bookmark
from utils.serializers import UnixTimestampModelSerializer
from multimedia.serializers import MultimediaSerializer
from authentication.serializers import CustomUserSerializer

class CategorySerializer(UnixTimestampModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def validate_title(self, value):
        if Category.objects.filter(title=value).exists():
            raise serializers.ValidationError("A category with this title already exists.")
        return value


class StorySerializer(UnixTimestampModelSerializer):
    """Serializer for the Story model."""
    has_liked = serializers.SerializerMethodField()
    has_bookmarked = serializers.SerializerMethodField()
    user = CustomUserSerializer(read_only=True)
    multimedia = MultimediaSerializer(many=True, read_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    total_dislikes = serializers.IntegerField(read_only=True)


    class Meta:
        model = Story
        fields = '__all__'
        # fields = ['id', 'title', 'slug', 'body', 'has_liked', 'likes_count', 'dislikes_count', 'bookmarked', 'category', 'parents', 'children', 'source_link', 'event_occurred_at', 'event_reported_at', 'created_at', 'updated_at'  ]  # other fields

    def get_has_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Like.objects.filter(story=obj, user=user).exists()
        return None
    
    def get_has_bookmarked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Bookmark.objects.filter(story=obj, user=user).exists()
        return None



class LikeSerializer(UnixTimestampModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'story', 'created_at']

class DislikeSerializer(UnixTimestampModelSerializer):
    class Meta:
        model = Dislike
        fields = ['user', 'story', 'created_at']

class BookmarkSerializer(UnixTimestampModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'story', 'created_at']

# stories/serializers.py