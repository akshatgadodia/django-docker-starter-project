from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return {
            "page_size": self.page.paginator.per_page,
            "page": self.page.number,
            'total_pages': self.page.paginator.num_pages,
            "count": self.page.paginator.count,
            "results": data
        }
