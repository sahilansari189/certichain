from course.models import Course,Enrollment
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Certificate, Badge, StudentBadge
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .tasks import send_certificate_email

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CertificateStatus(request, course_uid):
    '''
    API view to check if the authenticated user has a certificate for the given course.
    '''
    user = request.user
    course = get_object_or_404(Course, uid=course_uid)
    certificate = Certificate.objects.filter(user=user, course=course).first()
    
    if certificate:
        certificate_url = reverse('certificate', args=[certificate.uid])
        return Response({
            'status': True,
            'message': 'Certificate exists',
            'data': {
                'exists': True,
                'certificate_url': request.build_absolute_uri(certificate_url)
            },
            
        })
    else:
        return Response({
            'status': False,
            'message': 'No certificate found',
            'data': {
                'has_certificate': False
            },
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_certificate(request, course_uid):
    '''
    API view to create a certificate for the authenticated user.
    '''
    user = request.user
    course = get_object_or_404(Course, uid=course_uid)
    enrollment = get_object_or_404(Enrollment, user=user, course=course)
    
    # Check if certificate already exists
    existing_cert = Certificate.objects.filter(user=user, course=course).first()
    if existing_cert:
        certificate_url = reverse('certificate', args=[existing_cert.uid])
        return Response({
            'status': True,
            'data': {
                'certificate_url': request.build_absolute_uri(certificate_url)
            },
            'message': 'Certificate already exists'
        })
    
    # Create new certificate
    certificate = Certificate.objects.create(
        user=user,
        enrollment=enrollment,
        course=course
    )
    print(user.email)
    send_certificate_email.delay(  
        protocol=request.scheme,
        domain=request.get_host(),
        email=user.email,
        course_title=course.title,
        certificate_uid=certificate.uid
    )

    certificate_url = reverse('certificate', args=[certificate.uid])
    return Response({
        'status': True,
        'data': {
            'certificate_url': request.build_absolute_uri(certificate_url)
        },
        'message': 'Certificate created successfully'
    })
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def claim_badge(request, course_uid):
    '''
    API view to create a badge for the authenticated user.
    '''
    user = request.user
    course = get_object_or_404(Course, uid=course_uid)
    enrollment = get_object_or_404(Enrollment, user=user, course=course)
    
    # 1. Ensure Badge exists for the course
    badge, created = Badge.objects.get_or_create(
        course=course,
        defaults={
            'name': f"{course.title} Completion Badge",
            'description': f"Awarded for completing {course.title}",
        }
    )
    
    # Check if StudentBadge already exists
    existing_student_badge = StudentBadge.objects.filter(user=user, badge=badge).first()
    if existing_student_badge:
        return Response({
            'status': True,
            'data': {
                'badge_url': reverse('badge', args=[existing_student_badge.uid])
            },
            'message': 'Badge already claimed'
        })
    
    # Create StudentBadge
    student_badge = StudentBadge.objects.create(
        user=user,
        enrollment=enrollment,
        badge=badge
    )
    
    return Response({
        'status': True,
        'data': {
            'badge_url': reverse('badge', args=[student_badge.uid])
        },
        'message': 'Badge claimed successfully'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def badge_status(request, course_uid):
    '''
    API view to check if the authenticated user has a badge for the given course.
    '''
    user = request.user
    course = get_object_or_404(Course, uid=course_uid)
    badge = Badge.objects.filter(course=course).first()
    student_badge = StudentBadge.objects.filter(user=user, badge=badge).first()
    
    if student_badge:
        badge_url = reverse('badge', args=[student_badge.uid])
        return Response({
            'status': True,
            'data': {
                'badge_url': request.build_absolute_uri(badge_url)
            },
            'message': 'Badge exists'
        })
    else:
        return Response({
            'status': False,
            'data': {
                'has_badge': False
            },
            'message': 'No badge found'
        })

