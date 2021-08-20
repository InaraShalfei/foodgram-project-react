from rest_framework.pagination import PageNumberPagination


class PageNumberWithCustomLimitPagination(PageNumberPagination):
    page_size_query_param = 'limit'
