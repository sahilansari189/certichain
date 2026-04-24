from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from datetime import datetime
logger = logging.getLogger(__name__)
from django.urls import reverse

@shared_task(bind=True, max_retries=3, default_retry_delay=10)  # 10s between retries
def send_user_verification_email(self, protocol, domain, email, token):
    url = reverse('verify_view', args=[token])
    try:
        send_mail(
            "Verify SkillVerse Account!",
            f"Please verify your SkillVerse account by clicking this link {protocol}://{domain}{url}.",
            settings.EMAIL_HOST_USER,
            [email]
        )
        return True
    except Exception as exc:
        logger.error(f'Error in sending verification email: {exc}')
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_password_reset_email(self, protocol, domain, email, token):
    url = reverse('reset_password_view', args=[token])
    try:
        send_mail(
            "Reset Your SkillVerse Password",
            f"Click this link to reset your SkillVerse password: {protocol}://{domain}{url}. This link will expire in 30 minutes.",
            settings.EMAIL_HOST_USER,
            [email]
        )
        return True
    except Exception as exc:
        logger.error(f'Error in sending password reset email: {exc}')
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def got_enrollment_access_email(self, email, course_name, course_url):
    try:
        # Prepare context for the email template
        context = {
            'course_name': course_name,
            'course_url': course_url,
            'contact_email': 'support@allswiftsolutions.in',
            'current_year': datetime.now().year,
        }
        
        # Render HTML email
        html_content = render_to_string('account/emails/enrollment_email.html', context)
        
        # Create plain text version by stripping HTML tags
        text_content = strip_tags(html_content)
        
        # Create email with both HTML and plain text versions
        email_message = EmailMultiAlternatives(
            subject=f"You have been invited to {course_name}",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=email
        )
        
        # Attach HTML content
        email_message.attach_alternative(html_content, "text/html")
        
        # Send email
        email_message.send()
        
        return True
    except Exception as exc:
        logger.error(f'Error in sending enrollment access email: {exc}')
        raise self.retry(exc=exc)
    
@shared_task(bind=True, max_retries=3, default_retry_delay=10)  # 10s between retries
def send_user_email_verification(self, protocol, domain, email, token):
    url = reverse('verify_view', args=[token])
    try:
        context = {
            'url': f'{protocol}://{domain}{url}',
            'current_year': datetime.now().year,
        }
        html_content = render_to_string('account/emails/user_verification.html', context)
        text_content = strip_tags(html_content)
        email_message = EmailMultiAlternatives(
            subject="Verify SkillVerse Account!",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[email]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()
        return True
    except Exception as exc:
        logger.error(f'Error in sending verification email: {exc}')
        raise self.retry(exc=exc)