# neo_models.py

from django_neomodel import DjangoNode
from neomodel import (UniqueIdProperty, DateTimeProperty, 
                      IntegerProperty, StringProperty,  
                      RelationshipTo, RelationshipFrom)

class StoryNode(DjangoNode):
    node_id = UniqueIdProperty()
    story_id = IntegerProperty()
    event_occurred_at = DateTimeProperty()
    belongs_to_storyline = RelationshipTo('Storyline', 'PART_OF')
    next_story = RelationshipTo('StoryNode', 'FOLLOWS')
    previous_story = RelationshipFrom('StoryNode', 'FOLLOWS')

class Storyline(DjangoNode):
    id = UniqueIdProperty()
    description = StringProperty()
    summary = StringProperty()
    subject = StringProperty()
    hashtags = StringProperty()
    stories = RelationshipFrom('StoryNode', 'PART_OF')
