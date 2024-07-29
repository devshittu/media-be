# multimedia/admin.py

import logging
from django.contrib import admin
from .models import Multimedia

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class MultimediaAdmin(admin.ModelAdmin):
    list_display = ('media_type', 'user', 'story', 'created_at', 'updated_at')
    list_filter = ('media_type', 'user', 'story', 'created_at', 'updated_at')
    search_fields = ('media_type', 'user__email', 'story__id')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        logger.debug(f'Saving multimedia object {obj.id}')
        super().save_model(request, obj, form, change)
        logger.info(
            f'Multimedia object {obj.id} saved by {request.user.email}')

    def delete_model(self, request, obj):
        logger.debug(f'Deleting multimedia object {obj.id}')
        super().delete_model(request, obj)
        logger.info(
            f'Multimedia object {obj.id} deleted by {request.user.email}')


admin.site.register(Multimedia, MultimediaAdmin)
# multimedia/admin.py
