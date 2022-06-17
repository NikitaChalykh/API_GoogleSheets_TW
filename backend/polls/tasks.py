import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def check_orders():
    pass
    try:
        pass
        logger.info('Карточки товаров сохранены успешно')
    except Exception as error:
        logger.error(f'Сбой при парсинге артикулов: {error}')
