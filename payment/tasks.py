from celery import shared_task
from django.core.mail import send_mail
from accounts.models import BaseUser
from django.utils import timezone
from .models import Payment
from django.conf import settings

@shared_task
def send_subscription_expiration_email(user_id):
    user = BaseUser.objects.get(pk=user_id)
    subject = 'Subscription Expiring Soon'
    message = f'Dear {user.first_name}, your subscription is expiring soon. Renew now!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    
    
@shared_task
def send_subscription_success_email(user_id):
    user = BaseUser.objects.get(pk=user_id)
    subject = 'Subscription Success'
    message = f'Dear {user.first_name}, your subscription Success'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)    