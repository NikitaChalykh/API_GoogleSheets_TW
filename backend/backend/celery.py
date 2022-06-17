import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

app = Celery(
    'backend',
    broker=os.getenv('BROKER')
)

app.conf.broker_url = os.getenv('BROKER_URL')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'beat_getting_sheets_data': {
        'task': 'polls.tasks.check_orders',
        'schedule': crontab(minute='*/1')
    },
}
