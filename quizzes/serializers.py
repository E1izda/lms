from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizAttempt, UserAnswer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'

class QuizAttemptSerializer(serializers.ModelSerializer):
    user_answers = serializers.SerializerMethodField()

    class Meta:
        model = QuizAttempt
        fields = '__all__'

    def get_user_answers(self, obj):
        return UserAnswerSerializer(obj.user_answers.all(), many=True).data

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'