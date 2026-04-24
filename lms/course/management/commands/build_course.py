from django.core.management.base import BaseCommand
from course.models import Skill, DifficultyLevel, Language, OfferedBy, Industry, Tier, Course,Module, Lesson
from exam.models import Question, Option
from django.contrib.auth.models import User
import random
from faker import Faker
from course.choice import COURSE_TYPES
from utilities.generate_mock_question import questions as questions_set

fake = Faker()

class Command(BaseCommand):
    
    help = 'Set up initial data for the Course app'

    def handle(self, *args, **kwargs):
        course_title = input('Enter the title of the course : ')
        skills = Skill.objects.all()
        difficulty_levels = DifficultyLevel.objects.all()
        languages = Language.objects.all()
        offered_bys = OfferedBy.objects.all()
        industries = Industry.objects.all()
        tiers = Tier.objects.all()
        instructors = User.objects.all()
        durations = [36, 32, 50, 60]
        course_types = [ i[0] for i in COURSE_TYPES ]
        instructor, _ = User.objects.get_or_create(username='johndoe', first_name='John', last_name='Doe',email='shashwat.admin@certichain.io')
        if _ is True:
            instructor.set_password('password123')
            instructor.save()
        
        course_detail = {
            'title': course_title,
            'description': fake.paragraph(nb_sentences=15),
            'duration': random.choice(durations),
            'course_type': random.choice(course_types),
            'instructor': instructor,
            'difficulty_level' : random.choice(list(difficulty_levels)) if difficulty_levels else None,
            'language' : random.choice(list(languages)) if languages else None,
            'offered_by' : random.choice(list(offered_bys)) if offered_bys else None,
            'industry' : random.choice(list(industries)) if industries else None,
            'tier' : random.choice(list(tiers)) if tiers else None,
            'enrolled_count': random.randint(0, 5000),
            'rating': round(random.uniform(1.0, 5.0), 1),
        }
        course = Course.objects.create(**course_detail)
        course.skills.set(random.sample(list(skills), k=random.randint(1, min(3, skills.count()))) if skills else []) 
        course.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created course {course.title}.'))

        for i in range(1, 6):
            module = Module.objects.create(
                course=course,
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                order=i
            )
            self.stdout.write(self.style.SUCCESS(f'Created module: {module.title} for course: {course.title}'))

            # Create 5 lessons for each module
            for j in range(4):
                lesson = Lesson.objects.create(
                    module=module,
                    title=fake.sentence(nb_words=6),
                    content=fake.paragraph(nb_sentences=50),
                    order=j
                )
                if j==3:
                    for k in range(5):
                        a_question = random.choice(questions_set)
                        question = Question.objects.create(
                            question=a_question[0]
                        )
                        lesson.questions.add(question)
                        Option.objects.create(question=question,option = a_question[1][0], is_correct = a_question[2] == 'A')
                        Option.objects.create(question=question,option = a_question[1][1], is_correct = a_question[2] == 'B')
                        Option.objects.create(question=question,option = a_question[1][2], is_correct = a_question[2] == 'C')
                        Option.objects.create(question=question,option = a_question[1][3], is_correct = a_question[2] == 'D')

                self.stdout.write(self.style.SUCCESS(f'  Created lesson: {lesson.title} for module: {module.title}'))

        # Creating Final Exam
        final_exam_module = Module.objects.create(
                course=course,
                title='Final Exam',
                order=99,
                is_final_exam = True,
                final_exam_time = 5, 
            )
        final_exam_lesson = Lesson.objects.create(
                    module=final_exam_module,
                    title= 'Final Exam -' + fake.sentence(nb_words=6),
                    content=fake.paragraph(nb_sentences=3),
                    order=0
                )

        for k in range(10):
            a_question = random.choice(questions_set)
            question = Question.objects.create(
                question=a_question[0]
            )
            final_exam_lesson.questions.add(question)
            Option.objects.create(question=question,option = a_question[1][0], is_correct = a_question[2] == 'A')
            Option.objects.create(question=question,option = a_question[1][1], is_correct = a_question[2] == 'B')
            Option.objects.create(question=question,option = a_question[1][2], is_correct = a_question[2] == 'C')
            Option.objects.create(question=question,option = a_question[1][3], is_correct = a_question[2] == 'D')

        self.stdout.write(self.style.SUCCESS(f'Final Exam Created!'))
        self.stdout.write(self.style.SUCCESS('Successfully populated modules and lessons for all courses.'))
        
        

