# from core.settings import ANCESTORS_PER_PAGE, DESCENDANTS_PER_PAGE
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CenteredPageNumberPagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        default_page_size = self.get_page_size(request)
        page_size = int(request.query_params.get("page_size", default_page_size))
        last_viewed_story_id = request.query_params.get("last_viewed_story_id", None)
        requested_page = request.query_params.get("page", None)

        # Ensure the queryset is ordered
        queryset = queryset.order_by("id")

        if requested_page:
            page_number = int(requested_page)
        elif last_viewed_story_id:
            try:
                # Find the index of the last viewed story in the queryset
                story_ids = list(queryset.order_by("id").values_list("id", flat=True))
                story_index = story_ids.index(int(last_viewed_story_id))

                # Calculate the page number to center the last viewed story
                half_page = page_size // 2
                page_number = max(1, (story_index - half_page) // page_size + 1)
            except (ValueError, IndexError):
                page_number = 1
        else:
            page_number = 1

        paginator = Paginator(queryset, page_size)
        try:
            self.page = paginator.page(page_number)
        except EmptyPage:
            self.page = paginator.page(paginator.num_pages)  # Last page

        return list(self.page)

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "results": data,
            }
        )


# stories/pagination.py

