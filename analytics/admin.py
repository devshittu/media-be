from django.contrib import admin
from .models import (
     UserSession, 
    StoryInteraction, UserNotInterested, AccessibilityTool
)

class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_timestamp', 'device_type', 'operating_system', 'browser', 'ip_address', 'geolocation', 'time_zone')
    search_fields = ('user__username', 'device_type', 'operating_system', 'browser', 'ip_address', 'geolocation', 'time_zone')
    list_filter = ('start_timestamp',)

class StoryInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'interaction_type')
    search_fields = ('user__username', 'story__title', 'interaction_type')
    list_filter = ('interaction_type',)

class UserNotInterestedAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'reason')
    search_fields = ('user__username', 'story__title', 'reason')
    list_filter = ('created_at',)

class AccessibilityToolAdmin(admin.ModelAdmin):
    list_display = ('user', 'tool_name')
    search_fields = ('user__username', 'tool_name')
    list_filter = ('tool_name',)

admin.site.register(UserSession, UserSessionAdmin)
admin.site.register(StoryInteraction, StoryInteractionAdmin)
admin.site.register(UserNotInterested, UserNotInterestedAdmin)
admin.site.register(AccessibilityTool, AccessibilityToolAdmin)
