from rest_framework.decorators import action
from techapi.models import Type
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class TypeViewSet(ViewSet):
    def list(self, request):
        types = Type.objects.all()
        types_list = TypeSerializer(types, many=True, context={'request': request}).data
        return Response(types_list, status=status.HTTP_200_OK)

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'type')
