from rest_framework.pagination import CursorPagination, PageNumberPagination


class CursorPaginator(CursorPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    ordering = 'order'
    
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = 'order'

class SingleResultPaginator(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1
    ordering = 'order'

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50
    ordering = 'order'
