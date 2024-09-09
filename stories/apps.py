from django.apps import AppConfig

class StoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stories'

    def ready(self):
        import stories.neo_signals
        import stories.signals

# stories/apps.py
