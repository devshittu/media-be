from django.db import models
from django.conf import settings
from django.utils.text import slugify
import time
from django.utils import timezone
from autoslug import AutoSlugField
from utils.managers import ActiveManager

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    # slug = models.SlugField(unique=True)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


    objects = ActiveManager()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.title

class Story(models.Model):
    """Model representing a user's story."""
    title = models.CharField(max_length=70)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True, db_index=True)
    body = models.TextField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    parent_story = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='child_stories', db_index=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    source_link = models.URLField(blank=True, null=True, help_text="URL where the full story can be read.")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    event_occurred_at = models.DateTimeField(db_index=True, help_text="Date and time when the event/incident occurred.")
    event_reported_at = models.DateTimeField(db_index=True, auto_now_add=True, help_text="Date and time when the event/incident was reported to the system.")
    deleted_at = models.DateTimeField(null=True, blank=True)

   
    objects = ActiveManager()


    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.title
    
    # def get_all_parents(self):
    #     """Recursively retrieve all parent posts."""
    #     parents = []
    #     current = self.parent_post
    #     while current:
    #         parents.insert(0, current)
    #         current = current.parent_post
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




# class UserInterest(models.Model):
#     """Model representing a user's interest in a story."""
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     story = models.ForeignKey(Story, on_delete=models.CASCADE)
#     is_interested = models.BooleanField()
#     deleted_at = models.DateTimeField(null=True, blank=True)

#     objects = ActiveManager()

#     class Meta:
#         unique_together = ['user', 'story']

#     def __str__(self):
#         return f"{self.user.username} - {'Interested' if self.is_interested else 'Not Interested'} in {self.story.title}"

#     def delete(self, using=None, keep_parents=False):
#         self.deleted_at = timezone.now()
#         self.save()

#     def restore(self):
#         self.deleted_at = None
#         self.save()

# stories/models.py