import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'head.settings')

app = Celery('head')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-daily-analytics': {
        'task': 'analytics.tasks.send_daily_analytics',
        'schedule': crontab(hour=9, minute=0),
    },
    'cleanup-old-data': {
        'task': 'analytics.tasks.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')