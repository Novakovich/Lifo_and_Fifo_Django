import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lifo_and_Fifo_Django.settings')

app = Celery('Lifo_and_Fifo_Django')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
