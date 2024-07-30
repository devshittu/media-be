import logging
from django.db import models
from django.apps import apps

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class StoryManager(models.Manager):
    def for_user(self, user):
        logger.debug(f'Retrieving stories for user {user.id}')
        UserSetting = apps.get_model('users', 'UserSetting')
        StoryModel = apps.get_model('stories', 'Story')

        try:
            user_settings = UserSetting.objects.get(user=user)
            logger.info(f'User settings retrieved for user {user.id}')
        except UserSetting.DoesNotExist:
            logger.error(f'User settings not found for user {user.id}')
            return StoryModel.objects.none()
        favorite_categories = user_settings.personal_settings.get(
            'favorite_categories', ['__all__'])

        if '__all__' in favorite_categories:
            logger.debug(f'User {user.id} has favorite categories set to all')
            return StoryModel.active_unflagged_objects.all()
        else:
            # Ensure that all items in favorite_categories can be converted to integers
            try:
                category_ids = [
                    int(cat_id) for cat_id in favorite_categories if cat_id != '__all__']
                logger.debug(
                    f'Favorite category IDs for user {user.id}: {category_ids}')
            except ValueError as e:
                logger.error(
                    f'Invalid category ID in favorite categories for user {user.id}: {e}')
                return StoryModel.objects.none()

            return StoryModel.active_unflagged_objects.filter(category__id__in=category_ids)

# stories/managers.py
