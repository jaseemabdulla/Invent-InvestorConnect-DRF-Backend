from django.db import models
from accounts.models import BaseUser
from django.utils import timezone

# Create your models here.


class Payment(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='payment')
    session_id = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=20)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_status = models.CharField(max_length=20)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    # Add more fields as needed
    

    def is_subscription_active(self):
        # Check if the subscription is active based on current period dates
        now = timezone.now()
        if self.current_period_start <= now <= self.current_period_end:
            return True
        return False

    def __str__(self):
        return f'{self.user.email} - {self.session_id}'
