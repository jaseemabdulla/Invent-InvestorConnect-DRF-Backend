from rest_framework import serializers
from .models import ChatMessages

class MessageSerializer(serializers.ModelSerializer):
       class Meta:
           model = ChatMessages
           fields = ('id', 'sender', 'receiver','message', 'timestamp')
           read_only_fields = ('id', 'timestamp')