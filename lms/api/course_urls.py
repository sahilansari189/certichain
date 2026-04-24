from django.urls import path
from course.api_views import course_list_api
from learning.api_views import get_modules_and_lessons

urlpatterns = [
    path('', course_list_api, name='course_list_api'),
    path('<slug>/modules-lessons/', get_modules_and_lessons, name='get_modules_and_lessons'),
]