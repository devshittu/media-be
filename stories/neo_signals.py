# signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Story
from .neo_models import StoryNode, Hashtag
from .utils import extract_hashtags


@receiver(post_save, sender=Story)
def create_or_update_story_node(sender, instance, created, **kwargs):
    hashtags = extract_hashtags(instance.body)

    if created:
        story_node = StoryNode(
            story_id=instance.id, event_occurred_at=instance.event_occurred_at
        )
        story_node.save()

        for hashtag in hashtags:
            tag_node, _ = Hashtag.get_or_create({"name": hashtag})
            story_node.hashtags.connect(tag_node)
    else:
        story_node = StoryNode.nodes.get(story_id=instance.id)
        story_node.event_occurred_at = instance.event_occurred_at
        story_node.save()

        # Update hashtags
        current_hashtags = set(tag.name for tag in story_node.hashtags.all())
        for hashtag in hashtags - current_hashtags:
            tag_node, _ = Hashtag.get_or_create({"name": hashtag})
            story_node.hashtags.connect(tag_node)
        for hashtag in current_hashtags - hashtags:
            tag_node = Hashtag.nodes.get(name=hashtag)
            story_node.hashtags.disconnect(tag_node)


@receiver(post_delete, sender=Story)
def delete_story_node(sender, instance, **kwargs):
    story_node = StoryNode.nodes.get(story_id=instance.id)
    story_node.delete()


# stories/neo_signals.py
