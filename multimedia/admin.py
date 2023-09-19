from django.contrib import admin
from .models import Multimedia

class MultimediaAdmin(admin.ModelAdmin):
    list_display = ('media_type', 'user', 'story', 'created_at', 'updated_at')
    list_filter = ('media_type', 'user', 'story', 'created_at', 'updated_at')
    search_fields = ('media_type', 'user__email', 'story__id')
    ordering = ('-created_at',)

admin.site.register(Multimedia, MultimediaAdmin)