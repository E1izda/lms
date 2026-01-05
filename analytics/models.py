from django.db import models
from django.conf import settings
from courses.models import Course

class CourseAnalytics(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    total_enrollments = models.PositiveIntegerField(default=0)
    total_completions = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.course.title}"

class UserActivity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('enrollment', 'Enrollment'),
        ('completion', 'Completion'),
        ('payment', 'Payment'),
        ('review', 'Review'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"
