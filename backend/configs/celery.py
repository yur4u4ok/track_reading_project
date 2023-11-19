import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')
app = Celery('configs')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_reading_statistics': {
        'task': 'apps.books.tasks.update_reading_statistics',
        'schedule': crontab(minute='0', hour='9'),
    },
}
