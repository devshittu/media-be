from difflib import get_close_matches
import re
import time
from datetime import datetime
import logging
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, status, serializers
from django.db import IntegrityError
from users.models import UserSetting
from stories.neo_models import StoryNode
from .models import Story, Like, Dislike, Bookmark, Category, UserSearchHistory
from django_redis import get_redis_connection
from rest_framework.response import Response
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
    CompoundSearchFilterBackend,
)

from elasticsearch_dsl import Q as ElasticsearchQ
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from .documents import StoryDocument
from .serializers import StoryDocumentSerializer, UserSearchHistorySerializer
from .utils import (cache_search_query,
                    store_user_search_history)

from utils.permissions import CustomIsAuthenticated
from utils.mixins import SoftDeleteMixin
from .serializers import (
    LikeSerializer,
    DislikeSerializer,
    CategorySerializer,
    TrendingStorySerializer, StorySerializer, BookmarkSerializer,
    AutocompleteSerializer
)
# from .documents import AutocompleteDocument
from utils.pagination import CustomPageNumberPagination
from utils.permissions import IsOwner
from .mixins import StoryMixin
from django.db.models import F, Count, Q as DjangoQ

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]
    ordering = ["-created_at"]

    def list(self, request, *args, **kwargs):
        logger.debug('Listing all categories')
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.debug('Creating a new category')
        return super().create(request, *args, **kwargs)


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving category with slug {kwargs['slug']}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating category with slug {kwargs['slug']}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting category with slug {kwargs['slug']}")
        return super().destroy(request, *args, **kwargs)


class StoriesByCategoryView(generics.ListAPIView):
    queryset = Story.active_unflagged_objects.all()
    serializer_class = StorySerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        logger.debug(f'Fetching stories for category slug: {category_slug}')
        return self.queryset.filter(category__slug=category_slug)


class StoryListCreateView(generics.ListCreateAPIView):
    """View to list all stories or create a new story."""

    # permission_classes = [CustomIsAuthenticated]
    serializer_class = StorySerializer

    def get_queryset(self):
        logger.debug('Fetching all stories with annotations and prefetches')
        stories = (
            Story.objects.all()
            .annotate(
                total_likes=Count("likes_set"), total_dislikes=Count("dislikes_set")
            )
            .prefetch_related("multimedia")
            .order_by("-created_at")
        )

        logger.debug('Prefetching related StoryNode objects from Neo4j')
        # Prefetch related StoryNode objects from Neo4j
        story_ids = [story.id for story in stories]
        story_nodes = StoryNode.nodes.filter(story_id__in=story_ids)
        # Create a dictionary to map story IDs to their corresponding StoryNode objects
        story_node_map = {node.story_id: node for node in story_nodes}
        for story in stories:
            story.story_node = story_node_map.get(story.id)

        return stories

    def create(self, request, *args, **kwargs):
        logger.debug('Creating a new story')
        return super().create(request, *args, **kwargs)


class StoryRetrieveUpdateDestroyView(
    SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView
):
    """View to retrieve, update, or delete a story."""

    queryset = Story.objects.all()
    serializer_class = StorySerializer
    lookup_field = "slug"  # Use the slug for lookup
    lookup_url_kwarg = "story_slug"

    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving story with slug {kwargs['story_slug']}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating story with slug {kwargs['story_slug']}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting story with slug {kwargs['story_slug']}")
        return super().destroy(request, *args, **kwargs)


