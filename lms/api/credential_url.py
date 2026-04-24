from django.urls import path
from credential.api_views import request_certificate, CertificateStatus, claim_badge,badge_status

urlpatterns = [
    path('certificate/request/<course_uid>/', request_certificate, name='request_certificate'),
    path('certificate/status/<course_uid>/', CertificateStatus, name='certificate_status'),
    path('badge/claim/<course_uid>/', claim_badge, name='claim_badge'),
    path('badge/status/<course_uid>/', badge_status, name='badge_status'),
]
