from django.contrib import admin
from .models import (Story, Category, Like, Dislike, Bookmark)

class ActiveUnflaggedFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('active_unflagged', 'Active and Unflagged'),
            ('flagged', 'Flagged'),
            ('deleted', 'Deleted'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active_unflagged':
            return queryset.filter(deleted_at__isnull=True, is_flagged=False)
        if self.value() == 'flagged':
            return queryset.filter(is_flagged=True)
        if self.value() == 'deleted':
            return queryset.filter(deleted_at__isnull=False)



def unflag_stories(modeladmin, request, queryset):
    queryset.update(is_flagged=False)
unflag_stories.short_description = "Unflag selected stories"

def restore_stories(modeladmin, request, queryset):
    queryset.update(deleted_at=None)
restore_stories.short_description = "Restore soft-deleted stories"

# @admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'slug', 'category', 'event_occurred_at', 'event_reported_at', 'likes_count', 'dislikes_count', 'is_flagged', 'deleted_at']
    list_filter = [ActiveUnflaggedFilter, 'user', 'category', 'event_occurred_at', 'event_reported_at']
    actions = [unflag_stories, restore_stories]
    search_fields = ('title', 'body')
    # list_filter = ('user', 'category', 'event_occurred_at', 'event_reported_at')
    # prepopulated_fields = {'slug': ('title',)}


# @admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'slug']
    search_fields = ('title', 'description')
    # prepopulated_fields = {'slug': ('title',)}

class LikeInline(admin.TabularInline):
    model = Like
    extra = 0

class DislikeInline(admin.TabularInline):
    model = Dislike
    extra = 0

class BookmarkInline(admin.TabularInline):
    model = Bookmark
    extra = 0

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'story')
    list_filter = ('user', 'story')

class DislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'created_at')
    list_filter = ('user', 'story')

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('story', 'bookmark_category', 'note')
    list_filter = ('bookmark_category',)
    search_fields = ('story__title', 'note')

# Register the models with their custom admin views
admin.site.register(Category, CategoryAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)
admin.site.register(Bookmark, BookmarkAdmin)

# stories/admin.py