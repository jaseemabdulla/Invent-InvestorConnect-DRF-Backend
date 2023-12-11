from django.db import models
from accounts.models import EntrepreneurProfile,MentorProfile

# Create your models here.


class MentorRequest(models.Model):
    entrepreneur = models.ForeignKey(EntrepreneurProfile, on_delete=models.CASCADE)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.SET_NULL,null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)