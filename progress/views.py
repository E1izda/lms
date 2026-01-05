from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import CourseProgress, LessonProgress
from .serializers import CourseProgressSerializer, LessonProgressSerializer

class CourseProgressListView(generics.ListAPIView):
    serializer_class = CourseProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseProgress.objects.filter(user=self.request.user)

class CourseProgressDetailView(generics.RetrieveAPIView):
    serializer_class = CourseProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseProgress.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request, course_id):
    from courses.models import Course
    try:
        course = Course.objects.get(id=course_id)
        progress, created = CourseProgress.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={'enrolled_at': timezone.now()}
        )
        if created:
            # Create lesson progress for all lessons
            for lesson in course.lessons.all():
                LessonProgress.objects.create(
                    user=request.user,
                    lesson=lesson,
                    course_progress=progress
                )
        return Response(CourseProgressSerializer(progress).data, status=status.HTTP_201_CREATED)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_lesson(request, lesson_id):
    try:
        lesson_progress = LessonProgress.objects.get(
            user=request.user,
            lesson_id=lesson_id
        )
        lesson_progress.is_completed = True
        lesson_progress.completed_at = timezone.now()
        lesson_progress.save()

        # Update course progress
        course_progress = lesson_progress.course_progress
        total_lessons = course_progress.lessonprogress_set.count()
        completed_lessons = course_progress.lessonprogress_set.filter(is_completed=True).count()
        course_progress.completion_percentage = (completed_lessons / total_lessons) * 100

        if course_progress.completion_percentage == 100:
            course_progress.is_completed = True
            course_progress.completed_at = timezone.now()
            # Generate certificate asynchronously
            from .tasks import generate_certificate
            generate_certificate.delay(course_progress.id)
            # Send completion email
            from users.tasks import send_course_completion_email
            send_course_completion_email.delay(
                course_progress.user.email,
                course_progress.user.get_full_name(),
                course_progress.course.title
            )
            # Send notification
            from notifications.utils import send_notification_to_user
            send_notification_to_user(
                course_progress.user,
                'Course Completed!',
                f'Congratulations! You have completed {course_progress.course.title}',
                'course_completed',
                {'course_id': course_progress.course.id}
            )

        course_progress.save()

        return Response(CourseProgressSerializer(course_progress).data)
    except LessonProgress.DoesNotExist:
        return Response({'error': 'Lesson progress not found'}, status=status.HTTP_404_NOT_FOUND)
