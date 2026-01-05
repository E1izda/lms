from django.db import models
from django.conf import settings
from courses.models import Course

class UserInteraction(models.Model):
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('enroll', 'Enroll'),
        ('complete', 'Complete'),
        ('rate', 'Rate'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    weight = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course', 'interaction_type')

class CourseSimilarity(models.Model):
    course1 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='similarities1')
    course2 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='similarities2')
    similarity_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course1', 'course2')
