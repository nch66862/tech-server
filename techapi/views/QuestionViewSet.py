from techapi.models.answer import Answer
from rest_framework.decorators import action
from techapi.models import Question, Type
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class QuestionViewSet(ViewSet):
    def retrieve(self, request, pk):
        response = {}
        question = Question.objects.get(pk=pk)
        question_dict = QuestionSerializer(question, many=False, context={'request': request}).data
        response['question'] = question_dict
        answers = Answer.objects.filter(question_id=question.id)
        answers_list = AnswerSerializer(answers, many=True, context={'request': request}).data
        response['question']['answer_values'] = []
        for answer in answers_list:
            response['question']['answer_values'].append({
                'answer_value': answer['answer_value'],
                'id': answer['id']
                })
        return Response(response, status=status.HTTP_200_OK)
    def create(self, request):
        new_question = Question()
        new_question.type = request.data['type_id']
        new_question.question_text = request.data['question_text']
        new_question.required = request.data['required']
        new_question.save()
        serializer = QuestionSerializer(new_question, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'type')
class QuestionSerializer(serializers.ModelSerializer):
    type = TypeSerializer(many=False)
    class Meta:
        model = Question
        fields = ('id', 'type', 'question_text', 'required')
class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False)
    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer_value')
