from rest_framework import serializers
from .models import CourseProgress, LessonProgress

class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = LessonProgress
        fields = '__all__'

class CourseProgressSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    lesson_progress = LessonProgressSerializer(source='lessonprogress_set', many=True, read_only=True)

    class Meta:
        model = CourseProgress
        fields = '__all__'