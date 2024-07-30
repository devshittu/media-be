import logging
import re
from django.db.models import Max
from .models import AppVersion

# Set up the logger for this module
logger = logging.getLogger('app_logger')


def get_latest_version(version_prefix):
    """
    Get the latest version that matches the provided version prefix.
    For example, if version_prefix is '1', it returns the latest '1.x.x'.
    """
    logger.debug(f'Getting latest version for prefix: {version_prefix}')
    # Extract major and minor version numbers if they exist
    match = re.match(r"v?(\d+)(?:\.(\d+))?", version_prefix)
    if not match:
        logger.warning(f'Invalid version prefix: {version_prefix}')
        return None

    major, minor = match.groups()
    major = int(major)
    minor = int(minor) if minor is not None else None

    logger.debug(f'Parsed version prefix: major={major}, minor={minor}')

    # Filter versions based on major (and minor if provided)
    version_filter = {"major_version": major}
    if minor is not None:
        version_filter["minor_version"] = minor

    logger.debug(f'Applying version filter: {version_filter}')

    # Aggregate to find the latest version
    try:
        latest_version = AppVersion.objects.filter(**version_filter).aggregate(
            latest_version=Max("version")
        )["latest_version"]
        logger.info(f'Found latest version: {latest_version}')
    except Exception as e:
        logger.error(f'Error finding latest version: {e}')
        return None

    return latest_version

# support/utils.py
