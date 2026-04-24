from course.models import Module, Lesson,  Course, Enrollment
from learning.models import LessionTracking
from django.shortcuts import redirect
import uuid
from django.contrib import messages

def get_lessons_of_course_module(course):
    modules = Module.objects.filter(course=course).order_by('order')
    lessons = Lesson.objects.filter(module__in=modules).order_by('module__order', 'order')
    return lessons

def get_queryset_uid_list(obj):
    return list(map(str, obj.values_list('uid', flat=True)))

def get_resume_lesson_uid(request,slug) -> str:
    course = Course.objects.filter(slug=slug).first()
    enrollment = course.enrollments.get(user=request.user)
    lessons = get_lessons_of_course_module(course)
    if not lessons.exists():
        return None
    pending_lessons = LessionTracking.objects.filter(lesson__in=lessons,enrollment=enrollment, completed=False)
    if pending_lessons.exists():
        return str(pending_lessons.first().lesson.uid)
    for i in range (len(lessons)):
        track = LessionTracking.objects.filter(enrollment=enrollment,lesson=lessons[i])
        if not track.exists():
            LessionTracking.objects.create(enrollment=enrollment, lesson=lessons[i])
            return str(lessons[i].uid)
    messages.success(request, 'All lessons are completed.')
    return lessons[0].uid

def check_enrollment(request,course):
    if not request.user.is_authenticated or not Enrollment.objects.filter(user=request.user, course=course).exists():
        return False
    return True

def check_valid_uuid(uid):
    try:
        uuid.UUID(uid)
        return True
    except ValueError:
        return False
