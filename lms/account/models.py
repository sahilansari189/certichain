from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from course.models import Course
from .choices import BULK_ALLOWED_EMAIL_STATUS
import pandas as pd
from django.utils import timezone
from account.tasks import got_enrollment_access_email
import logging
logger = logging.getLogger(__name__)
from django.urls import reverse

# Create your models here.

class UserInfo(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')
    is_verified = models.BooleanField(default=True)
    verification_code = models.CharField(max_length=100, null=True, blank=True)
    verification_code_created_at = models.DateTimeField(null=True, blank=True)
    verification_code_expires_at = models.DateTimeField(null=True, blank=True)
    verification_code_used_at = models.DateTimeField(null=True, blank=True)
    
    # Password Reset Fields
    password_reset_token = models.CharField(max_length=100, null=True, blank=True)
    password_reset_token_created_at = models.DateTimeField(null=True, blank=True)
    password_reset_token_expires_at = models.DateTimeField(null=True, blank=True)
    password_reset_token_used_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()
    
class AllowedEmail(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='allowed_emails')
    is_allowed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email


class BulkAllowedEmail(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='bulk_allowed_emails')
    file = models.FileField(upload_to='bulk_allowed_emails')
    is_processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_status = models.CharField(max_length=100, choices=BULK_ALLOWED_EMAIL_STATUS, default='pending')    
    log = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.course.title

    def save(self, *args, **kwargs):
        if self.is_processed:
            return
        else:
            if self.file:
                self.create_allowed_emails()
        super().save(*args, **kwargs)
    
    def create_allowed_emails(self):
        try:
            df = pd.read_excel(self.file)
        except Exception as e:
            self.log = f"Error reading file: {e}"
            self.save()
            logger.error(f"Error reading file: {e}")
            return False
        emails = []
        for index, row in df.iterrows():
            email = row['Email Id']
            name = row['Name']
            course = row['Course']

            try:
                course = Course.objects.get(code=course)
            except Exception as e:
                logger.error(f"Error creating allowed email: {e}")
                print(e)
                return False
            emails.append(email)
            allowed_email, created = AllowedEmail.objects.get_or_create(email=email,course=course)
            allowed_email.is_allowed = True
            allowed_email.save()

            if not created:
                print(f"Email {email} already exists")
                logger.info(f"Email {email} already exists")
            else:
                print(f"Email {email} created successfully")
                logger.info(f"Email {email} created successfully")

        self.is_processed = True
        self.processed_at = timezone.now()
        self.processed_status = 'completed'
        self.save()

        course_url = reverse('register')
        url = 'https://sv.allswiftsolutions.in'

        got_enrollment_access_email.delay(
            email=emails,
            course_name=course.title,
            course_url=f'{url}{course_url}',
        )
        logger.info(f'Allowed Email Created: {email}')
        return True