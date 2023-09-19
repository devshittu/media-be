from autoseed.utils.base_seed import BaseSeed
from .models import Category, Story, Bookmark, Like, Dislike
from django.utils import timezone
from utils.helpers import unix_to_datetime

class CategorySeed(BaseSeed):
    raw_file = 'categories'
    model = Category

    @classmethod
    def get_fields(cls, item):
        # Directly return the fields you want
        # Use timezone-aware datetime
        current_time = timezone.now().isoformat()
        return {
            'title': item['title'],
            'slug': item['slug'],
            'description': item['description'],
            'created_at': current_time,
            'updated_at': current_time
        } 


class StorySeed(BaseSeed):
    raw_file = 'stories'
    model = Story

    @classmethod
    def get_fields(cls, item):
        # Convert Unix timestamp to timezone-aware datetime
        created_time = unix_to_datetime(item['created_at'])
        updated_time = unix_to_datetime(item['updated_at'])

        # Check if 'news_channel' key exists
        source_link = item['user']['news_channel']['feedUrl'] if 'news_channel' in item['user'] else None

        return {
            'title': item['title'],
            'slug': item['slug'],
            'body': item['body'],
            'user': item['user']['id'],
            'category': int(item['category_id']),
            'parent_story': item['parent_stories'][0] if item['parent_stories'] else None,
            'source_link': source_link,
            'created_at': created_time.isoformat(),
            'updated_at': updated_time.isoformat(),
            'event_reported_at': timezone.now().isoformat()  # Assuming you want the current time for this field
        }


class BookmarkSeed(BaseSeed):
    raw_file = 'bookmarks'
    model = Bookmark

    @classmethod
    def get_fields(cls, item):
        # Convert Unix timestamp to timezone-aware datetime
        created_time = timezone.now()
        updated_time = timezone.now()

        return {
            'user': item['user'],
            'story': item['story'],
            'bookmark_category': item['bookmark_category'],
            'note': item['note'],
            'created_at': created_time.isoformat(),
            'updated_at': updated_time.isoformat()
        }

class LikeSeed(BaseSeed):
    raw_file = 'likes'
    model = Like
    @classmethod
    def get_fields(cls, item):
        # Convert Unix timestamp to timezone-aware datetime
        created_time = timezone.now()
        updated_time = timezone.now()

        return {
            # 'id': item['id'],
            'user': item['user'],
            'story': item['story'],
            'created_at': created_time.isoformat(),
            'updated_at': updated_time.isoformat()
        }

# stories/seeds.py