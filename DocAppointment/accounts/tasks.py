from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_user_registration_mail(user_mail):
    send_mail(subject="DocApp User Registration", message="Thank you for signing up for DocApp. We hope to make your lives easier.", from_email=settings.EMAIL_HOST_USER, recipient_list=(user_mail,), fail_silently=False)