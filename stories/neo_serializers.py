from rest_framework import serializers
from .neo_models import Storyline


class StorylineSerializer(serializers.Serializer):
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
        # Assuming the get_hashtags method in the Storyline model returns a list of Hashtag objects
        hashtags = obj.get_hashtags()
        return [hashtag.name for hashtag in hashtags]


class HashtagSerializer(serializers.Serializer):
    name = serializers.CharField()
    stories_count = serializers.IntegerField()


# stories/neo_serializers.py
