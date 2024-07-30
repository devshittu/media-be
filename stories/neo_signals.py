import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Story
from .neo_models import StoryNode, Hashtag
from .utils import extract_hashtags

# Set up the logger for this module
logger = logging.getLogger('app_logger')


@receiver(post_save, sender=Story)
def create_or_update_story_node(sender, instance, created, **kwargs):
    if settings.SEEDING:
        logger.debug('Seeding mode enabled, skipping signal processing')
        return

    logger.debug(f'Processing post_save signal for Story id {instance.id}')
    hashtags = extract_hashtags(instance.body)

    if created:
        logger.info(f'Creating StoryNode for Story id {instance.id}')
        story_node = StoryNode(
            story_id=instance.id, event_occurred_at=instance.event_occurred_at
        )
        story_node.save()

        for hashtag in hashtags:
            tag_node, _ = Hashtag.get_or_create({"name": hashtag})
            if created:
                logger.debug(f'Created new Hashtag node for {hashtag}')
            story_node.hashtags.connect(tag_node)
            logger.debug(
                f'Connected Hashtag {hashtag} to StoryNode {instance.id}')
    else:
        logger.info(f'Updating StoryNode for Story id {instance.id}')
        story_node = StoryNode.nodes.get(story_id=instance.id)
        story_node.event_occurred_at = instance.event_occurred_at
        story_node.save()

        # TODO: Uncomment fast Update hashtags  as this works well before the
        # addition of loggers
        # current_hashtags = set(tag.name for tag in story_node.hashtags.all())
        # for hashtag in hashtags - current_hashtags:
        #     tag_node, _ = Hashtag.get_or_create({"name": hashtag})
        #     story_node.hashtags.connect(tag_node)
        # for hashtag in current_hashtags - hashtags:
        #     tag_node = Hashtag.nodes.get(name=hashtag)
        #     story_node.hashtags.disconnect(tag_node)

        # Update hashtags
        current_hashtags = set(tag.name for tag in story_node.hashtags.all())
        new_hashtags = set(hashtags)
        for hashtag in new_hashtags - current_hashtags:
            tag_node, created = Hashtag.get_or_create({"name": hashtag})
            if created:
                logger.debug(f'Created new Hashtag node for {hashtag}')
            story_node.hashtags.connect(tag_node)
            logger.debug(
                f'Connected new Hashtag {hashtag} to StoryNode {instance.id}')
        for hashtag in current_hashtags - new_hashtags:
            tag_node = Hashtag.nodes.get(name=hashtag)
            story_node.hashtags.disconnect(tag_node)
            logger.debug(
                f'Disconnected Hashtag {hashtag} from StoryNode {instance.id}')


@receiver(post_delete, sender=Story)
def delete_story_node(sender, instance, **kwargs):
    logger.info(f'Deleting StoryNode for Story id {instance.id}')
    story_node = StoryNode.nodes.get(story_id=instance.id)
    story_node.delete()
    logger.debug(f'Deleted StoryNode for Story id {instance.id}')


# stories/neo_signals.py
