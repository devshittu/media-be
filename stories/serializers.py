from .models import UserSearchHistory
import logging
from rest_framework import serializers
from .models import Story, Category, Like, Dislike, Bookmark
from .neo_models import StoryNode
from utils.serializers import UnixTimestampModelSerializer
from multimedia.serializers import MultimediaSerializer
from common.serializers import CustomUserSerializer
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import StoryDocument

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class CategorySerializer(UnixTimestampModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        # fields = '__all__'
        fields = ["id", "slug", "title", "description"]

    def validate_title(self, value):
        logger.debug(f'Validating title for category: {value}')
        if Category.objects.filter(title=value).exists():
            logger.warning(f'Category with title {value} already exists')
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
            logger.debug(f'Checking if user {user.id} liked story {obj.id}')
            return Like.objects.filter(story=obj, user=user).exists()
        return None

    def get_has_disliked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            logger.debug(f'Checking if user {user.id} disliked story {obj.id}')
            return Dislike.objects.filter(story=obj, user=user).exists()
        return None

    def get_has_bookmarked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            logger.debug(
                f'Checking if user {user.id} bookmarked story {obj.id}')
            return Bookmark.objects.filter(story=obj, user=user).exists()
        return None

    def get_storylines_count(self, obj):
        try:
            logger.debug(f'Getting storylines count for story {obj.id}')
            # Get the StoryNode from Neo4j
            story_node = StoryNode.nodes.get(story_id=obj.id)

            # Get all Storyline nodes this story belongs to
            storylines = list(story_node.belongs_to_storyline.all())
            return len(storylines)
        except Exception as e:
            logger.error(
                f'Error getting storylines count for story {obj.id}: {e}')
            return 0

    def get_storyline_id(self, obj):
        try:
            logger.debug(f'Getting storyline ID for story {obj.id}')
            story_node = StoryNode.nodes.get(story_id=obj.id)
            storyline = story_node.belongs_to_storyline.all()[
                0
            ]  # Assuming a story belongs to only one storyline
            return storyline.id
        except Exception as e:
            logger.error(f'Error getting storyline ID for story {obj.id}: {e}')
            return None


class StoryDocumentSerializer(DocumentSerializer):
    class Meta:
        document = StoryDocument
        fields = (
            'id',
            'title',
            'slug',
            'body',
            'user',
            'category',
            'parent_story',
            'source_link',
            'event_occurred_at',
            'event_reported_at',
        )


class AutocompleteSerializer(serializers.Serializer):
    # Customize based on the fields returned from Elasticsearch
    title = serializers.CharField()


# Set up the logger for this module
logger = logging.getLogger('app_logger')


class UserSearchHistorySerializer(serializers.ModelSerializer):
    searched_at = serializers.SerializerMethodField()

    class Meta:
        model = UserSearchHistory
        fields = ['query', 'searched_at']

    def get_searched_at(self, obj):
        # Return the Unix timestamp without microseconds
        return int(obj.searched_at.timestamp())
    
    def to_representation(self, instance):
        """
        Override to_representation to add logging when serializing the data.
        """
        logger.debug(
            f"Serializing UserSearchHistory for query: {instance.query}")
        return super().to_representation(instance)

    def create(self, validated_data):
        """
        Override the create method to log when a new search history record is created.
        """
        logger.info(
            f"Creating new UserSearchHistory entry for query: {validated_data.get('query')}")
        return super().create(validated_data)


class LikeSerializer(UnixTimestampModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    story = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ["user", "story", "created_at"]

    def validate(self, data):
        # Inject the user and story into the validated data
        request = self.context.get("request")
        data["user"] = request.user
        data["story"] = self.context["view"].get_story()
        return data


class DislikeSerializer(UnixTimestampModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    story = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Dislike
        fields = ["user", "story", "created_at"]

    def validate(self, data):
        # Inject the user and story into the validated data
        request = self.context.get("request")
        data["user"] = request.user
        data["story"] = self.context["view"].get_story()
        return data


class BookmarkSerializer(UnixTimestampModelSerializer):
    story = StorySerializer(read_only=True)
    story_id = serializers.PrimaryKeyRelatedField(
        queryset=Story.objects.all(), write_only=True
    )
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


class TrendingStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = [
            "id",
            "title",
            "body",
            "trending_score",
            "likes_count",
            "dislikes_count",
        ]


# stories/serializers.py
