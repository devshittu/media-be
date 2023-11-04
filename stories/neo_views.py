# views.py

from rest_framework import generics
from .models import Story
from .serializers import StorySerializer
from .neo_serializers import StorylineSerializer, HashtagSerializer
from .neo_models import Storyline, Hashtag
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .neo_models import StoryNode
from utils.pagination import CustomPageNumberPagination
from neomodel.exceptions import DoesNotExist


class StorylineListView(generics.ListAPIView):
    serializer_class = StorylineSerializer

    def get_queryset(self):
        storylines = Storyline.nodes.all()

        # Prefetch related Hashtag objects from Neo4j for all storylines
        for storyline in storylines:
            storyline.prefetched_hashtags = storyline.get_hashtags()
        
        # Sort by updated_at and then by the number of hashtags
        sorted_storylines = sorted(
            storylines,
            key=lambda x: (x.updated_at, len(x.prefetched_hashtags)), 
            reverse=True
        )

        return sorted_storylines


class StorylineDetailView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        storyline_id = self.kwargs["storyline_id"]

        try:
            storyline = Storyline.nodes.get(id=storyline_id)
        except Storyline.DoesNotExist:
            raise NotFound(detail="Storyline not found.")

        # Construct the response
        response_data = {
            "id": storyline.id,
            "description": storyline.description,
            "summary": storyline.summary,
            "subject": storyline.subject,
            "hashtags": storyline.hashtags,
        }

        return Response(response_data)


class StorylineStoriesView(generics.ListAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = StorySerializer

    def get_queryset(self):
        storyline_id = self.kwargs["storyline_id"]

        # Fetch related stories in order
        stories_in_order = list(
            Storyline.nodes.get(id=storyline_id).stories.order_by("event_occurred_at")
        )
        story_ids = [story.story_id for story in stories_in_order]

        # Fetch actual story data from PostgreSQL with optimization
        return (
            Story.objects.filter(id__in=story_ids)
            .select_related("user")
            .prefetch_related("multimedia")
            .order_by("event_occurred_at")
        )



class StorylinesForStoryView(generics.ListAPIView):
    serializer_class = StorylineSerializer
    pagination_class = CustomPageNumberPagination
    lookup_url_kwarg = "slug"
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        story = Story.objects.get(slug=slug)
        story_node = StoryNode.nodes.get(story_id=story.id)
        storylines = list(story_node.belongs_to_storyline.all())
        return storylines

# TODO: Implement like StorylinesForStoryView with metadata.
class TrendingHashtagsListView(generics.ListAPIView):
    serializer_class = HashtagSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        # Retrieve all hashtags and annotate them with their stories count
        hashtags = Hashtag.nodes.all()
        annotated_hashtags = [
            {"name": hashtag.name, "stories_count": len(hashtag.stories.all())}
            for hashtag in hashtags
        ]
        # Sort the hashtags by stories count in descending order
        return sorted(
            annotated_hashtags, key=lambda x: x["stories_count"], reverse=True
        )


class SpecificStorylineHashtagsView(generics.ListAPIView):
    serializer_class = HashtagSerializer

    def get_queryset(self):
        storyline_id = self.kwargs["storyline_id"]

        # Get the storyline
        storyline = Storyline.nodes.get(id=storyline_id)

        # Get all hashtags associated with this storyline
        hashtags = storyline.get_hashtags()

        return hashtags


# TODO: Implement like StorylinesForStoryView with metadata.
class StoriesByHashtagsView(generics.ListAPIView):
    serializer_class = StorySerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        # hashtag_name = self.request.query_params.get("hashtag", None)
        hashtag_name = self.kwargs.get("hashtag_name")
        if hashtag_name:
            try:
                hashtag = Hashtag.nodes.get(name=hashtag_name)
                story_ids = [story.story_id for story in hashtag.stories.all()]
                return Story.objects.filter(id__in=story_ids)
            except DoesNotExist:
                # Return an empty queryset if the hashtag doesn't exist
                return Story.objects.none()
        else:
            # If no hashtag is specified, return all stories (or you can modify this behavior)
            return Story.objects.all()


# stories/neo_views.py
