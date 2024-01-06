from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

import sys
print(sys.path)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yektanet.settings')

# create a Celery instance and configure it with the Django settings.
app = Celery('yektanet')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'ClicksInPastHour': {
        'task': 'advertiser_management.tasks.ClicksInPastHour',
        'schedule': 60
    },
    'ClicksInPastDay': {
        'task': 'advertiser_management.tasks.ClicksInPastDay',
        'schedule': crontab(minute='0', hour='0')
    },
    'ViewsInPastHour': {
        'task': 'advertiser_management.tasks.ViewsInPastHour',
        'schedule': 60
    },
    'ViewsInPastDay': {
        'task': 'advertiser_management.tasks.ViewsInPastDay',
        'schedule': crontab(minute='0', hour='0')
    },

}

