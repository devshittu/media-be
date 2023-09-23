# views.py

from rest_framework import generics
from .models import Story
from .serializers import StorySerializer
from .neo_models import Storyline
from neomodel import db
from rest_framework.response import Response


class StorylineView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        storyline_id = self.kwargs['storyline_id']
        storyline = Storyline.nodes.get(id=storyline_id)
        
        # Fetch related stories in order
        stories_in_order = list(storyline.stories.order_by('event_occurred_at'))
        story_ids = [story.story_id for story in stories_in_order]
        
        # Fetch actual story data from PostgreSQL
        stories = Story.objects.filter(id__in=story_ids).order_by('event_occurred_at')
        serialized_stories = StorySerializer(stories, many=True).data
        
        # Construct the response
        response_data = {
            'id': storyline.id,
            'description': storyline.description,
            'summary': storyline.summary,
            'subject': storyline.subject,
            'hashtags': storyline.hashtags,
            'stories': serialized_stories,
            # Add pagination links, count, total_pages, and current_page as needed
        }
        
        return Response(response_data)
