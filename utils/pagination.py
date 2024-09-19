from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, PAGE_SIZE_QUERY_PARAM


import logging

logger = logging.getLogger("app_logger")


class CustomPageNumberPagination(PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM
    max_page_size = MAX_PAGE_SIZE

    def paginate_queryset(self, queryset, request, view=None):
        """
        Override to add logging for better debugging.
        """
        logger.debug(f"Paginating queryset with {len(queryset)} items.")
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        response_data = {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
        }
        logger.debug(f"Paginated Response: {response_data}")
        return Response(response_data)


# utils/pagination.py
