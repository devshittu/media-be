from django.shortcuts import get_object_or_404
from .models import Story


class StoryMixin:
    def get_story(self):
        story_id = self.kwargs.get('story_id')
        story_slug = self.kwargs.get('story_slug')

        if story_id:
            return get_object_or_404(Story, id=story_id)
        elif story_slug:
            return get_object_or_404(Story, slug=story_slug)

# stories/mixins.py
