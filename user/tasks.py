from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(name="test")
def test():
    logger.info("Test1")
    return 5
