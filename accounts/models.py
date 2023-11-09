from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class BaseUser(AbstractUser):
    ROLES = (
        ('investor','Investor'),
        ('entrepreneur','Entrepreneur'),
        ('admin','Admin')
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=False,blank=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','role']
    role = models.CharField(max_length=15, choices=ROLES)
    is_blocked = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20,unique=True)
    
    
class InvestorProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE) 
    bio = models.TextField(blank=True,null=True)
    profile_picture = models.FileField(upload_to='student_profile/', blank=True,null=True)
    
    def __str__(self):
        return self.user.email


class EntrepreneurProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE) 
    bio = models.TextField(blank=True,null=True)
    profile_picture = models.FileField(upload_to='student_profile/', blank=True,null=True)
    
    def __str__(self):
        return self.user.email
    
    
class AdminProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE) 
    profile_picture = models.FileField(upload_to='student_profile/', blank=True,null=True)
    
    def __str__(self):
        return self.user.email
        