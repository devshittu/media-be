from django.contrib import admin
from .models import Report

class ReportAdmin(admin.ModelAdmin):
    # Fields to be displayed in the list view
    list_display = ('user', 'report_type', 'content_object', 'is_anonymous', 'created_at', 'updated_at')

    # Fields that can be used for searching
    search_fields = ('user__email', 'report_type', 'description')

    # Filters to be added on the right side of the admin page
    list_filter = ('report_type', 'is_anonymous', 'created_at', 'updated_at')

    # Add a date hierarchy based on created_at field
    date_hierarchy = 'created_at'

    # Add custom actions
    actions = ['mark_as_anonymous', 'unmark_as_anonymous']

    def mark_as_anonymous(self, request, queryset):
        queryset.update(is_anonymous=True)
    mark_as_anonymous.short_description = "Mark selected reports as anonymous"

    def unmark_as_anonymous(self, request, queryset):
        queryset.update(is_anonymous=False)
    unmark_as_anonymous.short_description = "Unmark selected reports as anonymous"

# Register the Report model with the custom admin class
admin.site.register(Report, ReportAdmin)
