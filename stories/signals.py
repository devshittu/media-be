from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Story
from .tasks import (index_story_to_elasticsearch,
                    remove_story_from_elasticsearch)
import logging

logger = logging.getLogger('app_logger')


@receiver(post_save, sender=Story)
def handle_story_saved(sender, instance, **kwargs):
    """
    Signal that triggers when a Story is created or updated.
    It sends a task to index the Story into Elasticsearch.
    """
    logger.debug(
        f'Story {instance.id} saved. Sending task to index it into Elasticsearch.')
    index_story_to_elasticsearch.delay(instance.id)


@receiver(post_delete, sender=Story)
def handle_story_deleted(sender, instance, **kwargs):
    """
    Signal that triggers when a Story is deleted.
    It sends a task to remove the Story from Elasticsearch.
    """
    logger.debug(
        f'Story {instance.id} deleted. Sending task to remove it from Elasticsearch.')
    remove_story_from_elasticsearch.delay(instance.id)

# stories/signals.py
