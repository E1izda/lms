from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Avg
from courses.models import Course
from courses.serializers import CourseSerializer
from .models import UserInteraction, CourseSimilarity

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    user = request.user

    # Get user's enrolled courses
    enrolled_course_ids = UserInteraction.objects.filter(
        user=user,
        interaction_type__in=['enroll', 'complete']
    ).values_list('course_id', flat=True)

    # Collaborative filtering: find similar users
    similar_users = UserInteraction.objects.filter(
        course_id__in=enrolled_course_ids
    ).exclude(user=user).values('user').annotate(
        common_courses=Count('course')
    ).order_by('-common_courses')[:10]

    similar_user_ids = [u['user'] for u in similar_users]

    # Get courses that similar users liked but user hasn't enrolled
    recommended_course_ids = UserInteraction.objects.filter(
        user_id__in=similar_user_ids,
        interaction_type__in=['enroll', 'complete']
    ).exclude(course_id__in=enrolled_course_ids).values('course').annotate(
        score=Count('course')
    ).order_by('-score')[:10]

    recommended_courses = Course.objects.filter(
        id__in=[r['course'] for r in recommended_course_ids],
        status='published'
    )

    # Content-based filtering as fallback
    if not recommended_courses:
        user_categories = Course.objects.filter(
            id__in=enrolled_course_ids
        ).values_list('category', flat=True).distinct()

        recommended_courses = Course.objects.filter(
            category__in=user_categories,
            status='published'
        ).exclude(id__in=enrolled_course_ids)[:10]

    # Popularity-based as final fallback
    if not recommended_courses:
        recommended_courses = Course.objects.filter(
            status='published'
        ).annotate(
            enrollments=Count('progress')
        ).order_by('-enrollments')[:10]

    serializer = CourseSerializer(recommended_courses, many=True)
    return Response(serializer.data)
