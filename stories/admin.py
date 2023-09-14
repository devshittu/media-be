from django.contrib import admin
from .models import Story

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

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'likes_count', 'dislikes_count', 'is_flagged', 'deleted_at']
    list_filter = [ActiveUnflaggedFilter]
    actions = [unflag_stories, restore_stories]






# stories/admin.py