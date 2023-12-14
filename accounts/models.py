from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class BaseUser(AbstractUser):
    ROLES = (
        ('investor','Investor'),
        ('entrepreneur','Entrepreneur'),
        ('admin','Admin'),
        ('mentor','Mentor')
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=False,blank=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','role']
    role = models.CharField(max_length=15, choices=ROLES,default='entrepreneur')
    is_blocked = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20,unique=True)
    joined_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    
class InvestorProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE) 
    bio = models.TextField(blank=True,null=True)
    profile_picture = models.FileField(upload_to='investor_profile/', blank=True,null=True)
    
    def __str__(self):
        return self.user.email
    
    
class MentorProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE) 
    bio = models.TextField(blank=True,null=True)
    profile_picture = models.FileField(upload_to='mentor_profile/', blank=True,null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return self.user.email    


class EntrepreneurProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE) 
    bio = models.TextField(blank=True,null=True)
    profile_picture = models.FileField(upload_to='entrepreneur_profile/', blank=True,null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='entrepreneurs')

    
    def __str__(self):
        return self.user.email 
    
    
class AdminProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE) 
    profile_picture = models.FileField(upload_to='student_profile/', blank=True,null=True)
    
    def __str__(self):
        return self.user.email
        