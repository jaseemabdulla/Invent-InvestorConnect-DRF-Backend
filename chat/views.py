from django.shortcuts import render
from rest_framework import generics
from .models import ChatMessages
from .serializer import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.models import BaseUser
from django.db.models import Q

# Create your views here.


class MessageList(generics.ListAPIView):
    serializer_class = MessageSerializer
    ordering = ('-timestamp',)

    def get_queryset(self):
        user = self.request.user
        receiver_id = self.kwargs.get('receiver_id')

        if receiver_id:
            receiver = BaseUser.objects.get(id=receiver_id)
            # Filter messages based on sender and receiver
            messages = ChatMessages.objects.filter(
                (Q(sender=user, receiver=receiver) |
                 Q(sender=receiver, receiver=user))
            )
        else:
            # If no receiver_id provided, return an empty queryset or handle it differently
            messages = ChatMessages.objects.none()

        return messages
