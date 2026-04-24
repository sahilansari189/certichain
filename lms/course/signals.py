from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Enrollment
from account.tasks import got_enrollment_access_email
from django.urls import reverse

# Enrollment model signals
@receiver(post_save, sender=Enrollment)
def increase_enrollment_count(sender, instance, created, **kwargs):
    if created:
        instance.course.enrolled_count += 1
        instance.course.save()

@receiver(post_delete, sender=Enrollment)
def decrease_enrollment_count(sender, instance, **kwargs):
    instance.course.enrolled_count -= 1
    instance.course.save()
    
    
# Course model signals

# Module model signals