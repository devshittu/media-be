import logging
from django.shortcuts import get_object_or_404
from .models import Story

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class StoryMixin:
    def get_story(self):
        story_id = self.kwargs.get('story_id')
        story_slug = self.kwargs.get('story_slug')

        logger.debug(
            f'Attempting to retrieve story with ID {story_id} or slug {story_slug}')

        if story_id:
            logger.debug(f'Retrieving story by ID: {story_id}')
            story = get_object_or_404(Story, id=story_id)
            logger.info(f'Successfully retrieved story with ID: {story_id}')
            return story
        elif story_slug:
            logger.debug(f'Retrieving story by slug: {story_slug}')
            story = get_object_or_404(Story, slug=story_slug)
            logger.info(
                f'Successfully retrieved story with slug: {story_slug}')
            return story
        else:
            logger.warning('No story ID or slug provided in request')
            return None

# stories/mixins.py
