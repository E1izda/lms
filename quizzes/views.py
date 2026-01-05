from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Quiz, QuizAttempt, Question, Answer, UserAnswer
from .serializers import QuizSerializer, QuizAttemptSerializer, QuestionSerializer, AnswerSerializer

class QuizListView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_quiz_attempt(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz)
        return Response(QuizAttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz_attempt(request, attempt_id):
    try:
        attempt = QuizAttempt.objects.get(id=attempt_id, user=request.user)
        if attempt.completed_at:
            return Response({'error': 'Quiz already completed'}, status=status.HTTP_400_BAD_REQUEST)

        answers_data = request.data.get('answers', [])
        score = 0
        total_questions = attempt.quiz.questions.count()

        for answer_data in answers_data:
            question_id = answer_data.get('question_id')
            selected_answers = answer_data.get('selected_answers', [])

            try:
                question = Question.objects.get(id=question_id, quiz=attempt.quiz)
                correct_answers = question.answers.filter(is_correct=True)
                user_selected = Answer.objects.filter(id__in=selected_answers)

                is_correct = set(correct_answers) == set(user_selected)
                if is_correct:
                    score += 1

                UserAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    is_correct=is_correct
                )
                for answer in user_selected:
                    attempt.user_answers.add(UserAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_answers=[answer]
                    ))
            except Question.DoesNotExist:
                continue

        attempt.score = score
        attempt.is_passed = (score / total_questions * 100) >= attempt.quiz.passing_score
        attempt.completed_at = timezone.now()
        attempt.save()

        return Response(QuizAttemptSerializer(attempt).data)
    except QuizAttempt.DoesNotExist:
        return Response({'error': 'Attempt not found'}, status=status.HTTP_404_NOT_FOUND)
