from celery import Celery

from config import settings
# from scheduler import BEAT_SCHEDULE


celery = Celery(
    'deribit_tasks',
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
    include=settings.celery_include
)

# celery.conf.beat_schedule = BEAT_SCHEDULE
