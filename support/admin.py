from django.contrib import admin
from .models import (
    Category,
    Ticket,
    TicketResponse,
    Tag,
    AppVersion,
    Article,
    FAQ,
    TermsAndConditions,
    PrivacyTerms,
)
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "category", "created_at", "updated_at")
    search_fields = ("subject", "description")
    list_filter = ("created_at", "updated_at", "category")
    raw_id_fields = ("user",)


@admin.register(TicketResponse)
class TicketResponseAdmin(admin.ModelAdmin):
    list_display = ("ticket", "user", "created_at", "updated_at")
    search_fields = ("message",)
    list_filter = ("created_at", "updated_at")
    raw_id_fields = ("user", "ticket")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(AppVersion)
class AppVersionAdmin(admin.ModelAdmin):
    list_display = (
        "version",
        "features",
        "updates",
        "bug_fixes",
        "deprecations",
        "created_at",
        "updated_at",
    )
    search_fields = ("version",)


# @admin.register(Article)
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = (
#         "title",
#         "slug",
#         "category",
#         "app_version",
#         "created_at",
#         "updated_at",
#     )
#     readonly_fields = ("slug",)  # Make slug read-only
#     search_fields = ("title", "content")
#     list_filter = ("created_at", "updated_at", "category", "app_version")
#     prepopulated_fields = {"slug": ("title",)}
#     filter_horizontal = ("tags",)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "app_version",
        "created_at",
        "updated_at",
    )
    # Removed slug from readonly_fields to allow prepopulated_fields to work
    search_fields = ("title", "content")
    list_filter = ("created_at", "updated_at", "category", "app_version")
    prepopulated_fields = {
        "slug": ("title",)
    }  # This line will auto-fill the slug field based on the title
    filter_horizontal = ("tags",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "app_version", "created_at", "updated_at")
    search_fields = ("question", "answer")
    list_filter = ("created_at", "updated_at", "app_version")


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ("title", "app_version", "created_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("created_at", "updated_at", "app_version")


@admin.register(PrivacyTerms)
class PrivacyTermsAdmin(admin.ModelAdmin):
    list_display = ("title", "app_version", "created_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("created_at", "updated_at", "app_version")


# support/admin.py
