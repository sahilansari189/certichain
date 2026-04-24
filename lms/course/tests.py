from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from faker import Faker
from .models import (
    Course, Skill, DifficultyLevel, Language, OfferedBy, 
    Industry, Tier, Module, Lesson, Enrollment
)
from account.models import AllowedEmail

fake = Faker()

class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass')
        self.skill = Skill.objects.create(name='Python')
        self.difficulty = DifficultyLevel.objects.create(level='Beginner')
        self.language = Language.objects.create(name='English', code='en')
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            instructor=self.user,
            duration=10
        )

    def test_course_creation(self):
        self.assertEqual(self.course.title, 'Test Course')
        self.assertEqual(self.course.slug, 'test-course')
        self.assertEqual(str(self.course), 'Test Course')

    def test_skill_str(self):
        self.assertEqual(str(self.skill), 'Python')

    def test_enrollment_creation(self):
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        self.assertEqual(str(enrollment), 'testuser - Test Course')
        self.assertFalse(enrollment.completed)

class ModuleLessonTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass')
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            instructor=self.user,
            duration=10
        )
        self.module = Module.objects.create(
            course=self.course,
            title='Test Module',
            order=1
        )
        self.lesson = Lesson.objects.create(
            module=self.module,
            title='Test Lesson',
            content='Test Content',
            order=1
        )

    def test_module_str(self):
        self.assertEqual(str(self.module), 'Test Course - Test Module')

    def test_lesson_module_name(self):
        self.assertEqual(self.lesson.module_name, 'Test Module')

class CourseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass')
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            instructor=self.user,
            duration=10
        )

    def test_course_list_view(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Explore Content')

    def test_course_detail_view(self):
        response = self.client.get(reverse('course_detail', args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)

    def test_enrollment_requires_login(self):
        response = self.client.post(reverse('create_enrollment', args=[self.course.slug]))
        self.assertEqual(response.status_code, 302)

    def test_enrollment_with_allowed_email(self):
        AllowedEmail.objects.create(email='test@test.com', is_allowed=True)
        self.client.login(username='testuser', password='pass')
        response = self.client.post(reverse('create_enrollment', args=[self.course.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.course).exists())

class CourseAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass')
        self.skill = Skill.objects.create(name='Python')
        self.language = Language.objects.create(name='English', code='en')
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            instructor=self.user,
            duration=10,
            language=self.language
        )
        self.course.skills.add(self.skill)

    def test_course_api_list(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)

    def test_course_api_filter_by_language(self):
        response = self.client.get('/api/courses/?languages=en')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)

    def test_course_api_filter_by_skill(self):
        response = self.client.get('/api/courses/?skills=Python')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)


