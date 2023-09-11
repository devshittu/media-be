from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response
from core.settings import ANCESTORS_PER_PAGE, DESCENDANTS_PER_PAGE


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


class CenteredPagination(CursorPagination):
    page_size_query_param = 'page_size'
    ordering = '-created_at'  # Assuming each story has a 'created_at' timestamp

    def paginate_queryset(self, queryset, request, view=None):
        leading_story = queryset.get(slug=request.GET.get('story_slug'))

        if 'direction' in request.GET and request.GET['direction'] == 'previous':
            # Get ancestors based on configuration
            queryset = queryset.filter(created_at__lte=leading_story.created_at).exclude(id=leading_story.id).order_by('-created_at')[:ANCESTORS_PER_PAGE]
        else:
            # Get descendants based on configuration
            queryset = queryset.filter(created_at__gte=leading_story.created_at).exclude(id=leading_story.id).order_by('created_at')[:DESCENDANTS_PER_PAGE]

        return super().paginate_queryset(queryset, request, view)


# stories/pagination.py