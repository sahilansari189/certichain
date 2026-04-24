from django.core.mail import send_mail
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

def send_contact_email_task(name, email, subject, message):
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
        return f"Email failed: {str(e)}"
