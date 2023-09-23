from django.core.management.base import BaseCommand
import json
from stories.neo_models import StoryNode, Storyline
import os
from datetime import datetime
from neomodel.exceptions import DoesNotExist


class Command(BaseCommand):
    help = "Import stories from stories_processed.json to StoryNode in Neo4j"

    def handle(self, *args, **kwargs):
        # Path to the stories_processed.json file
        file_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "data",
            "processed",
            "stories_processed.json",
        )

        # Load the JSON data
        with open(file_path, "r") as file:
            data = json.load(file)

        # First pass: Create all StoryNode instances and set up Storyline relationships
        for story_data in data:
            story = story_data["fields"]
            story_id = story_data["pk"]

            # Check if StoryNode with the same story_id already exists
            try:
                existing_node = StoryNode.nodes.get(story_id=story_id)
                continue  # Skip this iteration if node already exists
            except DoesNotExist:
                pass  # Node doesn't exist, so we'll create it

            # Convert ISO format to datetime
            event_date = datetime.fromisoformat(story['created_at'])
            story_node = StoryNode(story_id=story_id, event_occurred_at=event_date)
            story_node.save()

            # Determine Storyline association
            if not story["parent_story"]:
                # Create a new Storyline node
                description = story["body"][:200]
                summary = story["title"]
                subject = story["slug"]
                hashtags = "#".join(story["slug"].split("-"))
                
                storyline = Storyline(description=description, summary=summary, subject=subject, hashtags=hashtags)
                storyline.save()
                story_node.belongs_to_storyline.connect(storyline)
            else:
                # Associate with the parent's Storyline
                parent_node = StoryNode.nodes.get(story_id=story["parent_story"])
                parent_storyline = parent_node.belongs_to_storyline.all()[0]
                story_node.belongs_to_storyline.connect(parent_storyline)

        # Second pass: Set up previous_story relationships
        for story_data in data:
            story = story_data["fields"]
            story_id = story_data["pk"]

            story_node = StoryNode.nodes.get(story_id=story_id)

            # Handle previous_story relationships
            if story["parent_story"]:
                parent_node = StoryNode.nodes.get(story_id=story["parent_story"])
                story_node.previous_story.connect(parent_node)


        self.stdout.write(self.style.SUCCESS("Successfully imported stories to Neo4j"))

# stories/management/commands/importstories.py