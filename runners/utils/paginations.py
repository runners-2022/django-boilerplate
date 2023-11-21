from django.http import JsonResponse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import InvalidPage


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)
        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            return []
        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True
        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        if len(data) == 0:
            count = 0
            next = None
            previous = None
        else:
            count = self.page.paginator.count
            next = self.get_next_link()
            previous = self.get_previous_link()

        return JsonResponse({'code': 200,
                             'message': 'ok',
                             'count': count,
                             'next': next,
                             'previous': previous,
                             'data': data},
                            status=status.HTTP_200_OK)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 10000
