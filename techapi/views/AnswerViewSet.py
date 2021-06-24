from django.http.response import HttpResponse
from rest_framework.decorators import action
from techapi.models import Question, Answer, Type
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError
from rest_framework import status
from django.utils import timezone
import json

class AnswerViewSet(ViewSet):
    def create(self, request):
        new_answer = Answer()
        new_answer.question_id = request.data['question_id']
        new_answer.question_text = request.data['question_text']
        new_answer.required = request.data['required']
        new_answer.save()
        serializer = AnswerSerializer(new_answer, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'type')
class QuestionSerializer(serializers.ModelSerializer):
    type = TypeSerializer(many=False)
    class Meta:
        model = Question
        fields = ('id', 'type', 'question_text', 'question_display_text', 'required')
class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False)
    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer_value')
