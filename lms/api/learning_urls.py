from django.urls import path
from learning.api_views import get_module_tracking
from learning.api_views import lesson_graded_questions_detail, course_graded_questions_summary

urlpatterns = [
    path('progress/<course_uid>/', get_module_tracking, name='get_module_tracking'),
    path('lesson/<lesson_uid>/graded-questions/', lesson_graded_questions_detail, name='lesson_graded_questions'),
    path('course/<course_uid>/graded-questions-summary/', course_graded_questions_summary, name='course_graded_questions_summary'),
]
