from django.db import models
from accounts.models import EntrepreneurProfile

# Create your models here.


class StartupDetail(models.Model):

    APPROVAL_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    INDUSTRY_CHOICES = [
        ('tech', 'Technology'),
        ('health', 'Healthcare'),
        ('finance', 'Finance'),
        ('edu', 'Education'),
        ('retail', 'Retail'),
        ('entertainment', 'Entertainment'),
        ('food', 'Food and Beverage'),
        ('travel', 'Travel and Hospitality'),
        ('manufacturing', 'Manufacturing'),
        ('fashion', 'Fashion'),
        ('media', 'Media and Communication'),
        ('real_estate', 'Real Estate'),
        ('other', 'Other'),
    ]

    STAGE_CHOICES = [
        ('pre_seed', 'Pre-Seed Stage'),
        ('seed', 'Seed Stage'),
        ('early', 'Early Stage'),
        ('growth', 'Growth Stage'),
        ('expansion', 'Expansion Phase'),
        ('exit', 'Exit Phase'),
    ]
 
    entrepreneurs = models.ManyToManyField(
        EntrepreneurProfile, related_name='startups')
    startup_name = models.CharField(max_length=50)
    brief_about = models.TextField()
    startup_industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    startup_stage = models.CharField(max_length=50, choices=STAGE_CHOICES)
    presentation_video = models.FileField(upload_to='startup_videos/')
    approval_status = models.CharField(
        max_length=50, choices=APPROVAL_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
   
        
