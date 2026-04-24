from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from django.utils.text import slugify
from .choice import COURSE_TYPES
from exam.models import Question
import random

# Create your models here.

class Skill(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class DifficultyLevel(BaseModel):
    level = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.level

class Language(BaseModel):  
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class OfferedBy(BaseModel):
    organization_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.organization_name

    class Meta:
        verbose_name = 'Offered By'
        verbose_name_plural = 'Offered Bys'

class Industry(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'
    
class Tier(BaseModel):
    name = models.CharField(max_length=100)
    benefits = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Course(BaseModel):    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,null=True,blank=True)
    code = models.CharField(max_length=10,unique=True, null=True,blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    duration = models.IntegerField(help_text="Duration in hours")
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES, default='course')
    enrolled_count = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    review_count = models.IntegerField(default=0)
    skills = models.ManyToManyField(Skill, blank=True)
    difficulty_level = models.ForeignKey(DifficultyLevel, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    offered_by = models.ForeignKey(OfferedBy, on_delete=models.SET_NULL, null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.title

    def generate_code(self,title):
        """
            Generates a course code like:
            Data Science -> DS001
            last_number: the previous highest number in DB
        """
        prefix = ''.join(word[0].upper() for word in title.split())

        next_number = random.randint(100, 999)
        number_part = f"{next_number}"

        return f"{prefix}{number_part}"


    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code(self.title)
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
        
class Module(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(help_text="Order of the module in the course")
    is_final_exam = models.BooleanField(default=False,help_text="Is this final exam?")
    final_exam_time = models.IntegerField(help_text="Time in minutes for the final exam", default=0)
        
    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['order']
    
class Lesson(BaseModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Content of the lesson in markdown format")
    video_url = models.TextField(blank=True, null=True, verbose_name='Youtube embedded video', help_text='Paste here youtube video embedded.')
    order = models.IntegerField(help_text="Order of the lesson in the module")
    questions = models.ManyToManyField(Question, blank=True)
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"
    
    @property
    def module_name(self):
        return self.module.title
    
    class Meta:
        ordering = ['order']

class Enrollment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Progress percentage")
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    



