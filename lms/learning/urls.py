from django.urls import path
from .views import learning_home,learning_progress,learning_modules,mark_lesson_completed,attempt_quesiton,start_exam,end_exam


urlpatterns = [
    path('<slug>/', learning_home, name='learning_home'),
    path('<slug>/progress', learning_progress, name='learning_progress'),
    path('<slug>/modules', learning_modules, name='learning_modules'),
    path('next/lesson/<lesson_uid>/', mark_lesson_completed, name='mark_lesson_completed'),
    path('attempt/question/', attempt_quesiton, name='attempt_quesiton'),
    path('<module_uid>/start_exam/', start_exam, name='start_exam'),
    path('<module_uid>/end_exam/', end_exam, name='end_exam'),
]