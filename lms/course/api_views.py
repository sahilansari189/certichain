from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course
from .serializer import CourseSerializer

@api_view(['GET'])
def course_list_api(request):
    courses = Course.objects.all()
    if request.GET.get('languages'):
        languages = request.GET.get('languages').split(',')
        courses = courses.filter(language__code__in=languages)
    if request.GET.get('skills'):
        skills = request.GET.get('skills').split(',')
        courses = courses.filter(skills__name__in=skills)
    if request.GET.get('tiers'):
        tiers = str(request.GET.get('tiers')).split(',')
        courses = courses.filter(tier__name__in=tiers)
    if request.GET.get('difficulties'):
        difficulty_levels = request.GET.get('difficulties').split(',')
        courses = courses.filter(difficulty_level__level__in=difficulty_levels)
    if request.GET.get('offered_bys'):
        offered_bys = request.GET.get('offered_bys').split(',')
        courses = courses.filter(offered_by__organization_name__in=offered_bys)
    if request.GET.get('industries'):
        industries = request.GET.get('industries').split(',')
        courses = courses.filter(industry__name__in=industries)
    if request.GET.get('type') == 'courses':
        courses = courses.filter(course_type='course')
    serializer = CourseSerializer(courses, many=True)
    return Response({
        'status': 'success',
        'message': 'Courses retrieved successfully',
        'data': serializer.data
    })
    