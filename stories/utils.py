import re
from datetime import datetime, timedelta
from django.db.models import Count
from neomodel import db
from .models import Story, Category
from django.db.models import F, Count, Q


def extract_hashtags(text):
    return set(part[1:] for part in re.findall(r"#\w+", text))

# stories/utils.py
