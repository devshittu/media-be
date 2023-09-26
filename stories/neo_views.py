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
from neomodel.exceptions import DoesNotExist as HashtagDoesNotExist


class StorylineListView(generics.ListAPIView):
    serializer_class = StorylineSerializer

    def get_queryset(self):
        return Storyline.nodes.all()


class StorylineView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        storyline_id = self.kwargs["storyline_id"]

        try:
            storyline = Storyline.nodes.get(id=storyline_id)
        except Storyline.DoesNotExist:
            raise NotFound(detail="Storyline not found.")

        # Fetch related stories in order
        stories_in_order = list(storyline.stories.order_by("event_occurred_at"))
        story_ids = [story.story_id for story in stories_in_order]

        # Fetch actual story data from PostgreSQL with optimization
        stories = (
            Story.objects.filter(id__in=story_ids)
            .select_related("user")
            .prefetch_related("multimedia")
            .order_by("event_occurred_at")
        )

        # Apply pagination
        paginator = CustomPageNumberPagination()
        paginator.page_size = 10  # or any other number you prefer
        paginated_stories = paginator.paginate_queryset(stories, request)
        serialized_stories = StorySerializer(
            paginated_stories, many=True, context={"request": request}
        ).data

        # Construct the response
        response_data = {
            "id": storyline.id,
            "description": storyline.description,
            "summary": storyline.summary,
            "subject": storyline.subject,
            "hashtags": storyline.hashtags,
            "stories": serialized_stories,
        }

        return paginator.get_paginated_response(response_data)


class StorylinesForStoryView(generics.RetrieveAPIView):
    lookup_field = "slug"
    queryset = Story.objects.all()

    def retrieve(self, request, *args, **kwargs):
        story = self.get_object()
        story_id = story.id

        # Get the StoryNode from Neo4j
        story_node = StoryNode.nodes.get(story_id=story_id)

        # Get all Storyline nodes this story belongs to
        storylines = list(story_node.belongs_to_storyline.all())

        # Serialize and return the storylines
        serializer = StorylineSerializer(storylines, many=True)
        return Response(serializer.data)


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
            except HashtagDoesNotExist:
                # Return an empty queryset if the hashtag doesn't exist
                return Story.objects.none()
        else:
            # If no hashtag is specified, return all stories (or you can modify this behavior)
            return Story.objects.all()


# stories/neo_views.py