class AutocompleteView(DocumentViewSet):
    document = StoryDocument
    serializer_class = AutocompleteSerializer
    lookup_field = 'id'
    pagination_class = CustomPageNumberPagination  # Your custom pagination class
    filter_backends = [
        SearchFilterBackend,
        CompoundSearchFilterBackend,
    ]

    search_fields = ('title.suggest', 'title.ngram',
                     'body.ngram', 'category.title')

    def get_queryset(self):
        return self.document.search().source(False)

    def list(self, request, *args, **kwargs):
        start_time = time.time()  # Start time for calculating processing time
        query = request.query_params.get('q', '').lower()
        logger.debug(f"Received autocomplete request with query: {query}")
        redis_conn = get_redis_connection("default")

        # Get pagination params (page and page_size) from the request
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(self.paginator.get_page_size(request))
        except ValueError:
            logger.error("Invalid page or page_size value.")
            return Response({"detail": "Invalid page or page_size value."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the Elasticsearch `from` (offset) and `size` (limit)
        es_from = (page - 1) * page_size
        es_size = page_size

        try:
            # If cached suggestions exist in Redis, return them
            cached_suggestions = redis_conn.zrangebylex(
                "autocomplete_titles", f"[{query}", f"[{query}\xff", 0, 5
            )
            if cached_suggestions:
                logger.info(
                    f"Returning cached suggestions from Redis for query: {query}")
                paginated_suggestions = self.paginate_queryset(
                    cached_suggestions)
                return self.get_paginated_response(paginated_suggestions)

            # Elasticsearch fallback
            logger.info(
                f"No Redis cache found for query: {query}. Querying Elasticsearch.")

            search = self.document.search().query(
                ElasticsearchQ("multi_match", query=query, fields=[
                    'title.ngram^3', 'body.ngram', 'category.title'
                ], fuzziness="AUTO", operator="or", type="most_fields")
            ).extra(from_=es_from, size=es_size)

            response = search.execute()

            # Get the total results count from Elasticsearch
            total_hits = response.hits.total.value  # This is the total number of hits
            logger.debug(f"Total hits from Elasticsearch: {total_hits}")

            # Handle Invalid Page: If requested page exceeds total available results, return error
            if es_from >= total_hits:
                logger.error(
                    f"Invalid page request: page={page}, es_from={es_from}, total_hits={total_hits}")
                return Response({"detail": "Invalid page."}, status=status.HTTP_404_NOT_FOUND)

            # Process each hit individually, adding probable_next_words and story_keywords to each result
            results = []
            for hit in response.hits:
                story_dict = hit.to_dict()  # Convert each hit to a dict
                # Extract probable next words and keywords per story
                probable_next_words = self.extract_ngram_suggestions(
                    hit.title, hit.body, query)
                story_keywords = self.extract_story_keywords(
                    [hit])  # Only extract from this hit

                # Append probable next words and story keywords to the story data
                story_dict['probable_next_words'] = probable_next_words
                story_dict['story_keywords'] = story_keywords
                results.append(story_dict)

            # Paginate results using your custom pagination
            paginated_suggestions = self.paginator.paginate_queryset(
                results, request, view=self)

            # Manually set the paginator's count to the total hits from Elasticsearch
            self.paginator.page.paginator._count = total_hits
            self.paginator.page.paginator.num_pages = (
                total_hits + page_size - 1) // page_size  # Total number of pages

            logger.debug(f"Pagination count set to: {total_hits}")
            logger.debug(
                f"Total pages: {self.paginator.page.paginator.num_pages}")

            # Calculate processing time dynamically
            processing_time = round(
                (time.time() - start_time) * 1000)  # in milliseconds

            # Prepare metadata
            query_metadata = {
                "searched_term": query,
                "correction": query,  # No correction logic applied in this example
                "correction_details": {
                    "fuzziness_level": 2,  # Can be adjusted based on your setup
                    "suggested_by": "Elasticsearch"
                }
            }

            metadata = {
                "query_info": query_metadata,
                "stats": {
                    # Dynamically calculated
                    "processing_time": f"{processing_time}ms",
                    "suggestions_count": total_hits  # Total hits from Elasticsearch
                }
            }

            # Paginated response with metadata
            paginated_response = self.paginator.get_paginated_response(
                paginated_suggestions)
            paginated_response.data['metadata'] = metadata

            logger.debug(
                f"Returning paginated response with metadata: {paginated_response.data}")
            return paginated_response

        except Exception as e:
            logger.error(
                f"Error occurred during autocomplete search for query '{query}': {e}")
            return Response({
                "detail": "An error occurred while processing the autocomplete request."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def extract_ngram_suggestions(self, title, body, corrected_query_word):
        logger.debug(
            f"Extracting ngram suggestions for corrected query word: {corrected_query_word}")
        stopwords = {"and", "or", "it", "the", "is", "of",
                     "to", "for", "a", "in", "on", "at", "by", "an"}

        query_words = corrected_query_word.lower().split()

        # Function to generate ngrams
        def generate_ngrams(text, n):
            words = [word for word in re.findall(
                r'\w+', text.lower()) if word not in stopwords]
            ngrams = [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]
            logger.debug(f"Generated {n}-grams for text: {text} -> {ngrams}")
            return ngrams

        probable_keywords = []

        # Generate bigrams and trigrams for both title and body
        bigrams_title = generate_ngrams(title, 2)
        trigrams_title = generate_ngrams(title, 3)
        bigrams_body = generate_ngrams(body, 2)
        trigrams_body = generate_ngrams(body, 3)

        # Combine all ngrams
        all_ngrams = bigrams_title + trigrams_title + bigrams_body + trigrams_body

        logger.debug(f"All ngrams (bigrams & trigrams): {all_ngrams}")

        # Fuzzy Matching Logic: Use fuzzy matching to allow for typos
        for ngram in all_ngrams:
            for word in query_words:
                close_matches = get_close_matches(word, ngram, n=1, cutoff=0.7)
                if close_matches:
                    idx = ngram.index(close_matches[0])
                    # Suggest the next words in the ngram (return the rest of the ngram after the match)
                    if idx + 1 < len(ngram):
                        suggestion = f'{close_matches[0]} ' + \
                            ' '.join(ngram[idx + 1:])
                        if suggestion and suggestion not in probable_keywords:
                            probable_keywords.append(suggestion)

        logger.debug(
            f"Final probable keywords before deduplication: {probable_keywords}")
        probable_keywords = list(dict.fromkeys(
            probable_keywords))  # Remove duplicates
        logger.debug(
            f"Final probable keywords after deduplication: {probable_keywords}")

        return probable_keywords[:10]  # Limit to 10 probable keywords

    def extract_story_keywords(self, hits):
        logger.debug(f"Extracting story keywords from {len(hits)} hits")
        stopwords = {"and", "or", "it", "the", "is", "of",
                     "to", "for", "a", "in", "on", "at", "by", "an"}

        all_keywords = []

        for hit in hits:
            # Extract keywords from title and body
            words_in_title = re.findall(r'\w+', hit.title.lower())
            words_in_body = re.findall(r'\w+', hit.body.lower())

            # Remove stopwords and add to the list
            keywords = [word for word in (
                words_in_title + words_in_body) if word not in stopwords]
            all_keywords.extend(keywords)

        # Remove duplicates
        unique_keywords = list(dict.fromkeys(all_keywords))
        logger.debug(f"Unique keywords extracted: {unique_keywords}")

        return unique_keywords[:20]  # Limit to top 20 keywords


class StorySearchView(DocumentViewSet):
    document = StoryDocument
    # serializer_class = StoryDocumentSerializer
    serializer_class = StorySerializer
    lookup_field = 'id'
    pagination_class = CustomPageNumberPagination
    filter_backends = [
        SearchFilterBackend,
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]

    # Define search fields

    search_fields = (
        'title.ngram',
        'body.ngram',
        'user.username',
        'category.title',
        'parent_story.title',
    )
    # Define filtering fields
    filter_fields = {
        'category.id': None,
        'user.id': None,
        'event_occurred_at': {
            'field': 'event_occurred_at',
            'lookup': 'gte',
        },
        'event_reported_at': {
            'field': 'event_reported_at',
            'lookup': 'lte',
        },
    }

    # Define ordering fields
    ordering_fields = {
        'event_occurred_at': None,
        'event_reported_at': None,
        'created_at': None,
    }

    # Default ordering
    ordering = ('_score', '-created_at')

    def list(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')
        user = request.user

        if not query:
            logger.warning("Query parameter `q` is missing in the request.")
            return Response({"detail": "Query parameter `q` is required."}, status=400)

        logger.info(f"Received search request with query: {query}")

        try:
            # Use ngram-based matching for more flexibility
            search = self.document.search().query(
                ElasticsearchQ("multi_match", query=query, fields=[
                    'title.ngram^3', 'body.ngram', 'user.username', 'category.title'],
                    fuzziness="AUTO",
                    type="best_fields",
                    operator="or",
                )
            )

            # TODO: do not match phrase until we are ready to implement advanced search
            #  Optionally apply match_phrase for longer queries with a higher slop value
            # Apply match_phrase only for queries with more than 2 words
            if len(query.split()) > 2:
                search = search.query(
                    ElasticsearchQ(
                        "match_phrase",
                        body={
                            "query": query,
                            "slop": 10}
                    ),
                )
            # Fetch the results
            response = search.execute()

            # Calculate the number of search results
            result_count = response.hits.total.value

            # Cache the search query with the result count
            cache_search_query(query, result_count)
            # store_user_search_history(user, query)
            # Store the user search history if there are hits
            store_user_search_history(user, query, result_count)

            # Apply pagination
            page = self.paginate_queryset(response.hits)
            if page is not None:
                # Convert Elasticsearch documents into Django model instances
                story_ids = [hit.meta.id for hit in page]
                stories = Story.objects.filter(id__in=story_ids)

                # Serialize using the native StorySerializer
                serializer = self.get_serializer(stories, many=True)
                logger.info(
                    f"Returning paginated search results for query: {query}")
                return self.get_paginated_response(serializer.data)

            # Convert Elasticsearch documents into Django model instances
            story_ids = [hit.meta.id for hit in response.hits]
            stories = Story.objects.filter(id__in=story_ids)

            # Serialize using the native StorySerializer
            serializer = self.get_serializer(stories, many=True)
            logger.info(f"Returning search results for query: {query}")
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error occurred during search: {e}")
            return Response({"detail": "An error occurred during search."}, status=500)


class CachedSearchQueriesView(generics.ListAPIView):
    """
    View to return the most frequently used search queries from Redis, with metadata.
    """
    pagination_class = CustomPageNumberPagination  # Use your custom pagination class

    def list(self, request, *args, **kwargs):
        try:
            logger.debug("Attempting to retrieve search queries from Redis.")
            redis_conn = get_redis_connection("default")

            # Retrieve all queries ordered by their score (timestamp), sorted descending
            top_queries_with_scores = redis_conn.zrevrange(
                "search_queries", 0, -1, withscores=True
            )

            if not top_queries_with_scores:
                logger.info("No search queries found in Redis.")
                return Response({"detail": "No search queries found."}, status=204)

            # Collect metadata for each query
            top_queries = []
            logger.debug(
                f"Found {len(top_queries_with_scores)} queries in Redis, processing each.")
            for query, timestamp in top_queries_with_scores:
                query = query.decode('utf-8')
                query_data = redis_conn.hgetall(f"search_query:{query}")

                if not query_data:
                    logger.warning(
                        f"No metadata found for query '{query}'. Skipping.")
                    continue

                # Decode the Redis hash fields
                search_term = query_data.get(b'query').decode('utf-8')
                hits = int(query_data.get(b'hits').decode('utf-8'))
                searched_at = int(query_data.get(b'searched_at').decode(
                    'utf-8'))  # Use Unix timestamp

                # Add the query data to the list
                top_queries.append({
                    'query': search_term,
                    'hits': hits,
                    'searched_at': searched_at,  # Keep it as Unix timestamp
                })

            logger.info(
                f"Successfully retrieved {len(top_queries)} queries from Redis.")

            # Paginate the result
            page = self.paginate_queryset(top_queries)
            if page is not None:
                logger.debug(
                    "Returning paginated response for search queries.")
                return self.get_paginated_response(page)

            return Response(top_queries)
        except Exception as e:
            logger.error(f"Error retrieving cached search queries: {e}")
            return Response({"detail": "Error retrieving cached queries."}, status=500)


class UserSearchHistoryView(generics.ListAPIView):
    serializer_class = UserSearchHistorySerializer
    permission_classes = [CustomIsAuthenticated]
    pagination_class = CustomPageNumberPagination  # Add your custom pagination here

    def get_queryset(self):
        return UserSearchHistory.objects.filter(user=self.request.user)


class UserFeedView(generics.ListAPIView):
    serializer_class = StorySerializer
    # permission_classes = [CustomIsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        logger.debug(f"The logged user: {user}!")

        if not user.is_authenticated:
            logger.debug("User is not authenticated.")
            return Story.objects.none()

        try:
            user_settings = UserSetting.objects.get(user=user)
            preferred_categories = user_settings.personal_settings.get(
                "favorite_categories", []
            )
            logger.debug(
                f"The preferred_categories: {preferred_categories} found!")
        except UserSetting.DoesNotExist:
            logger.debug("User settings not found.")
            return Story.objects.none()

        if "__all__" in preferred_categories:
            return Story.objects.all().order_by("-created_at")
        elif preferred_categories:
            return Story.objects.filter(category__id__in=preferred_categories).order_by(
                "-created_at"
            )
        else:
            logger.debug("Favorite categories are empty.")
            return Story.objects.none()


class UserInverseFeedView(generics.ListAPIView):
    serializer_class = StorySerializer

    def get_queryset(self):
        user = self.request.user
        logger.debug(f"The logged user: {user}!")

        if not user.is_authenticated:
            logger.debug("User is not authenticated.")
            return Story.objects.none()

        try:
            user_settings = UserSetting.objects.get(user=user)
            preferred_categories = user_settings.personal_settings.get(
                "favorite_categories", []
            )
            logger.debug(
                f"The preferred_categories: {preferred_categories} found!")
        except UserSetting.DoesNotExist:
            logger.debug("User settings not found.")
            return Story.objects.none()

        if "__all__" in preferred_categories:
            # Return an empty queryset if user's favorite categories include all categories
            logger.debug("User's favorite categories include all categories.")
            return Story.objects.none()
        elif preferred_categories:
            # Exclude stories from preferred categories
            return Story.objects.exclude(
                category__id__in=preferred_categories
            ).order_by("-created_at")
        else:
            # Return all stories if favorite categories are empty
            return Story.objects.all().order_by("-created_at")


class TrendingStoriesView(generics.ListAPIView):
    serializer_class = TrendingStorySerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            logger.debug("User is not authenticated.")
            return Story.objects.none()

        try:
            user_settings = UserSetting.objects.get(user=user)
            favorite_categories = user_settings.personal_settings.get(
                "favorite_categories", []
            )
            logger.debug(
                f"Favorite categories for user {user.id}: {favorite_categories}")

        except UserSetting.DoesNotExist:
            logger.debug("User settings not found.")
            return Story.objects.none()

        queryset = (
            Story.objects.filter(category__id__in=favorite_categories)
            .annotate(
                like_count=Count("likes_set", distinct=True),
                dislike_count=Count("dislikes_set", distinct=True),
                view_count=Count(
                    "interactions",
                    filter=DjangoQ(
                        interactions__interaction_type="view"),
                    distinct=True,
                ),
            )
            .annotate(
                calculated_trending_score=F("like_count")
                - F("dislike_count")
                + F("view_count")
            )
            .order_by("-calculated_trending_score")
        )

        logger.debug("Trending stories queryset prepared.")
        return queryset


class LikeCreateView(StoryMixin, generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [CustomIsAuthenticated]

    def perform_create(self, serializer):
        try:
            logger.debug('Creating a like')
            serializer.save()
        except IntegrityError:
            logger.warning('User has already liked this story')
            raise serializers.ValidationError(
                "You have already liked this story.")


class DislikeCreateView(StoryMixin, generics.CreateAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    permission_classes = [CustomIsAuthenticated]

    def perform_create(self, serializer):
        try:
            logger.debug('Creating a dislike')
            serializer.save()
        except IntegrityError:
            logger.warning('User has already disliked this story')
            raise serializers.ValidationError(
                "You have already disliked this story.")


class LikeDestroyView(StoryMixin, generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [CustomIsAuthenticated]

    def get_queryset(self):
        story_id = self.kwargs.get("story_id")
        story_slug = self.kwargs.get("story_slug")
        logger.debug(
            f"Removing like for story_id: {story_id}, story_slug: {story_slug}")

        if story_id:
            return self.queryset.filter(user=self.request.user, story__id=story_id)
        elif story_slug:
            return self.queryset.filter(user=self.request.user, story__slug=story_slug)

    def get_object(self):
        story = self.get_story()
        obj = get_object_or_404(Like, user=self.request.user, story=story)
        self.check_object_permissions(self.request, obj)
        logger.debug(f"Removing like for story {story.id}")
        return obj


class DislikeDestroyView(StoryMixin, generics.DestroyAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    permission_classes = [CustomIsAuthenticated]

    def get_queryset(self):
        story_id = self.kwargs.get("story_id")
        story_slug = self.kwargs.get("story_slug")
        logger.debug(
            f"Removing dislike for story_id: {story_id}, story_slug: {story_slug}")

        if story_id:
            return self.queryset.filter(user=self.request.user, story__id=story_id)
        elif story_slug:
            return self.queryset.filter(user=self.request.user, story__slug=story_slug)

    def get_object(self):
        story = self.get_story()
        obj = get_object_or_404(Like, user=self.request.user, story=story)
        self.check_object_permissions(self.request, obj)
        logger.debug(f"Removing dislike for story {story.id}")
        return obj


class BookmarkCreateListView(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [CustomIsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        logger.debug(f"Listing bookmarks for user {user.id}")
        queryset = Bookmark.objects.filter(user=user)

        # Get the 'category' query parameter
        category = self.request.query_params.get("category", None)
        if category is not None:
            logger.debug(f"Filtering bookmarks by category: {category}")
            queryset = queryset.filter(bookmark_category=category)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        story_id = serializer.validated_data.get(
            "story_id"
        ).id  # Get the ID of the story instance

        # Check if the story has already been bookmarked by the user
        if Bookmark.objects.filter(story_id=story_id, user=user).exists():
            logger.warning(
                f"User {user.id} has already bookmarked story {story_id}")
            raise serializers.ValidationError(
                {"detail": "You have already bookmarked this story."}
            )

        # Update the validated_data with user and story_id
        validated_data = serializer.validated_data
        validated_data.update({"user": user, "story_id": story_id})

        # Save the bookmark with the updated validated_data
        logger.debug(
            f"Creating bookmark for story {story_id} by user {user.id}")
        serializer.save(**validated_data)

    def create(self, request, *args, **kwargs):
        response = super(BookmarkCreateListView, self).create(
            request, *args, **kwargs)

        # Check if creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            response.data = {"status": "success", "data": response.data}
        # Note: If there are other status codes you want to handle, you can add more conditions.
        return response


class BaseBookmarkView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [CustomIsAuthenticated, IsOwner]

    def get_user_bookmark(self, lookup_field, lookup_value):
        user = self.request.user
        logger.debug(
            f"Retrieving bookmark for user {user.id} by {lookup_field}: {lookup_value}")
        filter_kwargs = {lookup_field: lookup_value, "user": user}
        return get_object_or_404(Bookmark, **filter_kwargs)


class BookmarkRetrieveUpdateDestroyView(BaseBookmarkView):
    def get_object(self):
        bookmark_id = self.kwargs.get("bookmark_id")
        logger.debug(f"Retrieving bookmark with id {bookmark_id}")
        return self.get_user_bookmark("pk", bookmark_id)


class BookmarkRetrieveUpdateDestroyViewByStoryId(BaseBookmarkView):
    def get_object(self):
        story_id = self.kwargs.get("story_id")
        logger.debug(f"Retrieving bookmark for story id {story_id}")
        return self.get_user_bookmark("story_id", story_id)


# stories/views.py
