from django.urls import path
from .views import QuizListView, QuizDetailView, start_quiz_attempt, submit_quiz_attempt

app_name = 'quizzes'

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz-list'),
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('<int:quiz_id>/start/', start_quiz_attempt, name='start-quiz-attempt'),
    path('attempt/<int:attempt_id>/submit/', submit_quiz_attempt, name='submit-quiz-attempt'),
]