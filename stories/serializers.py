from django.urls import reverse
from rest_framework import serializers
from .models import Story, Category, Like, Dislike, Bookmark
from .neo_models import StoryNode
from utils.serializers import UnixTimestampModelSerializer
from multimedia.serializers import MultimediaSerializer
from common.serializers import CustomUserSerializer


class CategorySerializer(UnixTimestampModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        # fields = '__all__'
        fields = ["id", "slug", "title", "description"]

    def validate_title(self, value):
        if Category.objects.filter(title=value).exists():
            raise serializers.ValidationError(
                "A category with this title already exists."
            )
        return value


class StorySerializer(UnixTimestampModelSerializer):
    """Serializer for the Story model."""

    has_liked = serializers.SerializerMethodField()
    has_disliked = serializers.SerializerMethodField()
    has_bookmarked = serializers.SerializerMethodField()
    user = CustomUserSerializer(read_only=True)
    multimedia = MultimediaSerializer(many=True, read_only=True)
    storylines_count = serializers.SerializerMethodField()
    storyline_id = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Story
        # fields = '__all__'
        fields = [
            "storylines_count",
            "storyline_id",
            "has_liked",
            "has_disliked",
            "has_bookmarked",
            "user",
            "multimedia",
            "likes_count",
            "dislikes_count",

        ] + [f.name for f in Story._meta.fields]
        # if there are fields from the model that we don't want to show in the view here it is 'slug', 'body', 'deleted_at'.
        # fields = ['storylines_count', 'multimedia'] + [f.name for f in Story._meta.fields if f.name not in ['slug', 'body', 'deleted_at']]

    def get_has_liked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Like.objects.filter(story=obj, user=user).exists()
        return None
    
    def get_has_disliked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Dislike.objects.filter(story=obj, user=user).exists()
        return None

    def get_has_bookmarked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Bookmark.objects.filter(story=obj, user=user).exists()
        return None

    def get_storylines_count(self, obj):
        try:
            # Get the StoryNode from Neo4j
            story_node = StoryNode.nodes.get(story_id=obj.id)

            # Get all Storyline nodes this story belongs to
            storylines = list(story_node.belongs_to_storyline.all())
            return len(storylines)
        except:
            return 0
    
    def get_storyline_id(self, obj):
        try:
            story_node = StoryNode.nodes.get(story_id=obj.id)
            storyline = story_node.belongs_to_storyline.all()[0]  # Assuming a story belongs to only one storyline
            return storyline.id
        except:
            return None


class LikeSerializer(UnixTimestampModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    story = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Like
        fields = ["user", "story", "created_at"]
    
    def validate(self, data):
        # Inject the user and story into the validated data
        request = self.context.get('request')
        data['user'] = request.user
        data['story'] = self.context['view'].get_story()
        return data



class DislikeSerializer(UnixTimestampModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    story = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Dislike
        fields = ["user", "story", "created_at"]
    
    def validate(self, data):
        # Inject the user and story into the validated data
        request = self.context.get('request')
        data['user'] = request.user
        data['story'] = self.context['view'].get_story()
        return data



class BookmarkSerializer(UnixTimestampModelSerializer):
    story = StorySerializer(read_only=True)
    story_id = serializers.PrimaryKeyRelatedField(queryset=Story.objects.all(), write_only=True)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = [
            "id",
            "title",
            "bookmark_category",
            "note",
            "user",
            "story",
            "story_id",
            "created_at",
        ]


# stories/serializers.py
