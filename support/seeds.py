from django.utils import timezone
from managekit.utils.base_seed import BaseSeed
from .models import FAQ, Article, AppVersion, Category, Tag
from django.utils.text import slugify


class AppVersionSeed(BaseSeed):
    raw_file = "app_version"
    model = AppVersion
    # No dependencies for AppVersion since it's likely to be a standalone model

    @classmethod
    def get_fields(cls, item):
        return {
            "version": item["version"],
            "features": item["features"],
            "updates": item["updates"],
            "bug_fixes": item["bug_fixes"],
            "deprecations": item["deprecations"],
            "created_at": timezone.now().isoformat(),
            "updated_at": timezone.now().isoformat(),
        }


class CategorySeed(BaseSeed):
    raw_file = "categories"
    model = Category

    @classmethod
    def get_fields(cls, item):
        return {
            "name": item["name"],
            "slug": item.get("slug"),  # slug is auto-generated, but can be overridden
            "parent": item.get(
                "parent"
            ),  # This should be the ID of the parent category if it exists
            "created_at": timezone.now().isoformat(),
            "updated_at": timezone.now().isoformat(),
        }


class TagSeed(BaseSeed):
    raw_file = "tags"
    model = Tag

    @classmethod
    def get_fields(cls, item):
        return {
            "name": item["name"],
            "slug": item.get("slug"),  # slug is auto-generated, but can be overridden,
            "created_at": timezone.now().isoformat(),
            "updated_at": timezone.now().isoformat(),
        }


class FAQSeed(BaseSeed):
    raw_file = "faq"
    model = FAQ
    dependencies = [
        AppVersionSeed,  # Assuming FAQs depend on AppVersion
    ]

    @classmethod
    def get_fields(cls, item):
        return {
            "question": item["question"],
            "answer": item["answer"],
            "app_version": item["app_version"],
            "created_at": timezone.now().isoformat(),
            "updated_at": timezone.now().isoformat(),
        }


class ArticleSeed(BaseSeed):
    raw_file = "articles"
    model = Article
    dependencies = [
        AppVersionSeed,  # Assuming Articles depend on AppVersion
        CategorySeed,  # If articles depend on categories
        TagSeed,  # If articles have tags
    ]

    @classmethod
    def get_fields(cls, item):
        # Ensure that the title is unique to avoid slug conflicts
        unique_title = item["title"] + timezone.now().strftime(" %Y-%m-%d %H:%M:%S")
        return {
            "title": unique_title,
            "slug": slugify(unique_title),
            "content": item["content"],
            "app_version": item["app_version"],
            "category": item.get("category"),  # Assuming there's a category field
            "tags": item.get("tags", []),  # Assuming there's a tags field
            "created_at": timezone.now().isoformat(),
            "updated_at": timezone.now().isoformat(),
        }


# support/seeds.py
