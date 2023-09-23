from rest_framework import serializers
from .neo_models import Storyline

class StorylineSerializer(serializers.Serializer):
    id = serializers.CharField()
    description = serializers.CharField()
    summary = serializers.CharField()
    subject = serializers.CharField()
    hashtags = serializers.CharField()
    total_stories = serializers.IntegerField(read_only=True)

    class Meta:
        model = Storyline
        fields = ['id', 'description', 'summary', 'subject', 'hashtags', 'total_stories']

# stories/neo_serializers.py