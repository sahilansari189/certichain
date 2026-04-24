from django.contrib import admin
from .models import LessionTracking, ModuleTracking
# Register your models here.


class LessonTrackingAdmin(admin.ModelAdmin):
    list_display = ('uid','enrollment', 'lesson', 'completed')
    list_filter = ('enrollment', 'completed','lesson__module__title')
    search_fields = ('enrollment__user__username', 'lesson__title')
    
admin.site.register(LessionTracking, LessonTrackingAdmin)

class ModuleTrackingAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'module', 'completed','is_final_exam','final_exam_started','final_exam_completed')
    list_filter = ('enrollment', 'completed','is_final_exam','final_exam_started','final_exam_completed')
    search_fields = ('enrollment__user__username', 'module__title')

admin.site.register(ModuleTracking, ModuleTrackingAdmin)
