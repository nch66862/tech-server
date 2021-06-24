from techapi.models.answer import Answer
from django.http.response import HttpResponse
from rest_framework.decorators import action
from techapi.models import Question, Type
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError
from rest_framework import status
from django.utils import timezone
import json

class QuestionViewSet(ViewSet):
## Basic fetches
    def retrieve(self, request, pk):
        response = {}
        question = Question.objects.get(pk=pk)
        question_dict = QuestionSerializer(question, many=False, context={'request': request}).data
        response['question'] = question_dict
        # answers = Answer.objects.filter(question_id=question.id)
        # answers_list = AnswerSerializer(question, many=True, context={'request': request}).data
        # for answer in answers:
        #     answer.is_author = priority_user == answer.priority_user
        # affirmations_serialized = AffirmationSerializer(affirmations, many=True, context={'request': request})
        return Response(response, status=status.HTTP_200_OK)
    def create(self, request):
        new_question = Question()
        new_question.type = request.data['type_id']
        new_question.question_text = request.data['question_text']
        new_question.required = request.data['required']
        new_question.save()
        serializer = QuestionSerializer(new_question, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # def destroy(self, request, pk):
    #     affirmation = Affirmation.objects.get(pk=pk)
    #     affirmation.delete()
    #     return Response({}, status=status.HTTP_204_NO_CONTENT)
    # def list(self, request):

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'type')
class QuestionSerializer(serializers.ModelSerializer):
    type = TypeSerializer(many=False)
    class Meta:
        model = Question
        fields = ('id', 'type', 'question_text', 'required', 'answer_set')
class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False)
    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer_value')
