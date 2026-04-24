from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import Sum
from base.models import BaseModel
from django.contrib import messages

# Create your models here.
class Question(BaseModel):
    question = models.TextField(null=True, blank=True)
    
    @property
    def all_options(self):
        return self.options.all()
    
    def __str__(self):
        return f'{self.question}'
    
    class Meta:
        ordering = ['?']

class Option(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.question.question[:40]}-----{self.option[:20]}'
    
    class Meta:
        ordering = ['?']
        
class AttemptQuestion(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE,null=True, blank=True)
    score = models.FloatField(default=0)
    
    def attempts(self, user, question):
        return AttemptQuestion.objects.filter(user=user, question=question).count()

    def __str__(self):
        return f'{self.user.username}--{self.question.question[:40]}--{self.option.option[:20]}'

    class Meta:
        ordering = ['-created_at']
    

