from django.urls import path
from .views import CourseProgressListView, CourseProgressDetailView, enroll_course, complete_lesson

app_name = 'progress'

urlpatterns = [
    path('', CourseProgressListView.as_view(), name='course-progress-list'),
    path('<int:pk>/', CourseProgressDetailView.as_view(), name='course-progress-detail'),
    path('enroll/<int:course_id>/', enroll_course, name='enroll-course'),
    path('complete-lesson/<int:lesson_id>/', complete_lesson, name='complete-lesson'),
]