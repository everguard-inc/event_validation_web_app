import os
from random import randint

from celery import shared_task
from event_validation_app import celery_app
from celery.utils.log import get_task_logger


from events.data_fetcher import DataFetcher

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    random_number = randint(1, 20)
    logger.info(f'RANDOM NUMBER VALUE = {random_number} Task completed')


@celery_app.task(soft_time_limit=60 * 30)  # 30 minutes to run the task
def migrate_events():
    url = os.environ.get('EVENT_SERVICE_URL', 'http://localhost:9991')
    fetcher = DataFetcher(url=url)
    fetcher.process_migration()
