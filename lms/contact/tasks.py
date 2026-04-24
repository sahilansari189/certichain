from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging
logger = logging.getLogger(__name__)
from django.urls import reverse

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_contact_email_task(self, name, email, subject, message):
    try:    
        full_subject = f"New Contact Request: {subject}"
        body = f"""
        You have received a new message from the Contact Us form.

        Name: {name}
        Email: {email}
        Subject: {subject}

        Message:
        {message}
        """
        send_mail(
            subject=full_subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.RECIPIENT_EMAIL,
            fail_silently=False,
        )
        logger.info(f"Contact email sent successfully for {email}")
        return "Email sent"
    except Exception as e:
        logger.error(f"Failed to send contact email: {str(e)}")
        self.retry(exc=e, countdown=10)
        return f"Email failed: {str(e)}"


