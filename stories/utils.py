import logging
import re

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

# stories/utils.py
