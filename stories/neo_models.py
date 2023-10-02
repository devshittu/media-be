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
    def stories_count(self):
        return len(self.stories.all())
    

    def get_hashtags(self):
        # Get all stories associated with this storyline
        stories = self.stories.all()
        
        # Collect all unique hashtag names from these stories
        hashtag_names = set()
        for story in stories:
            for hashtag in story.hashtags.all():
                hashtag_names.add(hashtag.name)
        
        # Retrieve the actual Hashtag objects using their names
        hashtags = [Hashtag.nodes.get(name=hashtag_name) for hashtag_name in hashtag_names]
        
        return hashtags
    
class Hashtag(DjangoNode):
    name = StringProperty(unique_index=True)
    stories = RelationshipFrom('StoryNode', 'HAS_HASHTAG')

    @property
    def stories_count(self):
        return len(self.stories.all())

# stories/neo_models.py