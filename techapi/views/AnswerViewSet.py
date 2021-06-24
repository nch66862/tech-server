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
## Basic fetches
    # def retrieve(self, request, pk):
    #     priority_user = PriorityUser.objects.get(user=request.auth.user)
    #     affirmations = Affirmation.objects.filter(priority_id=pk)
    #     for affirmation in affirmations:
    #         affirmation.is_author = priority_user == affirmation.priority_user
    #     affirmations_serialized = AffirmationSerializer(affirmations, many=True, context={'request': request})
    #     return Response(affirmations_serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        new_answer = Answer()
        new_answer.question_id = request.data['question_id']
        new_answer.question_text = request.data['question_text']
        new_answer.required = request.data['required']
        new_answer.save()
        serializer = AnswerSerializer(new_answer, many=False, context={'request': request})
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
        fields = ('id', 'type', 'question_text', 'question_display_text', 'required')
class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False)
    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer_value')
