from celery import shared_task
from django.core.mail import send_mail
from .models import BaseUser
from django.conf import settings

@shared_task
def send_periodic_emails():
    users = BaseUser.objects.filter(is_active=True)  
    for user in users:
        subject = 'Periodic Email'
        message = f'Hello {user.first_name},\n\nThis is a periodic email sent to logged-in users.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)