from django.contrib import admin
from .models import (
    DeviceData, LocationData, ReferralData, UserSession, 
    StoryInteraction, UserNotInterested, AccessibilityTool
)

class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ('interaction', 'device_type', 'operating_system', 'browser')
    search_fields = ('device_type', 'operating_system', 'browser')
    list_filter = ('device_type', 'operating_system', 'browser')

class LocationDataAdmin(admin.ModelAdmin):
    list_display = ('interaction', 'ip_address', 'geolocation', 'time_zone')
    search_fields = ('ip_address', 'geolocation', 'time_zone')
    list_filter = ('geolocation', 'time_zone')

class ReferralDataAdmin(admin.ModelAdmin):
    list_display = ('interaction', 'referrer_url', 'search_terms')
    search_fields = ('referrer_url', 'search_terms')

class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'start_timestamp')
    search_fields = ('user__username', 'session_id')
    list_filter = ('start_timestamp',)

class StoryInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'interaction_type', 'session')
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

admin.site.register(DeviceData, DeviceDataAdmin)
admin.site.register(LocationData, LocationDataAdmin)
admin.site.register(ReferralData, ReferralDataAdmin)
admin.site.register(UserSession, UserSessionAdmin)
admin.site.register(StoryInteraction, StoryInteractionAdmin)
admin.site.register(UserNotInterested, UserNotInterestedAdmin)
admin.site.register(AccessibilityTool, AccessibilityToolAdmin)
