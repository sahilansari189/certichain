from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from .models import User,UserInfo, AllowedEmail
from account.tasks import got_enrollment_access_email
import logging
logger = logging.getLogger(__name__)
# User model signals
@receiver(post_save, sender=User)
def create_user_extra_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.get_or_create(user=instance)
        logger.info('User Extra Info Created')


@receiver(post_save, sender=AllowedEmail)
def create_user_extra_info(sender, instance, created, **kwargs):
    if created:
        logger.info('Allowed Email Created')
        course_url = reverse('register')
        url = 'https://certichain.io'
        got_enrollment_access_email(
            email=instance.email,
            course_name=instance.course.title,
            course_url=f'{url}{course_url}',
        )
        logger.info(f'Allowed Email Created: {instance.email}')


