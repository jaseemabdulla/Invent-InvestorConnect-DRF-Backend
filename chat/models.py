from django.db import models
from accounts.models import BaseUser
from django.utils import timezone

# Create your models here.


class ChatMessages(models.Model):
    sender = models.ForeignKey(BaseUser, on_delete=models.CASCADE,related_name='sent_messages')
    receiver = models.ForeignKey(BaseUser, on_delete=models.CASCADE,related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.sender.first_name} - {self.receiver.first_name} - {self.timestamp}"
    
    class Meta:
        db_table = "chat_message"
        ordering = ('timestamp',)
