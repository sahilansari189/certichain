from django.urls import path
from .views import  create_enrollment,course_list,course_detail

urlpatterns = [
    path('', course_list, name='course_list'),
    path('<slug:slug>/', course_detail, name='course_detail'),
    path('<slug:slug>/enroll/', create_enrollment, name='create_enrollment'),

]

