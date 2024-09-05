import logging
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


# Cache search query in Redis
def cache_search_query(query):
    try:
        redis_conn = get_redis_connection("default")
        # Add or increment the query in Redis sorted set with score representing recency
        redis_conn.zincrby("search_queries", 1, query)
        logger.info(f"Search query '{query}' cached in Redis.")
    except Exception as e:
        logger.error(f"Error caching search query '{query}': {e}")


def store_user_search_history(user, query):
    if user.is_authenticated:
        UserSearchHistory.objects.create(user=user, query=query)
        logger.info(f"Stored search query '{query}' for user '{user}'.")

# stories/utils.py
