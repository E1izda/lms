from django.test import TestCase
from django.contrib.auth import get_user_model
from courses.models import Category, Course
from .models import Payment
from django.urls import reverse

class PaymentModelTests(TestCase):
    def test_create_payment_record(self):
        User = get_user_model()
        user = User.objects.create_user(username='buyer', email='b@example.com', password='pass')
        instructor = User.objects.create_user(username='instr', email='ins@example.com', password='pass', role='instructor')
        cat = Category.objects.create(name='PayCat', slug='pay-cat')
        course = Course.objects.create(title='Paid Course', description='Desc', instructor=instructor, category=cat, price=10.00)
        payment = Payment.objects.create(user=user, course=course, amount=course.price)
        self.assertEqual(payment.status, 'pending')
        self.assertEqual(str(payment).split(' - ')[0], user.username)
from django.test import TestCase

class PaymentViewTests(TestCase):
    def test_payment_view(self):
        response = self.client.get(reverse('payments:payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/payment.html')
        self.assertContains(response, 'Payment')
    
    def test_payment_success_view(self):
        response = self.client.get(reverse('payments:payment_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/payment_success.html')
        self.assertContains(response, 'Payment Successful')

class PaymentAPITests(TestCase):
    def test_payment_api_endpoint(self):
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())

