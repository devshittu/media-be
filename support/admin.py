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
    PrivacyPolicy,
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    # prepopulated_fields = {"slug": ("name",)}


class TicketAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "category", "created_at", "updated_at")
    search_fields = ("subject", "description")
    list_filter = ("created_at", "updated_at", "category")
    raw_id_fields = ("user",)


class TicketResponseAdmin(admin.ModelAdmin):
    list_display = ("ticket", "user", "created_at", "updated_at")
    search_fields = ("message",)
    list_filter = ("created_at", "updated_at")
    raw_id_fields = ("user", "ticket")


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


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


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",  # Include slug here if you want to display it in the list
        "category",
        "app_version",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "content")
    list_filter = ("created_at", "updated_at", "category", "app_version")
    # Removed prepopulated_fields for slug since it's an AutoSlugField
    filter_horizontal = ("tags",)


class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "app_version", "created_at", "updated_at")
    search_fields = ("question", "answer")
    list_filter = ("created_at", "updated_at", "app_version")


class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ("title", "app_version", "created_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("created_at", "updated_at", "app_version")


class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ("title", "app_version", "created_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("created_at", "updated_at", "app_version")


# Register the models with their custom admin views
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(AppVersion, AppVersionAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketResponse, TicketResponseAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(TermsAndConditions, TermsAndConditionsAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)

# support/admin.py
