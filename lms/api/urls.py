from django.urls import path, include
from learning.api_views import get_module_tracking

urlpatterns = [
    path('courses/', include('api.course_urls')),
    path('learning/', include('api.learning_urls')),
    path('credentials/', include('api.credential_url')),
]