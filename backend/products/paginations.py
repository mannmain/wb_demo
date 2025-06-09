from rest_framework.pagination import PageNumberPagination


class ColorVariantPagination(PageNumberPagination):
    page_size = 50
