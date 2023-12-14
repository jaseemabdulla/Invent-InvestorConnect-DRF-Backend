from django.contrib import admin
from accounts.models import MentorProfile
from .models import MentorRequest

# Register your models here.


admin.site.register(MentorProfile) 
admin.site.register(MentorRequest) 