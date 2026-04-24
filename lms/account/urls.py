from django.urls import path
from .views import logout_view, my_courses, verify_view, forgot_password_view, reset_password_view

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('my-courses/', my_courses, name='my_courses'),
    path('verify/<token>', verify_view, name='verify_view'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('reset-password/<token>/', reset_password_view, name='reset_password_view'),
]

