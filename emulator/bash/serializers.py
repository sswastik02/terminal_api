from rest_framework import serializers

from .models import command_response

class BashSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = command_response
        fields = ('id','command', 'response',)