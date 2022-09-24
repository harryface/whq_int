import logging, os
from celery import Celery

logger = logging.getLogger("Celery")
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings')
 
app = Celery('payroll')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
