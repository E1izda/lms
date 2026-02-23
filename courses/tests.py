from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Course


class CourseModelTests(TestCase):
    def test_create_course_with_instructor(self):
        User = get_user_model()
        instructor = User.objects.create_user(username='inst', email='i@example.com', password='pass', role='instructor')
        cat = Category.objects.create(name='Test Cat', slug='test-cat')
        course = Course.objects.create(title='Test Course', description='Desc', instructor=instructor, category=cat)
        self.assertEqual(course.title, 'Test Course')
        self.assertEqual(course.instructor, instructor)
        self.assertEqual(course.price, 0)
from django.test import TestCase

# Create your tests here.
