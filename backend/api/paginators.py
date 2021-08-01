from rest_framework.pagination import PageNumberPagination


class TagsPagination(PageNumberPagination):
    page_size = 0
