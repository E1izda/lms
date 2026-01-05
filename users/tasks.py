from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email, user_name):
    subject = 'Welcome to Education Platform!'
    message = f'Hi {user_name},\n\nWelcome to our educational platform! Start learning today.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_course_completion_email(user_email, user_name, course_title):
    subject = 'Congratulations on Course Completion!'
    message = f'Hi {user_name},\n\nCongratulations! You have successfully completed the course: {course_title}.\n\nYour certificate is now available.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)