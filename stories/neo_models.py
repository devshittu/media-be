# neo_models.py

from django_neomodel import DjangoNode
from neomodel import (UniqueIdProperty, DateTimeProperty, 
                      IntegerProperty, StringProperty,  
                      RelationshipTo, RelationshipFrom)

class StoryNode(DjangoNode):
    node_id = UniqueIdProperty()
    story_id = IntegerProperty(unique_index=True)
    event_occurred_at = DateTimeProperty()
    belongs_to_storyline = RelationshipTo('Storyline', 'PART_OF')
    next_story = RelationshipTo('StoryNode', 'FOLLOWS')
    previous_story = RelationshipFrom('StoryNode', 'FOLLOWS')
    hashtags = RelationshipTo('Hashtag', 'HAS_HASHTAG')

class Storyline(DjangoNode):
    id = UniqueIdProperty()
    description = StringProperty()
    summary = StringProperty()
    subject = StringProperty()
    hashtags = StringProperty()
    stories = RelationshipFrom('StoryNode', 'PART_OF')

    @property
    def total_stories(self):
        return len(self.stories.all())
    
class Hashtag(DjangoNode):
    name = StringProperty(unique_index=True)
    stories = RelationshipFrom('StoryNode', 'HAS_HASHTAG')

# stories/neo_models.py