from django.db import models
from accounts.models import EntrepreneurProfile

# Create your models here.


class MentorRequest(models.Model):
    entrepreneur = models.ForeignKey(EntrepreneurProfile, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)