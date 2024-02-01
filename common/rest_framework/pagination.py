from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class for standard result sets.
    Attributes:
        page_size (int): Number of items per page.
        page_size_query_param (str): Query parameter to set the page size.
        max_page_size (int): Maximum number of items allowed per page.
        page_query_param (str): Query parameter to set the page number.
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500
    page_query_param = 'page'

    def get_paginated_response(self, data):
        """
        Custom method to format the paginated response.
        Args:
            data (list): The paginated data.
        Returns:
            dict: A dictionary containing paginated response information.
        """
        return {
            "page_size": self.page.paginator.per_page,
            "page": self.page.number,
            'total_pages': self.page.paginator.num_pages,
            "count": self.page.paginator.count,
            "results": data
        }
