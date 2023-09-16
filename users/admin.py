from django.contrib import admin
from .models import UserSetting, Follow
import json

class UserSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'system_settings', 'account_settings', 'notification_settings', 'personal_settings')
    search_fields = ('user__email', 'user__username')
    list_filter = ('deleted_at',)  # Filter by soft-deleted items

    # To make JSON fields more readable in the admin panel
    def pretty_json(self, obj, field_name):
        return json.dumps(getattr(obj, field_name), indent=4)

    def system_settings(self, obj):
        return self.pretty_json(obj, 'system_settings')

    def account_settings(self, obj):
        return self.pretty_json(obj, 'account_settings')

    def notification_settings(self, obj):
        return self.pretty_json(obj, 'notification_settings')

    def personal_settings(self, obj):
        return self.pretty_json(obj, 'personal_settings')

class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed', 'created_at')
    search_fields = ('follower__username', 'followed__username')
    list_filter = ('deleted_at', 'created_at')  # Filter by soft-deleted items and creation date

admin.site.register(UserSetting, UserSettingAdmin)
admin.site.register(Follow, FollowAdmin)
