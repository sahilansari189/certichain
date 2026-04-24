from django.shortcuts import render,redirect, get_object_or_404
from .models import Course,Skill,Tier,DifficultyLevel,Language,OfferedBy,Industry
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CourseSerializer
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import AllowedEmail

# Create your views here.
def course_list(request):
    course_type = request.GET.get('type', 'all')
    
    if course_type == 'courses':
        courses = Course.objects.filter(course_type='course')
    elif course_type == 'guided_projects':
        courses = Course.objects.filter(course_type='guided_project')
    else:
        courses = Course.objects.all()

    # Count for tabs
    all_count = Course.objects.count()
    courses_count = Course.objects.filter(course_type='course').count()
    guided_projects_count = Course.objects.filter(course_type='guided_project').count()
    
    skills = Skill.objects.all()
    tiers = Tier.objects.all()
    difficulty_levels = DifficultyLevel.objects.all()
    languages = Language.objects.all()
    offered_bys = OfferedBy.objects.all()
    industries = Industry.objects.all()
    
    context = {
        'courses': courses,
        'current_type': course_type,
        'all_count': all_count,
        'courses_count': courses_count,
        'guided_projects_count': guided_projects_count,
        'skills': skills,
        'tiers': tiers,
        'difficulty_levels': difficulty_levels,
        'languages': languages,
        'offered_bys': offered_bys,
        'industries': industries
    }
    return render(request, 'course/course_list.html', context)
    
def course_detail(request, slug):
    course =get_object_or_404(Course, slug=slug)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = course.enrollments.filter(user=request.user).exists()
    context = {
        'course': course,
        'is_enrolled': is_enrolled
    }
    return render(request, 'course/course_detail.html', context)

@login_required(login_url='login')
def create_enrollment(request,slug):
    course = Course.objects.filter(slug=slug).first()
    if request.method == 'POST':
        if AllowedEmail.objects.filter(email=request.user.email,course=course, is_allowed=True).exists():
            course.enrollments.create(user=request.user)
            messages.success(request, 'You have successfully enrolled in the course.')
            return redirect('learning_home', slug=slug)
        messages.error(request, 'You are not allowed to enroll in this course.')
        return redirect('course_detail', slug=slug)
    
    messages.error(request, "Method not allowed")
    return redirect('course_detail', slug=slug)

