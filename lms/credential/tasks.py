from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from datetime import datetime
logger = logging.getLogger(__name__)
from django.urls import reverse
from django.utils import timezone

@shared_task(bind=True, max_retries=3, default_retry_delay=10)  # 10s between retries
def send_certificate_email(self, protocol, domain, email, course_title, certificate_uid):
    certificate_url = reverse('certificate', args=[certificate_uid])
    try:
        subject = "Your Certificate is Ready!"
        context = {
            'url': f"{protocol}://{domain}{certificate_url}",
            'course_title': course_title,
            'current_year': timezone.now().year,
        }
        html_content = render_to_string('credential/certificate/cert_link_email.html', context)
        text_content = strip_tags(html_content)
        email_message = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [email]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()
        return True
    except Exception as exc:
        logger.error(f'Error in sending certificate email: {exc}')
        raise self.retry(exc=exc)
