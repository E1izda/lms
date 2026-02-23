from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def test_create_user_default_role(self):
        User = get_user_model()
        user = User.objects.create_user(username='student1', email='s1@example.com', password='pass')
        self.assertEqual(user.role, 'student')
        self.assertTrue(user.check_password('pass'))
from django.test import TestCase

# Create your tests here.
