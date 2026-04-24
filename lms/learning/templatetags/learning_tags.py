from django.template import Library
from exam.models import AttemptQuestion
register = Library()
from learning.models import LessionTracking, ModuleTracking 

@register.filter
def is_lesson_completed(lesson, enrollment):
    return LessionTracking.objects.filter(lesson=lesson,enrollment=enrollment,completed=True).exists()

@register.filter
def is_module_completed(module, enrollment):
    return ModuleTracking.objects.filter(module=module, enrollment=enrollment, completed=True).exists()

@register.filter
def marked_option(question, user):
    attempt = AttemptQuestion.objects.filter(question=question, user=user).first()
    if attempt:
        return attempt.option.uid
    return None

@register.filter
def question_attempt_count(question, user):
    return AttemptQuestion.objects.filter(question=question, user=user).count()

@register.simple_tag
def option_status(marked_option, option_uid, is_correct):
    if marked_option == option_uid and is_correct:
        return "correct"
    elif marked_option == option_uid and not is_correct:
        return "incorrect"
    return "neutral"

@register.simple_tag
def set_var(val=None):
    return val

