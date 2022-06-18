import datetime
import logging

from celery import shared_task

from orders.models import GoodsOrder

from .utils import (FORMAT, check_orders_delivery_date, create_orders,
                    get_data_in_sheets, send_telegram_message)

logger = logging.getLogger(__name__)


class CeleryException(Exception):
    """Создаем свое исключения для всех сбоев в программе."""


@shared_task
def check_data_in_sheets():
    '''Обновленеие и актуализация информации из google sheets в БД.'''
    try:
        # запрашиваем данные заказов из google sheets
        sheets_orders = get_data_in_sheets()
        logger.info('Получены данные из google sheets')
        # получаем все сохраненные заказы из БД
        orders = GoodsOrder.objects.all()
        # если google sheets пуст, то удаляем все заказы из БД
        if sheets_orders == []:
            orders.delete()
            logger.info('Таблица google sheets пуста')
        # если БД пуста, то заполняем БД данными из google sheets
        elif not orders.exists():
            create_orders(sheets_orders)
            logger.info('Пустая БД заполена данными из google sheets')
        # если оба источника не пусты, то проверям разницу
        # в количестве объектов и обновляем БД при наличии отличия
        elif orders.count() != len(sheets_orders):
            orders.delete()
            create_orders(sheets_orders)
            logger.info('Данные в БД обновлены')
        # если оба источника не пусты и их количество совпадает,
        # то проверям разницу каждого атрибута
        # и обновляем БД при наличии отличий
        else:
            for i in range(len(sheets_orders)):
                order_tuple = (
                    orders[i].serial_number,
                    orders[i].order_number,
                    orders[i].dollar_value,
                    orders[i].delivery_date
                )
                sheet_order_tuple = (
                    int(sheets_orders[i][0]),
                    int(sheets_orders[i][1]),
                    int(sheets_orders[i][2]),
                    datetime.datetime.strptime(
                        sheets_orders[i][3], FORMAT
                    ).date()
                )
                if order_tuple != sheet_order_tuple:
                    print(order_tuple)
                    print(sheet_order_tuple)
                    orders.delete()
                    create_orders(sheets_orders)
                    logger.info('Данные в БД обновлены')
                    break
        # проверяем актуальность сроков поставки заказов и отправляем сообщ.
        # c номерами заказов в телеграмм при наличии просроченных заказов
        lated_orders = check_orders_delivery_date()
        if lated_orders.exists():
            send_telegram_message(lated_orders)
            logger.info('Отправленны просроченные заказы в телеграмм')
            # сообщение в телеграм отправляется только один раз
            # (до следующего обновления данных в БД)
            lated_orders.update(is_sending=True)
            logger.info('Изменены статусы отправки сообщений в моделях')
    except Exception as error:
        logger.error(f'Сбой при работе Celery задачи: {error}')
        raise CeleryException
