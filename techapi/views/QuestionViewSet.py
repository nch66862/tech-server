from django.http.response import HttpResponse
from rest_framework.decorators import action
from techapi.models import Question
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
    # def retrieve(self, request, pk):
    #     priority_user = PriorityUser.objects.get(user=request.auth.user)
    #     affirmations = Affirmation.objects.filter(priority_id=pk)
    #     for affirmation in affirmations:
    #         affirmation.is_author = priority_user == affirmation.priority_user
    #     affirmations_serialized = AffirmationSerializer(affirmations, many=True, context={'request': request})
    #     return Response(affirmations_serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        new_question = Question()
        new_question.priority_user = PriorityUser.objects.get(user=request.auth.user)
        new_question.priority_id = request.data['priority_id']
        new_question.new_question = request.data['new_question']
        new_question.save()
        serializer = QuestionSerializer(new_question, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # def destroy(self, request, pk):
    #     affirmation = Affirmation.objects.get(pk=pk)
    #     affirmation.delete()
    #     return Response({}, status=status.HTTP_204_NO_CONTENT)
    # def list(self, request):

class QuestionSerializer(serializers.ModelSerializer):
    priority_user = PriorityUserSerializer(many=False)
    priority = PrioritySerializer(many=False)
    class Meta:
        model = Question
        fields = ('id', 'type', 'question_text', 'question_display_text', 'required')
