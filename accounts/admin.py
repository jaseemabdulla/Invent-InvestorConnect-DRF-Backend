from django.contrib import admin
from .models import BaseUser,InvestorProfile,EntrepreneurProfile,AdminProfile

# Register your models here.

admin.site.register(BaseUser)
admin.site.register(InvestorProfile)
admin.site.register(EntrepreneurProfile)
admin.site.register(AdminProfile)
