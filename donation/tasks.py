from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from Lifo_and_Fifo_Django import settings


@shared_task(bind=True)
def send_mail_func(self, user_id):
    user = get_user_model().objects.get(id=user_id)
    mail_subject = "Hi! Celery Testing"
    message = "Привет из CharityBar"
    to_email = user.email
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
    return "Done"
