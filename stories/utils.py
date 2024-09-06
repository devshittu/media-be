import logging
import time
import re
from django_redis import get_redis_connection
from .models import UserSearchHistory

# Set up the logger for this module
logger = logging.getLogger('app_logger')


def extract_hashtags(text):
    """
    Extract hashtags from a given text.

    Args:
        text (str): The text to extract hashtags from.

    Returns:
        set: A set of unique hashtags.
    """
    logger.debug(f'Extracting hashtags from text: {text}')
    hashtags = set(part[1:] for part in re.findall(r"#\w+", text))
    logger.info(f'Extracted hashtags: {hashtags}')
    return hashtags


# Cache search query in Redis with additional metadata (search_term, hits, searched_at)
def cache_search_query(query, hits):
    try:
        # Try to establish a connection to Redis
        redis_conn = get_redis_connection("default")
        # Current timestamp in seconds (Unix format)
        timestamp = int(time.time())

        # Log the caching action and check Redis connection
        logger.debug(
            f"Connecting to Redis to cache query '{query}' with hits: {hits} and timestamp: {timestamp}."
        )

        # Store query metadata in a Redis hash
        redis_conn.hset(f"search_query:{query}", mapping={
            "search_term": query,
            "hits": hits,
            "searched_at": timestamp,  # Store Unix timestamp without microseconds
        })

        # Log after successful hash set
        logger.debug(f"Cached metadata for query '{query}' in Redis.")

        # Use the timestamp as the score in a sorted set to keep queries ordered by recency
        redis_conn.zadd("search_queries", {query: timestamp})

        # Log after successful addition to sorted set
        logger.info(
            f"Search query '{query}' cached in Redis with hits {hits} and timestamp."
        )
    except Exception as e:
        # Log the exception if something goes wrong
        logger.error(f"Error caching search query '{query}': {e}")


def store_user_search_history(user, query):
    if user.is_authenticated:
        UserSearchHistory.objects.create(user=user, query=query)
        logger.info(f"Stored search query '{query}' for user '{user}'.")

# stories/utils.py
