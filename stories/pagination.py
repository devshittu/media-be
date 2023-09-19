from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response
from core.settings import ANCESTORS_PER_PAGE, DESCENDANTS_PER_PAGE
from stories.models import Story

# TODO can we make this more generic?
# class CenteredPagination(PageNumberPagination):
#     page_size = 10

#     def paginate_queryset(self, queryset, request, view=None):
#         leading_story = queryset.get(slug=request.GET.get('story_slug'))
#         if 'direction' in request.GET and request.GET['direction'] == 'previous':
#             # Get 10 ancestors
#             start = max(0, leading_story.id - 10)
#             queryset = queryset.filter(id__gte=start, id__lt=leading_story.id).order_by('-id')
#         else:
#             # Get 10 descendants
#             end = leading_story.id + 11
#             queryset = queryset.filter(id__gt=leading_story.id, id__lt=end)

#         return super().paginate_queryset(queryset, request, view)

#     def get_paginated_response(self, data):
#         return Response({
#             'next': self.get_next_link(),
#             'previous': self.get_previous_link(),
#             'results': data
#         })


# class CenteredPagination(CursorPagination):
#     page_size_query_param = 'page_size'
#     ordering = '-created_at'  # Assuming each story has a 'created_at' timestamp

#     def paginate_queryset(self, queryset, request, view=None):
#         leading_story = queryset.get(slug=request.GET.get('story_slug'))

#         if 'direction' in request.GET and request.GET['direction'] == 'previous':
#             # Get ancestors based on configuration
#             queryset = queryset.filter(created_at__lte=leading_story.created_at).exclude(id=leading_story.id).order_by('-created_at')[:ANCESTORS_PER_PAGE]
#         else:
#             # Get descendants based on configuration
#             queryset = queryset.filter(created_at__gte=leading_story.created_at).exclude(id=leading_story.id).order_by('created_at')[:DESCENDANTS_PER_PAGE]

#         return super().paginate_queryset(queryset, request, view)
# class CenteredPagination(CursorPagination):
#     page_size_query_param = 'page_size'
#     ordering = '-created_at'

#     def paginate_queryset(self, queryset, request, view=None):
#         # Convert the list to a queryset
#         story_ids = [story.id for story in queryset]
#         queryset = Story.objects.filter(id__in=story_ids)

#         print(f"Inside CenteredPagination.paginate_queryset with queryset type: {type(queryset)}")

#         try:
#             leading_story = queryset.get(slug=request.GET.get('story_slug'))
#             print(f"Found leading story with title: {leading_story.title}")
#         except Exception as e:
#             print(f"Error in CenteredPagination: {e}")
#             return []

#         if 'direction' in request.GET and request.GET['direction'] == 'previous':
#             queryset = queryset.filter(created_at__lte=leading_story.created_at).exclude(id=leading_story.id).order_by('-created_at')
#             queryset = queryset[:ANCESTORS_PER_PAGE]
#         else:
#             queryset = queryset.filter(created_at__gte=leading_story.created_at).exclude(id=leading_story.id).order_by('created_at')
#             queryset = queryset[:DESCENDANTS_PER_PAGE]

#         self.has_next = len(queryset) > self.page_size

#         return super().paginate_queryset(queryset, request, view)
    
#     def get_next_link(self):
#         # If you want to use the default behavior, you can just call the parent's method:
#         return super().get_next_link()

#         # If you want a custom implementation, replace the above line with your custom logic.



from rest_framework.pagination import CursorPagination

class CenteredPagination(CursorPagination):
    page_size_query_param = 'page_size'
    ordering = '-created_at'

    def paginate_queryset(self, queryset, request, view=None):
        # Convert the list to a queryset
        story_ids = [story.id for story in queryset]
        queryset = Story.objects.filter(id__in=story_ids)

        print(f"Inside CenteredPagination.paginate_queryset with queryset type: {type(queryset)}")

        try:
            leading_story = queryset.get(slug=request.GET.get('story_slug'))
            print(f"Found leading story with title: {leading_story.title}")
        except Exception as e:
            print(f"Error in CenteredPagination: {e}")
            return []

        if 'direction' in request.GET and request.GET['direction'] == 'previous':
            queryset = queryset.filter(created_at__lte=leading_story.created_at).exclude(id=leading_story.id).order_by('-created_at')
            queryset = queryset[:ANCESTORS_PER_PAGE]
        else:
            queryset = queryset.filter(created_at__gte=leading_story.created_at).exclude(id=leading_story.id).order_by('created_at')
            queryset = queryset[:DESCENDANTS_PER_PAGE]

        # Set has_next attribute
        self.has_next = len(queryset) > self.page_size

        # Return the sliced queryset directly
        return queryset
    
    def get_next_link(self):
        # If you want to use the default behavior, you can just call the parent's method:
        return super().get_next_link()

        # If you want a custom implementation, replace the above line with your custom logic.

# # stories/pagination.py

