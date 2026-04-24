from django.shortcuts import render
from .models import Certificate, Badge, StudentBadge
from utilities.utils import generate_certificate_linkedin_url, generate_qr_code_base64
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.

@login_required(login_url='login')
def certificates(request):
    certificates = Certificate.objects.filter(user=request.user)
    return render(request, 'credential/certificate/certificates.html', {'certificates': certificates})

def certificate(request, uid):
    certificate = Certificate.objects.get(uid=uid)

    protocol = request.scheme
    domain = request.get_host()

    certificate_url = f"{protocol}://{domain}{reverse('certificate', args=[certificate.uid])}"
    linkedin_url = generate_certificate_linkedin_url(certificate, certificate_url)
    qr_code = generate_qr_code_base64(certificate_url)
    course = certificate.enrollment.course
    data = {
        'certificate': certificate,
        'linkedin_url': linkedin_url,
        'certificate_url': certificate_url,
        'qr_code': qr_code,
        'course': course,
    }
    return render(request, 'credential/certificate/certificate_page.html', data)

@login_required(login_url='login')
def badges(request):
    badges = StudentBadge.objects.filter(user=request.user)
    return render(request, 'credential/badge/badges.html', {'badges': badges})

def badge(request, uid):
    student_badge = StudentBadge.objects.get(uid=uid)
    badge_url = reverse('badge', args=[student_badge.uid])
    return render(request, 'credential/badge/badge_page.html', {'badge': student_badge, })


# ─────────────────────────────────────────────
# NFT CertiChain Views (Blockchain Certificates)
# ─────────────────────────────────────────────

@login_required(login_url='login')
def nft_mint(request):
    """
    Issue a blockchain NFT certificate (teacher/admin facing).
    Pre-fills student info from query params if available.
    """
    student_name = request.GET.get('student_name', '')
    student_email = request.GET.get('student_email', '')
    course_title = request.GET.get('course_title', '')

    context = {
        'student_name': student_name,
        'student_email': student_email,
        'course_title': course_title,
        'emailjs_service_id': settings.EMAILJS_SERVICE_ID,
        'emailjs_template_id': settings.EMAILJS_TEMPLATE_ID,
        'emailjs_public_key': settings.EMAILJS_PUBLIC_KEY,
    }
    return render(request, 'credential/certificate/nft_mint.html', context)


def nft_verify(request):
    """
    Verify a blockchain NFT certificate (public facing).
    Can auto-verify if token_id is passed as a query param.
    """
    prefill_token_id = request.GET.get('token_id', '')

    context = {
        'prefill_token_id': prefill_token_id,
        'imgbb_key': settings.IMGBB_KEY,
    }
    return render(request, 'credential/certificate/nft_verify.html', context)