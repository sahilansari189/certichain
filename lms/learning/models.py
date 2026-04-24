from django.db import models
from base.models import BaseModel
from course.models import Course, Module, Enrollment,Lesson
from django.db import models
import logging
logger = logging.getLogger(__name__)
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class LessionTracking(BaseModel):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('enrollment', 'lesson')
    
    def __str__(self):
        return f"{self.enrollment.user.username} - {self.lesson.title} - {self.completed}"

class ModuleTracking(BaseModel):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    is_final_exam = models.BooleanField(default=False)
    final_exam_started = models.BooleanField(default=False)
    final_exam_started_at = models.DateTimeField(null=True, blank=True)
    final_exam_completed = models.BooleanField(default=False)
    final_exam_completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('enrollment', 'module')
    
    def __str__(self):
        return f"{self.enrollment.user.username} - {self.module.title}"

    def save(self, *args, **kwargs):
        if self.module.is_final_exam:
            self.is_final_exam = True
        super().save(*args, **kwargs)

    def start_final_exam(self):
        try:
            self.final_exam_started = True
            self.final_exam_started_at = timezone.now()
            self.save()
            return True
        except Exception as e:
            logger.error(f"Error starting final exam: {str(e)}")
            return False

    def get_final_exam_time_left(self):
        if self.final_exam_started:
            duration_seconds = self.module.final_exam_time * 60
            elapsed_seconds = (timezone.now() - self.final_exam_started_at).total_seconds()
            remaining_seconds = max(0, duration_seconds - int(elapsed_seconds))
            time_left = str(timedelta(seconds=remaining_seconds))
            return time_left[2:]
        return None

    def get_final_exam_duration_in_seconds(self):
        if self.final_exam_started:
            duration_seconds = self.module.final_exam_time * 60
            return duration_seconds
        return None

    def get_final_exam_time_left_seconds(self):
        if self.final_exam_started and not self.final_exam_completed:
            duration_seconds = self.module.final_exam_time * 60
            elapsed_seconds = (timezone.now() - self.final_exam_started_at).total_seconds()
            remaining_seconds = max(0, duration_seconds - int(elapsed_seconds))
            return remaining_seconds
        return None

    def end_final_exam(self):
        try:
            self.final_exam_completed = True
            self.final_exam_completed_at = timezone.now()
            self.save()
            return True
        except Exception as e:
            logger.error(f"Error ending final exam: {str(e)}")
            return False