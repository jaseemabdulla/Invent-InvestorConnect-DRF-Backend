from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from .models import BaseUser


@receiver(post_save, sender=BaseUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email_verified:
        subject = 'Welcome to Our Website'
        message = f'Hello {instance.email},\n\nWelcome to our website! Thank you for joining us.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)