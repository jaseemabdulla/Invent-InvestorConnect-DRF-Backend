from django.db import models
from accounts.models import BaseUser

# Create your models here.


class Payment(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=20)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_status = models.CharField(max_length=20)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    # Add more fields as needed

    def __str__(self):
        return f'{self.user.email} - {self.session_id}'
