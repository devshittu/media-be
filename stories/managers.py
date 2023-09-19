from django.db import models
from django.apps import apps

class StoryManager(models.Manager):
    def for_user(self, user):
        UserSetting = apps.get_model('users', 'UserSetting')
        StoryModel = apps.get_model('stories', 'Story')
        
        user_settings = UserSetting.objects.get(user=user)
        favorite_categories = user_settings.personal_settings.get('favorite_categories', ['__all__'])

        if '__all__' in favorite_categories:
            return StoryModel.active_unflagged_objects.all()
        else:
            # Ensure that all items in favorite_categories can be converted to integers
            category_ids = [int(cat_id) for cat_id in favorite_categories if cat_id != '__all__']
            return StoryModel.active_unflagged_objects.filter(category__id__in=category_ids)
