from django.urls import path
from .views import CourseListView, CourseDetailView, CategoryListView, TagListView, search_courses

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('search/', search_courses, name='course-search'),
]