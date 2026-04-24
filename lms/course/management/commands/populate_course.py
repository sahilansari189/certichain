from django.core.management.base import BaseCommand
from course.models import Skill, DifficultyLevel, Language, OfferedBy, Industry, Tier, Course
from django.contrib.auth.models import User
import random


class Command(BaseCommand):
    
    help = 'Set up initial data for the Course app'

    def handle(self, *args, **kwargs):
        skills = Skill.objects.all()
        difficulty_levels = DifficultyLevel.objects.all()
        languages = Language.objects.all()
        offered_bys = OfferedBy.objects.all()
        industries = Industry.objects.all()
        tiers = Tier.objects.all()
        instructors = User.objects.all()
        course_types = ['course', 'guided_project']
        
        for i in range(20):
            title = f'Sample Course {i+1}'
            description = f'This is a description for Sample Course {i+1}.'
            duration = random.randint(10, 100)
            course_type = random.choice(course_types)
            instructor = random.choice(instructors) if instructors else None
            
            course, created = Course.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'duration': duration,
                    'course_type': course_type,
                    'instructor': instructor,
                    'enrolled_count': random.randint(0, 5000),
                    'rating': round(random.uniform(1.0, 5.0), 1),
                }
            )
            
            if created:
                # Randomly assign many-to-many relationships
                course.skills.set(random.sample(list(skills), k=random.randint(1, min(3, skills.count()))) if skills else []) 
                course.difficulty_level = random.choice(list(difficulty_levels)) if difficulty_levels else None
                course.language = random.choice(list(languages)) if languages else None
                course.offered_by = random.choice(list(offered_bys)) if offered_bys else None
                course.industry = random.choice(list(industries)) if industries else None
                course.tier = random.choice(list(tiers)) if tiers else None
                course.save()
                # messaege
                self.stdout.write(self.style.SUCCESS(f'Created course: {title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Course already exists: {title}'))
        self.stdout.write(self.style.SUCCESS('Successfully populated courses'))
