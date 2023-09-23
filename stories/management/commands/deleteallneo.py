from django.core.management.base import BaseCommand
from stories.neo_models import StoryNode, Storyline

class Command(BaseCommand):
    help = 'Delete all StoryNode and Storyline instances from Neo4j'

    def handle(self, *args, **kwargs):
        # Query all StoryNode instances
        all_story_nodes = StoryNode.nodes.all()

        # Delete each StoryNode
        for node in all_story_nodes:
            node.delete()

        # Query all Storyline instances
        all_storylines = Storyline.nodes.all()

        # Delete each Storyline
        for storyline in all_storylines:
            storyline.delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all StoryNode and Storyline instances from Neo4j'))

# stories/management/commands/deleteallneo.py
