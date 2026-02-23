from django.test import TestCase
from django.contrib.auth import get_user_model
from courses.models import Category, Course
from lessons.models import Lesson
from .models import Quiz


class QuizModelTests(TestCase):
    def test_create_quiz_for_lesson(self):
        User = get_user_model()
        instructor = User.objects.create_user(username='inst2', email='i2@example.com', password='pass', role='instructor')
        cat = Category.objects.create(name='Cat2', slug='cat-2')
        course = Course.objects.create(title='Course2', description='Desc', instructor=instructor, category=cat)
        lesson = Lesson.objects.create(course=course, title='Lesson 1', content='Content')
        quiz = Quiz.objects.create(lesson=lesson, title='Quiz 1')
        self.assertEqual(quiz.lesson, lesson)
        self.assertIn('Quiz for', str(quiz))
from django.test import TestCase

# Create your tests here.
