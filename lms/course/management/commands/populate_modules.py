from faker import Faker
from course.models import Course, Module, Lesson
from django.core.management.base import BaseCommand
import random

fake = Faker()

class Command(BaseCommand): 
    help = 'Populate modules and lessons for existing courses'

    def handle(self, *args, **kwargs):
        course = Course.objects.get(id=1)
        # Create 10 modules for each course
        for i in range(1, 11):
            module = Module.objects.create(
                course=course,
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                order=i
            )
            self.stdout.write(self.style.SUCCESS(f'Created module: {module.title} for course: {course.title}'))

            # Create 5 lessons for each module
            for j in range(1, 6):
                rand = random.randint(0, 1)
                lesson = Lesson.objects.create(
                    module=module,
                    title=fake.sentence(nb_words=6),
                    content=fake.paragraph(nb_sentences=50),
                    video_url=fake.url() if rand else '',
                    order=j
                )
                self.stdout.write(self.style.SUCCESS(f'  Created lesson: {lesson.title} for module: {module.title}'))
    
        self.stdout.write(self.style.SUCCESS('Successfully populated modules and lessons for all courses.'))

