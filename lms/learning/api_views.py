from course.models import Course,Module,Lesson,Enrollment
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from course.serializer import LessonSerializer,TrackingModulSerializer,LessonGradedQuestionsSerializer
from .models import LessionTracking, ModuleTracking
from utilities.paginate import SingleResultPaginator
from utilities.logger import logger
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

@api_view(['GET'],)
def get_modules_and_lessons(request, slug):
    '''
    This view is not currently in use of frontend. this is just noice for now 
    because there is no need to fetch the question from api.
    '''
    course = Course.objects.filter(slug=slug).first()
    if not course:
        return Response({"error": "Course not found"}, status=404)
    
    data = request.data
    l = data.get('l', None)
    if l:
        lesson = Lesson.objects.filter(id=l).first()
        if not lesson:
            return Response({"error": "Lesson not found"}, status=404)

        
        # return Response({"status": False, "message": "Lesson not found"}, status=404)
        lt = LessionTracking.objects.get_or_create(
            enrollment=lesson.module.course.enrollments.filter(user=request.user).first(),
            lesson=lesson,
            completed=True
        )

            # Check if all lessons in the module are completed
        all_lessons_completed = True
        for l in Lesson.objects.filter(module=lesson.module):
            if not LessionTracking.objects.filter(enrollment=lt.enrollment, lesson=l).exists():
                all_lessons_completed = False
                break
                # Update the module tracking status
        if all_lessons_completed:
            ModuleTracking.objects.create(
                enrollment=lt.enrollment,
                module=lesson.module,
                completed=True
            )
            # Check if all modules in the course are completed
        all_modules_completed = True 
        for m in Module.objects.filter(course=course):
            if not ModuleTracking.objects.filter(enrollment=lt.enrollment, module=m).exists():
                all_modules_completed = False
                break    
        if all_modules_completed:
            lt.enrollment.completed = True
            lt.enrollment.save() 
        return Response({
            "status": True,
            "message": "Lesson completed successfully",
            "data": LessonSerializer(lesson).data
            }, status=200)

    modules = Module.objects.filter(course=course).order_by('order')
    lessons = Lesson.objects.filter(module__in=modules).order_by('module__order')
    
    lessor_paginator = SingleResultPaginator()
    paginated_lessons = lessor_paginator.paginate_queryset(lessons, request)
    
    serialized_lessons = LessonSerializer(paginated_lessons, many=True).data

    return Response({
        "status": True,
        "message": "Modules and lessons fetched successfully",
        "data": lessor_paginator.get_paginated_response(serialized_lessons).data
        }, status=200)
    
@api_view(['GET'])
def get_module_tracking(request, course_uid):
    if request.user.is_authenticated:
        try:
            course = Course.objects.get(uid=course_uid)
            enrollment = Enrollment.objects.get(user=request.user, course=course)
        except Exception as e:
            logger.error(f"Enrollment error for course_uid: {course_uid}, error: {str(e)}")
            return Response({"status": False, "message": "User not enrolled in this course"}, status=403)
        try:
            modules = Module.objects.filter(course=course).order_by('order')
            module_serialized = TrackingModulSerializer(modules, many=True, context={'request': request}).data
            
            return Response({
                "status": True,
                "message": "Details fetched successfully",
                "serialized_modules": module_serialized,
                
            })
        except Exception as e:
            logger.error(f"Error calculating module tracking for course_uid: {course_uid}, user: {request.user}, error: {str(e)}")
            return Response({"status": False, "message": "Internal server error"}, status=500)
    else:
        return Response({"status": False, "message": "Authentication required"}, status=401)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lesson_graded_questions_detail(request, lesson_uid):
    """API to get graded questions details for a specific lesson"""
    try:
        lesson = get_object_or_404(Lesson, uid=lesson_uid)
        serializer = LessonGradedQuestionsSerializer(lesson, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_graded_questions_summary(request, course_uid):
    """API to get graded questions summary for all lessons in a course"""
    try:
        course = get_object_or_404(Course, uid=course_uid)
        lessons = Lesson.objects.filter(module__course=course)
        serializer = LessonGradedQuestionsSerializer(lessons, many=True, context={'request': request})
        
        # Calculate overall course statistics
        total_questions = sum(lesson['graded_questions_detail']['total_questions'] for lesson in serializer.data)
        completed_questions = sum(lesson['graded_questions_detail']['completed_questions'] for lesson in serializer.data)
        
        if total_questions > 0:
            overall_completion = (completed_questions / total_questions * 100)
            total_correct = sum(
                lesson['graded_questions_detail']['total_questions'] * lesson['graded_questions_detail']['average_score'] / 100 
                for lesson in serializer.data
            )
            overall_score = (total_correct / total_questions * 100) if total_questions > 0 else 0
        else:
            overall_completion = 0
            overall_score = 0
            
        response_data = {
            'course_uid': course_uid,
            'course_title': course.title,
            'overall_summary': {
                'total_questions': total_questions,
                'completed_questions': completed_questions,
                'completion_percentage': round(overall_completion, 2),
                'average_score': round(overall_score, 2),
                'passed': overall_score >= 70,
                'pass_threshold': 70
            },
            'lessons': serializer.data
        }
        
        return Response(response_data)
    except Exception as e:
        print(e)
        logger.error(f"Error fetching course graded questions summary for course_uid: {course_uid}, user: {request.user}, error: {str(e)}")
        return Response({'error': str(e)}, status=400)