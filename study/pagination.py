from rest_framework.pagination import PageNumberPagination


class CourseAndLessonPagination(PageNumberPagination):
    """Пагинатор для страниц курсов и уроков"""
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 50
