from django.db import models
from base.models import BaseModel
from course.models import Enrollment, Course
from django.contrib.auth.models import User
# Create your models here.

class Certificate(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username + " - " + self.course.title

class Badge(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='badges/')
    description = models.TextField(null=True, blank=True)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='badge')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'

class StudentBadge(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_badges')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='student_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='student_badges')

    def __str__(self):
        return self.user.username + " - " + self.badge.name
    
    class Meta:
        verbose_name = 'Student Badge'
        verbose_name_plural = 'Student Badges'
        unique_together = ('enrollment', 'badge')

