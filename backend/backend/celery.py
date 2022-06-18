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
        'task': 'polls.tasks.check_data_in_sheets',
        # задача вызывается каждую минуту для
        # обновления и актуализации информации из google sheets
        'schedule': crontab(minute='*/1')
    },
}
