from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from course.models import Course,Module,Lesson
from exam.models import Question,Option,AttemptQuestion
from account.models import AllowedEmail
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from course.serializer import ModuleSerializer, LessonSerializer
from django.contrib.auth.decorators import login_required
from .models import LessionTracking, ModuleTracking
from utilities.paginate import SingleResultPaginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from .utils import get_lessons_of_course_module,get_queryset_uid_list,get_resume_lesson_uid,check_enrollment,check_valid_uuid
import logging
logger = logging.getLogger(__name__)
# Create your views here.

NONES = ['None', 'none', 'null', 'NULL', None, '']

@login_required
def learning_home(request, slug):
    course = Course.objects.filter(slug=slug).first()
    try:
        enrollment = course.enrollments.get(user=request.user)
    except Exception as e:
        print(e)
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('course_list')
    modules = Module.objects.filter(course=course).order_by('order')
    
    enrollment = None
    if request.user.is_authenticated:
        enrollment = course.enrollments.filter(user=request.user).first()
    context = {
        'course': course,
        'modules': modules,
        'enrollment' : enrollment,
        'resume' : get_resume_lesson_uid(request, slug)
    }
    return render(request, 'learning/detail.html', context)

@login_required
def learning_progress(request, slug):
    course = get_object_or_404(Course, slug=slug)
    try:
        enrollment = course.enrollments.get(user=request.user)
    except Exception as e:
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('course_list')
    context = {
        'course': course
    }
    return render(request, 'learning/course_dashboard_progress.html', context)

@login_required
def learning_modules(request, slug):
    
    course = Course.objects.filter(slug=slug).first()
    try:
        enrollment = course.enrollments.get(user=request.user)
    except Exception as e:
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('course_list')
    
    current = request.GET.get('l')
    
    lesson_uids = get_queryset_uid_list(get_lessons_of_course_module(course))
    context = {
        'prev' : None,
        'next' : None,
    }

    if current not in NONES:
        if not enrollment.started:
            enrollment.started = True
            enrollment.save()
        try:
            current_index = lesson_uids.index(current)
        except Exception as e:
            messages.error(request, 'Invalid lesson.')
            logger.error(e)
            return redirect('learning_home', slug=slug)
    else:
        current=get_resume_lesson_uid(request, slug)
        if current in NONES:
            messages.success(request, 'Course completed successfully.')
            return redirect('learning_home', slug=slug)
        try:
            current_index = lesson_uids.index(current)
        except Exception as e:
            messages.error(request, 'Invalid lesson.')
            logger.error(e)
            return redirect('learning_home', slug=slug)
        
    if current_index > 0:
            context['prev'] = lesson_uids[current_index - 1]
    if current_index < len(lesson_uids) - 1:
            context['next'] = lesson_uids[current_index + 1]
            
    lesson = Lesson.objects.get(uid=current)
    track , _ = LessionTracking.objects.get_or_create(enrollment=enrollment, lesson=lesson)
    module_tracking = None
    if lesson.module.is_final_exam:
        # if lesson.module.final_exam_started:
        #     duration_seconds = lesson.module.final_exam_time * 60
        #     elapsed_seconds = (timezone.now() - lesson.module.final_exam_started_at).total_seconds()
        #     remaining_seconds = max(0, duration_seconds - int(elapsed_seconds))
        #     time_left = str(timedelta(seconds=remaining_seconds))
        #     context['time_left'] = time_left[2:]
        #     context["total_time"] = duration_seconds
        #     context["time_remaining"] = remaining_seconds

        module_tracking , _ = ModuleTracking.objects.get_or_create(enrollment=enrollment, module=lesson.module)     
        if module_tracking.final_exam_started:
            context['time_left'] = module_tracking.get_final_exam_time_left()
            context["total_time"] = module_tracking.get_final_exam_duration_in_seconds()
            context["time_remaining"] = module_tracking.get_final_exam_time_left_seconds()

    context['course'] = course
    context['lesson'] = lesson
    context['completed'] = track.completed
    context['module_tracking'] = module_tracking

    return render(request, 'learning/module.html', context)

