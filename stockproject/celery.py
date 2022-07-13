from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# from celery.schedules import crontab 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockproject.settings')
app = Celery('stockproject')
app.conf.enable_utc = False
app.conf.update(timezone=('Asia/Karachi'))
app.config_from_object('django.conf:settings', namespace='CELERY')

#celery beat settings
#Note: while run celery beat, celery worker will also have to be run on the same machine 
app.conf.beat_schedule = {
    'every-10-seconds' : {
        'task': 'mainapp.tasks.update_stock',
        'schedule': 10,
        'args': (['RELIANCE.NS', 'BAJAJFINSV.NS'],)
    },
}
#END celery beat settings

app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))