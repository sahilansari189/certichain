from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
logger = logging.getLogger(__name__)
from django.utils import timezone

ADMIN_EMAIL = 'sahilsa7807887@gmail.com'
GOOGLE_FORM_URL = 'https://forms.gle/2iEQREU8JLkZJZS46'

def send_certificate_email(protocol, domain, email, course_title, certificate_uid):
    try:
        subject = "Your Certificate Request — CertiChain"
        context = {
            'url': GOOGLE_FORM_URL,
            'course_title': course_title,
            'current_year': timezone.now().year,
        }
        html_content = render_to_string('credential/certificate/cert_link_email.html', context)
        text_content = strip_tags(html_content)

        # Send to the user
        user_email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [email]
        )
        user_email.attach_alternative(html_content, "text/html")
        user_email.send()

        # Send notification to admin
        admin_subject = f"[CertiChain] Certificate Request: {course_title}"
        admin_body = f"""New certificate request received.

Student Email: {email}
Course: {course_title}
Certificate ID: {certificate_uid}
Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

Issue the certificate at: https://certichain-smoky.vercel.app/
"""
        send_mail(
            admin_subject,
            admin_body,
            settings.EMAIL_HOST_USER,
            [ADMIN_EMAIL],
            fail_silently=True,
        )

        logger.info(f'Certificate email sent to {email} and admin for course {course_title}')
        return True
    except Exception as exc:
        logger.error(f'Error in sending certificate email: {exc}')
