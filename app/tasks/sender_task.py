import asyncio

from celery import shared_task

@shared_task
def sender_task():
    ...