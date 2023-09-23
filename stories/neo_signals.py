# signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Story
from .neo_models import StoryNode

@receiver(post_save, sender=Story)
def create_or_update_story_node(sender, instance, created, **kwargs):
    if created:
        StoryNode(story_id=instance.id, event_occurred_at=instance.event_occurred_at).save()
    else:
        story_node = StoryNode.nodes.get(story_id=instance.id)
        story_node.event_occurred_at = instance.event_occurred_at
        story_node.save()

@receiver(post_delete, sender=Story)
def delete_story_node(sender, instance, **kwargs):
    story_node = StoryNode.nodes.get(story_id=instance.id)
    story_node.delete()
