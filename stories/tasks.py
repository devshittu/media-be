from django_redis import get_redis_connection
import logging
from celery import shared_task
from .models import Story
from .documents import StoryDocument

logger = logging.getLogger('app_logger')


@shared_task
def index_story_to_elasticsearch(story_id):
    """
    Task to index a single story into Elasticsearch.
    """
    try:
        # Fetch the story from the database
        story = Story.objects.get(id=story_id)
        logger.debug(f'Indexing story with ID {story_id} into Elasticsearch.')

        # Index the story using StoryDocument
        StoryDocument().update(story)

        logger.info(
            f'Successfully indexed story with ID {story_id} into Elasticsearch.')

    except Story.DoesNotExist:
        logger.error(
            f'Story with ID {story_id} does not exist. Skipping indexing.')


@shared_task
def remove_story_from_elasticsearch(story_id):
    """
    Task to remove a story from the Elasticsearch index.
    """
    try:
        # Fetch the story from the database
        story = Story.objects.get(id=story_id)
        logger.debug(f'Removing story with ID {story_id} from Elasticsearch.')

        # Remove the story using StoryDocument
        StoryDocument().delete(story)

        logger.info(
            f'Successfully removed story with ID {story_id} from Elasticsearch.')

    except Story.DoesNotExist:
        logger.error(
            f'Story with ID {story_id} does not exist. Skipping deletion.')


@shared_task
def reindex_all_stories():
    """
    Task to reindex all stories into Elasticsearch.
    """
    logger.debug('Starting full reindex of all stories into Elasticsearch.')
    # Get all stories from the database
    stories = Story.objects.all()

    # Loop through and reindex each story
    for story in stories:
        logger.debug(f'Indexing story with ID {story.id} into Elasticsearch.')
        StoryDocument().update(story)

    logger.info('Successfully completed full reindex of all stories.')


@shared_task
def update_autocomplete_cache():
    logger.info("Starting the autocomplete cache update task.")
    redis_conn = get_redis_connection("default")

    try:
        # Fetch the top 100 common story titles from Postgres
        top_stories = Story.objects.values_list('title', flat=True)[:100]
        logger.info(
            f"Fetched {len(top_stories)} story titles from the database.")

        # Store these titles in Redis
        for title in top_stories:
            # Add the title with score 0
            redis_conn.zadd("autocomplete_titles", {title: 0})
        logger.info("Successfully updated the autocomplete cache in Redis.")

    except Exception as e:
        logger.error(f"Error occurred while updating autocomplete cache: {e}")
        raise


@shared_task
def clean_old_search_queries():
    """
    Task to clean up old or infrequent search queries from Redis.
    """
    redis_conn = get_redis_connection("default")
    try:
        # Remove queries with a score below 5 (infrequent searches)
        redis_conn.zremrangebyscore("search_queries", "-inf", 5)
        logger.info("Cleaned up infrequent search queries from Redis.")
    except Exception as e:
        logger.error(f"Error cleaning search queries: {e}")
# stories/tasks.py
