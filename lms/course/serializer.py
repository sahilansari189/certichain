from rest_framework.serializers import ModelSerializer
from .models import Course, Skill, DifficultyLevel, Language, OfferedBy, Industry, Tier, Module, Lesson
from learning.models import LessionTracking
from  exam.serializer import QuestionSerializer
from rest_framework import serializers
from exam.models import AttemptQuestion

class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name', 'description']
        
class DifficultyLevelSerializer(ModelSerializer):
    class Meta:
        model = DifficultyLevel
        fields = ['level', 'description']
        
class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = ['name', 'code']
        
class OfferedBySerializer(ModelSerializer):
    class Meta:
        model = OfferedBy
        fields = ['organization_name', 'website']
        
class IndustrySerializer(ModelSerializer):
    class Meta:
        model = Industry
        fields = ['name', 'description']
        
class TierSerializer(ModelSerializer):
    class Meta:
        model = Tier
        fields = ['name', 'benefits']
        

class CourseSerializer(ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    difficulty_level = DifficultyLevelSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    offered_by = OfferedBySerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)
    tier = TierSerializer(read_only=True)
    class Meta:
        model = Course
        fields = '__all__'
        
class LessonSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    graded_questions_detail = serializers.SerializerMethodField()
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'order','module_name','module_title','questions', 'graded_questions_detail']
        
    def get_graded_questions_detail(self, obj):
        """Get graded questions details for this lesson"""
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        
        if not user or not user.is_authenticated:
            return {
                "total_questions": 0,
                "completed_questions": 0,
                "correct_answers": 0,
                "completion_percentage": 0,
                "average_score": 0,
                "passed": False,
                "pass_threshold": 70
            }
            
        total_questions = obj.questions.count()
        
        if total_questions == 0:
            return {
                "total_questions": 0,
                "completed_questions": 0,
                "correct_answers": 0,
                "completion_percentage": 0,
                "average_score": 0,
                "passed": False,
                "pass_threshold": 70
            }
            
        attempted_questions = AttemptQuestion.objects.filter(
            user=user,
            question__in=obj.questions.all()
        ).values('question').distinct()
        
        completed_questions = attempted_questions.count()
        completion_percentage = (completed_questions / total_questions * 100) if total_questions > 0 else 0
        
        # Calculate total score from latest attempts
        total_score = 0
        for question in obj.questions.all():
            latest_attempt = AttemptQuestion.objects.filter(
                user=user,
                question=question
            ).order_by('-created_at').first()
            
            if latest_attempt:
                total_score += latest_attempt.score
        
        correct_answers = 0 # Placeholder
        
        average_score = (total_score / total_questions * 100) if total_questions > 0 else 0
        passed = average_score >= 70
        
        return {
            "total_questions": total_questions,
            "completed_questions": completed_questions,
            "correct_answers": correct_answers,
            "total_score": total_score,
            "completion_percentage": round(completion_percentage, 2),
            "average_score": round(average_score, 2),
            "passed": passed,
            "pass_threshold": 70
        }

class ModuleSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'lessons']
        
class TrackingModulSerializer(ModelSerializer):
    progress_detail = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'progress_detail']
        
    def get_progress_detail(self, obj):
        """
        Compute and return both completed_lesson_count and completed_percentage
        for the logged-in user.
        """
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        course = obj.course

        # Get enrollment
        enrollment = course.enrollments.filter(user=user).first()
        total_lessons = obj.lessons.count()
        
        
        if not enrollment:
            return {
                "completed_lesson_count": 0,
                "completed_percentage": 0,
                "total_lesson_count": total_lessons
            }

        completed_lessons = LessionTracking.objects.filter(
            enrollment=enrollment,
            lesson__in=obj.lessons.all(),
            completed=True
        ).count()

        completed_percentage = round((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0

        return {
            "completed_lesson_count": completed_lessons,
            "completed_percentage": completed_percentage,
            "total_lesson_count": total_lessons
        }

class GradedQuestionsSerializer(serializers.Serializer):
    """Serializer for graded questions details with pass/fail status"""
    total_questions = serializers.IntegerField()
    completed_questions = serializers.IntegerField()
    completion_percentage = serializers.FloatField()
    average_score = serializers.FloatField()
    passed = serializers.BooleanField()
    pass_threshold = serializers.IntegerField(default=70)
    
class LessonGradedQuestionsSerializer(ModelSerializer):
    graded_questions_detail = serializers.SerializerMethodField()
    module_title = serializers.CharField(source='module.title', read_only=True)
    module_uid = serializers.CharField(source='module.uid', read_only=True)
    module_is_final_exam = serializers.BooleanField(source='module.is_final_exam', read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'uid', 'title', 'module_title', 'module_uid','module_is_final_exam', 'graded_questions_detail']
        
    def get_graded_questions_detail(self, obj):
        """Get graded questions details for this lesson"""
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        
        if not user or not user.is_authenticated:
            return {
                "total_questions": 0,
                "completed_questions": 0,
                "correct_answers": 0,
                "completion_percentage": 0,
                "average_score": 0,
                "passed": False,
                "pass_threshold": 70
            }
            
        # Get all questions for this lesson
        total_questions = obj.questions.count()
        
        if total_questions == 0:
            return {
                "total_questions": 0,
                "completed_questions": 0,
                "correct_answers": 0,
                "completion_percentage": 0,
                "average_score": 0,
                "passed": False,
                "pass_threshold": 70
            }
            
        # Get user's attempts for questions in this lesson
        attempted_questions = AttemptQuestion.objects.filter(
            user=user,
            question__in=obj.questions.all()
        ).values('question').distinct()
        
        completed_questions = attempted_questions.count()
        completion_percentage = (completed_questions / total_questions * 100) if total_questions > 0 else 0
        
        # Calculate total score from latest attempts
        total_score = 0
        for question in obj.questions.all():
            latest_attempt = AttemptQuestion.objects.filter(
                user=user,
                question=question
            ).order_by('-created_at').first()
            
            if latest_attempt:
                total_score += latest_attempt.score
        
        correct_answers = 0 # Placeholder
        
        average_score = (total_score / total_questions * 100) if total_questions > 0 else 0
        passed = average_score >= 70
        
        return {
            "total_questions": total_questions,
            "completed_questions": completed_questions,
            "correct_answers": correct_answers,
            "total_score": total_score,
            "completion_percentage": round(completion_percentage, 2),
            "average_score": round(average_score, 2),
            "passed": passed,
            "pass_threshold": 70
        }
