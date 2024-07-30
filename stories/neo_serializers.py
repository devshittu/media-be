import logging
from rest_framework import serializers
from .neo_models import Storyline

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class StorylineSerializer(serializers.Serializer):
    logger.debug('Initializing StorylineSerializer')
    id = serializers.CharField()
    description = serializers.CharField()
    summary = serializers.CharField()
    subject = serializers.CharField()
    hashtags = serializers.SerializerMethodField()
    stories_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Storyline
        fields = [
            "id",
            "description",
            "summary",
            "subject",
            "hashtags",
            "stories_count",
            "created_at",
            "updated_at",
        ]

    def get_hashtags(self, obj):
        logger.debug(f'Getting hashtags for storyline {obj.id}')
        # Assuming the get_hashtags method in the Storyline model returns a list of Hashtag objects
        try:
            hashtags = obj.get_hashtags()
            logger.info(f'Hashtags retrieved for storyline {obj.id}')
            return [hashtag.name for hashtag in hashtags]
        except Exception as e:
            logger.error(
                f'Error retrieving hashtags for storyline {obj.id}: {e}')
            return []


class HashtagSerializer(serializers.Serializer):
    logger.debug('Initializing HashtagSerializer')
    name = serializers.CharField()
    stories_count = serializers.IntegerField()


# stories/neo_serializers.py
