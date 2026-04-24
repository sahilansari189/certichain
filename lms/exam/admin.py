from django.contrib import admin
from .models import Question,Option, AttemptQuestion
# Register your models here.
admin.site.register(Option)
class QuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'score')
    list_filter = ('user', 'question',)
    search_fields = ('question__question', 'user__username')
    ordering = ('-score',)

admin.site.register(AttemptQuestion, QuestionAttemptAdmin)


class OptionInline(admin.StackedInline):
    model = Option
    extra = 1

class QuestionInline(admin.ModelAdmin):
    inlines = [OptionInline]
    
admin.site.register(Question, QuestionInline)