@login_required
def mark_lesson_completed(request,lesson_uid):
    
    if request.method == 'POST':
        lesson = Lesson.objects.get(uid=lesson_uid)
        try:
            enrollment = lesson.module.course.enrollments.get(user=request.user)
        except Exception as e:
            messages.error(request, 'You are not enrolled in this course.')
            return redirect('course_list')
        
        nxt = request.POST.get('nxt', None)
        lesson_track,_ = LessionTracking.objects.get_or_create(enrollment=enrollment, lesson=lesson)
        lesson_track.completed = True
        lesson_track.save()
        print('mark lesson completed')
        
            
        lesson_module = lesson.module.lessons.all()
        print(lesson_module.count() , LessionTracking.objects.filter(enrollment=enrollment, lesson__module=lesson.module,completed=True).count())
        if lesson_module.count() == LessionTracking.objects.filter(enrollment=enrollment, lesson__module=lesson.module,completed=True).count():
            track , __ = ModuleTracking.objects.get_or_create(enrollment=enrollment, module=lesson.module)
            track.completed = True
            track.save()
            print('mark module completed')
        
        url = reverse('learning_modules', kwargs={'slug': lesson.module.course.slug})

        if nxt not in NONES:
            print("next lesson uid : " , nxt)
            return redirect(f'{url}?l={nxt if nxt else ''}')
        else:   
            resume_uid = get_resume_lesson_uid(request, lesson.module.course.slug)
            if resume_uid not in NONES:
                return redirect(f'{url}?l={resume_uid}')
            else:
                messages.success(request, 'Course completed successfully.')
                return redirect('learning_home', slug=lesson.module.course.slug)
    else:
        messages.error(request, 'Method not allowed')
        return redirect('home')
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def attempt_quesiton(request):
    data = request.data
    
    course_uid = data.get('c')
    course = Course.objects.get(uid=course_uid) 
    
    # Returns true or false on the basis of the enrollment status of the user 
    if check_enrollment(request,course): 
    
        question_uid = data.get('q')
        option_uid = data.get('o')
        user = request.user

        question = Question.objects.get(uid=question_uid) 
        option = Option.objects.get(uid=option_uid) 
        
        
        # Calculate score based on attempts
        previous_attempts = AttemptQuestion.objects.filter(user=user, question=question).count()
        score = 0
        if option.is_correct:
            if previous_attempts == 0:
                score = 1
            elif previous_attempts == 1:
                score = 0.5
            else:
                score = 0
        
        attempt = AttemptQuestion.objects.create(user=user,question=question,option=option, score=score)

        return Response({
            'status' : True,
            'message' : 'question attempted',
            'data' : {
                'is_correct' : option.is_correct,
                'attempts' : attempt.attempts(user , question)
            }
        })
    else:
        return Response({
            'status' : False,
            'message' : 'You are not enrolled in this course',
            'data' : {}
        })
        

@login_required
def start_exam(request, module_uid):
    try:
        module = Module.objects.get(uid=module_uid)
        enrollment = module.course.enrollments.get(user=request.user)
        module_tracking = ModuleTracking.objects.get(enrollment=enrollment, module=module)
    except Exception as e:
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('course_list')
    
    if request.method == 'POST':
        if not module_tracking.final_exam_started:
            started = module_tracking.start_final_exam()
            if started:
                messages.success(request, "Exam started sucessfully")
            else:
                messages.error(request, "Error starting exam")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "Method not allowed")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required
def end_exam(request, module_uid):
    try:
        module = Module.objects.get(uid=module_uid)
        enrollment = module.course.enrollments.get(user=request.user)
        module_tracking = ModuleTracking.objects.get(enrollment=enrollment, module=module)
    except Exception as e:
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('course_list')
    if module_tracking.final_exam_started:
        module_tracking.end_final_exam()
        
        current = request.GET.get('l')
        lesson = Lesson.objects.get(uid=current)
        
        lesson_track,_ = LessionTracking.objects.get_or_create(enrollment=enrollment, lesson=lesson)
        lesson_track.completed = True
        lesson_track.save()
        print('final exam lesson and  module completed')
        
        messages.success(request, 'Exam completed successfully.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

