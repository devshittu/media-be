import logging
from django_neomodel import DjangoNode
from neomodel import (UniqueIdProperty, DateTimeProperty,
                      IntegerProperty, StringProperty,
                      RelationshipTo, RelationshipFrom)

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class StoryNode(DjangoNode):
    logger.debug('Initializing StoryNode model')
    node_id = UniqueIdProperty()
    story_id = IntegerProperty(unique_index=True)
    event_occurred_at = DateTimeProperty()
    belongs_to_storyline = RelationshipTo('Storyline', 'PART_OF')
    next_story = RelationshipTo('StoryNode', 'FOLLOWS')
    previous_story = RelationshipFrom('StoryNode', 'FOLLOWS')
    hashtags = RelationshipTo('Hashtag', 'HAS_HASHTAG')


class Storyline(DjangoNode):
    logger.debug('Initializing Storyline model')
    id = UniqueIdProperty()
    description = StringProperty()
    summary = StringProperty()
    subject = StringProperty()
    hashtags = StringProperty()
    stories = RelationshipFrom('StoryNode', 'PART_OF')

    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True, on_update=True)
    prefetched_hashtags = None  # Temporary attribute for caching

    @property
    def stories_count(self):
        count = len(self.stories.all())
        logger.debug(f'Calculating stories count: {count}')
        return count

    def get_hashtags(self):
        logger.debug(f'Retrieving hashtags for storyline {self.id}')
        # Get all stories associated with this storyline
        stories = self.stories.all()

        # Collect all unique hashtag names from these stories
        hashtag_names = set()
        for story in stories:
            for hashtag in story.hashtags.all():
                logger.debug(
                    f'Adding hashtag {hashtag.name} from story {story.story_id}')
                hashtag_names.add(hashtag.name)

        # Retrieve the actual Hashtag objects using their names
        hashtags = [Hashtag.nodes.get(name=hashtag_name)
                    for hashtag_name in hashtag_names]

        logger.info(
            f'Hashtags retrieved for storyline {self.id}: {hashtag_names}')
        return hashtags


class Hashtag(DjangoNode):
    logger.debug('Initializing Hashtag model')

    name = StringProperty(unique_index=True)
    stories = RelationshipFrom('StoryNode', 'HAS_HASHTAG')

    @property
    def stories_count(self):
        count = len(self.stories.all())
        logger.debug(
            f'Calculating stories count for hashtag {self.name}: {count}')
        return count

# stories/neo_models.py
