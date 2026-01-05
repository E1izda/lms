from django.db import models
from courses.models import Course

class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('quiz', 'Quiz'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='text')
    content = models.TextField()  # For text content or video URL
    video_file = models.FileField(upload_to='lesson_videos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    duration = models.PositiveIntegerField(help_text='Duration in minutes', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"
