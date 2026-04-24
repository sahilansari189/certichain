from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from datetime import datetime
logger = logging.getLogger(__name__)
from django.urls import reverse

def send_user_verification_email(protocol, domain, email, token):
    url = reverse('verify_view', args=[token])
    try:
        send_mail(
            "Verify CertiChain Account!",
            f"Please verify your CertiChain account by clicking this link {protocol}://{domain}{url}.",
            settings.EMAIL_HOST_USER,
            [email]
        )
        return True
    except Exception as exc:
        logger.error(f'Error in sending verification email: {exc}')

def send_password_reset_email(protocol, domain, email, token):
    url = reverse('reset_password_view', args=[token])
    try:
        send_mail(
            "Reset Your CertiChain Password",
            f"Click this link to reset your CertiChain password: {protocol}://{domain}{url}. This link will expire in 30 minutes.",
            settings.EMAIL_HOST_USER,
            [email]
        )
        return True
    except Exception as exc:
        logger.error(f'Error in sending password reset email: {exc}')

def got_enrollment_access_email(email, course_name, course_url):
    try:
        context = {
            'course_name': course_name,
            'course_url': course_url,
            'contact_email': 'support@certichain.io',
            'current_year': datetime.now().year,
        }
        html_content = render_to_string('account/emails/enrollment_email.html', context)
        text_content = strip_tags(html_content)
        email_message = EmailMultiAlternatives(
            subject=f"You have been invited to {course_name}",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=email
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()
        return True
    except Exception as exc:
        logger.error(f'Error in sending enrollment access email: {exc}')
    
def send_user_email_verification(protocol, domain, email, token):
    url = reverse('verify_view', args=[token])
    try:
        context = {
            'url': f'{protocol}://{domain}{url}',
            'current_year': datetime.now().year,
        }
        html_content = render_to_string('account/emails/user_verification.html', context)
        text_content = strip_tags(html_content)
        email_message = EmailMultiAlternatives(
            subject="Verify CertiChain Account!",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[email]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()
        return True
    except Exception as exc:
        logger.error(f'Error in sending verification email: {exc}')
