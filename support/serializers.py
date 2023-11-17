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
    PrivacyPolicy,
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


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class CategorySerializer(UnixTimestampModelSerializer):
    subcategories = SubcategorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "subcategories", "created_at", "updated_at"]


class TicketSerializer(UnixTimestampModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
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
        fields = ["id", "name", "slug", "created_at", "updated_at"]


class AppVersionSerializer(UnixTimestampModelSerializer):
    class Meta:
        model = AppVersion
        fields = [
            "id",
            "version",
            "major_version",
            "minor_version",
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
    # content = MarkdownField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "reading_time",
            "summary",
            "category",
            "tags",
            "app_version",
            "created_at",
            "updated_at",
        ]

    def get_summary(self, obj):
        return obj.summary()

    def get_reading_time(self, obj):
        return obj.reading_time()


class FAQSerializer(UnixTimestampModelSerializer):
    # answer = MarkdownField()

    class Meta:
        model = FAQ
        fields = [
            "question",
            "answer",
            "app_version",
            "created_at",
            "updated_at",
        ]


class VersionedDocumentSerializer(UnixTimestampModelSerializer):
    # content = MarkdownField()

    class Meta:
        model = VersionedDocument
        fields = ["content", "app_version", "created_at", "updated_at"]
        abstract = True


class TermsAndConditionsSerializer(VersionedDocumentSerializer):
    class Meta(VersionedDocumentSerializer.Meta):
        model = TermsAndConditions
        fields = VersionedDocumentSerializer.Meta.fields + ["title"]


# support/serializers.py


class PrivacyPolicySerializer(VersionedDocumentSerializer):
    class Meta(VersionedDocumentSerializer.Meta):
        model = PrivacyPolicy
        fields = VersionedDocumentSerializer.Meta.fields + ["title"]


# support/serializers.py
