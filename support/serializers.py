from rest_framework import serializers
from .models import (
    Category,
    Ticket,
    TicketResponse,
    Tag,
    AppVersion,
    Article,
    FAQ,
    VersionedDocument,
    TermsAndConditions,
    PrivacyTerms,
)
from django.utils.html import mark_safe
from markdown import markdown
from utils.serializers import UnixTimestampModelSerializer


# Custom Markdown Field
class MarkdownField(serializers.CharField):
    def to_representation(self, value):
        # Convert Markdown to HTML
        return mark_safe(markdown(value))

    def to_internal_value(self, data):
        # Sanitize Markdown content
        # You can add your sanitization logic here
        return super().to_internal_value(data)


class CategorySerializer(UnixTimestampModelSerializer):
    subcategories = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="category-detail"
    )

    class Meta:
        model = Category
        fields = ["url", "name", "subcategories", "created_at", "updated_at"]


class TicketSerializer(UnixTimestampModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "url",
            "user",
            "category",
            "subject",
            "description",
            "created_at",
            "updated_at",
        ]


class TicketResponseSerializer(UnixTimestampModelSerializer):
    class Meta:
        model = TicketResponse
        fields = ["url", "ticket", "user", "message", "created_at", "updated_at"]


class TagSerializer(UnixTimestampModelSerializer):
    class Meta:
        model = Tag
        fields = ["url", "name", "slug", "created_at", "updated_at"]


class AppVersionSerializer(UnixTimestampModelSerializer):
    class Meta:
        model = AppVersion
        fields = [
            "url",
            "version",
            "features",
            "updates",
            "bug_fixes",
            "deprecations",
            "created_at",
            "updated_at",
        ]


class ArticleSerializer(UnixTimestampModelSerializer):
    category = CategorySerializer(read_only=True)
    app_version = AppVersionSerializer(read_only=True)
    content = MarkdownField()

    class Meta:
        model = Article
        fields = [
            "url",
            "title",
            "slug",
            "content",
            "category",
            "tags",
            "app_version",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"url": {"lookup_field": "slug", "view_name": "article-detail"}}


class FAQSerializer(UnixTimestampModelSerializer):
    answer = MarkdownField()

    class Meta:
        model = FAQ
        fields = [
            "url",
            "question",
            "answer",
            "app_version",
            "created_at",
            "updated_at",
        ]


class VersionedDocumentSerializer(UnixTimestampModelSerializer):
    content = MarkdownField()

    class Meta:
        model = VersionedDocument
        fields = ["url", "content", "app_version", "created_at", "updated_at"]
        abstract = True


class TermsAndConditionsSerializer(VersionedDocumentSerializer):
    class Meta(VersionedDocumentSerializer.Meta):
        model = TermsAndConditions
        fields = VersionedDocumentSerializer.Meta.fields + ["title"]


class PrivacyTermsSerializer(VersionedDocumentSerializer):
    class Meta(VersionedDocumentSerializer.Meta):
        model = PrivacyTerms
        fields = VersionedDocumentSerializer.Meta.fields + ["title"]
