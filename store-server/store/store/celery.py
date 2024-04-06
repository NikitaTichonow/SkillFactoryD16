import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

app = Celery('store')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'send_top_15_ads_weekly': {
        'task': 'ads.tasks.weekly_notification',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    }
}


app.autodiscover_tasks()