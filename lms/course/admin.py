from django.contrib import admin
from .models import Skill, DifficultyLevel, Language, OfferedBy, Industry, Tier, Course, Module, Lesson, Enrollment
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'course_type', 'duration', 'enrolled_count', 'rating')
    search_fields = ('title', 'instructor__username', 'course_type')
    list_filter = ('course_type', 'duration')

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    
class LessonAdmin(admin.ModelAdmin):
    list_display = ('uid','title', 'module', 'order')
    list_filter = ('module__course__title','module__title')
    
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'progress', 'completed')
    list_filter = ('course', 'completed')




admin.site.register(Skill)
admin.site.register(DifficultyLevel)
admin.site.register(Language)
admin.site.register(OfferedBy)
admin.site.register(Industry)
admin.site.register(Tier)
admin.site.register(Course, CourseAdmin)

admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)

