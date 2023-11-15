# utils/version_utils.py

from django.db.models import Max
from .models import AppVersion
import re


def get_latest_version(version_prefix):
    """
    Get the latest version that matches the provided version prefix.
    For example, if version_prefix is '1', it returns the latest '1.x.x'.
    """
    # Extract major and minor version numbers if they exist
    match = re.match(r"v?(\d+)(?:\.(\d+))?", version_prefix)
    if not match:
        return None

    major, minor = match.groups()
    major = int(major)
    minor = int(minor) if minor is not None else None

    # Filter versions based on major (and minor if provided)
    version_filter = {"major_version": major}
    if minor is not None:
        version_filter["minor_version"] = minor

    # Aggregate to find the latest version
    latest_version = AppVersion.objects.filter(**version_filter).aggregate(
        latest_version=Max("version")
    )["latest_version"]

    return latest_version
