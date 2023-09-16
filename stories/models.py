from django.db import models
from django.urls import reverse
from django.conf import settings
from autoslug import AutoSlugField
from utils.managers import SoftDeleteManager, ActiveUnflaggedManager
from feedback.managers import ReportManager
from utils.models import SoftDeletableModel, TimestampedModel, FlaggedContentMixin

class Category(SoftDeletableModel, TimestampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    
    objects = SoftDeleteManager()


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Story(FlaggedContentMixin, SoftDeletableModel, TimestampedModel):
    """Model representing a user's story."""
    title = models.CharField(max_length=70)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True, db_index=True)
    body = models.TextField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    parent_story = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='child_stories', db_index=True)
    source_link = models.URLField(blank=True, null=True, help_text="URL where the full story can be read.")
    event_occurred_at = models.DateTimeField(blank=True, null=True, db_index=True, help_text="Date and time when the event/incident occurred.")
    event_reported_at = models.DateTimeField(blank=True, null=True, db_index=True, auto_now_add=True, help_text="Date and time when the event/incident was reported to the system.")

    objects = models.Manager()  # Default manager
    active_objects = SoftDeleteManager()  # For filtering soft-deleted items
    report_objects = ReportManager()  # For filtering flagged items
    # active_unflagged_objects = StoryManager()  # For filtering both soft-deleted and flagged items

    active_unflagged_objects = ActiveUnflaggedManager()

    @property
    def likes_count(self):
        return self.likes_set.count()

    @property
    def dislikes_count(self):
        return self.dislikes_set.count()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Stories"
    
    # def get_all_parents(self):
    #     """Recursively retrieve all parent posts."""
    #     parents = []
    #     current = self.parent_story
    #     while current:
    #         parents.insert(0, current)
    #         current = current.parent_story
    #     return parents

    # def get_all_children(self):
    #     """Recursively retrieve all child posts."""
    #     children = list(self.child_posts.all())
    #     for child in children:
    #         children.extend(child.get_all_children())
    #     return children

    def get_all_parents(self):
        """Retrieve all parent stories without recursive queries."""
        all_stories = {story.id: story for story in Story.objects.all()}
        parents = []
        current = self.parent_story
        while current:
            parents.insert(0, current)
            current = all_stories.get(current.parent_story_id)
        return parents
    
    def get_all_children(self):
        """Retrieve all child stories without recursive queries."""
        all_stories = {story.id: story for story in Story.objects.all()}
        children = list(self.child_stories.all())
        i = 0
        while i < len(children):
            child = children[i]
            children.extend(child.child_stories.all())
            i += 1
        return children
    
    def get_absolute_url(self):
        return reverse('story-retrieve-update-destroy', kwargs={'story_slug': self.slug})


class Like(SoftDeletableModel, TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='likes_set')
    
    class Meta:
        unique_together = ['user', 'story']

class Dislike(SoftDeletableModel, TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='dislikes_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Dislikes"
        unique_together = ['user', 'story']

class Bookmark(SoftDeletableModel, TimestampedModel):
    BOOKMARK_CATEGORIES = [
        ('Read Later', 'Read Later'),
        ('Favorites', 'Favorites'),
        ('Save', 'Save')
    ]

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='bookmarks')
    bookmark_category = models.CharField(max_length=50, choices=BOOKMARK_CATEGORIES, default='Read Later')
    note = models.TextField(null=True, blank=True)

    @property
    def title(self):
        return self.story.title

    @property
    def url(self):
        # Assuming you have a get_absolute_url method in the Story model
        return self.story.get_absolute_url()

    @property
    def thumbnail_url(self):
        # Assuming the multimedia model has a method to get the thumbnail URL
        multimedia = self.story.multimedia.first()
        return multimedia.thumbnail.url if multimedia else None

    @property
    def story_published_at(self):
        return self.story.created_at
    class Meta:
        # db_table = ''
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'

    def __str__(self):
        return f"Bookmark of story: {self.story.title}"


# stories/models.py